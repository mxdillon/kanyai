import pytest


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS',
                       './test/mock-secrets/sample-creds.json')


@pytest.fixture
def client():
    """Flask test client."""
    from app import create_app
    app = create_app()
    client = app.test_client()
    return client
