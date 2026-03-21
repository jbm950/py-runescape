import httpx

from model import Player

HISCORES_BASE_URL = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.json?player='


async def get_player(player):
    async with httpx.AsyncClient() as client:
        resp = await client.get(HISCORES_BASE_URL + player)

    return Player(**resp.json())
