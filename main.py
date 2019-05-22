from the_flood import Zerg
from sc2.player import Bot,Computer
from sc2 import Race, Difficulty,run_game,maps
from sc2.constants import *
import random

"""
I have made four overridable methods allow for easier control of the bot.
  1. spread, put in code to control your base expansion
  2. train_units, this will train any unit with the train_anything method
  3. research_upgrades this will make any upgrade happen with the upgrade_anythin method
  4. seek_and_destroy this method controls how and when to attack outside your base
"""
class TheFlood(Zerg):
    
    async def spread(self):
        pass   

    async def train_units(self):
        # Do not erase these two
        await self.supply_up()
        await self.train_queen() 

   
    async def research_upgrades(self):
        """
        Upgrade with the upgrade_anything method in the research upgrades method.
        Example: await self.upgrade_anything(CENTRIFICALHOOKS)
        """
        pass
        
    
    async def seek_and_Destroy(self):
        pass
        
# this helps pick a rndom lvl
def pick_level():
    lvls = ['HonorgroundsLE','AbyssalReefLE','BelShirVestigeLE',
    'CactusValleyLE','NewkirkPrecinctTE','PaladinoTerminalLE','ProximaStationLE']  
    return random.choice(lvls)

if __name__ == '__main__':   

    run_game(maps.get(pick_level()), [
        #Human(Race.Zerg),
        Bot(Race.Zerg, TheFlood()),
        Computer(Race.Terran,Difficulty.Medium),
    ], realtime=True)    
    