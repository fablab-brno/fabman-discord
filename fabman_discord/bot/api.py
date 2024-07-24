import requests

from fabman_discord.dependencies import get_settings

settings = get_settings()


def send_message(channel_id: int, message: str):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    authorization = f"Bot {settings.discord.bot_token}"
    requests.post(
        url, headers={"Authorization": authorization}, json={"content": message}
    )
