import pytest
from app.main import PORTFOLIO, ORDERS


@pytest.fixture(autouse=True)
def clear_state():
    # Clear in-memory state before each test
    PORTFOLIO.clear()
    ORDERS.clear()
    yield
