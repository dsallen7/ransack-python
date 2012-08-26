from UTIL import const

heal = lambda s: [s[0] + 5] + [s[1]] + [s[2] - 5] + s[3:]
frbl = lambda s: s[:2] + [s[2] - 5] + s[3:]
icbl = lambda s: s[:2] + [s[2] - 5] + s[3:]
tlpt = lambda s: s[:2] + [s[2] - 5] + s[3:]
nothing = lambda s: s

spellDict = { (const.HEAL, True): heal,
              (const.HEAL, False): heal,
              (const.FRBL, True): frbl,
              (const.FRBL, False): nothing,
              (const.ICBL, True): frbl,
              (const.ICBL, False): nothing,
              (const.TLPT, True): nothing,
              (const.TLPT, False): tlpt,

                }

descDict = {const.HEAL: 'Heal I',
            const.FRBL: 'Fireball I',
            const.ICBL: 'Iceball I',
            const.TLPT: 'Teleport',
            const.ASCD: 'Ascend I',
            const.DSCD: 'Descend I',
            const.ACD2: 'Ascend II'
            }

costDict = { const.HEAL: 4,
             const.FRBL: 4,
             const.ICBL: 5,
             const.TLPT: 5
            }

timeDict = { const.HEAL: 60,
             const.FRBL: 30,
             const.ICBL: 30,
             const.TLPT: 60
            }

castMsgs = { const.HEAL: 'You feel better.',
             const.FRBL: 'A ball of fire materializes before your fingertips!',
             const.ICBL: 'A grim and frostbitten ball of ice emerges!',
             const.TLPT: 'Your body disintegrates...'
            }