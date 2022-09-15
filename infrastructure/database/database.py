import sqlalchemy
import databases
from coverage.env import TESTING
from settings import settings


metadata = sqlalchemy.MetaData(schema="deposit")
engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=False)
metadata.create_all(engine)

if TESTING:
    database = databases.Database(settings.TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(settings.SQLALCHEMY_DATABASE_URI, min_size=5, max_size=20)
