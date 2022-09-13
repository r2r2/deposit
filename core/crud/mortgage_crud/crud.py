from infrastructure.database.database import database
from sqlalchemy.sql import select, exists, update
from infrastructure.database import models, schemas


async def get_bank(bank_id: int) -> schemas.Bank:
    query = select(models.banks).where(models.banks.c.id == bank_id)
    return await database.fetch_one(query)


async def get_bank_by_name(bank_name: str) -> int:
    query = select(models.banks).where(models.banks.c.bank_name == bank_name)
    return await database.fetch_one(query)


async def get_banks(skip: int = 0, limit: int = 100) -> list[schemas.Bank]:
    query = models.banks.select().limit(limit).offset(skip)
    return await database.fetch_all(query)


@database.transaction()
async def create_bank(bank: schemas.BankCreate) -> dict[str, ...]:
    query = models.banks.insert().values(**bank.dict())
    last_record_id = await database.execute(query)
    return {**bank.dict(), "id": last_record_id}


@database.transaction()
async def update_bank(bank_id: int, bank: schemas.BankUpdate):
    query = models.banks.update().where(models.banks.c.id == bank_id).values(**bank.dict(exclude_none=True))
    await database.execute(query)


async def check_exists(bank_id: int) -> bool:
    # query = exists(models.banks).where(models.banks.c.id == bank_id)
    # query = select(models.banks.c.id).where(exists(select(models.banks.c.id).where(models.banks.c.id == bank_id)))
    query = select(models.banks.c.id).where(exists(models.banks.c.id == bank_id))
    # query = models.banks
    print(query)
    res = await database.execute(query)
    print(res)
    return res
