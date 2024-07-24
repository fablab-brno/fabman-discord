from fastapi import APIRouter, Response, status

from fabman_discord.dependencies import get_settings
from fabman_discord.fabman.webhook import (
    FabmanPayload,
    FabmanWebhookResponse,
    fabman_webhook,
)

router = APIRouter()

settings = get_settings()


@router.post("/webhook", response_model=FabmanWebhookResponse)
async def webhook(key: str, payload: FabmanPayload, response: Response):
    if key != settings.fabman_webhook_secret:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"status": "unauthorized"}

    details = payload.details

    if payload.type == "test":
        return {"status": details["message"]}

    return fabman_webhook(details)
