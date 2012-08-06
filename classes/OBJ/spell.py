# A dictionary assigning item ID numbers to functions which
# carry out the effects of the spells

from const import *
from SCRIPTS import spellScr

class Spell():
    
    def __init__(self, type):
        self.type = type
        self.img = type + 102
        self.cost = 5
        self.level = 0
        self.name = 'spell'
    
    def getType(self):
        return self.type
    
    def getImg(self):
        return self.img
    
    def getLevel(self):
        return self.level
    
    def execute(self, hero):
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX] = hero.getPlayerStats()
        stats = [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX]
        fn = spellScr.spellDict[self.getType()]
        stats = fn(stats)
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX] = stats
        hero.setPlayerStats( (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) )