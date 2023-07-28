from airflow import DAG
from airflow.operators.python import PythonOperator
from pytz import timezone
from datetime import datetime, timedelta
from random import sample
from pymongo import MongoClient
from config import user_api_key, sharded_db_connection_string
from updated_lol import MatchCollect, User
import pymongo
import time

# 한국 시간대 설정
korea_tz = timezone('Asia/Seoul')

# 오늘 자정을 한국 시간대 기준으로 계산
start_date = datetime.now(korea_tz).replace(hour=0, minute=0, second=0, microsecond=0)

dag = DAG(
    'update_mongodb_dag',
    default_args={
        'owner': 'airflow',
        'start_date': start_date,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple tutorial DAG',
    schedule='*/5 * * * *',  # Change to every 5 minutes
    catchup=False,
    dagrun_timeout=timedelta(minutes=60)
)


def update_mongodb():

    client = MongoClient(sharded_db_connection_string)
    Users_DB = client['users']
    Match_DB = client['match']

    start_time = time.time()

    total = 0

    all_docs = list(Users_DB['New_User_Matchlist'].find({}, {'_id':0, 'name':1, 'puuid':1, 'matchlist':1}).limit(100))
    selected_docs = sample(all_docs, 5)
    # New_User_Matchlist에 저장되어 있는 유저들에 대해서 가져옴.
    for doc in selected_docs:
        users_name = doc.get('name') 
        users_puuid = doc.get('puuid') 
        old_matchlist = doc.get('matchlist')

        users = User(user_api_key)
        users_new_puuid = users.get_summon_by_gamename(users_name).get('puuid') 
        new_matchlist = users.get_users_matchlist_by_puuid(puuid = users_new_puuid)

        matches_to_update = set(new_matchlist)-set(old_matchlist)
        total += len(matches_to_update)
        
        Users_DB['New_User_Matchlist'].update_one({'name': users_name}, {'$set': {'matchlist': new_matchlist}})

        if len(matches_to_update)>0:    
            for matchId in matches_to_update:
                try:
                    raw_data = (MatchCollect(matchId, user_api_key).get_raw_matchinfo())['info']
                except Exception as e:
                    continue
                gameVersion = raw_data['gameVersion']
                mainVersion, secondVersion = map(int,gameVersion.split('.')[0:2])
                if mainVersion>=13 and secondVersion>=11:
                    collection_name = f'test_Airflow_test_Match_info_ver_{str(mainVersion)}_{str(secondVersion)}'
                    try:
                        Match_DB[collection_name].insert_one(raw_data)
                    except pymongo.errors.DuplicateKeyError:
                        pass  
                else:
                    pass

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Updated {total} matches. It took {elapsed_time} seconds.")

update_mongodb_task = PythonOperator(
    task_id='update_mongodb_task', 
    python_callable=update_mongodb,
    dag=dag
)