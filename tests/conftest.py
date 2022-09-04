import pytest
from fastapi.testclient import TestClient

from core.server.server import server


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(server.app)
    yield client
