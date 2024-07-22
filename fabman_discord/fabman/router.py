from datetime import datetime

from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from fabman_discord.bot.api import send_message
from fabman_discord.dependencies import get_settings

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

    allowed_log_types = ["resourceDisabled", "resourceEnabled"]
    if log["type"] not in allowed_log_types:
        return {"status": f"ignored, log type isn't {' or '.join(allowed_log_types)}"}

    resource_status = (
        "je mimo provoz" if log["type"] == "resourceDisabled" else "je opět funkční"
    )

    message = f"{resource_name} {resource_status}"
    send_message(message)
    return {"status": message}
