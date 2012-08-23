from UTIL import const
from SCRIPTS import weaponScr

class Weapon():
    
    def __init__(self, type, level):
        self.type = type
        self.level = level
        self.imgNum = type + const.FRUIT1
        self.name = 'weapon'
        self.desc = weaponScr.descDict[self.type]
    
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