from fastapi.testclient import TestClient

from . import main

from . import config

client = TestClient(main.app)


def get_settings_override():
    return config.Settings(admin_email="testing_admin@example.com")


main.app.dependency_overrides[config.get_settings] = get_settings_override

def test_app():
    response = client.get("/r/test")
    data = response.json()
    assert data == config.Settings(admin_email="testing_admin@example.com")