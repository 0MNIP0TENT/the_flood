"""
You will want to modify seek and destroy, in order to determin how and when to attack.
Kill_invakers is a good function for defending the base.
"""

import random,common

# The main file calls this. Do not delete or change
async def destroy_all(self):
    await kill_invaders(self,25.0)
    await seek_and_destroy(self)
# A good function for defending the base
async def kill_invaders(self,radius):
    for base in common.get_bases(self):
        invaders = common.get_enemy_units(self).closer_than(radius,base)
        if invaders.exists and common.get_forces(self).amount >= 2:
            target = invaders.closest_to(common.get_forces(self).center)
            await self.do_actions([unit.attack(target) for unit in common.get_forces(self)])

def get_target(self):
    if self.known_enemy_units.not_structure.exists:
        return random.choice(self.known_enemy_units.not_structure)
    
    elif self.known_enemy_structures.exists:
        return random.choice(self.known_enemy_structures)

"""
Add whatever attack code to seek_and_destroy that you want.
The code inside already is just an example you can delete.
"""
async def seek_and_destroy(self):
    # # attack if supply used > 130
    if self.supply_used >= 180 and self.known_enemy_units.exists and self.townhalls.amount >= 3:
        if self.known_enemy_units.not_structure.exists:
            target = self.known_enemy_units.not_structure.closest_to(common.get_forces(self).center)
            #target = self.known_enemy_units.closest_to(common.get_forces(self).center)
            await self.do_actions([unit.attack(target) for unit in common.get_forces(self)])
        
        elif self.known_enemy_units.exists:
            target = self.known_enemy_units.closest_to(common.get_forces(self).center)
            await self.do_actions([unit.attack(target) for unit in common.get_forces(self)])

    elif self.supply_used >= 180 and self.known_enemy_units.empty and self.townhalls.amount >= 3:
        spot = random.choice(self.enemy_start_locations)
        await self.do_actions([unit.attack(spot) for unit in common.get_forces(self).idle])

  
