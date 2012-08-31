import pygame
from load_image import *
from const import *
import random
from SCRIPTS import enemyScr
from random import choice

class enemy():
    def __init__(self, name, level):
        self.level = random.randrange(level, level+2)
        self.name = name
        if self.name in enemyScr.pEnemies:
            self.poison = True
        else: self.poison = False
        self.maxHP = random.randrange( enemyScr.healthDict[self.name]-5, enemyScr.healthDict[self.name]+5 )
        self.baseAttack = enemyScr.attackDict[self.name]
        self.currHP = self.maxHP
    
    def getLevel(self):
        return self.level
    def getHP(self):
        return self.currHP
    def getMaxHP(self):
        return maxHP
    def getName(self):
        return self.name
    def getBaseAttack(self):
        return self.baseAttack
    
    def takeDmg(self, dmg):
        if dmg:
            self.currHP -= dmg