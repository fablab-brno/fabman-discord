from datetime import datetime

from starlette.testclient import TestClient

from fabman_discord.dependencies import get_settings
from fabman_discord.fabman import router

client = TestClient(router)

settings = get_settings()


def test_webhook(mocker):
    mocker.patch("fabman_discord.fabman.router.send_message")
    response = client.post(
        f"/webhook?key={settings.fabman_webhook_secret}",
        json={
            "id": 42,
            "type": "test",
            "createdAt": str(datetime.now()),
            "details": {"message": "Testing Py.Test"},
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "Testing Py.Test",
    }
