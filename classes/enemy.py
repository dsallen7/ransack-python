import pygame
from load_image import *
from const import *
import random

class enemy():
    def __init__(self):
        self.maxHP = random.randrange(10,20)
        self.currHP = self.maxHP
    
    
    def getHP(self):
        return self.currHP
    
    def takeDmg(self, dmg):
        self.currHP -= dmg