# A dictionary assigning item ID numbers to functions which
# carry out the effects of the items

from const import *

class Item():
    
    def __init__(self, type):
        self.type = type
        self.img = type
        self.name = 'item'
        self.qty = 0
    
    def getType(self):
        return self.type
    
    def getImg(self):
        return self.img
    
    def execute(self, hero):
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX] = hero.getPlayerStats()
        stats = [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX]
        addHP1 = lambda s: [s[0] + 5] + s[1:]
        addHP2 = lambda s: [s[0] + 10] + s[1:]
        addHP3 = lambda s: [s[0] + 20] + s[1:]
        addMP1 = lambda s: s[:2] + [s[2]+5] + s[3:]
        addMP2 = lambda s: s[:2] + [s[2]+10] + s[3:]
        addMP3 = lambda s: s[:2] + [s[2]+20] + s[3:]
        itemDict = { FRUIT1: addHP1,
                     FRUIT2: addHP1,
                     BREAD1: addHP2,
                     BREAD2: addHP2,
                     SHP: addHP1,
                     MHP: addHP2,
                     LHP: addHP3,
                     SMP: addMP1,
                     MMP: addMP2,
                     LMP: addMP3,
                        }
        fn = itemDict[self.getType()]
        stats = fn(stats)
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX] = stats
        hero.setPlayerStats( (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) )