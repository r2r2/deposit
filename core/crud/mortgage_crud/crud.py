from infrastructure.database.database import database
from sqlalchemy.sql import select, exists
from infrastructure.database import models, schemas


async def get_bank(bank_id: int) -> schemas.Bank:
    query = select(models.banks).where(models.banks.c.id == bank_id)
    return await database.fetch_one(query)


async def get_bank_by_name(bank_name: str) -> int:
    query = select(models.banks).where(models.banks.c.bank_name == bank_name)
    return await database.fetch_one(query)


async def get_banks(offset: int = None, limit: int = None) -> list[schemas.BankAll]:
    query = models.banks.select().limit(limit).offset(offset)
    return await database.fetch_all(query)


@database.transaction()
async def create_bank(bank: schemas.BankBase) -> dict[str, ...]:
    query = models.banks.insert().values(**bank.dict())
    last_record_id = await database.execute(query)
    return {**bank.dict(), "id": last_record_id}


@database.transaction()
async def update_bank(bank_id: int, bank: schemas.BankUpdate) -> None:
    query = models.banks.update().where(models.banks.c.id == bank_id).values(**bank.dict(exclude_none=True))
    await database.execute(query)


@database.transaction()
async def delete_bank(bank_id: int) -> None:
    query = models.banks.delete().where(models.banks.c.id == bank_id)
    await database.execute(query)


async def check_exists(bank_id: int) -> bool:
    # query = select(exists(select(models.banks.c.id).where(models.banks.c.id == bank_id)))
    # exists_criteria = (
    #     select(models.banks.c.id).
    #     where(models.banks.c.id == bank_id).
    #     exists()
    # )
    exists_criteria = exists().where(models.banks.c.id == bank_id)
    stmt = select(models.banks.c.id).where(exists_criteria)
    return await database.execute(stmt)
