from UTIL import const

addHP1 = lambda s: [s[0] + 5] + s[1:]
addHP2 = lambda s: [s[0] + 10] + s[1:]
addHP3 = lambda s: [s[0] + 20] + s[1:]
addMP1 = lambda s: s[:2] + [s[2]+5] + s[3:]
addMP2 = lambda s: s[:2] + [s[2]+10] + s[3:]
addMP3 = lambda s: s[:2] + [s[2]+20] + s[3:]
curePSN = lambda s: s[:11] + [False]

itemDict = { const.FRUIT1: addHP1,
             const.CHEESE: addHP1,
             const.BREAD: addHP2,
             const.ANTIDOTE: curePSN,
             const.SHP: addHP1,
             const.MHP: addHP2,
             const.LHP: addHP3,
             const.SMP: addMP1,
             const.MMP: addMP2,
             const.LMP: addMP3,
                }

descDict = { 
             const.KEY: 'A dungeon key',
             const.SPELLBOOK: 'A spellbook',
             const.PARCHMENT: 'A magic parchment',
             const.FRUIT1: 'A small apple',
             const.CHEESE: 'A wedge of cheese',
             const.BREAD: 'A loaf of bread',
             const.ANTIDOTE: 'Poison antidote',
             const.SHP: 'Small Healing Potion',
             const.MHP: 'Medium Healing Potion',
             const.SMP: 'Small Magic Potion',
             const.MMP: 'Medium Magic Potion',
             const.GOLD: 'Gold Pieces'
            }