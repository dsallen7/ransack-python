import pygame, random, math, os
from UTIL import const, misc

from SCRIPTS import npcScr

from IMG import images

from npc import Npc

from random import choice

class Enemy(Npc):
    def __init__(self, x, y, name, filename, mID):
        Npc.__init__(self, x, y, name, filename)
        self.name = name
        self.turn = False
        self.confused = 0
        self.ID = mID
    
    def move(self, dir, map, heroPos):
        (hX, hY) = heroPos
        self.moving = True
        (sX, sY) = self.getXY()
        (mX, mY) = const.scrollingDict[dir]
        self.dir = dir
        sX += mX
        sY += mY
        if map.getEntry(sX, sY) in range(25):
            if (sX, sY) != (hX, hY):
                self.setXY(sX, sY)
            else:
                self.moving = False
                return 'battle'
        else: 
            self.moving = False
            return False
        self.imgIdx = const.imgDict[dir]
        self.image = self.images[self.imgIdx]
        return True
    def seek(self, map, heroPos):
        (sX, sY) = self.getXY()
        (hX, hY) = heroPos
        if misc.DistanceX(self.getXY(), heroPos) > misc.DistanceY(self.getXY(), heroPos):
            if hX > sX:
                return self.move('right', map, heroPos)
            else:
                return self.move('left', map, heroPos)
        else:
            if hY > sY:
                return self.move('down', map, heroPos)
            else:
                return self.move('up', map, heroPos)
    
    def interact(self, interface, game):
        interface.boxMessage('The battle is joined!')
        return 'battle'
    def update(self, map, heroPos):
        if self.confused > 0:
            imgCopy = self.image.copy()
            imgCopy.blit( self.images[8],(0,0) )
            if self.confused/2 == 0:
                self.image = imgCopy
            else: self.image = self.images[self.imgIdx]
            self.confused -= 1
            return True
        (hX, hY) = heroPos
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        heroPos = (hX, hY)
        if misc.Distance(self.getXY(), heroPos) < 3:
            self.turn = not self.turn
            if self.turn:
                return self.seek(map, heroPos)
        else:
            i = random.randrange(1, 10)
            if i == 5:
                return self.move(random.choice(['up', 'down', 'left', 'right']), map, heroPos)
    def confuse(self, t):
        self.confused = t
    def getID(self):
        return self.ID
    
class skeletonKing(Enemy):
    
    def __init__(self, x, y, name, filename, mID, d):
        
        Enemy.__init__(self, x, y, name, filename, mID)
        self.Director = d
        
    def interact(self, interface, game):
        interface.npcMessage('Welcome to your death!', self.images[2])
        return 'battle'
    
    def update(self, map, heropos):
        i = random.randrange(1, 6)
        if i == 5:
            self.takeStep()
    def die(self):
        self.Director.setEvent(11)