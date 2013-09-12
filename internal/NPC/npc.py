import pygame, random, math, os
from UTIL import const, misc, queue

from SCRIPTS import npcScr

#import citizen, enemy

from IMG import images

from random import choice

class Npc(pygame.sprite.Sprite):
    
    def __init__(self, x, y, message, imgFile, name=''):
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
        self.movingRate = 20
        self.moveQueue = queue.Queue()
        self.name = name
    
    def setRect(self, x1, y1, x2, y2):
        self.rect = (x1, y1, x2, y2)
    def getRect(self):
        return self.rect
    def getXY(self):
        return (self.X, self.Y)
    def setXY(self, x, y):
        self.X = x
        self.Y = y
    
    def moveEnqueue(self, moves):
        for c in moves:
            self.moveQueue.push(int(c))
    
    def moveFromQueue(self):
        d = self.moveQueue.pop()
        if d == 0:
            return 'right'
        elif d == 1:
            return 'down'
        elif d == 2:
            return 'left'
        elif d == 3:
            return 'up'
    
    def takeStep(self):
        #self.imgIdx = (1 - (self.imgIdx % 2)) + (2 * (self.imgIdx / 2))
        self.imgIdx = self.imgIdx + const.walkingList[self.stepIdx]
        self.stepIdx = ( self.stepIdx + 1 ) % 4
        
        self.image = self.images[self.imgIdx]
    
    def interact(self, interface, game):
        (hX, hY) = game.myHero.getXY()
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        (sX, sY) = self.getXY()
        for (cX, cY) in const.CARDINALS:
            if (sX + cX, sY + cY) == (hX, hY):
                if (cX, cY) == (0,-1):
                    self.dir = 'up'
                elif (cX, cY) == (0,1):
                    self.dir = 'down'
                elif (cX, cY) == (-1, 0):
                    self.dir = 'left'
                elif (cX, cY) == (1,0):
                    self.dir = 'right'
        interface.npcMessage(self.message, self.images[8])
        return None
    
    def playerIsFacingMe(self, hero):
        (hX, hY) = hero.getXY()
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        (sX, sY) = self.getXY()
        for (cX, cY) in const.CARDINALS:
            if (sX + cX, sY + cY) == (hX, hY):
                if (cX, cY) == (0,-1):
                    if hero.dir == 'down':
                        return True
                elif (cX, cY) == (0,1):
                    if hero.dir == 'up':
                        return True
                elif (cX, cY) == (-1, 0):
                    if hero.dir == 'right':
                        return True
                elif (cX, cY) == (1,0):
                    if hero.dir == 'left':
                        return True
        return False
        
    def moveIT(self, map, heroPos):
        (hX, hY) = heroPos
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        (sX, sY) = self.getXY()
        for (cX, cY) in const.CARDINALS:
            if map.getEntry(sX + cX, sY + cY) in range(25) and (sX + cX, sY + cY) != (hX, hY) and not map.isOccupied(sX + cX, sY + cY):
                if (cX, cY) == (0,-1):
                    self.dir = 'up'
                elif (cX, cY) == (0,1):
                    self.dir = 'down'
                elif (cX, cY) == (-1, 0):
                    self.dir = 'left'
                elif (cX, cY) == (1,0):
                    self.dir = 'right'
                self.moving = True
                return
        self.moving = False
        
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
            map.clearOccupied(sX, sY)
            map.setOccupied(sX+mX, sY+mY)
        else: self.moving = False
    
    def confuse(self, t):
        self.confused = t
        
    def update(self, map, heroPos):
        if self.moving == True:
            #print 'Im Moving IT!'
            self.move(self.dir, map, heroPos)
            return True
        i = random.randrange(1, self.movingRate)
        if i == 1:
            self.move(random.choice(['up', 'down', 'left', 'right']), map, heroPos)
            return True
        else: return False
    
    def getID(self):
        try:
            return self.ID
        except AttributeError:
            return None
    
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