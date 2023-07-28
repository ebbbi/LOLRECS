import requests
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os


class ItemRecommender:
    def __init__(self):
        self.legendary_items = self.get_legendary_items()
        self.mythic_items = self.get_mythic_items()
        self.core_items = self.get_core_items()
        self.en_to_kr = self.get_en_to_kr()
        self.kr_to_id = self.get_kr_to_id()
        self.cluster = AsyncIOMotorClient(os.environ["DB_URL"])
        # data load -> mongodb 사용시 변경
        with open("./app/assets/item.json", "r", encoding='UTF-8') as f:
            self.data = json.load(f)
            
    def get_legendary_items(self):
        url = "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items.json"
        data = requests.get(url).json()
        legendary_item = []
        for key in data:
            if data[key]["shop"]["purchasable"]:
                if data[key]["rank"] == ["LEGENDARY"]:
                    legendary_item.append(key)
        
        return legendary_item


    def get_mythic_items(self):
        url = "https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items.json"
        data = requests.get(url).json()
        mythic_item = []
        for key in data:
            if data[key]["shop"]["purchasable"]:
                if data[key]["rank"] == ["MYTHIC"]:
                    mythic_item.append(key)
        
        return mythic_item


    def get_core_items(self):
        legendary_items = self.get_legendary_items()
        legendary_items.extend(self.get_mythic_items())
        return legendary_items
        
        
    def get_en_to_kr(self):
        champion = dict()
        map_id = requests.get('http://ddragon.leagueoflegends.com/cdn/13.14.1/data/ko_KR/champion.json')
        map_id = map_id.json()
        for k, v in map_id["data"].items():
            champion[v["id"]]=v["name"]
        return champion
        
        
    def get_kr_to_id(self):
        url = "http://ddragon.leagueoflegends.com/cdn/13.14.1/data/ko_KR/item.json"
        data = requests.get(url).json()
        core_items = self.get_core_items()
        kr_to_id = {}
        for item in core_items:
            name = data["data"][item]["name"]
            if name not in kr_to_id:
                kr_to_id[name] = item
        return kr_to_id


    # model에서 2개, 3개, 4개 추천
    """
    get_two_items를 예로 들면 get_two_items는 2 * 3 = 6개의 아이템을 담은 list를 return
    list[0], list[1] 이 첫번째 추천, list[2], list[3] 이 두번째 추천, list[4], list[5]가 세번째 추천
    이런식으로 반환해주면 됩니당
    """
    # 아이템을 2개씩 3번 추천한 값을 return
    async def get_two_items(self, my, pos, op):
        Items_DB = self.cluster['items']
        doc = await Items_DB['item_rec_result_13_13'].find_one({"championName":self.en_to_kr[my], "position":pos, "enemy":self.en_to_kr[op]},{"_id":0, "twoItemRec":1})
    
        return doc.get("twoItemRec")

    # 아이템을 3개씩 3번 추천한 값을 return
    async def get_three_items(self, my, pos, op):
        Items_DB = self.cluster['items']
        doc = await Items_DB['item_rec_result_13_13'].find_one({"championName":self.en_to_kr[my], "position":pos, "enemy":self.en_to_kr[op]},{"_id":0, "threeItemRec":1})
        return doc.get("threeItemRec")

    # 아이템을 4개씩 3번 추천한 값을 return
    async def get_four_items(self, my, pos, op):
        Items_DB = self.cluster['items']
        doc = await Items_DB['item_rec_result_13_13'].find_one({"championName":self.en_to_kr[my], "position":pos, "enemy":self.en_to_kr[op]},{"_id":0, "fourItemRec":1})
        return doc.get("fourItemRec")
    