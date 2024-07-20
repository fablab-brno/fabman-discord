from functools import lru_cache
from starlette_discord import DiscordOAuthClient

from .settings import Settings


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_discord_client():
    settings = get_settings()

    return DiscordOAuthClient(
        settings.discord.client_id,
        settings.discord.client_secret,
        settings.discord.redirect_uri,
    )
