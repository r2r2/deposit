import calendar
from datetime import date, datetime, timedelta
from core.dto.dto import DepositDto
from core.errors.dto_error import DtoValidationError


async def calculate(dto: DepositDto) -> dict:
    """
    amount * rate / 100 / 12 + amount
    """
    result = dict()
    date1 = datetime.strptime(dto.date, '%d.%m.%Y')

    for _ in range(dto.periods):
        last_day_of_month = date(date1.year, date1.month, calendar.monthrange(date1.year, date1.month)[1])
        dto.amount = dto.amount * dto.rate / 100 / 12 + dto.amount
        result.update({last_day_of_month: round(dto.amount, 2)})
        date1 += timedelta(weeks=4)

    return result


