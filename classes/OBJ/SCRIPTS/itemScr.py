from const import *

addHP1 = lambda s: [s[0] + 5] + s[1:]
addHP2 = lambda s: [s[0] + 10] + s[1:]
addHP3 = lambda s: [s[0] + 20] + s[1:]
addMP1 = lambda s: s[:2] + [s[2]+5] + s[3:]
addMP2 = lambda s: s[:2] + [s[2]+10] + s[3:]
addMP3 = lambda s: s[:2] + [s[2]+20] + s[3:]
itemDict = { FRUIT1: addHP1,
             CHEESE: addHP1,
             BREAD1: addHP2,
             BREAD2: addHP2,
             SHP: addHP1,
             MHP: addHP2,
             LHP: addHP3,
             SMP: addMP1,
             MMP: addMP2,
             LMP: addMP3,
                }

descDict = { 
             98: 'A dungeon key',
             100: 'A spellbook',
             101: 'A magic parchment',
             FRUIT1: 'A small apple',
             CHEESE: 'A wedge of cheese',
             BREAD1: 'A loaf of bread',
             SHP: 'Small Healing Potion',
             MHP: 'Medium Healing Potion',
             SMP: 'Small Magic Potion',
             MMP: 'Medium Magic Potion'
            }