from odmantic import Model

class Match(Model):
    tier: str
    division:str
    leagueId: str
    summonerId: str
    summonerName: str
    

    class Config:
        collection = "match"
