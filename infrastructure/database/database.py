import sqlalchemy
import databases
from settings import settings
from starlette.config import Config


config = Config(".env")
TESTING = config('TESTING', cast=bool, default=False)
schema_name = settings.POSTGRES_SCHEMA

metadata = sqlalchemy.MetaData(schema="deposit")
engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=False)

if not engine.dialect.has_schema(engine, schema_name):
    engine.execute(sqlalchemy.schema.CreateSchema(schema_name))

metadata.create_all(engine)


if TESTING:
    database = databases.Database(settings.TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(settings.SQLALCHEMY_DATABASE_URI, min_size=5, max_size=20)
