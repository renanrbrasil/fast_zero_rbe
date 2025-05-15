import pytest
from fastapi.testclient import TestClient

from fast_zero_rbe.app import app


@pytest.fixture
def client():
    return TestClient(app)
