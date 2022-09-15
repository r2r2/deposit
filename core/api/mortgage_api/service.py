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
