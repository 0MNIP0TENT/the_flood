
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
        if self.townhalls.amount < 2 and self.can_afford(HATCHERY):
        # if self.townhalls.amount < 2:
        #     await self.expand_now()
        # elif self.supply_used > 80:
            await self.expand_now()   

    async def train_units(self):
        # Do not erase supply_up or train_queen
        await self.supply_up()
        await self.train_queen() 

        await self.train_anything(RAVAGER)
       

    """
    Upgrade with the upgrade_anything method in the research upgrades method.
    Example: await self.upgrade_anything(CENTRIFICALHOOKS)
    """
    async def research_upgrades(self):
        await self.upgrade_anything(ZERGMISSILEWEAPONSLEVEL1)
        
    
    async def seek_and_Destroy(self):
        if self.supply_used >= 100 and self.known_enemy_units.exists:
            if self.known_enemy_units.not_structure.exists:
                target = self.known_enemy_units.not_structure.closest_to(self.get_forces().center)
                #target = self.known_enemy_units.closest_to(get_forces(self).center)
                await self.do_actions([unit.attack(target) for unit in self.get_forces().idle])
        
            elif self.known_enemy_units.exists:
                target = self.known_enemy_units.closest_to(self.get_forces().center)
                await self.do_actions([unit.attack(target) for unit in self.get_forces().idle])

        # remove idle above here
        elif self.supply_used >= 100 and self.known_enemy_units.empty:
            spot = random.choice(self.enemy_start_locations)
            await self.do_actions([unit.attack(spot) for unit in self.get_forces().idle])
        
# this helps pick a rndom lvl
def pick_level():
    lvls = ['HonorgroundsLE','AbyssalReefLE','BelShirVestigeLE',
    'CactusValleyLE','NewkirkPrecinctTE','PaladinoTerminalLE','ProximaStationLE']  
    return random.choice(lvls)

if __name__ == '__main__':   

    run_game(maps.get(pick_level()), [
        #Human(Race.Zerg),
        Bot(Race.Zerg, TheFlood()),
        #Bot(Race.Protoss, Sentinel()),
        Computer(Race.Terran,Difficulty.Medium),
    ], realtime=True)    
    