from const import *

class Weapon():
    
    def __init__(self, type, level):
        self.type = type
        self.level = level
        self.imgNum = type + SWORD
        self.name = 'weapon'
    
    def getType(self):
        return self.type
    def getLevel(self):
        return self.level
    def getImg(self):
        return self.imgNum
    def getName(self):
        return self.name