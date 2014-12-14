# A dictionary assigning item ID numbers to functions which
# carry out the effects of the items

from UTIL import const
from SCRIPTS import itemScr

class Item():
    
    def __init__(self, type, num=None):
        self.type = type
        if type == const.GOLD:
            self.qty = num
            self.name = 'gold'
        if self.type == const.SPELLBOOK:
            from SCRIPTS import spellScr
            self.name = 'spellbook'
            self.spellNum = num
            self.descrip = itemScr.descDict[self.type] + ': ' + spellScr.descDict[num]
            self.ID = num + 40
        elif self.type == const.PARCHMENT:
            from SCRIPTS import spellScr
            self.name = 'parchment'
            self.spellNum = num
            self.descrip = itemScr.descDict[self.type] + ': ' + spellScr.descDict[num]
            self.ID = num + 70
        elif self.type == const.CERTIFICATE:
            self.name = 'certificate'
            self.certNum = num
            self.descrip = itemScr.descDict[self.type]
            self.effects = itemScr.itemFX[self.certNum]
            self.ID = type - const.FRUIT1
        elif self.type in const.GAMEITEMS:
            self.name = 'gameitem'
            self.descrip = itemScr.descDict[self.type]
            self.ID = type - const.FRUIT1
        else:
            self.name = 'item'
            self.descrip = itemScr.descDict[self.type]
            self.ID = type - const.FRUIT1
        self.img = type
        if type in itemScr.foodItems:
            self.category = 'Food'
        elif type in [const.SPELLBOOK, const.PARCHMENT]:
            self.category = 'Magic'
        else: self.category = 'Tools'
    
    def getType(self):
        return self.type
    
    def getImg(self):
        return self.img
    
    def setQty(self, qty):
        self.qty = qty
    def getQty(self):
        if self.qty == 0:
            return 999
        else: return self.qty
    
    def getID(self):
        return self.ID
    
    def getName(self):
        return self.name
    def getLevel(self):
        return self.level
    def getSpellNum(self):
        return self.spellNum
    def getDesc(self):
        return self.descrip
    
    def execute(self, hero):
        if self.name == 'spellbook':
            hero.learnSpell( self.spellNum )
            return
        if self.name == 'gameitem':
            return itemScr.itemFX[ self.getType() ]
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn] = hero.getPlayerStats()
        stats = [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn]
        fn = itemScr.itemDict[self.getType()]
        stats = fn(stats)
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn] = stats
        hero.setPlayerStats( (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn) )