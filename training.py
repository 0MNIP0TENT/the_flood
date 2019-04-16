from sc2.constants import LURKERMP,RAVAGER,ROACHWARREN,SPAWNINGPOOL,ROACHWARREN,ROACH,ZERGLING,HATCHERY,DRONE,OVERLORD,BANELING,BANELINGNEST, \
INFESTATIONPIT,HYDRALISK,HYDRALISKDEN,LURKERDENMP,LAIR,HIVE,ULTRALISK,ULTRALISKCAVERN,VIPER,MUTALISK,SPIRE,CORRUPTOR,BROODLORD,GREATERSPIRE,INFESTOR, \
SWARMHOSTMP,OVERSEER,OVERLORD,LARVA,QUEEN,ZERGMISSILEWEAPONSLEVEL3,ZERGMISSILEWEAPONSLEVEL2,ZERGMISSILEWEAPONSLEVEL1
import common as c
import build
"""
Contains all code for training units
"""

async def train_anything(self,unit):
    
    """
    CAN TRAIN ANY UNIT, EVEN ONE THAT HAS TO BE MORPHED. It will aslo build the required buildings needed

    REQUIRMENTS IS THE BUILDINGS IN THE TECH TREE REQUIRED FOR TRAINGING THE UNIT
    UNIT_TYPE IS WETHER THE UNIT NEEDS TO BE MORPHED OR NOT
    MORPHER IS THE UNIT THAT MORPHS INTO THE UNIT YOU WANT
    REQUIRMENT IS ACTUAL and last BUILDING REQUIRED TO TRAIN THE UNIT

    NOT EVERY ENTRY IS GOING TO NEED TO FILL MORPHER

    THIS FUNCTION SHOULD WORK NO MATTER WHAT IF THE DICTIONARIES ARE SET UP PROBERLY. I THINK

    DATA ADDED: INFESTOR, ULTRALISK, VIPER LAIR, HIVE?, ZERGLING, ROACH, BANELIN, infestation pit?, HYDRALISK, RAVAGER, LURKERMP
    SWARMHOST, OVERSEER

    NOTE TO SELF: LARVA MAY BE A BETTER REQUIRMENT THEN HATCHERY, THAT MAY FIX WHEN THE EXTRA HATCHERY BUG
    LURKERS DONT WORK
    """
    requirments = {HATCHERY:[DRONE],OVERLORD:[HATCHERY],DRONE:[HATCHERY],OVERSEER:[LAIR,SPAWNINGPOOL],SWARMHOSTMP:[SPAWNINGPOOL,LAIR,INFESTATIONPIT],INFESTOR:[SPAWNINGPOOL,LAIR,INFESTATIONPIT],
    GREATERSPIRE:[SPIRE,HIVE,LAIR,INFESTATIONPIT,SPAWNINGPOOL],BROODLORD:[GREATERSPIRE,SPIRE,HIVE,LAIR,INFESTATIONPIT,SPAWNINGPOOL],
    CORRUPTOR:[SPIRE,HIVE,LAIR,INFESTATIONPIT,SPAWNINGPOOL],SPIRE:[HIVE,LAIR,INFESTATIONPIT,SPAWNINGPOOL],MUTALISK:[LAIR,SPAWNINGPOOL,SPIRE],VIPER:
    [HIVE,LAIR,SPAWNINGPOOL,INFESTATIONPIT],HATCHERY:[DRONE],ULTRALISKCAVERN:[HIVE,LAIR,SPAWNINGPOOL,INFESTATIONPIT],ULTRALISK:[ULTRALISKCAVERN,HIVE,LAIR,SPAWNINGPOOL,
    INFESTATIONPIT],HYDRALISKDEN:[LAIR,SPAWNINGPOOL],LURKERDENMP:[HYDRALISKDEN,LAIR,SPAWNINGPOOL],LURKERMP:[INFESTATIONPIT,LURKERDENMP,SPAWNINGPOOL,HYDRALISKDEN,LAIR],
    RAVAGER:[ROACHWARREN,SPAWNINGPOOL],HYDRALISK:[HYDRALISKDEN,LAIR,SPAWNINGPOOL],HIVE:[LAIR,SPAWNINGPOOL,INFESTATIONPIT],INFESTATIONPIT:[SPAWNINGPOOL,LAIR],LAIR:[SPAWNINGPOOL],
    ZERGLING:[SPAWNINGPOOL],ROACH:[SPAWNINGPOOL,ROACHWARREN],BANELING:[SPAWNINGPOOL,BANELINGNEST]}
    
    unit_type = {HATCHERY:'larva',OVERLORD:'larva',DRONE:'larva',OVERSEER:'morph',SWARMHOSTMP:'larva',INFESTOR:'larva',GREATERSPIRE:'morph',BROODLORD:'morph',CORRUPTOR:'larva',SPIRE:'larva',MUTALISK:'larva',
    VIPER:'larva',HATCHERY:'larva',ULTRALISK:'larva',ULTRALISKCAVERN:'larva',LURKERDENMP:'larva',LURKERMP:'morph',RAVAGER:'morph',ROACHWARREN:'larva',HYDRALISK:'larva',HYDRALISKDEN:'larva',LAIR:'morph',HIVE:'morph',
    INFESTATIONPIT:'larva',ZERGLING:'larva',ROACH:'larva',BANELING:'morph',BANELINGNEST:'larva',SPAWNINGPOOL:'larva',INFESTATIONPIT:'larva'}
    
    morpher = {OVERSEER:OVERLORD,GREATERSPIRE:SPIRE,BROODLORD:CORRUPTOR,LURKERMP:HYDRALISK,RAVAGER:ROACH,HIVE:LAIR,LAIR:HATCHERY,HIVE:LAIR,BANELING:ZERGLING}
    
    requirment = {HATCHERY:DRONE,OVERLORD:HATCHERY,DRONE:HATCHERY,OVERSEER:LAIR,SWARMHOSTMP:INFESTATIONPIT,INFESTOR:INFESTATIONPIT,GREATERSPIRE:SPIRE,BROODLORD:GREATERSPIRE,CORRUPTOR:SPIRE,SPIRE:HIVE,MUTALISK:SPIRE,VIPER:HIVE,HATCHERY:DRONE,
    ULTRALISK:ULTRALISKCAVERN,ULTRALISKCAVERN:HIVE,LURKERMP:LURKERDENMP,LURKERDENMP:LAIR,RAVAGER:ROACHWARREN,HYDRALISK:HYDRALISKDEN,LAIR:SPAWNINGPOOL,HIVE:INFESTATIONPIT,INFESTATIONPIT:LAIR,ZERGLING:SPAWNINGPOOL,
    ROACH:ROACHWARREN,BANELING:BANELINGNEST}

    # if the requirment has not been built
    if self.units(requirment[unit]).empty:   
        # builds the requirments of the requirment
        for req in requirments[unit]:
            # if the req we need to build is morphed from a townhall we have to call the function recursivily with that req as the argument.
            #print(req)
            if self.units(req).empty and not self.already_pending(req) and unit_type[req] == 'larva':
                await build.build_requirment(self,req)
            elif self.units(req).empty and not self.already_pending(req) and unit_type[req] == 'morph':
                await train_anything(self,req)
                     
    # we have to take 2 different actions depending on wether the unit spawns from larva or morphed from another unit
    if unit_type[unit] == 'larva' and self.units(requirment[unit]).ready.exists and c.get_larva(self).idle.exists and self.can_afford(unit):
        larva = c.get_larva(self).random
        await self.do(larva.train(unit))

    # if we morph the unit from another unit
    elif unit_type[unit] == 'morph' and self.units(requirment[unit]).ready.exists and c.get_larva(self).idle.exists and self.can_afford(unit):             
        
        # if the unit we need to morph from exists
        if self.units(morpher[unit]).exists:
            await c.morph(self,self.units(morpher[unit]),unit)
        
        # if the unit we need to morph does not exist we recursivily call the functions with the unit we need to morph into arguments 
        elif self.units(morpher[unit]).empty and self.can_afford(morpher[unit]):
            await train_anything(self,morpher[unit])    

# This function deals with craeting and distributing workers.
async def supply_up(self):
        
    await self.distribute_workers()

    if self.townhalls.exists and self.units(DRONE).amount < self.townhalls.amount * 18:
        if self.can_afford(DRONE) and c.get_larva(self).exists:
            await self.do(c.get_larva(self).random.train(DRONE))

    if self.supply_left < 10 and not self.supply_cap >= 200:
        if self.can_afford(OVERLORD) and c.get_larva(self).exists:
            await self.do(c.get_larva(self).random.train(OVERLORD))

    await build.build_extractor(self)        


# train queen should stay as it is
async def train_queen(self):
    if self.units(SPAWNINGPOOL).ready.exists and self.can_afford(QUEEN):
        if self.units(QUEEN).amount < c.get_bases(self).amount * 2:
            if c.get_bases(self).ready:
                hatchery = c.get_bases(self).ready.random
                await self.do(hatchery.train(QUEEN))  

"""
 Your code goes into the train_units function,
 You can train any unit except for lurkers.
"""     
async def train_units(self):
    # Do not erase these two
    await supply_up(self)
    await train_queen(self)

    # train whatever you want here based on whatever condition you want.
    
    if self.units(ZERGLING).amount / c.get_forces(self).amount <= 0.25:
        await train_anything(self,ZERGLING)
    if self.units(MUTALISK).amount / c.get_forces(self).amount <= 0.25:
        await train_anything(self,BANELING)
    if self.units(ROACH).amount / c.get_forces(self).amount <= 0.5:
        await train_anything(self,ROACH)    
       

   
        
        
            


    
    