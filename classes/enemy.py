import pygame
from load_image import *
from const import *
import random
from SCRIPTS import enemyScr
from random import choice

class enemy():
    def __init__(self, level):
        self.level = random.randrange(level, level+2)
        self.name = choice( enemyScr.enemiesByLevel[self.level] )
        if self.name in enemyScr.pEnemies:
            self.poison = True
        else: self.poison = False
        self.maxHP = random.randrange(level+10,level+20)
        self.currHP = self.maxHP
    
    def getLevel(self):
        return self.level
    def getHP(self):
        return self.currHP
    def getMaxHP(self):
        return maxHP
    def getName(self):
        return self.name
    
    def takeDmg(self, dmg):
        self.currHP -= dmg