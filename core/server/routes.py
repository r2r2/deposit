from core.errors.dto_error import DtoValidationError
from fastapi.responses import JSONResponse
from core.dto.dto import DepositDto
from core.dto.validator import validate


async def calculate(dto: DepositDto) -> JSONResponse:
    if not dto:
        raise DtoValidationError(detail="Empty json")

    # params = validate(DepositDto, dto)
    params = dto
    print(params)
    return params


