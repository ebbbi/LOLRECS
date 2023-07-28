import pymongo
from collections import defaultdict
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from updated_lol import MatchCollect, User, League, get_tier_by_user, collect_summonerId, collect_matchId_from_summonerpkl, create_directory_path, collect_preprocessing_matchdata, get_gameids, get_timeline_match_data_list_participants, most_common_player
import requests
import urllib.parse
import pandas as pd
from datetime import datetime, timedelta
import time
from collections import defaultdict
import argparse
import os
import aiofiles
from config import db_connection_string, user_api_key, sharded_db_connection_string
from motor.motor_asyncio import AsyncIOMotorClient

from scipy.spatial import distance
import argparse
import sys

import time
import pytz
import asyncio 
import aiohttp
import pickle

# 파일로부터 데이터를 불러옵니다.
with open('data_file.pkl', 'rb') as file:
    loaded_docslist = pickle.load(file)
docslist = loaded_docslist

# 우선 MongoDB 접속
cluster = AsyncIOMotorClient(sharded_db_connection_string)
Users_DB = cluster['users']
Match_DB = cluster['match']

async def write_log(log_file, message):
    now = datetime.now(pytz.timezone('Asia/Seoul'))  # Get the current time in KST
    time_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")  # Convert it to a string in the provided format
    async with aiofiles.open(log_file, mode='a') as f:
        await f.write(f'{time_string} {message}\n')  # Prepend the time string to the message

async def fetch_and_insert(i, api_key, info_log, error_log):
    try:
        matchId = i.get('_matchId')
        # await write_log(info_log, f"Fetching match info for {matchId}")
        try:
            raw_data = (await MatchCollect(matchId, api_key).get_raw_matchinfo())['info']
        except Exception as e:
            await write_log(error_log, f'Error fetching data for {matchId}: {e}')
            return False  # We return False from the function here because if data fetching failed, the rest of the function can't proceed
        gameVersion = raw_data['gameVersion']
        mainVersion, secondVersion = map(int,gameVersion.split('.')[0:2])
        if mainVersion>=13 and secondVersion>=11:
            collection_name = f'Match_info_ver_{str(mainVersion)}_{str(secondVersion)}'
            try:
                await write_log(info_log, f"Attempting to insert matchId {matchId} into {collection_name}")
                await Match_DB[collection_name].insert_one(raw_data)
                await write_log(info_log, f"Successfully inserted matchId {matchId} into {collection_name}")  # matchId 정보 로그에 추가
            except DuplicateKeyError:
                pass  # Ignore duplicate key errors
        else:
            pass
    except Exception as e:
        await write_log(error_log, f'Error on {i}: {e}')
        return False
    return True  # Return True if everything went well

async def main(start, end, api_key, info_log, error_log):
    semaphore = asyncio.Semaphore(40)
    async def fetch_and_insert_semaphore(i):
        async with semaphore:
            return await fetch_and_insert(i, api_key, info_log, error_log)
        
    tasks = [fetch_and_insert_semaphore(i) for i in docslist[start:end]]
    results = await asyncio.gather(*tasks)
    
    successful_insertions = results.count(True)
    await write_log(info_log, f"Successful insertions: {successful_insertions}")
    
    # 모든 로그 기록 작업이 완료될 때까지 대기
    while not asyncio.all_tasks() == {asyncio.current_task()}:
        await asyncio.sleep(1)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--start', type=int, required=True, help='Start index for docslist')
    parser.add_argument('--end', type=int, required=True, help='End index for docslist')
    parser.add_argument('--api_key', type=str, required=True, help='API key')
    parser.add_argument('--log_dir', type=str, required=True, help='Log directory')

    args = parser.parse_args()

    # Now instead of creating a new directory every time, we'll use the one provided in args.log_dir
    # Get rid of the previous time string creation logic

    info_log = os.path.join(args.log_dir, 'info.log')
    error_log = os.path.join(args.log_dir, 'error.log')

    loop = asyncio.get_event_loop()

    # 시작 시간 기록
    start_time = time.time()

    # 메인 함수 실행
    loop.run_until_complete(main(args.start, args.end, args.api_key, info_log, error_log))

    # 종료 시간 기록
    end_time = time.time()

    # 전체 시간 로그에 기록
    loop.run_until_complete(write_log(info_log, f'Start: {args.start}, End: {args.end}, Total time: {end_time - start_time} seconds'))
