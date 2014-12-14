from UTIL import const

heal = lambda s: [s[0] + 5] + s[1:]
nothing = lambda s: s

spellDict = {(const.HEAL, True): heal,
             (const.HEAL, False): heal,
             (const.FRBL, True): nothing,
             (const.FRBL, False): nothing,
             (const.ICBL, True): nothing,
             (const.ICBL, False): nothing,
             (const.TLPT, True): nothing,
             (const.TLPT, False): nothing, }

descDict = {const.HEAL: 'Heal I',
            const.FRBL: 'Fireball I',
            const.ICBL: 'Iceball I',
            const.TLPT: 'Teleport',
            const.ASCD: 'Ascend I'
            #const.DSCD: 'Descend I',
            #$const.ACD2: 'Ascend II'
            }

costDict = {const.HEAL: 4,
            const.FRBL: 4,
            const.ICBL: 5,
            const.TLPT: 5
            }

timeDict = {const.HEAL: 60,
            const.FRBL: 30,
            const.ICBL: 30,
            const.TLPT: 60
            }

castMsgs = {const.HEAL: 'You feel better.',
            const.FRBL: 'A ball of fire materializes before your fingertips!',
            const.ICBL: 'A grim and frostbitten ball of ice emerges!',
            const.TLPT: 'Your body disintegrates...'
            }
