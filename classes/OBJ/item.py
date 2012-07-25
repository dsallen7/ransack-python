# A dictionary assigning item ID numbers to functions which
# carry out the effects of the items

from const import *
from effects import *

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
    
    def setQty(self, qty):
        self.qty = qty
    
    def execute(self, hero):
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX] = hero.getPlayerStats()
        stats = [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX]
        fn = itemDict[self.getType()]
        stats = fn(stats)
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX] = stats
        hero.setPlayerStats( (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) )