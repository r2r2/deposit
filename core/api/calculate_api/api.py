from datetime import datetime

from dateutil.relativedelta import *
from fastapi.responses import JSONResponse

from core.dto.dto import CalculateDto
from core.errors.exceptions import InconsistencyError
from settings import settings


async def calculate(dto: CalculateDto) -> JSONResponse:
    """
    Calculate deposit using formula:
        amount * rate / 100 / 12 + amount
    """
    result = dict()
    try:
        date_py = datetime.strptime(dto.date, settings.date_format)
    except ValueError:
        raise InconsistencyError(detail="You should provide date in format: dd.mm.YYYY")

    for num in range(dto.periods):
        date_to_pay = date_py + relativedelta(months=+num)
        dto.amount = dto.amount * dto.rate / 100 / 12 + dto.amount
        result.update({date_to_pay.strftime(settings.date_format): round(dto.amount, 2)})
    return JSONResponse(result)
