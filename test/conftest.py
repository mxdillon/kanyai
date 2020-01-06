import pytest
import logging
from google.cloud.logging.client import Client


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    """Mock the credentials environment variable for when the Google logging client is initialised."""
    monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS',
                       './test/mock-data/sample-creds.json')


@pytest.fixture
def client():
    """Flask test client with Google Cloud logging client removed."""
    from app import create_app
    app = create_app()
    client = app.test_client()

    # Remove the Google Cloud logging client for local tests
    test_logger = logging.getLogger()
    for handler in test_logger.handlers:
        if hasattr(handler, 'client'):
            if isinstance(handler.client, Client):
                test_logger.removeHandler(handler)

    return client
