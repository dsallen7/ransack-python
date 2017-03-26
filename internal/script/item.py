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
foodItems = [const.FRUIT1,
             const.CHEESE,
             const.BREAD
             ]
foodValue = dict(zip( foodItems,
                      [1,2,4] ))
descDict = { 
             const.KEY: 'Dungeon key',
             const.SPELLBOOK: 'Spellbook',
             const.PARCHMENT: 'Magic parchment',
             const.CERTIFICATE: 'Official Town Document',
             const.FRUIT1: 'Small apple',
             const.CHEESE: 'Wedge of cheese',
             const.BREAD: 'Loaf of bread',
             const.ANTIDOTE: 'Poison antidote',
             const.SHP: 'Small Healing Potion',
             const.MHP: 'Medium Healing Potion',
             const.SMP: 'Small Magic Potion',
             const.MMP: 'Medium Magic Potion',
             const.GOLD: 'Gold Pieces',
             const.LANTERN: 'Lantern'
            }
itemFX = { 
             const.KEY: 'Unlocks a dungeon door',
             const.SPELLBOOK: 'Teaches you a new spell',
             const.PARCHMENT: 'Magic parchment',
             const.SAVECERT: 'Certificate of Saving: allows you to save once',
             const.RETURNCERT: 'Certificate of Return: returns you to point of purchase',
             const.FRUIT1: '+5 HP, -1 Hunger',
             const.CHEESE: '+5 HP, -2 Hunger',
             const.BREAD: '+10 HP, -4 Hunger',
             const.ANTIDOTE: 'Cures poison.',
             const.SHP: '+5 HP',
             const.MHP: '+10 HP',
             const.SMP: '+5 MP',
             const.MMP: '+10 MP',
             const.GOLD: 'Gold Pieces',
             const.LANTERN: 'Lantern: Increases your visibility in the dark'
            }