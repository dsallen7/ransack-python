import pygame
from load_image import *
from const import *
import random

class enemy():
    def __init__(self, level):
        self.maxHP = random.randrange(10,20)
        self.currHP = self.maxHP
        self.level = random.randrange(level, level+2)
    
    
    def getHP(self):
        return self.currHP
    
    def getMaxHP(self):
        return maxHP
    
    def takeDmg(self, dmg):
        self.currHP -= dmg