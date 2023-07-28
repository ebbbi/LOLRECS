* updated_lol.py가 기본적인 함수이며 collect_로 시작하는 파일들 中 비동기 함수를 사용하는 주된 모듈입니다. 
* updated_lol_backup.py는 이전 코드들 중 동기 함수로 작업한 적이 있었는데, 해당 파일을 백업해둔 것입니다.
* data_file.pkl 은 기존에 저장되어 있던 matchId list 모음입니다. MongoDB를 이용해서 모든 docs들에서 matchlist 필드를 읽은 뒤 unwind 시키고 그것들 중 unique 한 것을 모으는 작업이 메모리를 많이 잡아먹는다는 판단이 들어서 서버의 부하를 줄이기 위해 우선 pkl 파일로 별도로 사용했습니다.
* multiprocess_match_info.py와 sh 스크립트 파일은, collect_match_info의 속도를 올리기 위한 별도의 함수로, multiprocess 함수는 collect_match_info를 여러 터미널에서 동시에 돌리는 코드입니다. 다만 date.file로 받아온 경기 정보들을 반복적으로 슬라이싱해서 각각의 api_key를 각각의 터미널을 할당해서 matchlist에 대한 정보를 분할작업하는 코드입니다. 이렇게 구성하지 않으면 DB 서버가 메모리를 많이 지속적으로 잡아먹기 때문에 서버가 터지는 일이 발생합니다.
* 마지막으로 refactoring_collect_data.py는 현재는 사용하지 않는 함수이지만, 일련의 과정을 전부 수행하는 코드입니다. 추후에는 refactoring_collect_data를 개선시킬 필요가 있습니다. leauge page로부터 유저들의 이름들을 받아오고, 그 유저들의 매치리스트를 받아오고 또 매치리스트들을 풀어서 각각 matchlist에 저장하는 코드였습니다. 
* data_mining은 aistages에서 제공된 서버에서 실행시키는 함수들입니다.
* 용량상 data_file.pkl을 올리진 않지만 다음과 같은 코드를 통해 data_file.pkl을 만들었습니다.

```python
 import asyncio
 from motor.motor_asyncio import AsyncIOMotorClient


 async def fetch_matchlist_group(skip, limit):
     cluster = AsyncIOMotorClient(sharded_db_connection_string)
     api_key = user_api_key
     Users_DB = cluster['users']
     Match_DB = cluster['match']
     cursor = Users_DB['New_User_Matchlist'].find({}, {'matchlist': 1}).skip(skip).limit(limit)
     matchlist_group = set()

     async for doc in cursor:
         matchlist_group.update(doc['matchlist'])

     return matchlist_group

 async def fetch_user_matchlists_parallel(num_users):
     all_matchlists = set()
     group_size = 20000  # 한 그룹에 속하는 사용자 수
     num_groups = num_users // group_size  # 사용자를 나눌 그룹 수

     if num_users % group_size > 0:
         num_groups += 1  # 사용자 수가 group_size로 나누어 떨어지지 않으면 한 그룹을 더 추가

     tasks = [fetch_matchlist_group(i * group_size, group_size) for i in range(num_groups)]
     matchlist_groups = await asyncio.gather(*tasks)

     for matchlist_group in matchlist_groups:
         all_matchlists.update(matchlist_group)
     return all_matchlists

 num_users = await Users_DB['New_User_Matchlist'].count_documents({})  
 
 # 전체 사용자 수
 loop = asyncio.get_event_loop()
 all_matchlists = loop.run_until_complete(fetch_user_matchlists_parallel(num_users))

import pickle

docslist = [{'_matchId': matchId} for matchId in all_matchlists]
# 파일에 데이터를 저장합니다.
with open('data_file.pkl', 'wb') as file:
    pickle.dump(docslist, file)
```