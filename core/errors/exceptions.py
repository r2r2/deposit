# from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException


class ApplicationError(StarletteHTTPException):
    def __init__(self, detail: str | None = None, status_code: int = 400):
        self.detail = detail
        super().__init__(status_code, detail)


class InconsistencyError(ApplicationError):
    def __init__(self, detail: str | None = None, status_code: int = 400):
        super().__init__(detail=detail, status_code=status_code)
