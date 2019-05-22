
import sc2
from sc2.constants import *
from sc2 import Race, Difficulty,run_game,maps
from sc2.player import Bot,Computer
from sc2.data import race_townhalls
from sc2.ids.ability_id import AbilityId
import random

import training,upgrades

class Zerg(sc2.BotAI):
    async def on_step(self,iteration):

        await self.spread()

        await self.do_abilities()
    
        await self.train_units()

        await self.destroy_all()

        await self.research_upgrades()


#### building code

    """
    Building is handled by the training and upgrading files
    """

    async def build_requirment(self,building):
        if self.can_afford(building) and self.units(building).empty:
            bases = self.townhalls
            if bases.exists:
                base = bases.random
                for d in range(4,18):
                    pos = base.position.to2.towards_with_random_angle(self.game_info.map_center,d)
                    if await self.can_place(building, pos) and not self.already_pending(building):
                        drone = self.workers.closest_to(pos)
                        err = await self.do(drone.build(
                            building, pos))
                        if err:
                            print(err)    

    # build_requirment will only build if that building does not exist
    async def build_building(self,building):
        if self.can_afford(building):
            bases = self.townhalls
            if bases.exists:
                base = bases.random
                for d in range(4,18):
                    pos = base.position.to2.towards_with_random_angle(self.game_info.map_center,d)
                    if await self.can_place(building, pos) and not self.already_pending(building):
                        drone = self.workers.closest_to(pos)
                        err = await self.do(drone.build(
                            building, pos))
                        if err:
                            print(err)    

    async def build_extractor(self):
        if self.units(EXTRACTOR).amount < self.units(HATCHERY).amount * 2:
            if self.can_afford(EXTRACTOR) and not self.already_pending(EXTRACTOR):
                drone = self.workers.random
                target = self.state.vespene_geyser.closest_to(drone.position)
                await self.do(drone.build(EXTRACTOR, target)) 

##### training code
    """
    Contains all code for training units.
    you should use this method for train new units
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

        Note to self: LURKERS DONT WORK, if something requires a HIVE DO NOT INCLUDE a LAIR

        """
    
        # if the requirment does not exist
        if self.units(training.requirment[unit]).empty:   
            # builds the requirments of the requirment
            for req in training.requirments[unit]:
                # if the req we need to build is morphed from a townhall we have to call the function recursivily with that req as the argument.
                if self.units(req).empty and not self.already_pending(req) and training.unit_type[req] == 'larva':
                    await self.build_requirment(req)
                elif self.units(req).empty and not self.already_pending(req) and training.unit_type[req] == 'morph':
                    if req == LAIR and self.units(LAIR).exists or self.already_pending(LAIR):
                        continue
                    elif req == HIVE and self.units(HIVE).exists or self.already_pending(HIVE):  
                        continue
                    await self.train_anything(req)
                     
        # we have to take 2 different actions depending on wether the unit spawns from larva or morphed from another unit
        if training.unit_type[unit] == 'larva' and self.units(training.requirment[unit]).ready.exists and self.get_larva().idle.exists and self.can_afford(unit):
            larva = self.get_larva().random
            await self.do(larva.train(unit))

        # if we morph the unit from another unit
        elif training.unit_type[unit] == 'morph' and self.units(training.requirment[unit]).ready.exists and self.get_larva().idle.exists and self.can_afford(unit):             
        
            # if the unit we need to morph from exists
            if self.units(training.morpher[unit]).exists:
                await self.morph(self.units(training.morpher[unit]),unit)
        
            # if the unit we need to morph does not exist we recursivily call the functions with the unit we need to morph into arguments 
            elif self.units(training.morpher[unit]).empty and self.can_afford(training.morpher[unit]):
                await self.train_anything(training.morpher[unit])    

    # This function deals with craeting and distributing workers.
    async def supply_up(self):
        
        await self.distribute_workers()

        if self.townhalls.exists and self.units(DRONE).amount < self.townhalls.amount * 18:
            if self.can_afford(DRONE) and self.get_larva().exists:
                await self.do(self.get_larva().random.train(DRONE))

        if self.supply_left < 10 and not self.supply_cap >= 200:
            if self.can_afford(OVERLORD) and self.get_larva().exists:
                await self.do(self.get_larva().random.train(OVERLORD))

        await self.build_extractor()        


    # train queen should stay as it is
    async def train_queen(self):
        if self.units(SPAWNINGPOOL).ready.exists and self.can_afford(QUEEN):
            if self.units(QUEEN).amount < self.get_bases().amount * 2:
                if self.get_bases().ready:
                    hatchery = self.get_bases().ready.random
                    await self.do(hatchery.train(QUEEN))  

    """
    Your code goes into the train_units method,
    You can train any unit except for lurkers, but I haven't tested it in awhile.
    """     
    async def train_units(self):
        pass

#### Attack Code
    """
    You will want to modify seek and destroy, in order to determin how and when to attack.
    Kill_invakers is a good function for defending the base.
    """

   # The main file calls this. Do not delete or change
    async def destroy_all(self):    
        await self.kill_invaders(25.0)
        await self.seek_and_destroy()

    # A good function for defending the base
    async def kill_invaders(self,radius):
        for base in self.get_bases():
            invaders = self.get_enemy_units().closer_than(radius,base)
            if invaders.exists and self.get_forces().amount >= 2:
                target = invaders.closest_to(self.get_forces().center)
                await self.do_actions([unit.attack(target) for unit in self.get_forces()])

    def get_target(self):
        if self.known_enemy_units.not_structure.exists:
            return random.choice(self.known_enemy_units.not_structure)
    
        elif self.known_enemy_structures.exists:
            return random.choice(self.known_enemy_structures)

    """
    override this in the main file.
    """
    async def seek_and_destroy(self):
        pass
    
#### upgrade code

    async def upgrade_anything(self,upgrade):
        if self.units(upgrades.requirment[upgrade]).empty:
            for req in upgrades.requirments[upgrade]:
            
                if upgrades.req_type[req] == 'DRONE' and self.units(req).empty:
                    await self.build_requirment(req)
            
                elif upgrades.req_type[req] == 'MORPH':
                    if req == LAIR and self.units(LAIR).exists or self.already_pending(LAIR):
                        continue
                    elif req == HIVE and self.units(HIVE).exists or self.already_pending(HIVE):  
                        continue
                    await self.train_anything(req) 
              
                elif upgrades.req_type[req] == 'UPGRADE':
                    await self.upgrade_anything(req)    
        else:
            if self.can_afford(upgrade) and not self.already_pending_upgrade(upgrade) and self.units(upgrades.researcher[upgrade]).exists:
                await self.do(self.units(upgrades.researcher[upgrade]).random.research(upgrade))

    """
    Add your research code here.
    """
    async def research_upgrades(self):
        pass

#### ABILITIES
    async def lay_eggs(self):
        bases = self.townhalls
        if bases.ready.exists:
            base = bases.ready.random
            for unit in self.units(QUEEN).idle:
                abilities = await self.get_available_abilities(unit)
                if AbilityId.EFFECT_INJECTLARVA in abilities:
                    await self.do(unit(EFFECT_INJECTLARVA,base))

    async def recover_roaches(self):
        if self.units(ROACH).exists:
            for roach in self.units(ROACH):
                if roach.health_percentage < 0.3 and not roach.is_burrowed:
                    await self.do(roach(BURROWDOWN_ROACH))
                    await self.do(roach.move(self.townhalls.random.position.towards_with_random_angle(self.game_info.map_center, 16)))
                if roach.health_percentage >= 0.99 and roach.is_burrowed:
                    print('HEALTH = ' + str(roach.health_percentage))
                    await self.do(roach(BURROWUP_ROACH))
    
    async def do_abilities(self):
        await self.lay_eggs()               
       #await self.recover_roaches()     
    """
    implement spread in main file to controll base expansions
    """
    async def spread(self):
        pass

#### utility methods
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