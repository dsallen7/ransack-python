from const import *

heal = lambda s: [s[0] + 5] + [s[1]] + [s[2] - 5] + s[3:]
frbl = lambda s: s[:2] + [s[2] - 5] + s[3:]
spellDict = { HEAL: heal,
             FRBL: frbl

                }