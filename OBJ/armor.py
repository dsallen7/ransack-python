from UTIL import const
from SCRIPTS import armorScr

class Armor():
    
    def __init__(self, type, resist=None):
        self.type = type
        self.level = armorScr.aLevels[type]
        self.imgNum = type
        self.name = 'armor'
        self.desc = armorScr.descDict[self.type]
        self.category = armorScr.categories[type]
        self.resist = resist
    
    def getType(self):
        return self.type
    def getLevel(self):
        return self.level
    def getImg(self):
        return self.imgNum
    def getName(self):
        return self.name
    def getDesc(self):
        return self.desc
    def getStats(self):
        return self.desc+' '+'Level '+str(self.level)+' Resist: '+str(self.resist)