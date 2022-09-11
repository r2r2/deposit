from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from infrastructure.database.database import Base


# class AbstractBaseModel(Base):
#     id = Column(Integer, primary_key=True, index=True)


class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String(255), unique=True, index=True)
    term_min = Column(Integer, comment="Срок ипотеки, ОТ")
    term_max = Column(Integer, comment="Срок ипотеки, ДО")
    rate_min = Column(Float, doc="Ставка, ОТ")
    rate_max = Column(Float, doc="Ставка, ДО")
    payment_min = Column(Integer, doc="Сумма кредита, ОТ")
    payment_max = Column(Integer, doc="Сумма кредита, ДО")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")