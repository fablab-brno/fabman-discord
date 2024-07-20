from fastapi import APIRouter

from fabman_discord.dependencies import get_discord_client

router = APIRouter()


@router.get("/login")
async def start_login():
    discord_client = get_discord_client()
    return discord_client.redirect()


@router.get("/callback")
async def finish_login(code: str):
    discord_client = get_discord_client()
    user = await discord_client.login(code)

    # print(user.id)
    # print(user.username)
    # print(user)

    return user
