import calendar
from datetime import date, datetime, timedelta
from fastapi.responses import JSONResponse

from core.errors.exceptions import InconsistencyError
from core.dto.dto import CalculateDto
from core.utils.increment_date import add_months


async def calculate(dto: CalculateDto) -> JSONResponse:
    """
    Calculate deposit using formula:
        amount * rate / 100 / 12 + amount
    """
    result = dict()
    try:
        date_py = datetime.strptime(dto.date, '%d.%m.%Y')
    except ValueError:
        raise InconsistencyError(detail="You should provide date in format: dd.mm.YYYY")

    for _ in range(dto.periods):
        last_day_of_month = date(
            date_py.year, date_py.month, calendar.monthrange(date_py.year, date_py.month)[1]
        ).strftime('%d.%m.%Y')
        dto.amount = dto.amount * dto.rate / 100 / 12 + dto.amount
        result.update({last_day_of_month: round(dto.amount, 2)})
        date_py = add_months(date_py, 1)

    return JSONResponse(result)
