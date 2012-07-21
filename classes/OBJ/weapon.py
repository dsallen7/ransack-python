from const import *

class Weapon():
    
    def __init__(self, type, level):
        self.type = type
        self.level = level
        self.imgNum = type + SWORD
    
    def getType(self):
        return self.type
    def getLevel(self):
        return self.level
    def getImgNum(self):
        return self.imgNum