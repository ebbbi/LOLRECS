from fastapi import FastAPI
from typing import List, Dict, Any, Union
import asyncio, aiohttp
import ujson
import ssl
import os

app = FastAPI()

api = os.environ["RIOT_API_KEY"]

async def get_summoner_name(summoner: str, region: str) -> Dict[str, Any]:
    try:
        async with aiohttp.ClientSession() as client:
            r = await client.get(f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={api}", ssl=ssl.SSLContext())
            return await r.json(loads=ujson.loads)
    except Exception as e:
        print('Error with Summoner')
        print(f"Error: {e}")


async def get_masteries(id: str, region: str) -> Dict[str, Any]:
    try:
        async with aiohttp.ClientSession() as client:
            r = await client.get(f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id}?api_key={api}", ssl=ssl.SSLContext())
            r = await r.json(loads=ujson.loads)
            result = {hist["championId"]:hist["championPoints"] for hist in r}
            return result
    except Exception:
        print('Masteries not found')
        return {}


async def get_rank(id: str, region: str) -> Dict[str, Any]:
    try:
        async with aiohttp.ClientSession() as client:
            r = await client.get(f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}?api_key={api}", ssl=ssl.SSLContext())
            return await r.json(loads=ujson.loads)
    except Exception:
        print('Error with Rank')
        return {}


async def get_version() -> str:
    try:
        async with aiohttp.ClientSession() as client:
            # r = await client.get('https://ddragon.leagueoflegends.com/api/versions.json')
            r = await client.get('https://ddragon.leagueoflegends.com/api/versions.json', ssl=ssl.SSLContext())
            data = await r.json(loads=ujson.loads)
            return data[0]
    # except Exception:
    #     print('Error with Version')
    #     return ""
    except Exception as e:
        print('Error with Version')
        print(f"Error: {e}")


async def get_maps() -> List[Dict[str, Any]]:
    try:
        async with aiohttp.ClientSession() as client:
            # r = await client.get('https://static.developer.riotgames.com/docs/lol/maps.json')
            r = await client.get('https://static.developer.riotgames.com/docs/lol/maps.json', ssl=ssl.SSLContext())
            return await r.json(loads=ujson.loads)
    # except Exception:
    #     print('Error with Maps')
    #     return []
    except Exception as e:
        print('Error with Maps')
        print(f"Error: {e}")


async def get_queues() -> List[Dict[str, Any]]:
    try:
        async with aiohttp.ClientSession() as client:
            # r = await client.get('https://static.developer.riotgames.com/docs/lol/queues.json')
            r = await client.get('https://static.developer.riotgames.com/docs/lol/queues.json', ssl=ssl.SSLContext())
            r = await r.json(loads=ujson.loads)
            r.append({"queueId": 1700, 
                        "map": "Arena",
                        "description": "Arena",
                        "notes": None})
            return r
    # except Exception:
    #     print('Error with Queues')
    #     return []
    except Exception as e:
        print('Error with Queues')
        print(f"Error: {e}")


async def get_match_list(id: str, region: str, start: int, count: int) -> List[int]:
    # Replace this function with the equivalent in Python
    def convert_region(region: str) -> str:
        if region in ['NA1', 'BR1', 'LA1', 'OC1']:
            return 'americas'
        elif region in ['EUN1', 'EUW1', 'RU', 'TR1']:
            return 'europe'
        elif region in ['JP1', 'KR']:
            return 'asia'
    try:
        async with aiohttp.ClientSession() as client:
            r = await client.get(f"https://{convert_region(region)}.api.riotgames.com/lol/match/v5/matches/by-puuid/{id}/ids?start={start}&count={count}&api_key={api}", ssl=ssl.SSLContext())
            # print(r.json())
            return await r.json(loads=ujson.loads)
    except Exception:
        return []


async def get_match_details(id: str, region: str) -> Dict[str, Any]:
    def convert_region(region: str) -> str:
        if region in ['NA1', 'BR1', 'LA1', 'OC1']:
            return 'americas'
        elif region in ['EUN1', 'EUW1', 'RU', 'TR1']:
            return 'europe'
        elif region in ['JP1', 'KR']:
            return 'asia'

    try:
        async with aiohttp.ClientSession() as client:
            r = await client.get(f"https://{convert_region(region)}.api.riotgames.com/lol/match/v5/matches/{id}?api_key={api}", ssl=ssl.SSLContext())
            data = await r.json(loads=ujson.loads)
            return data.get('info', {})
    except Exception:
        if hasattr(Exception, 'response') and hasattr(Exception.response, 'status'):
            return {"participants": []}
        else:
            return {}


async def get_live(id: str, region: str, queues: List[Dict[str, Any]]) -> Union[Dict[str, Any], str]:
    try:
        async with aiohttp.ClientSession() as client:
            r = await client.get(f"https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{id}?api_key={api}", ssl=ssl.SSLContext())
            live_data = await r.json()
            rank_array = await asyncio.gather(
                *[client.get(f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{player['summonerId']}?api_key={api}", ssl=ssl.SSLContext()) for player in live_data['participants']]
            )
            live_data['rankArray'] = [await resp.json() for resp in rank_array]
            for queue in queues:
                if live_data['gameQueueConfigId'] == queue['queueId']:
                    live_data['queueName'] = ' '.join(queue['description'].split(' ')[:3])
            return live_data
    except Exception:
        print('Not in Live Game')
        return 'Not In Live Game'

def get_backup() -> Dict[str, Any]:
    try:
        with open('../Items/backupItems.json') as f:
            data = ujson.load(f)
        return data
    except Exception:
        print('Backup not available')
        return {}
