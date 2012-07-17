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
        addHP = lambda s: [s[0] + 5] + s[1:]
        addMP = lambda s: s[:2] + [s[2]+5] + s[3:]
        itemDict = { FRUIT1: addHP,
                     FRUIT2: addHP,
                     SHP: addHP,
                     SMP: addMP

                        }
        fn = itemDict[self.getType()]
        stats = fn(stats)
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX] = stats
        hero.setPlayerStats( (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) )