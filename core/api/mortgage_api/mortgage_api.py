from core.crud.mortgage_crud import crud
from infrastructure.database import schemas
from infrastructure.database.setup_db import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from core.errors.exceptions import InconsistencyError


async def create_bank(bank: schemas.Bank, db: Session = Depends(get_db)):
    db_bank = crud.get_bank_by_bank_name(db, bank.bank_name)
    if db_bank:
        raise InconsistencyError(detail=f"Bank with name={bank.bank_name} already exists.")
    return crud.create_bank(db, bank)


async def read_banks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    banks = crud.get_banks(db, skip=skip, limit=limit)
    return banks


async def read_bank(bank_id: int, db: Session = Depends(get_db)):
    db_bank = crud.get_bank(db, bank_id)
    if db_bank is None:
        raise InconsistencyError(status_code=404, detail="Bank not found")
    return db_bank


def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise InconsistencyError(detail="Email already registered")
    return crud.create_user(db=db, user=user)


def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise InconsistencyError(status_code=404, detail="User not found")
#     return db_user
#
#
# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items