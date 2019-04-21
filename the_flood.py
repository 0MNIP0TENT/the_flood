
import random
import sc2
from sc2 import Race, Difficulty,run_game,maps
from sc2.constants import DRONE,OVERLORD,HATCHERY,ZERGMISSILEWEAPONSLEVEL3
from sc2.player import Bot,Computer
from sc2.data import race_townhalls

import training,build,assault,abilities,upgrade
import common as c

class Zerg(sc2.BotAI):
    async def on_step(self,iteration):

        await self.spread()

        await abilities.do_abilities(self)
    
        await training.train_units(self)

        await assault.destroy_all(self)

        await upgrade.research_upgrades(self)

    async def spread(self):
        if self.townhalls.amount < 3 and self.can_afford(HATCHERY):
            # if self.townhalls.amount < 2:
            #     await self.expand_now()
            # elif self.supply_used > 80:
            await self.expand_now()   

def pick_level():
    lvls = ['HonorgroundsLE','AbyssalReefLE','BelShirVestigeLE',
    'CactusValleyLE','NewkirkPrecinctTE','PaladinoTerminalLE','ProximaStationLE']  
    return random.choice(lvls)

if __name__ == '__main__':   

    run_game(maps.get(pick_level()), [
        #Human(Race.Zerg),
        Bot(Race.Zerg, Zerg()),
        #Bot(Race.Protoss, Sentinel()),
        Computer(Race.Terran,Difficulty.VeryEasy),
    ], realtime=False)