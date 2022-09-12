import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases
from settings import settings


database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
metadata = sqlalchemy.MetaData(schema="deposit")
engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
metadata.create_all(engine)




# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base(metadata=metadata)
