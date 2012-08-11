from const import *

heal = lambda s: [s[0] + 5] + [s[1]] + [s[2] - 5] + s[3:]
frbl = lambda s: s[:2] + [s[2] - 5] + s[3:]
icbl = lambda s: s[:2] + [s[2] - 5] + s[3:]
tlpt = lambda s: s[:2] + [s[2] - 5] + s[3:]
nothing = lambda s: s

spellDict = { (HEAL, True): heal,
              (HEAL, False): heal,
              (FRBL, True): frbl,
              (FRBL, False): nothing,
              (ICBL, True): frbl,
              (ICBL, False): nothing,
              (TLPT, True): nothing,
              (TLPT, False): tlpt,

                }

descDict = { HEAL: 'Heal I',
            FRBL: 'Fireball I',
            ICBL: 'Iceball I',
            TLPT: 'Teleport',
            ASCD: 'Ascend I',
            DSCD: 'Descend I',
            ACD2: 'Ascend II'
            }

costDict = { HEAL: 4,
             FRBL: 4,
             ICBL: 5,
             TLPT: 5
            }

castMsgs = { HEAL: 'You feel better.',
             FRBL: 'A ball of fire materializes before your fingertips!',
             ICBL: 'A grim and frostbitten ball of ice emerges!',
             TLPT: 'Your body disintegrates...'
            }