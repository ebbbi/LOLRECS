import ujson as json
import aiohttp
import asyncio

class Dependency:
    
    def __init__(self):
        self.version = None
        self.queues = None
        self.maps = None
        self.champions = None
    
    async def fetch(self, session, url):
        async with session.get(url) as response:
            response = await response.read()
            response = json.loads(response)
            return response
        
    async def fetch_champion(self, session, url):
        async with session.get(url) as response:
            response = await response.read()
            version = json.loads(response)[0]
            
            champions = await self.fetch(session, f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json")
            
            return [version, champions]

    async def get_dependencies(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_champion(session, 'https://ddragon.leagueoflegends.com/api/versions.json'),
                    self.fetch(session, 'https://static.developer.riotgames.com/docs/lol/maps.json'),
                    self.fetch(session, 'https://static.developer.riotgames.com/docs/lol/queues.json')]
            responses = await asyncio.gather(*tasks)
            
            return responses
    
    async def setup(self):  # Make setup method asynchronous
        responses = await self.get_dependencies()  # Await the get_dependencies method
        self.version, self.queues = responses[0]
        self.maps = responses[1]
        self.champions = responses[2]
        
        
dependency = Dependency()