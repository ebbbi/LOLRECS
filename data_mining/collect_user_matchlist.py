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
import logging
from config import db_connection_string, user_api_key

from scipy.spatial import distance
import argparse
import sys

import time
import pytz
import asyncio 
import aiohttp

async def main(args):
    class KSTFormatter(logging.Formatter):
        def formatTime(self, record, datefmt=None):
            ct = self.converter(record.created)
            if datefmt:
                s = time.strftime(datefmt, ct)
            else:
                t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
                s = "%s,%03d" % (t, record.msecs)
            return s

        def converter(self, timestamp):
            utc_dt = datetime.utcfromtimestamp(timestamp)
            aware_utc_dt = pytz.utc.localize(utc_dt)
            kst_dt = aware_utc_dt.astimezone(pytz.timezone('Asia/Seoul'))
            return kst_dt.timetuple()
        


    formatter = KSTFormatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')

    # 로거 생성
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Info log directory
    info_log_dir = '/opt/ml/final/logging/Collect_Summonerprofile'
    if not os.path.exists(info_log_dir):
        os.makedirs(info_log_dir)

    # Info 로그 파일 핸들러를 설정합니다.
    info_file_handler = logging.FileHandler(f'{info_log_dir}/info.log')
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)

    # Error log directory
    error_log_dir = '/opt/ml/final/logging/Collect_Summonerprofile'
    if not os.path.exists(error_log_dir):
        os.makedirs(error_log_dir)

    # Error 로그 파일 핸들러를 설정합니다.
    error_file_handler = logging.FileHandler(f'{error_log_dir}/error.log')
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)

    # 각 핸들러를 로거에 추가합니다.
    logger.addHandler(info_file_handler)
    logger.addHandler(error_file_handler)


    # 우선 MongoDB 접속
    cluster = MongoClient(db_connection_string)
    Users_DB = cluster['users']

    num_parts = 6  # 실행하려는 프로세스 수
    part = args.part  # 이 프로세스가 처리해야 할 부분 (0부터 num_parts-1까지)

    total_documents = Users_DB['test_New_League_User_info'].count_documents({})
    documents_per_part = total_documents // num_parts

    skip = part * documents_per_part
    limit = documents_per_part if part < num_parts - 1 else total_documents - skip
    cursor = Users_DB['test_New_League_User_info'].find({}, {'summonerName':1}).skip(skip).limit(limit)
    summoner_names_in_db = set(document['name'] for document in Users_DB['New_User_Matchlist'].find({}, {'name': 1}))


 
    for doc in cursor:
        summonerName = doc.get('summonerName')
        if summonerName in summoner_names_in_db:
            logger.info(f"User {summonerName} already exists in the database")
            continue
        try:
            user = User(args.api_key)

            # 두 함수를 동시에 실행
            users_info_future = user.get_raw_summon_by_gamename(gamename=summonerName)
            users_info = await users_info_future
            matchlist_future = user.get_users_matchlist_by_puuid(puuid = users_info.get('puuid'))
            
            # Match list를 가져올 때 까지 기다립니다.
            matchlist = await matchlist_future

            Users_DB['New_User_Matchlist'].update_one({'name': summonerName},
                                                     {'$set': {'summonerId':users_info.get('id'),
                                                               'puuid':users_info.get('puuid'),
                                                               'matchlist': matchlist}},
                                                     upsert=True)

            logger.info(f"Successfully updated user {summonerName}")
        except Exception as e:
            logger.error(f"Error processing summoner {summonerName}: {e}")
        # 로깅 메시지 추가
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Collect summoner IDs and match IDs from Riot API.")
    parser.add_argument('--api_key', type=str, required=True, help='API key for Riot API')
    parser.add_argument('--part', type=int, required=True, help='Splited data part')
    args = parser.parse_args()
    
    # 이벤트 루프 가져오기 및 실행
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))