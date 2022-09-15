from core.api.mortgage_api.service import calculate_payment
from core.errors.exceptions import InconsistencyError
from infrastructure.database.database import database
from sqlalchemy.sql import select, exists
from infrastructure.database import models, schemas


async def get_bank(bank_id: int) -> schemas.Bank:
    query = select(models.banks).where(models.banks.c.id == bank_id)
    return await database.fetch_one(query)


async def get_bank_by_name(bank_name: str) -> int:
    query = select(models.banks).where(models.banks.c.bank_name == bank_name)
    return await database.fetch_one(query)


async def get_banks(offset: int = None, limit: int = None) -> list[schemas.BankAll]:
    query = models.banks.select().limit(limit).offset(offset)
    return await database.fetch_all(query)


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


@database.transaction()
async def create_bank(bank: schemas.BankBase) -> dict[str, ...]:
    query = models.banks.insert().values(**bank.dict())
    last_record_id = await database.execute(query)
    return {**bank.dict(), "id": last_record_id}


@database.transaction()
async def update_bank(bank_id: int, bank: schemas.BankUpdate) -> None:
    query = models.banks.update().where(models.banks.c.id == bank_id).values(**bank.dict(exclude_none=True))
    await database.execute(query)


@database.transaction()
async def delete_bank(bank_id: int) -> None:
    query = models.banks.delete().where(models.banks.c.id == bank_id)
    await database.execute(query)


async def check_exists(bank_id: int) -> bool:
    # query = select(exists(select(models.banks.c.id).where(models.banks.c.id == bank_id)))
    # exists_criteria = (
    #     select(models.banks.c.id).
    #     where(models.banks.c.id == bank_id).
    #     exists()
    # )
    exists_criteria = exists().where(models.banks.c.id == bank_id)
    stmt = select(models.banks.c.id).where(exists_criteria)
    return await database.execute(stmt)
