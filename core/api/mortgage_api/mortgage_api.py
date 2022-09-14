from core.crud.mortgage_crud import crud
from infrastructure.database import schemas
from core.errors.exceptions import InconsistencyError


async def create_bank(bank: schemas.BankCreate) -> dict[str, ...]:
    db_bank = await crud.get_bank_by_name(bank.bank_name)
    if db_bank:
        raise InconsistencyError(detail=f"Bank with name={bank.bank_name} already exists.")
    return await crud.create_bank(bank)


async def read_banks(skip: int = 0, limit: int = 100) -> list[schemas.Bank]:
    banks = await crud.get_banks(skip=skip, limit=limit)
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
