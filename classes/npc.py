import pygame, random, math, os
from load_image import *
from UTIL import const

from IMG import images

class npc(pygame.sprite.Sprite):
    
    def __init__(self, x, y, imgFile):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.X = x
        self.Y = y
        self.images = images.loadNPC(imgFile)
        self.imgIdx = 2
        self.image = self.images[self.imgIdx]
        self.dir = 'down'
        self.moving = False
        self.setRect(x*const.blocksize, y*const.blocksize, const.blocksize, const.blocksize)
    
    def setRect(self,x1,y1,x2,y2):
        self.rect = (x1,y1,x2,y2)
    def getRect(self):
        return self.rect
    def getXY(self):
        return (self.X, self.Y)
    def setXY(self, x, y):
        self.X = x
        self.Y = y
    
    def takeStep(self):
        self.imgIdx = ( 1 - (self.imgIdx % 2) ) + (2 * (self.imgIdx / 2))
        self.image = self.images[self.imgIdx]
    
    def interact(self, hud):
        hud.boxMessage('Hello, hero!')
    
    def move(self, dir, map, heroPos):
        (hX, hY) = heroPos
        hX = hX /const.blocksize
        hY = hY /const.blocksize
        self.moving = True
        (sX, sY) = self.getXY()
        self.dir = dir
        if dir == 'up':
            self.imgIdx = 0
            if map.getEntry(sX, sY-1) in range(25) and (sX, sY-1) != (hX,hY):
                self.setXY(sX, sY-1)
            else: self.moving = False
        elif dir == 'down':
            self.imgIdx = 2
            if map.getEntry(sX, sY+1) in range(25) and (sX, sY+1) != (hX,hY):
                self.setXY(sX, sY+1)
            else: self.moving = False
        elif dir == 'left':
            self.imgIdx = 4
            if map.getEntry(sX-1, sY) in range(25) and (sX-1, sY) != (hX,hY):
                self.setXY(sX-1, sY)
            else: self.moving = False
        elif dir == 'right':
            self.imgIdx = 6
            if map.getEntry(sX+1, sY) in range(25) and (sX+1, sY) != (hX,hY):
                self.setXY(sX+1, sY)
            else: self.moving = False
        self.image = self.images[self.imgIdx]
    
    def update(self, map, heroPos):
        i = random.randrange(1, 10)
        if i == 5:
            self.move(random.choice(['up','down','left','right']), map, heroPos )
    
    def shiftOnePixel(self, dir, sign):
        (x1, y1, x2, y2) = self.rect
        if dir == 'up':
            self.setRect(x1, y1+sign, x2, y2)
        if dir == 'down':
            self.setRect(x1, y1-sign, x2, y2)
        if dir == 'left':
            self.setRect(x1+sign, y1, x2, y2)
        if dir == 'right':
            self.setRect(x1-sign, y1, x2, y2)