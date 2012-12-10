import pygame, random, math, os
from UTIL import const, misc

from SCRIPTS import npcScr

#import citizen, enemy

from IMG import images

from random import choice

class Npc(pygame.sprite.Sprite):
    
    def __init__(self, x, y, message, imgFile):
        self.start = (x, y)
        self.X = x
        self.Y = y
        self.images = images.loadNPC(imgFile)
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.imgIdx = 2
        self.stepIdx = 0
        self.image = self.images[self.imgIdx]
        self.dir = 'down'
        self.moving = False
        self.message = message
        self.setRect(x * const.blocksize, y * const.blocksize, const.blocksize, const.blocksize)
    
    def setRect(self, x1, y1, x2, y2):
        self.rect = (x1, y1, x2, y2)
    def getRect(self):
        return self.rect
    def getXY(self):
        return (self.X, self.Y)
    def setXY(self, x, y):
        self.X = x
        self.Y = y
    
    def takeStep(self):
        #self.imgIdx = (1 - (self.imgIdx % 2)) + (2 * (self.imgIdx / 2))
        self.imgIdx = self.imgIdx + const.walkingList[self.stepIdx]
        self.stepIdx = ( self.stepIdx + 1 ) % 4
        
        self.image = self.images[self.imgIdx]
    
    def interact(self, interface, game):
        interface.npcMessage(self.message, self.images[8])
        return None
    
    def move(self, dir, map, heroPos):
        (hX, hY) = heroPos
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        self.moving = True
        (sX, sY) = self.getXY()
        self.dir = dir
        (mX, mY) = const.scrollingDict[dir]
        self.imgIdx = const.imgDict[dir]
        self.image = self.images[self.imgIdx]
        if map.getEntry(sX + mX, sY + mY) in range(25) and (sX + mX, sY + mY) != (hX, hY) and not map.isOccupied(sX + mX, sY + mY):
            self.setXY(sX + mX, sY + mY)
        else: self.moving = False
    
    def update(self, map, heroPos):
        i = random.randrange(1, 20)
        if i == 5:
            self.move(random.choice(['up', 'down', 'left', 'right']), map, heroPos)
            return True
        else: return False
    
    def shiftOnePixel(self, dir, sign):
        (x1, y1, x2, y2) = self.rect
        if dir == 'up':
            self.setRect(x1, y1 + sign, x2, y2)
        if dir == 'down':
            self.setRect(x1, y1 - sign, x2, y2)
        if dir == 'left':
            self.setRect(x1 + sign, y1, x2, y2)
        if dir == 'right':
            self.setRect(x1 - sign, y1, x2, y2)