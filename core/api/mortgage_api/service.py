from core.errors.exceptions import InconsistencyError
from infrastructure.database import models
from infrastructure.database.database import database
from sqlalchemy import select


async def get_offer(price: int | None = None, deposit: int | None = None,
                    term: int | None = None, order: str | None = None,
                    payment_min: int | None = None, payment_max: int | None = None,
                    limit: int = None, offset: int = None) -> list[dict[str, ...]]:
    match order:
        case str(value) if value not in ("payment", "-payment", "rate", "-rate"):
            raise InconsistencyError(detail="Field order should be either: 'payment', '-payment', 'rate', '-rate'")
        case str(value) if value == "rate":
            order = "rate_min"
        case str(value) if value == "-rate":
            order = "-rate_min"

    deposit_min = (models.banks.c.rate_min <= deposit) if deposit else True
    deposit_max = (models.banks.c.rate_max >= deposit) if deposit else True
    max_price = (models.banks.c.payment_max >= price) if price else True
    min_price = (models.banks.c.payment_min <= price) if price else True
    min_years = (models.banks.c.term_min <= term) if term else True
    max_years = (models.banks.c.term_max >= term) if term else True

    query = select(models.banks).where(
        deposit_min & deposit_max & max_price & min_price & min_years & max_years
    ).limit(limit).offset(offset)
    banks = await database.fetch_all(query)

    if all((price, deposit, term)):
        reverse = True if order.startswith("-") else False
        new_order = order[1:] if order.startswith("-") else order
        res = list()
        for bank in banks:
            payment = await calculate_payment(bank.rate_min, price, deposit, term, payment_min, payment_max)
            if payment:
                res.append({"payment": payment, **bank._mapping})  # noqa
        return sorted(res, key=lambda k: k[new_order], reverse=reverse)

    return banks


async def calculate_payment(rate: float, price: int, deposit: int, term: int,
                            payment_min: int | None = None, payment_max: int | None = None) -> int | None:
    """
    Calculate mortgage payment with formula: payment = Sz*r/(1-(1/(1+r))*n)
    """
    r = rate / 12  # процентная ставка за год, разделенная на двенадцать месяцев
    n = term * 12  # количество месяцев
    sz = price - deposit  # общая сумма займа
    payment = int(abs(sz * r / (1 - (1 / (1 + r)) * n)))

    if payment_min and payment_max:
        payment_ok = payment_min <= payment <= payment_max
        if payment_ok:
            return payment
    elif payment_min and not payment_max:
        payment_ok = payment_min >= payment
        if payment_ok:
            return payment
    elif not payment_min and payment_max:
        payment_ok = payment <= payment_max
        if payment_ok:
            return payment
    else:
        return payment
