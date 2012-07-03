import pygame
from load_image import *
from const import *
import random

class sword(pygame.sprite.Sprite):
    
    def __init__(self):
        self.images = range(4)
        self.images[0], self.rect = load_image('sword_d.bmp', -1)
        
        self.image = self.images[0]
        
        self.swordTimer = 0
        self.swordLoc = (0,0)
        self.swordDir = 'd'
        
    
    def drawSword(self):
        self.swordTimer -= 1
        x,y = self.swordLoc
        if self.swordDir == 'd':
            self.newGame.gameBoard.blit(self.images[0], (x,y) )
        elif self.swordDir == 'u':
            self.newGame.gameBoard.blit(self.images[0], (x,y) )
        elif self.swordDir == 'l':
            self.newGame.gameBoard.blit(self.images[0], (x,y) )
        elif self.swordDir == 'r':
            self.newGame.gameBoard.blit(self.images[0], (x,y) )

    def attack(self, x, y, direction):
        swordX = 0
        swordY = 0
        if direction == 'd':
            swordY = blocksize
        if direction == 'u':
            swordY = -blocksize
        if direction == 'l':
            swordX = -blocksize
        if direction == 'r':
            swordX = blocksize
        
        self.swordLoc = (x + swordX, y + swordY)
        self.swordTimer = 5
        self.swordDir = direction
        for b in self.newGame.badguys:
            (x2,y2) = b.location
            if (x + swordX) == x2 and (y + swordY) == y2:
                b.die()
                self.newGame.badguys.remove(b)