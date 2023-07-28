from odmantic import Model

class Summoner(Model):
    summonerInfo: str
    mastery:str
    rank: str
    matchHistory: str
    matchList: str
    
    class Config:
        collection = "summoner"
