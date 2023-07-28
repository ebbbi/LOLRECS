from pydantic import BaseModel

class Summoner(BaseModel):
    name: str
    region: str

class MatchList(BaseModel):
    summoner_id: str
    region: str

class MatchDetails(BaseModel):
    match_id: str
    region: str

class Live(BaseModel):
    summoner_id: str
    region: str