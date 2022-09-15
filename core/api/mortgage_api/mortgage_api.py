from core.crud.mortgage_crud import crud
from infrastructure.database import schemas
from core.api.mortgage_api import service
from core.errors.exceptions import InconsistencyError
from fastapi import Query


async def create_bank(bank: schemas.BankBase) -> dict[str, ...]:
    db_bank = await crud.get_bank_by_name(bank.bank_name)
    if db_bank:
        raise InconsistencyError(detail=f"Bank with name={bank.bank_name} already exists.")
    return await crud.create_bank(bank)


async def read_banks(price: int | None = Query(default=None, le=100_000_000, description="Цена объекта недвижимости"),
                     deposit: int | None = Query(default=None, le=100, description="Первоночальный взнос в процентах"),
                     term: int | None = Query(default=None, le=70, description="Количество лет ипотечного рабства"),
                     payment_min: int | None = Query(default=None, ge=0, description="Минимальный платеж"),
                     payment_max: int | None = Query(default=None, le=100_000_000, description="Максимальный платеж"),
                     order: str | None = Query(default="payment", description="Сортировка по полю"),
                     offset: int = 0, limit: int = 100) -> list[dict[str, ...] | schemas.BankAll]:

    if any((price, deposit, term)):
        banks = await service.get_offer(price, deposit, term, order, payment_min, payment_max, limit, offset)
        return banks

    banks = await crud.get_banks(offset=offset, limit=limit)
    return banks


async def read_bank(bank_id: int) -> schemas.Bank:
    db_bank = await crud.get_bank(bank_id)
    if db_bank is None:
        raise InconsistencyError(status_code=404, detail="Bank not found")
    return db_bank


async def patch_bank(bank_id: int, bank: schemas.BankUpdate) -> schemas.Bank:
    if not await crud.check_exists(bank_id):
        raise InconsistencyError(detail=f"Bank with id={bank_id} not found.")
    await crud.update_bank(bank_id, bank)
    return await read_bank(bank_id)


async def delete_bank(bank_id: int) -> dict[str, str]:
    if not await crud.check_exists(bank_id):
        raise InconsistencyError(detail=f"Bank with id={bank_id} not found.")
    await crud.delete_bank(bank_id)
    return {"message": f"Bank with id={bank_id} was successfully deleted from database."}
