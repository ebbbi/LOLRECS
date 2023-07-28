from fastapi import FastAPI
from typing import List
from datetime import datetime
from .summoner import get_masteries, get_match_list, get_match_details
from copy import deepcopy
import asyncio


app = FastAPI()


async def get_summoner_masteries(id: str, region: str, champInfo: List):
    masteryRes = await get_masteries(id, region)
    champObject = []
    if not masteryRes:
        return champObject
    champMastery = len(masteryRes) if len(masteryRes) < 5 else 5
    
    for i in range(champMastery):
        for champ in champInfo:
            if int(champ["key"]) == masteryRes[i]['championId']:
                object = {
                    'name': champ["name"],
                    'id': champ["id"],
                    'key': masteryRes[i]['championId'],
                    'image': champ["image"]['full'],
                    'level': masteryRes[i]['championLevel'],
                    'points': masteryRes[i]['championPoints'],
                }
                champObject.append(object)
    return champObject


async def get_summoner_matches(summoner_res, region: str, queues: List, champInfo: List, start: int, count: int):
    match_list = await get_match_list(summoner_res["puuid"], region, start, count)
    matchArr = []
    if not match_list:
        return matchArr
    matches = len(match_list) if len(match_list) < 7 else 7
    
    tasks = []
    for i in range(matches):
        matchDetails = asyncio.create_task(get_match_details(match_list[i], region))
        tasks.append(create_game_object(summoner_res, queues, champInfo, matchDetails))
    matchArr = await asyncio.gather(*tasks)
    
    return matchArr


async def get_more_matches(gameIds: List[str], summoner_res, region: str, queues: List, champInfo: List):
    matchArr = []
    for game_id in gameIds:
        matchDetails = await get_match_details(game_id, region)
        matchArr.append(await create_game_object(summoner_res, queues, champInfo, matchDetails))
    return matchArr


async def create_game_object(summoner_res, queues, champInfo, matchDetails):
    matchDetails = await matchDetails
    matchObj = [queue for queue in queues if queue["queueId"] == matchDetails['queueId']]
    if len(matchObj) == 0:
        return {}
    matchObj = deepcopy(matchObj[0])

    matchObj["map"] = matchObj["map"]
    matchObj["gameType"] = matchObj["description"]
    matchObj['gameCreation'] = datetime.fromtimestamp(matchDetails['gameCreation'] / 1e3).strftime('%c')
    matchObj['originalDate'] = matchDetails['gameCreation']
    matchObj['gameDuration'] = matchDetails['gameDuration']
    matchObj['gameVersion'] = '.'.join(matchDetails['gameVersion'].split('.')[:2])
    matchObj['players'] = []
    matchObj['participants'] = matchDetails['participants']
    matchObj['platformId'] = matchDetails['platformId']

    playerObj = {}
    for id in matchDetails['participants']:
        if id['puuid'] == summoner_res['puuid'] or id['summonerId'] == summoner_res['id']:
            matchObj['participantId'] = id['participantId']
            
        for part in matchDetails['participants']:
            if id['participantId'] == part['participantId']:
                playerObj = {
                    'id': id['participantId'],
                    'name': id['summonerName'],
                    'champId': part['championId'],
                    'champName': part['championName'],
                }
                
                for key in champInfo:
                    if playerObj['champName'].lower() == key['id'].lower():
                        playerObj['image'] = key['image']['full']
        matchObj['players'].append(playerObj)

    for data in matchDetails['participants']:
        if data['participantId'] == matchObj['participantId']:
            playerStats = data
            matchObj['playerInfo'] = playerStats

    for champ in champInfo:
        if 'playerInfo' in matchObj and matchObj['playerInfo']['championName'].lower() == champ['id'].lower():
            matchObj['championName'] = champ['name']
            matchObj['championImage'] = champ['image']['full']
    return matchObj