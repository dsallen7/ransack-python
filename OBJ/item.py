# A dictionary assigning item ID numbers to functions which
# carry out the effects of the items

from UTIL import const
from SCRIPTS import itemScr, spellScr


class Item():

    def __init__(self, type, level=None, spellNum=None):
        self.type = type
        if type == 99:
            self.qty = level
            self.name = 'gold'
        if self.type == 100:
            self.name = 'spellbook'
            self.spellNum = spellNum
            self.level = level
            self.descrip = itemScr.descDict[
                self.type] + ': ' + spellScr.descDict[spellNum]
        elif self.type == 101:
            self.name = 'parchment'
            self.spellNum = spellNum
            self.level = level
            self.descrip = itemScr.descDict[
                self.type] + ': ' + spellScr.descDict[spellNum]
        elif type in range(102, 108):
            self.name = 'magicitem'
            self.level = level
        else:
            self.name = 'item'
            self.descrip = itemScr.descDict[self.type]
        self.img = type

    def getType(self):
        return self.type

    def getImg(self):
        return self.img

    def setQty(self, qty):
        self.qty = qty

    def getQty(self):
        if self.qty == 0:
            return 999
        else:
            return self.qty

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
            hero.learnSpell(self.spellNum)
            return
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX,
            nEX, psn] = hero.getPlayerStats()
        stats = [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn]
        fn = itemScr.itemDict[self.getType()]
        stats = fn(stats)
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn] = stats
        hero.setPlayerStats((cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys,
            cEX, nEX, psn))
