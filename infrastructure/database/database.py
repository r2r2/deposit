import sqlalchemy
import databases
from settings import settings


database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
metadata = sqlalchemy.MetaData(schema="deposit")
engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=False)
metadata.create_all(engine)
