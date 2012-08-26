from UTIL import const
from SCRIPTS import weaponScr

class Weapon():
    
    def __init__(self, type, level, plusStr=0, plusItl=0, plusDex=0):
        self.type = type
        self.level = level
        self.imgNum = type + const.FRUIT1
        self.name = 'weapon'
        self.desc = weaponScr.descDict[self.type]
        
        self.plusStr = plusStr
        self.plusItl = plusItl
        self.plusDex = plusDex
    
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
        return self.desc+' '+'Level '+str(self.level)+' +'+str(self.plusStr)+' Strength +'+str(self.plusItl)+' Intel +'+str(self.plusDex)+'Dex'