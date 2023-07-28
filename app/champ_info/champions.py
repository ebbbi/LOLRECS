from fastapi import FastAPI, HTTPException
import aiohttp
import logging
import ssl
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

api = os.environ["RIOT_API_KEY"]


async def get_free_champs(region: str):
    try:
        async with aiohttp.ClientSession() as client:
            r = await client.get(f"https://{region}.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={api}", ssl=ssl.SSLContext())
        return await r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def get_champ_info(version: str):
    try:
        async with aiohttp.ClientSession() as client:
            # async with client.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json") as r:
            async with client.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json", ssl=ssl.SSLContext()) as r:
                if r.status != 200:
                    logger.error(f"Error: HTTP status is {r.status}, text: {await r.text()}")
                    return []
                else:
                    data = await r.json()
                    if 'data' in data:
                        return list(data['data'].values())
                    else:
                        logger.error("Error: 'data' not in response")
                        return []
    except Exception as e:
        logger.error(f"Error when getting champion info: {str(e)}")
        return []
