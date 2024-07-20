from pydantic import BaseModel

from pydantic_settings import BaseSettings


class DiscordSettings(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str

    bot_token: str
    bot_channel_id: int


class Settings(BaseSettings):
    discord: DiscordSettings
    fabman_webhook_secret: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
