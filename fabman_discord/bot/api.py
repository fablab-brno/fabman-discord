import requests

from fabman_discord.dependencies import get_settings

settings = get_settings()


def send_message(channel_id: str, message: str):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    authorization = f"Bot {settings.discord.bot_token}"
    try:
        response = requests.post(
            url, headers={"Authorization": authorization}, json={"content": message}
        )
    except Exception as e:
        print(f"Unknown error: {e}")
        return

    if response.status_code != 200:
        print(
            f"Message failed to send to {channel_id}: {response.status_code} {response.text}"
        )
