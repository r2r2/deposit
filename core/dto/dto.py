from pydantic import BaseModel, conint, confloat


class CalculateDto(BaseModel):
    date: str
    periods: conint(ge=1, le=60)
    amount: conint(ge=10_000, le=3_000_000)
    rate: confloat(ge=1.0, le=8.0)
