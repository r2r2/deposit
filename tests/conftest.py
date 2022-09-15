from typing import Generator

import pytest
from fastapi.testclient import TestClient

from core.server.server import server
from httpx import AsyncClient


# @pytest.fixture(scope="module")
# def test_app() -> Generator:
#     with TestClient(server.app) as client:
#         yield client
@pytest.fixture(scope="module")
async def client() -> Generator:
    async with AsyncClient(app=server.app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="module")
def anyio_backend():
    return 'asyncio'
