from pydantic import BaseModel

from pydantic_settings import BaseSettings, SettingsConfigDict


class DiscordSettings(BaseModel):
    bot_token: str


class Settings(BaseSettings):
    discord: DiscordSettings
    fabman_webhook_secret: str
    bridge_secret: str
    error_handler_channel_id: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )
