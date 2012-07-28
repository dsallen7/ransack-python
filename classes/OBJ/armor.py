from const import *

class Armor():
    
    def __init__(self, type, level):
        self.type = type
        self.level = level
        self.imgNum = type + SHIELD
        self.name = 'armor'
    
    def getType(self):
        return self.type
    def getLevel(self):
        return self.level
    def getImg(self):
        return self.imgNum
    def getName(self):
        return self.name