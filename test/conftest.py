import pytest
from app import create_app


@pytest.fixture
def client():
    """Flask test client."""
    app = create_app()
    client = app.test_client()
    return client
