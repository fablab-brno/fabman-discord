from datetime import datetime

from starlette.testclient import TestClient

from fabman_discord.dependencies import get_settings
from fabman_discord.fabman import router
from fabman_discord.fabman.webhook import fabman_webhook

client = TestClient(router)

settings = get_settings()


def test_webhook(mocker):
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


def test_resource_disabled(mocker):
    mocker.patch("fabman_discord.fabman.webhook.send_message")

    response = fabman_webhook(resource_disabled_details)
    assert (
        response.status
        == "CNC frézka Jeřábek je mimo provoz - Nutné znovu zaměřit trn."
    )


def test_resource_enabled(mocker):
    mocker.patch("fabman_discord.fabman.webhook.send_message")

    response = fabman_webhook(resource_enabled_details)
    assert response.status == "CNC frézka Jeřábek je opět funkční"


resource_enabled_details = {
    "log": {
        "id": 2048004,
        "type": "resourceEnabled",
        "stoppedAt": "2024-07-23T17:18:34.233Z",
        "lockVersion": 1,
        "createdAt": "2024-07-23T17:18:34.233Z",
        "updatedAt": "2024-07-23T17:18:34.233Z",
        "stopType": None,
        "idleDurationSeconds": None,
        "reason": None,
        "notes": None,
        "account": 4,
        "originalMember": None,
        "updatedBy": None,
        "extraChargeDescription": None,
        "extraChargePrice": None,
        "extraChargeTaxPercent": None,
        "extraChargeDetails": "",
    },
    "resource": {
        "id": 3358,
        "name": "CNC frézka Jeřábek",
        "state": "active",
        "metadata": {"DISCORD_CHANNEL_ID": 42},
    },
    "member": {},
}

resource_disabled_details = {
    "log": {
        "id": 2047931,
        "type": "resourceDisabled",
        "stoppedAt": "2024-07-23T16:19:43.694Z",
        "lockVersion": 1,
        "createdAt": "2024-07-23T16:19:43.694Z",
        "updatedAt": "2024-07-23T16:19:43.694Z",
        "stopType": None,
        "idleDurationSeconds": None,
        "reason": None,
        "notes": "<div>Nutné znovu zaměřit trn.</div>",
        "account": 4,
        "originalMember": None,
        "updatedBy": None,
        "extraChargeDescription": None,
        "extraChargePrice": None,
        "extraChargeTaxPercent": None,
        "extraChargeDetails": "",
    },
    "resource": {
        "id": 3358,
        "name": "CNC frézka Jeřábek",
        "state": "active",
        "metadata": {"DISCORD_CHANNEL_ID": 42},
    },
    "member": {},
}
