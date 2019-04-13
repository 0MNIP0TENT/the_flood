"""
Building is handled by the training and upgrading files
"""

from sc2.constants import *
from sc2.data import race_townhalls

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