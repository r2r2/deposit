import pydantic
from fastapi.requests import Request
from core.errors.dto_error import DtoValidationError


def validate(dto_cls, request_dto):
    print(dto_cls)
    print(type(dto_cls))
    print("*" * 399)
    print(request_dto)
    print(type(request_dto))
    print(request_dto.json)

    if not request_dto:
        raise DtoValidationError(detail="json is empty")
    try:
        dto = dto_cls(request_dto.json)
        return dto
    except pydantic.ValidationError as ex:
        raise DtoValidationError(ex)
