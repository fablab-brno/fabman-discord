from pydantic import BaseModel

from pydantic_settings import BaseSettings, SettingsConfigDict


class DiscordSettings(BaseModel):
    bot_token: str
    bot_channel_id: int


class Settings(BaseSettings):
    discord: DiscordSettings
    fabman_webhook_secret: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )
