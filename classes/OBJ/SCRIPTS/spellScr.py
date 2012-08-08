from const import *

heal = lambda s: [s[0] + 5] + [s[1]] + [s[2] - 5] + s[3:]
frbl = lambda s: s[:2] + [s[2] - 5] + s[3:]
icbl = lambda s: s[:2] + [s[2] - 5] + s[3:]
tlpt = lambda s: s[:2] + [s[2] - 5] + s[3:]

spellDict = { HEAL: heal,
              FRBL: frbl,
              ICBL: icbl,
              TLPT: tlpt

                }

descDict = { HEAL: 'Heal I',
            FRBL: 'Fireball I',
            ICBL: 'Iceball I',
            TLPT: 'Teleport',
            ASCD: 'Ascend I',
            DSCD: 'Descend I',
            ACD2: 'Ascend II'
            }