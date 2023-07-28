from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
import base64
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../..')) 

from app.champ_info.summoner import get_summoner_name, get_rank, get_version, get_maps, get_queues, get_masteries, get_match_list, get_live
from app.champ_info.champions import get_champ_info
from app.champ_info.utils import get_summoner_matches

from app.champ_classification.datasets import makeData
from app.champ_classification.inference import getChampNameList
from app.champ_rec import inference

from app.item_rec import ItemRecommender
import asyncio

app = FastAPI()

@app.middleware("http")
async def correct_requests(request: Request, call_next):

    if "http" == request.scope["path"][:4]:
        request.scope["path"] = request.scope["path"][7+request.scope["path"][7:].find('/'):]
        request.scope["raw_path"] = request.scope["path"].encode('utf-8')

    response = await call_next(request)

    return response

# Set CORS
# origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

maps = None
queues = None
version = None
champInfo = None

async def fetch_data():
    maps = await get_maps()
    queues = await get_queues()
    version = await get_version()
    champInfo = await get_champ_info(version)
    return maps, queues, version, champInfo


@app.get("/summoners/{summoner}")
async def get_summoner_info(summoner: str):
    summoner_res = await get_summoner_name(summoner, 'kr')
    print(f"summoner_res: {summoner_res}")
    if summoner_res["id"]:
        data = await get_rank(summoner_res["id"], 'kr')
        return {
            "summonerInfo": summoner_res,
            "rank": data
        }
    else:
        raise HTTPException(status_code=404, detail="Summoner not found")


@app.get("/summoners/{summoner}/exists")
async def get_summoner_exists(summoner: str):
    summoner_res = await get_summoner_name(summoner, 'kr')
    if summoner_res["id"]:
    
        return {
            "existence": "Summoner found"
        }
    else:
        raise HTTPException(status_code=404, detail="Summoner not found")


@app.get("/matches/{summoner}/{start}/{count}")
async def get_match_info(summoner: str, start: int, count: int):
    summoner_res = await get_summoner_name(summoner, 'kr')

    if summoner_res["id"]:
        data = await get_summoner_matches(summoner_res, 'KR', queues, champInfo, start, count)
        return {
            "matchHistory": data
        }
    else:
        raise HTTPException(status_code=404, detail="Summoner not found")



# 화면 인식, 챔피언 분류
@app.post("/recognize")
async def get_recognize(request: Request):
    data = await request.json()
    image_data = data.get("image")
    image_data = base64.b64decode(image_data.split(",")[1])

    image_data = np.fromstring(image_data, dtype=np.uint8)
    image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    makeData(image_data)
    banpicList = getChampNameList()     # 이름 20개 들어 있음
    print(banpicList)
    return {
        'banpicList': banpicList
        }


# 챔피언 추천
@app.post("/get-pick-data")
async def send_data(data: Request):
    data = await data.json()
    summoner = data["username"]
    summoner_res = await get_summoner_name(summoner, 'kr')
    if summoner_res["id"]:
        masteries = await get_masteries(summoner_res["id"], 'kr')
        results = inference(data["allies"], data["enemies"], data['bans'], masteries)
        print(results)
        return {"results" : results}
    else:
       raise HTTPException(status_code=404, detail="Summoner not found")

# 아이템 추천
@app.post("/get-item-data")
async def send_item_data(data: Request):
    data = await data.json()
    """
    request에는 내 챔피언, 포지션, 상대챔피언 정보가 담겨있음
    """
    my = data["my"]
    pos = data["posi"]
    op = data["op"]
    
    itemrec = ItemRecommender()
    
    result = await asyncio.gather(*[
        itemrec.get_two_items(my, pos, op),
        itemrec.get_three_items(my, pos, op),
        itemrec.get_four_items(my, pos, op)
    ])

    results = [*result[0], *result[1], *result[2]]


    return {
        "results" : results
    }



@app.on_event("startup")
async def on_app_start():
    global maps, queues, version, champInfo
    maps, queues, version, champInfo = await fetch_data()


@app.on_event("shutdown")
async def on_app_shutdown():
    pass
