from datetime import datetime
import re


from pydantic import BaseModel

from fabman_discord.bot.api import send_message


class FabmanPayload(BaseModel):
    id: int
    type: str
    createdAt: datetime
    details: dict


class FabmanWebhookResponse(BaseModel):
    status: str


def fabman_webhook(details: dict) -> FabmanWebhookResponse:
    log = details["log"]

    resource = details["resource"]
    resource_name = resource["name"]

    allowed_log_types = ["resourceDisabled", "resourceEnabled"]
    if log["type"] not in allowed_log_types:
        return FabmanWebhookResponse(
            status=f"ignored, log type isn't {' or '.join(allowed_log_types)}: {log['type']}"
        )

    resource_status = (
        "je mimo provoz" if log["type"] == "resourceDisabled" else "je opět funkční"
    )

    if notes := remove_html_tags(log.get("notes") or ""):
        resource_status += f" - {notes}"

    message = f"{resource_name} {resource_status}"

    if log["type"] == "resourceDisabled":
        icon = ":exclamation:"
    else:
        icon = ":white_check_mark:"

    send_message(f"{icon} {message}")
    return FabmanWebhookResponse(status=message)


strip_html_re = re.compile("<.*?>")


def remove_html_tags(text):
    return re.sub(strip_html_re, "", text)
