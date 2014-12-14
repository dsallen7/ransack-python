from UTIL import const
from SCRIPTS import weaponScr


class Weapon():

    def __init__(self, type, mods=None):
        self.type = type
        self.level = weaponScr.wLevel[type]
        self.imgNum = type + const.FRUIT1
        self.name = 'weapon'
        self.desc = weaponScr.descDict[self.type]

        if mods is not None:
            self.plusStr = mods[0]
            self.plusItl = mods[1]
            self.plusDex = mods[2]
        else:
            self.plusStr = 0
            self.plusItl = 0
            self.plusDex = 0

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
        return self.desc + ' ' + 'Level ' + str(self.level) + ' +' + str(
            self.plusStr) + ' Str +' + str(self.plusItl) + ' Intel +' + str(
            self.plusDex) + 'Dex'
