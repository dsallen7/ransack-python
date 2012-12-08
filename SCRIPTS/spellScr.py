from UTIL import const

from random import randrange

heal = lambda s: [s[0] + randrange(5, 15) ] + s[1:]
nothing = lambda s: s

spellDict = { (const.HEAL, True): heal,
              (const.HEAL, False): heal,
              (const.FRBL, True): nothing,
              (const.FRBL, False): nothing,
              (const.ICBL, True): nothing,
              (const.ICBL, False): nothing,
              (const.TLPT, True): nothing,
              (const.TLPT, False): nothing,

                }

descDict = {const.HEAL: 'Heal I',
            const.DART: 'Magic Dart',
            const.FRBL: 'Fireball I',
            const.ICBL: 'Iceball I',
            const.TLPT: 'Teleport',
            const.ASCD: 'Ascend I'
            }

costDict = { const.HEAL: 4,
             const.DART: 3,
             const.FRBL: 4,
             const.ICBL: 5,
             const.TLPT: 5
            }

timeDict = { const.HEAL: 60,
            const.DART: 30,
             const.FRBL: 30,
             const.ICBL: 30,
             const.TLPT: 60
            }

attackSpells = [const.DART, 
                const.FRBL, 
                const.FBL2, 
                const.ICBL, 
                const.IBL2
                ]
baseDmg = {const.DART : 5, 
                const.FRBL : 10, 
                const.FBL2 : 25, 
                const.ICBL : 15, 
                const.IBL2 : 30
           }

castMsgs = { const.HEAL: 'You feel better.',
             const.DART: 'An electric dart stabs the enemy!',
             const.FRBL: 'A ball of fire materializes before your fingertips!',
             const.ICBL: 'A grim and frostbitten ball of ice emerges!',
             const.TLPT: 'Your body disintegrates...'
            }