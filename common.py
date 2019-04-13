"""
This file contains general functions for the bot
"""
from sc2.constants import OVERLORD, LARVA, DRONE, QUEEN, HATCHERY, LAIR, CORRUPTOR, HIVE, BROODLORD, ZERGLING
from operator import or_
from sc2.data import race_townhalls

def get_enemys(self):
    return self.known_enemy_units

def get_enemy_structures(self):
    return self.enemy_structures

def get_enemy_units(self):
    return self.known_enemy_units.not_structure     

def get_visible_enemys(self,enemys):
    return enemys.filter(lambda u: u.is_visible)

def get_larva(self):
    return self.units(LARVA).idle
    
def get_forces(self):
    return self.units.exclude_type({DRONE,OVERLORD,QUEEN})   

def get_bases(self):
    return self.townhalls

async def morph(self,units,morph):
    if units.exists and self.can_afford(morph):
        await self.do(units.random.train(morph))    

    

   

