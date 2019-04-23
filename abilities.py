from sc2.constants import HATCHERY, QUEEN ,EFFECT_INJECTLARVA, LAIR
from sc2.ids.ability_id import AbilityId
from sc2.data import race_townhalls


async def lay_eggs(self):
    bases = self.townhalls
    if bases.ready.exists:
        base = bases.ready.random
        for unit in self.units(QUEEN).idle:
            abilities = await self.get_available_abilities(unit)
            if AbilityId.EFFECT_INJECTLARVA  in abilities:
                await self.do(unit(EFFECT_INJECTLARVA,base))

async def do_abilities(self):
    await lay_eggs(self)                