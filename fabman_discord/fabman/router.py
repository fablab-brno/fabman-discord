from fastapi import APIRouter, Response, status

from fabman_discord.dependencies import get_settings
from fabman_discord.fabman.webhook import (
    FabmanPayload,
    ErrorInfo,
    FabmanWebhookResponse,
    fabman_webhook,
    error_handler_fn,
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


@router.post("/errors", response_model=FabmanWebhookResponse)
async def error_handler(key: str, payload: ErrorInfo, response: Response):
    if key != settings.bridge_secret:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"status": "unauthorized"}

    return error_handler_fn(payload)
