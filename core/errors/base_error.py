from typing import Any
from fastapi.exceptions import HTTPException


class BaseError(HTTPException):
    def __init__(self, ex=None, detail=None, status_code: int = None):
        self.status_code = status_code
        if not detail:
            self.detail = self.make_payload(ex)
        else:
            self.detail = detail

    def make_payload(self, ex: Exception) -> Any:
        pass
