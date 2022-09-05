from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Make all pydantic validation errors return 400 status code."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"error": f"Field [{exc.errors()[0]['loc'][1]}] - {exc.errors()[0]['msg']}"}
        ),
    )
