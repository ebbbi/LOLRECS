import requests
import urllib.parse
import pandas as pd
import time
from collections import defaultdict
import numpy as np
import logging
import os
import datetime
import pickle
from scipy.spatial import distance
from collections import Counter
from datetime import datetime
from pytz import timezone
import aiohttp
import asyncio


tier_dict=defaultdict(int)
for ind, value in enumerate(['IRON','BRONZE','SILVER','GOLD','PLATINUM', 'DIAMOND']):
    for ind2, value2 in enumerate(['IV','III', 'II', 'I']):
        tier_dict[value+'-'+value2] = 100*ind + 25*ind2
tier_dict['UNRANK']=np.nan
tier_dict['MASTER']=700
tier_dict['GRANDMASTER']=800
tier_dict['CHALLENGER']=900

position_dict = {'TOP':0, 'JUNGLE':1, "MIDDLE":2, "BOTTOM":3, "UTILITY":4}
position_average_coordinate = {'player0_pos': (2597.8559999999993, 10679.276000000003), 'player1_pos': (6022.248000000001, 6103.911999999999), 'player2_pos': (6601.931999999998, 6747.974000000001), 'player3_pos': (10762.358, 2229.248), 'player4_pos': (10754.846000000001, 2303.772), 'player5_pos': (3859.06, 12433.024000000001), 'player6_pos': (9216.403999999999, 8342.454000000002), 'player7_pos': (8226.187999999996, 8140.3780000000015), 'player8_pos': (12645.816, 3841.8700000000017), 'player9_pos': (12350.0, 4155.099999999999)}

player_to_position = {
    "player0_pos": "TOP",
    "player1_pos": "JUNGLE",
    "player2_pos": "MIDDLE",
    "player3_pos": "CARRY",
    "player4_pos": "SUPPORT",
    "player5_pos": "TOP",
    "player6_pos": "JUNGLE",
    "player7_pos": "MIDDLE",
    "player8_pos": "CARRY",
    "player9_pos": "SUPPORT"
}

# def get_current_time():
#     # 한국 시간으로 현재 시간을 반환하는 함수
#     korea_tz = timezone('Asia/Seoul')
#     current_time = datetime.now(tz=korea_tz)
#     return current_time.strftime("%Y-%m-%d %H:%M:%S")

class KSTFormatter(logging.Formatter):
    converter = datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.astimezone(timezone('Asia/Seoul')).strftime(datefmt)
        else:
            try:
                s = dt.astimezone(timezone('Asia/Seoul')).isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.astimezone(timezone('Asia/Seoul')).isoformat()
        return s

handler = logging.StreamHandler()
handler.setFormatter(KSTFormatter('%(asctime)s [%(levelname)s] %(message)s'))
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

def get_tier_by_user(summonerid:str, region:str='kr', api_key=None):
    r = f"https://{region}.api.riotgames.com/lol/league/v4/entries/{summonerid}?api_key={api_key}"
    r = requests.get(r).json()
    if isinstance(r, dict) and r.get('status', {}).get('status_code') == 429:
        # API rate limit exceeded, wait for a specific duration
        wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
        logging.info("API rate limit exceeded. Waiting for rate limit reset...(get_tier_by_users)")
        time.sleep(wait_duration)
        return get_tier_by_user(summonerid, region, api_key)  # Retry the API call after waiting


    if len(r)==2:
        if r[0]['queueType']=='RANKED_SOLO_5x5':
            # "Here1", r[0]['queueType'], r[0]['tier']+'-'+r[0]['rank'], 
            return r[0]['tier']+'-'+r[0]['rank']
        else:
            #"Here2", r[1]['queueType'], r[1]['tier']+'-'+r[1]['rank'], 
            return r[1]['tier']+'-'+r[1]['rank']
    
    elif r == []:
        return 'UNRANK'
    
    else:
        return r[0]['tier']+'-'+r[0]['rank']


class MatchCollect():
    def __init__(self, gameid, api_key):
        self.tier_dict = tier_dict
        self.api_key = api_key
        self.gameid = gameid

        # 다음 df 설정은, gmae_participants에 killingSprees와 같이 중복되는, 하지만 다른 의미를
        # 갖는 column들을 구분하기 위함. 아마 killingSprees는 연속적으로 몇 번 킬을 했는지 (개인별, 팀별)의 의미를
        # 가지고 있을 가능성이 있다.
        # ---------------------------------------

    def get_banlist(self, gameid:str=None, region:str='asia', api_key=None):
        '''
        특정 게임에서 밴 된 캐릭터들을 불러오는 코드입니다. 이는 get_teaminfo()를 사용합니다.
        '''
        if gameid == None:
            gameid = self.gameid
        if api_key == None : 
            api_key = self.api_key

        teams = self.get_teaminfo(gameid, region, api_key)['info']['teams']

        if teams == []:
            ban_list = None
        else:
            ban_list = [v for i in pd.DataFrame(teams).bans for j in i for k, v in j.items() if k == 'championId']
        
        return ban_list

    def get_raw_matchinfo(self, gameid:str=None, region:str='asia', api_key=None):
        '''
        game_metadata는 받아온 json 파일을 그대로 사용한다.
        game_info는 participants와 perks를 제외한 자료이다. 실질적인 game의 시작시간, 종료시간 등의 정보를 담았지만, 개별 플레이어에 대한 정보는 없다.
        df_game_participants가 해당 게임의 0~9번째 플레이어들의 룬, 스펠, challenges (분당 데미지 등등)을 담고 있는 정보이다.

        11시즌을 포함해서 11시즌 이전에는 challenges라는 column이 존재하지 않는다. 따라서 반복적으로 df를 concat할 일이 있다면 예외처리를 해줘야한다.
        '''
        if gameid == None:
            gameid = self.gameid
        if api_key == None : 
            api_key = self.api_key

        r = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{gameid}?api_key={api_key}'
        game = requests.get(r).json()

        if isinstance(game, dict) and game.get('status', {}).get('status_code') == 429:
            # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            logging.info("API rate limit exceeded. Waiting for rate limit reset...")
            time.sleep(wait_duration)
            return self.get_raw_matchinfo(gameid, region, api_key)  # Retry the API call after waiting
        
        return game

    def get_matchinfo(self, gameid:str=None, region:str='asia', api_key=None):
        '''
        game_metadata는 받아온 json 파일을 그대로 사용한다.
        game_info는 participants와 perks를 제외한 자료이다. 실질적인 game의 시작시간, 종료시간 등의 정보를 담았지만, 개별 플레이어에 대한 정보는 없다.
        df_game_participants가 해당 게임의 0~9번째 플레이어들의 룬, 스펠, challenges (분당 데미지 등등)을 담고 있는 정보이다.

        11시즌을 포함해서 11시즌 이전에는 challenges라는 column이 존재하지 않는다. 따라서 반복적으로 df를 concat할 일이 있다면 예외처리를 해줘야한다.
        '''
        if gameid == None:
            gameid = self.gameid
        if api_key == None : 
            api_key = self.api_key

        r = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{gameid}?api_key={api_key}'
        game = requests.get(r).json()

        if isinstance(game, dict) and game.get('status', {}).get('status_code') == 429:
            # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            logging.info("API rate limit exceeded. Waiting for rate limit reset...")
            time.sleep(wait_duration)
            return self.get_matchinfo(gameid, region, api_key)  # Retry the API call after waiting

    
        # 다음 1줄은 game_metadata에 관련된 부분
        # 다음은 game_info와 관련된 부분
        try:
            game_metadata = game['metadata']   
            game_info = game['info']
        except KeyError as e:
            logging.error(f"KeyError occurred with game id: {gameid}, key: {e.args[0]}")
            raise ValueError("Metadata or info is missing from the game data")

        filtered_info = {key: value for key, value in game_info.items() if key not in ['participants', 'teams']}
        game_info = pd.DataFrame.from_dict(filtered_info, orient='index').T

        game_participants = game['info']['participants']
        df_game_participants = pd.DataFrame(game_participants)    
        try:
            # Check if 'challenges' column exists
            if 'challenges' in df_game_participants.columns:
                try:
                    df_challenge_list = [pd.DataFrame([pd.DataFrame(df_game_participants.challenges).iloc[i][0]]) for i in range(10)]
                    Y = pd.concat(df_challenge_list, axis=0).reset_index(drop=True)
                except Exception as e:
                    logging.error(f"An error occurred with gameid {gameid}: {str(e)}")
            else:
                Y = pd.DataFrame()  # Create an empty DataFrame for Y if 'challenges' does not exist

            df_perks_list = [pd.DataFrame([pd.DataFrame(df_game_participants.perks).iloc[i][0]]) for i in range(10)]
            Z = pd.concat(df_perks_list, axis=0)
            Z = Z.reset_index(drop=True)
            statPerks_df = Z['statPerks'].apply(pd.Series)

            def extract_styles(data):
                primary_style = data[0]
                sub_style = data[1]

                # primary style의 딕셔너리를 분해하여 새로운 딕셔너리 생성
                primary_style_dict = {'primary_'+key: value for key, value in primary_style.items() if key != 'selections'}

                # primary style의 'selections' 리스트를 각각의 column으로 분리
                for i, sel in enumerate(primary_style['selections']):
                    primary_style_dict.update({f"primary_selection_{i+1}_{key}": value for key, value in sel.items()})

                # sub style도 동일하게 처리
                sub_style_dict = {'sub_'+key: value for key, value in sub_style.items() if key != 'selections'}
                for i, sel in enumerate(sub_style['selections']):
                    sub_style_dict.update({f"sub_selection_{i+1}_{key}": value for key, value in sel.items()})

                # primary style과 sub style의 정보를 결합
                return {**primary_style_dict, **sub_style_dict}

            # 'styles' column을 처리
            styles_df = Z['styles'].apply(extract_styles).apply(pd.Series)

            # 처리한 'styles' column을 원래의 DataFrame에 결합
            Z_expanded = pd.concat([Z, statPerks_df, styles_df], axis=1)

            # 원래의 'statPerks'와 'styles' column은 제거
            Z_expanded = Z_expanded.drop(['statPerks', 'styles'], axis=1)

            # Drop 'perks' and 'challenges' columns if they exist in df_game_participants
            if 'perks' in df_game_participants.columns:
                df_game_participants = df_game_participants.drop('perks', axis=1)
            if 'challenges' in df_game_participants.columns:
                df_game_participants = df_game_participants.drop('challenges', axis=1)

            # Handle concatenation based on the presence of 'challenges' column
            if Y.empty:
                df_game_participants = pd.concat([df_game_participants, Z_expanded], axis=1)
            else:
                W = pd.concat([Y,Z_expanded], axis=1)
                df_game_participants = pd.concat([df_game_participants, W], axis=1)
            cols = [col for col in df_game_participants.columns if col != 'win']

            # 'win' column을 리스트의 마지막에 추가합니다.
            cols.append('win')

            # 새로운 column 순서를 DataFrame에 적용합니다.
            df_game_participants = df_game_participants[cols]
            
            df = df_game_participants
            # 'killingSprees' column들을 선택
            cols = pd.Series(df.columns)
            for dup in cols[cols.duplicated()].unique(): 
                cols[cols[cols == dup].index.values.tolist()] = [dup + '-' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]

            df.columns = cols

            df_game_participants = df


            return game_metadata, game_info, df_game_participants
        except:
            return None, None, None
    
    def get_teaminfo(self, gameid:str=None, region:str='asia', api_key=None):
        '''
        game_metadata는 받아온 json 파일을 그대로 사용한다.
        game_info는 participants와 perks를 제외한 자료이다. 실질적인 game의 시작시간, 종료시간 등의 정보를 담았지만, 개별 플레이어에 대한 정보는 없다.
        df_game_participants가 해당 게임의 0~9번째 플레이어들의 룬, 스펠, challenges (분당 데미지 등등)을 담고 있는 정보이다.
        '''

        if gameid == None:
            gameid = self.gameid
        if api_key == None : 
            api_key = self.api_key

        r = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{gameid}?api_key={api_key}'
        game = requests.get(r).json()

        if isinstance(game, dict) and game.get('status', {}).get('status_code') == 429:
        # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            logging.info("API rate limit exceeded while requesting get_teaminfo. Waiting for rate limit reset...")
            time.sleep(wait_duration)
            return self.get_teaminfo(gameid, region, api_key)  # Retry the API call after waiting
        return game
        

    def get_timeline_match(self, gameid:str=None, region:str='asia', api_key=None):
        
        if gameid == None:
            gameid = self.gameid
        if api_key == None : 
            api_key = self.api_key

        r = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{gameid}/timeline?api_key={api_key}"
        game = requests.get(r).json()

        if isinstance(game, dict) and game.get('status', {}).get('status_code') == 429:
            # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            logging.info("API rate limit exceeded while requesting get_timeline_match. Waiting for rate limit reset...")
            time.sleep(wait_duration)
            return self.get_timeline_match(gameid, region, api_key)  # Retry the API call after waiting

        return game
    
    def get_timeline_match_participants(self, gameid:str=None, region:str="asia", api_key=None):

        if gameid == None:
            gameid = self.gameid
        if api_key == None : 
            api_key = self.api_key

        test_match = MatchCollect(gameid, api_key)
        X = test_match.get_timeline_match()

        p1 = []
        p2 = []
        p3 = []
        p4 = []
        p5 = []
        p6 = []
        p7 = []
        p8 = []
        p9 = []
        p10 = []

        if len(X['info']['frames'])<2:
            return None
        
        for i in range(len(X['info']['frames'])):
            p1.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['1'])  
            p2.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['2'])  
            p3.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['3'])  
            p4.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['4'])  
            p5.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['5'])  
            p6.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['6'])  
            p7.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['7'])  
            p8.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['8'])  
            p9.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['9'])  
            p10.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['10'])

        p1_timeline = pd.concat(p1, axis=1)
        p2_timeline = pd.concat(p2, axis=1)
        p3_timeline = pd.concat(p3, axis=1)
        p4_timeline = pd.concat(p4, axis=1)
        p5_timeline = pd.concat(p5, axis=1)
        p6_timeline = pd.concat(p6, axis=1)
        p7_timeline = pd.concat(p7, axis=1)
        p8_timeline = pd.concat(p8, axis=1)
        p9_timeline = pd.concat(p9, axis=1)
        p10_timeline = pd.concat(p10, axis=1)

        dataframes = [p1_timeline, p2_timeline, p3_timeline, p4_timeline, p5_timeline,
                    p6_timeline, p7_timeline, p8_timeline, p9_timeline, p10_timeline]
        
        result = []

        
        for user_df in dataframes:
            # Transpose each user DataFrame
            user_df = user_df.T.copy()

            # Concatenate championStats rows for each time period
            user_championStats = pd.concat([pd.DataFrame([user_df.championStats[i]]) for i in range(len(user_df))], axis=0).reset_index(drop=True)
            user_damageStats = pd.concat([pd.DataFrame([user_df.damageStats[i]]) for i in range(len(user_df))], axis=0).reset_index(drop=True)
            user_positions = pd.concat([pd.DataFrame([user_df.position[i]]) for i in range(len(user_df))], axis=0).reset_index(drop=True)

            # Remove already processed columns
            user_df.drop(columns=["championStats", "damageStats", "position"], inplace=True)

            # Concatenate remaining rows for each time period
            user_rest = pd.concat([user_df.iloc[i] for i in range(len(user_df))], axis=1).T.reset_index(drop=True)

            # Concatenate all user_df DataFrames
            user_df_concat = pd.concat([user_championStats, user_damageStats, user_positions, user_rest], axis=1)

            result.append(user_df_concat)

        return result
    

class User():
    def __init__(self, api_key):
        self.api_key = api_key

    def get_summon_by_gamename(self, gamename:str, nation:str = 'kr', api_key=None) -> dict :
        '''
        우리가 아는 gamename을 가지고 (메두사의 쌍독니) 해당 유저의 puuid, accountid 등을 반환해줌
        기본으론 한국으로 설정할 건데, 다른 나라를 쓰고 싶으면 nation을 확인해보아야함.

        return 되는 dict 값은 key가 id, accountId, puuid, name, profileIconId, revisionDate, summonerLevel이 있다. 이 중에서 사용할만한건 id, puuid 인것 같다. id가 다른 곳에서 encryptedsummonerId?로 쓰이는 것 같았기 때문.
        '''
        if api_key==None:
            api_key = self.api_key

        gamename = gamename.encode('utf-8')
        gamename = urllib.parse.quote(gamename)

        r = f"https://{nation}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{gamename}?api_key={api_key}"
        r_url = r
        r = requests.get(r)
        r = r.json()

        if isinstance(r, dict) and r.get('status', {}).get('status_code') == 429:
            # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            logging.info(f"API rate limit exceeded while requesting {r_url}. Waiting for rate limit reset...")
            time.sleep(wait_duration)
            return self.get_summon_by_gamename(gamename, nation, api_key)  # Retry the API call after waiting
        
        self.summonerId = r['id']
        self.accountId = r['accountId']
        self.puuid = r['puuid']
        self.name = r['name']
        self.revisionDate = r['revisionDate']
        self.summonerLevel = r['summonerLevel']
        return r
    
    async def get_raw_summon_by_gamename(self, gamename:str, nation:str = 'kr', api_key=None) -> dict :
        '''
        우리가 아는 gamename을 가지고 (메두사의 쌍독니) 해당 유저의 puuid, accountid 등을 반환해줌
        기본으론 한국으로 설정할 건데, 다른 나라를 쓰고 싶으면 nation을 확인해보아야함.

        return 되는 dict 값은 key가 id, accountId, puuid, name, profileIconId, revisionDate, summonerLevel이 있다. 이 중에서 사용할만한건 id, puuid 인것 같다. id가 다른 곳에서 encryptedsummonerId?로 쓰이는 것 같았기 때문.
        '''
        if api_key == None:
            api_key = self.api_key

        gamename = gamename.encode('utf-8')
        gamename = urllib.parse.quote(gamename)

        r = f"https://{nation}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{gamename}?api_key={api_key}"

        async with aiohttp.ClientSession() as session:
            async with session.get(r) as resp:
                r = await resp.json()

                if isinstance(r, dict) and r.get('status', {}).get('status_code') == 429:
                    # API rate limit exceeded, wait for a specific duration
                    wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
                    logging.info(f"API rate limit exceeded while requesting {r}. Waiting for rate limit reset...")
                    await asyncio.sleep(wait_duration)
                    return await self.get_raw_summon_by_gamename(gamename, nation, api_key)  # Retry the API call after waiting
                
        return r
    
    def get_summon_by_summonerId(self, summonerId:str, nation:str = 'kr', api_key=None) -> dict :
        '''
        우리가 아는 summonerId를 가지고 (메두사의 쌍독니) 해당 유저의 puuid, accountid 등을 반환해줌
        기본으론 한국으로 설정할 건데, 다른 나라를 쓰고 싶으면 nation을 확인해보아야함.
        return 되는 dict 값은 key가 id, accountId, puuid, name, profileIconId, revisionDate, summonerLevel이 있다. 이 중에서 사용할만한건 id, puuid 인것 같다. id가 다른 곳에서 encryptedsummonerId?로 쓰이는 것 같았기 때문.
        '''
        if api_key==None:
            api_key = self.api_key

        # 여기에서 요청하는 url은 /lol/summoner/v4/summoners/{encryptedSummonerId} 여기에 해당하는 것
        r = f"https://{nation}.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}?api_key={api_key}"
        r_url = r
        r = requests.get(r)
        r = r.json()

        if isinstance(r, dict) and r.get('status', {}).get('status_code') == 429:
            # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            logging.info(f"API rate limit exceeded while requesting {r_url}. Waiting for rate limit reset...")
            time.sleep(wait_duration)
            return self.get_summon_by_summonerId(summonerId, nation, api_key)  # Retry the API call after waiting
    
        
        self.summonerId = r['id']
        self.accountId = r['accountId']
        self.puuid = r['puuid']
        self.name = r['name']
        self.revisionDate = r['revisionDate']
        self.summonerLevel = r['summonerLevel']
        return r
    

    def get_summon_by_puuid(self, puuid:str=None, nation:str = 'kr', api_key=None) -> dict:
        '''
        우리가 아는 puuid을 가지고 (sV9_0TuPoRXdUBNS-nqzK8VNpznC9OJVQX53p_Dq2iEV4YrqujJGL2LQQLw4DpcUeDSV_FY2tsZswg) 해당 유저의 puuid, accountid 등을 반환해줌
        기본으론 한국으로 설정할 건데, 다른 나라를 쓰고 싶으면 nation을 확인해보아야함.

        return 되는 dict 값은 key가 id, accountId, puuid, name, profileIconId, revisionDate, summonerLevel이 있다. 이 중에서 사용할만한건 id, puuid 인것 같다. id가 다른 곳에서 encryptedsummonerId?로 쓰이는 것 같았기 때문.
        '''
        if api_key is None:
            api_key = self.api_key

        r = f"https://{nation}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
        response = requests.get(r)
        if response.status_code == 429:
            # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            logging.info("API rate limit exceeded. Waiting for rate limit reset...")
            time.sleep(wait_duration)
            return self.get_summon_by_puuid(puuid, nation, api_key)  # Retry the API call after waiting

        response_data = response.json()
        self.summonerId = response_data['id']
        self.accountId = response_data['accountId']
        self.puuid = response_data['puuid']
        self.name = response_data['name']
        self.revisionDate = response_data['revisionDate']
        self.summonerLevel = response_data['summonerLevel']
        return response_data
    
    def get_users_matchlist_by_puuid(self, puuid:str=None, start:int=0, count:int=30, type:str='ranked', startTime:int=None, endTime:int=None, region:str='asia', api_key=None) -> list :
        ''' 
        puuid를 알고 있다는 전에 하에, start는 시작 index의 숫자, count는 몇개의 게임을 불러올 것이냐,
        type : ranked, normal, tourney, tutorial
        startTime : Epoch timestamp in seconds. The matchlist started storing timestamps on June 16th, 2021. Any matches played before June 16th, 2021 won't be included in the results if the startTime filter is set.
        endTime: Epoch timestamp in seconds. 
        region : asia, americas, europe, sea
        '''
        if api_key == None:
            api_key = self.api_key
        if puuid == None:
            puuid = self.puuid
        
        r = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type={type}&start={start}&count={count}&api_key={api_key}'
        response = requests.get(r)
        if response.status_code == 429:
            # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            logging.info("API rate limit exceeded. Waiting for rate limit reset...")
            time.sleep(wait_duration)
            return self.get_users_matchlist_by_puuid(puuid, start, count, type, startTime, endTime, region, api_key)  # Retry the API call after waiting

        return response.json()
    
    def get_league_by_user_summonerid(self, summonerid:str=None, region:str='kr', api_key=None):
        
        if api_key is None:
            api_key = self.api_key
        r = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerid}?api_key={api_key}"
        response = requests.get(r)
        if response.status_code == 429:
            # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            logging.info("API rate limit exceeded. Waiting for rate limit reset...")
            time.sleep(wait_duration)
            return self.get_league_by_user_summonerid(summonerid, region, api_key)  # Retry the API call after waiting

        return response.json()
    

    def get_tier_by_user_summonerid(self, summonerid:str=None, region:str='kr', api_key=None):
        '''
        summonerId를 받아서, GOLD-I 과 같은 티어 정보를 알려주는 것. 어떤 매치의 평균 티어를 맞추기 위해서 설정한 함수임.
        '''
        if summonerid==None:
            summonerid = self.summonerId            
        r = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerid}?api_key={api_key}"
        r = requests.get(r).json()
        if len(r)==2:
            if r[0]['queueType']=='RANKED_SOLO_5x5':
                # "Here1", r[0]['queueType'], r[0]['tier']+'-'+r[0]['rank'], 
                return r[0]['tier']+'-'+r[0]['rank']
            else:
                #"Here2", r[1]['queueType'], r[1]['tier']+'-'+r[1]['rank'], 
                return r[1]['tier']+'-'+r[1]['rank']
        
        else:
            return r[0]['tier']+'-'+r[0]['rank']
        
class League():
    def __init__(self, api_key):
        self.api_key = api_key

    def get_users_league(self, division:str, tier:str, page:int, queue='RANKED_SOLO_5x5', region:str='kr', api_key=None):
        '''
        이거는 잘 사용 안하는 함수임.
        '''
        if api_key==None:
            api_key = self.api_key

        r = f"https://{region}.api.riotgames.com/lol/league/v4/entries/{queue}/{tier}/{division}?page={page}&api_key={api_key}"
        r = requests.get(r).json()
        return r
    
    def get_league_summonerId(self, division:str, tier:str, page:int, queue='RANKED_SOLO_5x5', region:str='kr', api_key=None):
        '''
        특정 티어 (division : I, tier, SILVER)에 속하는 유저들의 목록을 받아오는 함수입니다. 
        df로 만들 필요가 있나, 고민을 하고 있습니다.
        '''
        if api_key==None:
            api_key = self.api_key

        r = f"https://{region}.api.riotgames.com/lol/league/v4/entries/{queue}/{tier}/{division}?page={page}&api_key={api_key}"
        logging.info(f"API request URL: {r}")  # 로깅: API 요청 URL 정보

        r = requests.get(r).json()
        


        if isinstance(r, dict) and r.get('status', {}).get('status_code') == 429:
            # API rate limit exceeded, wait for a specific duration
            wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
            message = f"API rate limit exceeded for {r.get('status', {}).get('message')}. Waiting for rate limit reset..."
            logging.info(f"{message}")  # 로깅: API 요청 제한 초과 정보
            time.sleep(wait_duration)

            return self.get_league_summonerId(division, tier, page, queue, region, api_key)  # Retry the API call after waiting
        
        logging.info(f"API request URL: {r}")  # 로깅: API 요청 URL 정보

        
        df = pd.DataFrame(r)
        columns_to_drop = ['leagueId','queueType', 'leaguePoints', 'wins', 'losses', 'veteran', 'inactive', 'freshBlood', 'hotStreak']
        if 'miniSeries' in df.columns:
            columns_to_drop.append('miniSeries') # Check if 'miniSeries' column exists

        # Check if each column in columns_to_drop is in df
        for column in columns_to_drop:
            if column not in df.columns:
                logging.warning(f"Column '{column}' is not in DataFrame.")

        # Safely drop columns
        return df.drop([col for col in columns_to_drop if col in df.columns], axis=1)
    
    def get_raw_league_summonerId(self, division:str, tier:str, page:int, queue='RANKED_SOLO_5x5', region:str='kr', api_key=None):
            '''
            특정 티어 (division : I, tier, SILVER)에 속하는 유저들의 목록을 받아오는 함수입니다. 
            return되는 값은 
                    {
                "leagueId": "e70248dc-b517-4669-ab68-c5aa7537cb4a",
                "queueType": "RANKED_SOLO_5x5",
                "tier": "SILVER",
                "rank": "II",
                "summonerId": "i-0qjh_gMs-gIvqV4p8ECBmEMdkLD8d-Bb49w1Q8bEw0Rp9s",
                "summonerName": "니달리 원챔충",
                "leaguePoints": 21,
                "wins": 134,
                "losses": 145,
                "veteran": false,
                "inactive": false,
                "freshBlood": false,
                "hotStreak": false
            } 위와 같은 데이터의 집합입니다.
            '''
            if api_key==None:
                api_key = self.api_key

            r = f"https://{region}.api.riotgames.com/lol/league/v4/entries/{queue}/{tier}/{division}?page={page}&api_key={api_key}"
            logging.info(f"API request URL: {r}")  # 로깅: API 요청 URL 정보

            r = requests.get(r).json()
            


            if isinstance(r, dict) and r.get('status', {}).get('status_code') == 429:
                # API rate limit exceeded, wait for a specific duration
                wait_duration = 5  # Wait for 5 seconds (adjust according to your needs)
                message = f"API rate limit exceeded for {r.get('status', {}).get('message')}. Waiting for rate limit reset..."
                logging.info(f"{message}")  # 로깅: API 요청 제한 초과 정보
                time.sleep(wait_duration)

                return self.get_raw_league_summonerId(division, tier, page, queue, region, api_key)  # Retry the API call after waiting
            
            logging.info(f"API request URL: {r}")  # 로깅: API 요청 URL 정보
            return r
    
def create_directory_path(base_path, tier, division):
    today = datetime.datetime.now().strftime('%Y%m%d')
    dir_name = os.path.join(base_path, f"{tier}-{division}")
    os.makedirs(dir_name, exist_ok=True)
    return dir_name


def collect_summonerId(start_ind:int, end_ind:int, division:str, tier:str, base_path, api_key=None):
    '''
    이건 api_key를 받아와야만 한다.
    '''
    l = League(api_key)
    df_list = []
    for i in range(start_ind,end_ind):
        X = l.get_league_summonerId(division=division,tier=tier,page=i)
        df_list.append(X)

    dir_name = create_directory_path(base_path, tier, division)

    # Set 객체를 생성합니다.
    summoner_id_set = set(X.summonerId)

    # Set 객체를 저장합니다.
    with open(os.path.join(dir_name, 'summonerId.pkl'), 'wb') as f:
        pickle.dump(summoner_id_set, f)

def collect_matchId_from_summonerpkl(base_path, tier, division, api_key=None):
    '''
    이제 잘 사용하지 않는 함수
    '''
    dir_name = create_directory_path(base_path, tier, division)
    
    pkl_path = os.path.join(dir_name, 'summonerId.pkl')
    with open(pkl_path, 'rb') as f :
        summonerId_set = pickle.load(f)

    user = User(api_key)
    return_set = set()
    for i in summonerId_set:
        user.get_summon_by_summonerId(i)
        X = set(user.get_users_matchlist_by_puuid())
        return_set.update(X)

    result_path = os.path.join(dir_name, 'return_set.pkl')
    with open(result_path, 'wb') as f:
        pickle.dump(return_set, f)

def get_gameids(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Filter rows where the 'gameid' column starts with 'KR_'
    df = df[df.iloc[:, -1].str.startswith('KR_', na=False)]

    # Extract the 'gameid' column values
    gameids = df.iloc[:, -1].values

    return gameids

def collect_preprocessing_matchdata(base_path, tier, division, api_key=None):
    dir_name = create_directory_path(base_path, tier, division)
    pkl_path = os.path.join(dir_name, 'return_set.pkl')
    with open(pkl_path, 'rb') as f:
        match_list = pickle.load(f)

    csv_path = os.path.join(dir_name, 'processed_match_data.csv')
    print(csv_path)
    if os.path.exists(csv_path):  
        df = pd.read_csv(csv_path) # header == None 부분이 있어서 생기는 문제가 있을 수도 있음.
        df = df[df.iloc[:, -1].str.startswith('KR_', na=False)]
        gameids = df.iloc[:, -1].values
    else:
        df = pd.DataFrame()  
        gameids = []
    for i in list(match_list):  # Start from the index after the last processed gameid
        if i not in gameids:  # If i is not in gameids, then process it
            test_match = MatchCollect(i, api_key)
            X = test_match.get_converted_data()
            try:
                X['win']=test_match.teams[0]['win']
                print("ban_list:", test_match.ban_list)
                ban_list_df = pd.DataFrame([test_match.ban_list], columns=[f"ban_{j}" for j in range(len(test_match.ban_list))])
                X = pd.concat([X, ban_list_df], axis=1)
                X['gameid'] = test_match.gameid  # Add gameid column

                # Append the DataFrame to the CSV file
                X.to_csv(csv_path, mode='a', index=False)
            except:
                pass
                

    # Load the final DataFrame from the CSV file
    final_df = pd.read_csv(csv_path)

    return final_df

        
def zip_pos(data, ind, position_average_coordinate):
    try:
        pos_data = data[ind]
        if len(pos_data) < 5:
            X = list(zip(pos_data.x[1:], pos_data.y[1:]))
        else:
            X = list(zip(pos_data.x[1:8], pos_data.y[1:8]))
        return X
    except Exception as e:
        logging.error(f"An error occurred in 'zip_pos' function with index {ind}: {str(e)}")
        return []

def closest_player(data, ind, position_average_coordinate):
    # f 함수를 사용하여 점 리스트를 가져옵니다.
    points = zip_pos(data, ind, position_average_coordinate)
    closest_players = []
    # 각 점에 대해
    for point in points:
        closest_distance = None
        closest_player = None
        # 모든 플레이어의 평균 위치와의 거리를 계산합니다.
        try:
            for player, player_position in position_average_coordinate.items():
                player_ind = int(player.replace("player", "").replace("_pos", ""))
                # ind가 0에서 4 사이인 경우에는 player0_pos부터 player4_pos까지 비교하고
                # ind가 5에서 9 사이인 경우에는 player5_pos부터 player9_pos까지 비교합니다.
                if (ind < 5 and player_ind < 5) or (ind >= 5 and player_ind >= 5):
                    dist = distance.euclidean(point, player_position)
                    if closest_distance is None or dist < closest_distance:
                        closest_distance = dist
                        closest_player = player
        except Exception as e:
            logging.error(f"An error occurred in 'closest_player' function with index {ind}, point {point}: {str(e)}")
            continue  # continue to the next point
        # 각 점에 가장 가까운 플레이어를 추가합니다.
        closest_players.append(closest_player)
    return closest_players

def most_common_player(data, ind, position_average_coordinate):
    # closest_player 함수를 사용하여 가장 가까운 플레이어 리스트를 가져옵니다.
    closest_players = closest_player(data, ind, position_average_coordinate)
    # Counter를 사용하여 가장 많이 나타나는 플레이어를 찾습니다.
    player_count = Counter(closest_players)
    most_common_player = player_count.most_common(1)[0][0]

    if 0<=ind<=4:
        if (most_common_player=='player1_pos' or most_common_player=='player2_pos') and max(data[ind].jungleMinionsKilled)==max(max(data[1].jungleMinionsKilled), max(data[2].jungleMinionsKilled)):
            return 'player1_pos'
        elif max(data[ind].jungleMinionsKilled)==max([max(data[j].jungleMinionsKilled) for j in range(5)]):
            return 'player1_pos'
        elif (most_common_player=='player1_pos' or most_common_player=='player2_pos') and max(max(data[1].minionsKilled),max(data[2].minionsKilled)):
            return 'player2_pos'
        elif (most_common_player=='player3_pos' or most_common_player=='player4_pos') and max(data[ind].minionsKilled) == max(max(data[3].minionsKilled), max(data[4].minionsKilled)):
            return 'player3_pos'
        elif (most_common_player=='player3_pos' or most_common_player=='player4_pos') and max(data[ind].minionsKilled) == min(max(data[3].minionsKilled), max(data[4].minionsKilled)):
            return 'player4_pos'
        else:
            return 'player0_pos'
        
        
    if 5<=ind<=9:
        if (most_common_player=='player6_pos' or most_common_player=='player7_pos') and max(data[ind].jungleMinionsKilled)==max(max(data[6].jungleMinionsKilled), max(data[7].jungleMinionsKilled)):
            return 'player6_pos'
        elif max(data[ind].jungleMinionsKilled)==max([max(data[j].jungleMinionsKilled) for j in range(5,10)]):
            return 'player6_pos'
        elif (most_common_player=='player6_pos' or most_common_player=='player7_pos') and max(max(data[6].minionsKilled),max(data[7].minionsKilled)):
            return 'player7_pos'
        elif (most_common_player=='player8_pos' or most_common_player=='player9_pos') and max(data[ind].minionsKilled) == max(max(data[8].minionsKilled), max(data[9].minionsKilled)):
            return 'player8_pos'
        elif (most_common_player=='player8_pos' or most_common_player=='player9_pos') and max(data[ind].minionsKilled) == min(max(data[8].minionsKilled), max(data[9].minionsKilled)):
            return 'player9_pos'
        else:
            return 'player5_pos'
        
    return most_common_player

    
def get_timeline_match_data_list_participants(data_list:list, api_key=None):
    '''
    match_list를 받아서 dict 형태로 데이터를 저장. 각 dict의 key는 data_list의 원소들이다.
    예를 들어 data_list = ['KR_6532865027', 'KR_6532865028'] 이라면 return되는 dict의 key는 'KR_6532865027'이다.
    현재는 실험을 위해 200개의 게임 데이터만 받아올 예정이다.
    '''
    result = defaultdict(list)
    for data in data_list:
        logging.info(data)
        logging.info('-'*30)
        test_match = MatchCollect(data, api_key)
        X = test_match.get_timeline_match()
        p1 = []
        p2 = []
        p3 = []
        p4 = []
        p5 = []
        p6 = []
        p7 = []
        p8 = []
        p9 = []
        p10 = []

        for i in range(len(X['info']['frames'])):
            p1.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['1'])  
            p2.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['2'])  
            p3.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['3'])  
            p4.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['4'])  
            p5.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['5'])  
            p6.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['6'])  
            p7.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['7'])  
            p8.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['8'])  
            p9.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['9'])  
            p10.append(pd.DataFrame(X['info']['frames'][i]['participantFrames'])['10'])

        p1_timeline = pd.concat(p1, axis=1)
        p2_timeline = pd.concat(p2, axis=1)
        p3_timeline = pd.concat(p3, axis=1)
        p4_timeline = pd.concat(p4, axis=1)
        p5_timeline = pd.concat(p5, axis=1)
        p6_timeline = pd.concat(p6, axis=1)
        p7_timeline = pd.concat(p7, axis=1)
        p8_timeline = pd.concat(p8, axis=1)
        p9_timeline = pd.concat(p9, axis=1)
        p10_timeline = pd.concat(p10, axis=1)

        dataframes = [p1_timeline, p2_timeline, p3_timeline, p4_timeline, p5_timeline,
                    p6_timeline, p7_timeline, p8_timeline, p9_timeline, p10_timeline]

        # Rename the columns
        for i, df in enumerate(dataframes):
            df.columns = range(df.shape[1])
        
        user_dfs = []
        # Loop through all user dataframes
        for user_df in dataframes:
            # Transpose each user DataFrame
            user_df = user_df.T.copy()

            # Concatenate championStats rows for each time period
            user_championStats = pd.concat([pd.DataFrame([user_df.championStats[i]]) for i in range(len(user_df))], axis=0).reset_index(drop=True)
            user_damageStats = pd.concat([pd.DataFrame([user_df.damageStats[i]]) for i in range(len(user_df))], axis=0).reset_index(drop=True)
            user_positions = pd.concat([pd.DataFrame([user_df.position[i]]) for i in range(len(user_df))], axis=0).reset_index(drop=True)

            # Remove already processed columns
            user_df.drop(columns=["championStats", "damageStats", "position"], inplace=True)

            # Concatenate remaining rows for each time period
            user_rest = pd.concat([user_df.iloc[i] for i in range(len(user_df))], axis=1).T.reset_index(drop=True)

            # Concatenate all user_df DataFrames
            user_df_concat = pd.concat([user_championStats, user_damageStats, user_positions, user_rest], axis=1)

            # Append the user DataFrame to the list
            user_dfs.append(user_df_concat)
        
        result[data] = user_dfs
    return result


