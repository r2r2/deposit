from infrastructure.database.database import database
from sqlalchemy import select, update
from sqlalchemy.orm import Session, Query

from infrastructure.database import models, schemas


async def get_bank(db: Session, bank_id: int):
    # return db.query(models.Bank).filter(models.Bank.id == bank_id).first()

    return db.query(models.Bank).filter(models.Bank.id == bank_id).first()


def get_bank_by_bank_name(db: Session, bank_name: str) -> Query:
    return db.query(models.Bank).filter(models.Bank.bank_name == bank_name).first()


async def get_banks(db: Session, skip: int = 0, limit: int = 100) -> Query:
    # return db.query(models.Bank).offset(skip).limit(limit).all()
    query = db.query(models.Bank).offset(skip).limit(limit).all()
    return await database.fetch_all(query)
    # return db.query(models.Bank).offset(skip).limit(limit).all()


def create_bank(db: Session, bank: schemas.Bank):
    db_bank = models.Bank(**bank.dict())
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank


def update_bank(db: Session, db_bank: models.Bank, bank: schemas.BankUpdate):
    db.add(db_bank)
    # db.query(db_bank).update(bank.dict())
    # db.execute(update(db_bank), values=bank.dict())
    db.execute(update(db_bank).where(models.Bank == db_bank.id).values(bank.dict()))
    # db.execute(update(db_bank).values(bank.dict()))
    # db_bank.update().values(bank.dict())
    db.commit()
    db.refresh(db_bank)
    # session.execute(update(User).where(User.name == "sandy").values(fullname="Sandy Squirrel Extraordinaire"))
    return db_bank


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
