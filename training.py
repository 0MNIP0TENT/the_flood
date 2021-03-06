from sc2.constants import LURKERMP,RAVAGER,ROACHWARREN,SPAWNINGPOOL,ROACH,ZERGLING,\
HATCHERY,DRONE,OVERLORD,BANELING,BANELINGNEST,INFESTATIONPIT,HYDRALISK,HYDRALISKDEN,LURKERDENMP,\
LAIR,HIVE,ULTRALISK,ULTRALISKCAVERN,VIPER,MUTALISK,SPIRE,CORRUPTOR,BROODLORD,GREATERSPIRE,INFESTOR,\
SWARMHOSTMP,OVERSEER,OVERLORD,LARVA,QUEEN

requirments = {
    HATCHERY:[DRONE],
    OVERLORD:[HATCHERY],
    DRONE:[HATCHERY],
    OVERSEER:[LAIR,SPAWNINGPOOL],
    SWARMHOSTMP:[SPAWNINGPOOL,LAIR,INFESTATIONPIT],
    INFESTOR:[SPAWNINGPOOL,LAIR,INFESTATIONPIT],
    GREATERSPIRE:[SPIRE,HIVE,INFESTATIONPIT,SPAWNINGPOOL],
    BROODLORD:[GREATERSPIRE,SPIRE,HIVE,INFESTATIONPIT,SPAWNINGPOOL],
    CORRUPTOR:[SPIRE,HIVE,INFESTATIONPIT,SPAWNINGPOOL],
    SPIRE:[HIVE,INFESTATIONPIT,SPAWNINGPOOL],
    MUTALISK:[LAIR,SPAWNINGPOOL,SPIRE],
    VIPER:[HIVE,SPAWNINGPOOL,INFESTATIONPIT],
    HATCHERY:[DRONE],
    ULTRALISKCAVERN:[HIVE,SPAWNINGPOOL,INFESTATIONPIT],
    ULTRALISK:[ULTRALISKCAVERN,HIVE,SPAWNINGPOOL,INFESTATIONPIT],
    HYDRALISKDEN:[LAIR,SPAWNINGPOOL],
    LURKERDENMP:[HYDRALISKDEN,LAIR,SPAWNINGPOOL],
    LURKERMP:[INFESTATIONPIT,LURKERDENMP,SPAWNINGPOOL,HYDRALISKDEN,LAIR],
    RAVAGER:[ROACHWARREN,SPAWNINGPOOL],
    HYDRALISK:[HYDRALISKDEN,LAIR,SPAWNINGPOOL],
    HIVE:[LAIR,SPAWNINGPOOL,INFESTATIONPIT],
    INFESTATIONPIT:[SPAWNINGPOOL,LAIR],
    LAIR:[SPAWNINGPOOL],
    ZERGLING:[SPAWNINGPOOL],
    ROACH:[SPAWNINGPOOL,ROACHWARREN],
    BANELING:[SPAWNINGPOOL,BANELINGNEST]
    }
    
unit_type = {HATCHERY:'larva',
    OVERLORD:'larva',
    DRONE:'larva',
    OVERSEER:'morph',
    SWARMHOSTMP:'larva',
    INFESTOR:'larva',
    GREATERSPIRE:'morph',
    BROODLORD:'morph',
    CORRUPTOR:'larva',
    SPIRE:'larva',
    MUTALISK:'larva',
    VIPER:'larva',
    HATCHERY:'larva',
    ULTRALISK:'larva',
    ULTRALISKCAVERN:'larva',
    LURKERDENMP:'larva',
    LURKERMP:'morph',
    RAVAGER:'morph',
    ROACHWARREN:'larva',
    HYDRALISK:'larva',
    HYDRALISKDEN:'larva',
    LAIR:'morph',HIVE:'morph',
    INFESTATIONPIT:'larva',
    ZERGLING:'larva',
    ROACH:'larva',
    BANELING:'morph',
    BANELINGNEST:'larva',
    SPAWNINGPOOL:'larva',
    INFESTATIONPIT:'larva'
    }
    
morpher = {
    OVERSEER:OVERLORD,
    GREATERSPIRE:SPIRE,
    BROODLORD:CORRUPTOR,
    LURKERMP:HYDRALISK,
    RAVAGER:ROACH,
    HIVE:LAIR,
    LAIR:HATCHERY,
    HIVE:LAIR,
    BANELING:ZERGLING
    }
    
requirment = {
    HATCHERY:DRONE,
    OVERLORD:HATCHERY,
    DRONE:HATCHERY,
    OVERSEER:LAIR,
    SWARMHOSTMP:INFESTATIONPIT,
    INFESTOR:INFESTATIONPIT,
    GREATERSPIRE:SPIRE,
    BROODLORD:GREATERSPIRE,
    CORRUPTOR:SPIRE,
    SPIRE:HIVE,
    MUTALISK:SPIRE,
    VIPER:HIVE,
    HATCHERY:DRONE,
    ULTRALISK:ULTRALISKCAVERN,
    ULTRALISKCAVERN:HIVE,
    LURKERMP:LURKERDENMP,
    LURKERDENMP:LAIR,
    RAVAGER:ROACHWARREN,
    HYDRALISK:HYDRALISKDEN,
    LAIR:SPAWNINGPOOL,
    HIVE:INFESTATIONPIT,
    INFESTATIONPIT:LAIR,
    ZERGLING:SPAWNINGPOOL,
    ROACH:ROACHWARREN,
    BANELING:BANELINGNEST
    }
