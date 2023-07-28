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
info_log_dir = '/opt/ml/final/logging/Collect_League'
if not os.path.exists(info_log_dir):
    os.makedirs(info_log_dir)

# Info 로그 파일 핸들러를 설정합니다.
info_file_handler = logging.FileHandler(f'{info_log_dir}/info.log')
info_file_handler.setLevel(logging.INFO)
info_file_handler.setFormatter(formatter)

# Error log directory
error_log_dir = '/opt/ml/final/logging/Collect_League'
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
api_key = user_api_key # 철현 API
Users_DB = cluster['users']
Match_DB = cluster['match']

# 플레이어 이름으로 인덱스를 생성
Users_DB['test_New_League_User_info'].create_index('summonerName', unique=True)


# Restart from the last successful location
restart_tier = 'IRON'
restart_division = 'IV'
restart_page = 150

tiers = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']
divisions = ['IV', 'III', 'II', 'I']

tier_idx = tiers.index(restart_tier)
divisions = divisions[divisions.index(restart_division):]

# 존재하지 않는 페이지에 도달하면 stop 이라는 변수를 사용하여 반복을 중지합니다.
for tier in tiers[tier_idx:]:
    for division in divisions:
        stop = False
        if tier == restart_tier and division == restart_division:
            i = restart_page
        else:
            i = 1
        while not stop:
            try:
                logger.info(f"Processing {tier} {division} page {i}")
                l = League(api_key).get_raw_league_summonerId(division, tier, page=i)
                if not l:  
                    stop = True
                    logger.info(f"No more pages in {tier} {division}. Stopping.")
                    continue
                try:
                    Users_DB['test_New_League_User_info'].insert_many(l, ordered=False)
                    logger.info(f"Inserted page {i} of {tier} {division} successfully")
                except pymongo.errors.BulkWriteError as e:
                    # ignore duplicate key errors
                    errors = e.details.get('writeErrors')
                    if errors:
                        for err in errors:
                            if err.get('code') == 11000:  # duplicate key error code
                                logger.warning(f"Duplicated key error ignored: {err.get('errmsg')}")
                            else:
                                logger.error(f"BulkWriteError: {err.get('errmsg')}")
                                raise
            except Exception as e:
                logger.error(f"An error occurred: {e}")
            finally:
                i += 1

