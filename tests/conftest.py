from typing import Generator
from alembic import command
from alembic.config import Config
from sqlalchemy.sql.ddl import CreateSchema
from starlette.config import environ
import pytest
from httpx import AsyncClient
from settings import settings
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

environ['TESTING'] = 'True'
from core.server.server import server
from infrastructure.database.database import metadata, database


@pytest.fixture()
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture()
async def db() -> None:
    await database.connect()


@pytest.fixture(autouse=True)
def create_test_database(anyio_backend):
    """
    Create a clean database on every test case.
    For safety, we should abort if a database already exists.

    We use the `sqlalchemy_utils` package here for a few helpers in consistently
    creating and dropping the database.
    """
    url = settings.TEST_DATABASE_URL
    schema_name = settings.POSTGRES_SCHEMA
    engine = create_engine(url)
    assert not database_exists(url), 'Test database already exists. Aborting tests.'
    create_database(url)                      # Create the test database.
    engine.execute(CreateSchema(schema_name))
    # config = Config("alembic.ini")          # Run the migrations.
    # command.upgrade(config, "head")
    metadata.create_all(engine)               # Create the tables.
    yield                                     # Run the tests.
    drop_database(url)                        # Drop the test database.


@pytest.fixture()
async def client() -> Generator:
    async with AsyncClient(app=server.app,
                           base_url="http://test",
                           headers={"Content-Type": "application/json"}
                           ) as client:
        yield client


