from UTIL import const
from SCRIPTS import armorScr

class Armor():
    
    def __init__(self, type, resist=None):
        self.type = type
        self.desc, self.level, self.category, self.imgNum = armorScr.armorDict[type]
        self.name = 'armor'
        self.resist = resist
        self.enh = None
        self.enhAmt = 0
    
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
        return 'Resist: '+str(self.resist)

class Ring(Armor):
    def __init__(self, type, resist=None, pE=None):
        Armor.__init__(self, type, resist)
        if pE is not None:
            if pE[0] == 'plusHP':
                self.enh = 'Plus HP'
                self.enhAmt = pE[1]
            elif pE[0] == 'plusMP':
                self.enh = 'Plus MP'
                self.enhAmt = pE[1]
            elif pE[0] == 'plusWP':
                self.enh = 'Plus WC'
                self.enhAmt = pE[1]
        else:
            (self.enh, self.enhAmt) = (None, 0)
    
    def getStats(self):
        return 'Resist: '+str(self.resist)+str(self.enhAmt)+' '+self.enh