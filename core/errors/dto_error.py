from pydantic import ValidationError

from core.errors.base_error import BaseError


class DtoValidationError(BaseError):
    status_code = 400

    def __init__(self, ex: ValidationError = None, detail=None):
        super().__init__(ex=ex, detail=detail, status_code=self.status_code)

    def make_payload(self, exeption: ValidationError) -> dict:
        failed_fields = exeption.errors()
        commment_str = "Some of essential params failed : "
        return {
            "comment": commment_str + ", ".join([field["loc"][-1] + " - " + field["msg"] for field in failed_fields])}
