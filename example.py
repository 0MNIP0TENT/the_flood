
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
    
    # Override to change the default way you expand more bases.
    async def spread(self):
        if self.townhalls.amount < 3 and self.can_afford(HATCHERY):
            await self.expand_now()   

    # This function deals with creating and distributing workers.
    # Override this to define custom behavour.
    async def supply_up(self):
        
        await self.distribute_workers()

        if self.townhalls.exists and self.units(DRONE).amount < self.townhalls.amount * 16:
            if self.can_afford(DRONE) and self.get_larva().exists:
                await self.do(self.get_larva().random.train(DRONE))

        if self.supply_left < 10 and not self.supply_cap >= 200:
            if self.can_afford(OVERLORD) and self.get_larva().exists:
                await self.do(self.get_larva().random.train(OVERLORD))

        await self.build_extractor()        
    # Override this to change how many extractors are built.
    async def build_extractor(self):
        if self.units(EXTRACTOR).amount < self.units(HATCHERY).amount * 2:
            if self.can_afford(EXTRACTOR) and not self.already_pending(EXTRACTOR):
                drone = self.workers.random
                target = self.state.vespene_geyser.closest_to(drone.position)
                await self.do(drone.build(EXTRACTOR, target)) 

    """
    These are units you can train with await self.train_anything():
    BANELING, BROODLORD, CORRUPTOR, INFESTOR, HYDRALISK, LURKERMP MUTALISK,
    ULTRALISK, RAVAGER, ROACH, VIPER, ZERGLING
    """
    async def train_units(self):
        # Do not erase supply_up or train_queen
        await self.supply_up()
        await self.train_queen() 
        #if not self.units(ROACHWARREN).ready:
         #   await self.train_anything(ZERGLING)
        
        await self.train_anything(ZERGLING)
        await self.train_anything(MUTALISK)

    """
    Upgrade with the upgrade_anything method in the research upgrades method.
    Example: await self.upgrade_anything(CENTRIFICALHOOKS)
    
    ZERGFLYERWEAPONSLEVEL1, ZERGFLYERWEAPONSLEVEL2, ZERGFLYERWEAPONSLEVEL3,
    ZERGFLYERARMORSLEVEL1, ZERGFLYERARMORSLEVEL2, ZERGFLYERARMORSLEVEL3,
    ZERGGROUNDARMORSLEVEL1, ZERGGROUNDARMORSLEVEL2, ZERGGROUNDARMORSLEVEL3,
    ZERGMISSILEWEAPONSLEVEL1, ZERGMISSILEWEAPONSLEVEL2, ZERGMISSILEWEAPONSLEVEL3,
    ZERGMELEEWEAPONSLEVEL1, ZERGMELEEWEAPONSLEVEL2, ZERGMELEEWEAPONSLEVEL3,
    ZERGLINGMOVEMENTSPEED, ZERGLINGATTACKSPEED
    """
    async def research_upgrades(self):
       await self.upgrade_anything(ZERGLINGMOVEMENTSPEED)
       await self.upgrade_anything(ZERGLINGATTACKSPEED) 

    async def seek_and_destroy(self):
        if self.supply_used >= 130 and not self.known_enemy_units().empty:
            target = self.known_enemy_units().closest_to(self.get_forces().center)
            if target != None:
                await self.do_actions([unit.attack(target) for unit in self.get_forces()])
        
        elif self.supply_used >= 130 and self.known_enemy_units.empty:
            spot = random.choice(self.enemy_start_locations)
            await self.do_actions([unit.attack(spot) for unit in self.get_forces().idle])
        
# this helps pick a random lvl
def pick_level():
    lvls = ['HonorgroundsLE','AbyssalReefLE','BelShirVestigeLE',
    'CactusValleyLE','NewkirkPrecinctTE','PaladinoTerminalLE','ProximaStationLE']  
    return random.choice(lvls)

if __name__ == '__main__':   

    run_game(maps.get(pick_level()), [
        #Human(Race.Zerg),
        Bot(Race.Zerg, TheFlood()),
        #Bot(Race.Protoss, Sentinel()),
        Computer(Race.Terran,Difficulty.Hard),
    ], realtime=True)    
    
