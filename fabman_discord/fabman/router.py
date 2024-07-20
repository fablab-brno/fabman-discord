from datetime import datetime

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from rich import print

from fabman_discord.bot.api import send_message
from fabman_discord.dependencies import get_settings
from fabman_discord.utils import td_format

router = APIRouter()

settings = get_settings()


class FabmanPayload(BaseModel):
    id: int
    type: str
    createdAt: datetime
    details: dict


class WebhookResponse(BaseModel):
    status: str


@router.post("/webhook", response_model=WebhookResponse)
async def webhook(key: str, payload: FabmanPayload, response: Response):
    if key != settings.fabman_webhook_secret:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"status": "unauthorized"}

    details = payload.details

    if payload.type == "test":
        send_message(details["message"])
        return {"status": details["message"]}

    log = details["log"]
    resource = details["resource"]
    resource_name = resource["name"]

    is_3d_printer = resource_name.startswith("3D printer") or resource_name.startswith(
        "3D Prusa"
    )
    if not is_3d_printer:
        return {"status": f"ignored, resource isn't 3d printer: {resource_name}"}

    if log["type"] != "allowed":
        return {"status": "ignored, access not allowed"}

    stopped_at = log["stoppedAt"]
    if not stopped_at:
        return {"status": "ignored, resource still running"}

    # with open(f"./logs/{payload.id}.json", "w") as file:
    #     file.write(payload.model_dump_json())

    run_time = td_format(
        datetime.strptime(log["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        - datetime.strptime(stopped_at, "%Y-%m-%dT%H:%M:%S.%fZ")
    )
    message = f"{resource_name} has stopped after {run_time}"
    send_message(message)
    return {"status": message}
