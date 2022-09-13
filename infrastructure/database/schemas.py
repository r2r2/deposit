import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


class MyBaseModel(BaseModel):
    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BankBase(MyBaseModel):
    bank_name: str


class BankCreate(BankBase):
    term_min: int
    term_max: int
    rate_min: float
    rate_max: float
    payment_min: int
    payment_max: int


class BankUpdate(BankBase):
    bank_name: str | None
    term_min: int | None
    term_max: int | None
    rate_min: float | None
    rate_max: float | None
    payment_min: int | None
    payment_max: int | None


class Bank(BankBase):
    id: int
    term_min: int
    term_max: int
    rate_min: float
    rate_max: float
    payment_min: int
    payment_max: int


class ItemBase(MyBaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int


class UserBase(MyBaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = list()
