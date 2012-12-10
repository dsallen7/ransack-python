import pygame, random, math, os
from UTIL import const, misc

from SCRIPTS import npcScr

from IMG import images

from npc import Npc

from random import choice

class Animal(Npc):
    def __init__(self, x, y, name, filename, roam=5):
        Npc.__init__(self, x, y, name, filename)
        self.home = (x,y)
        self.roam = 5
    
    def flee(self, map, heroPos):
        (sX, sY) = self.getXY()
        (hX, hY) = heroPos
        if misc.DistanceX(self.getXY(), heroPos) > misc.DistanceY(self.getXY(), heroPos):
            if hX > sX:
                return self.move('left', map, heroPos)
            else:
                return self.move('right', map, heroPos)
        else:
            if hY > sY:
                return self.move('up', map, heroPos)
            else:
                return self.move('down', map, heroPos)
    def update(self, map, heroPos):
        (hX, hY) = heroPos
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        heroPos = (hX, hY)
        if misc.Distance(self.getXY(), heroPos) < 3:
            return self.flee(map, heroPos)
        else:
            i = random.randrange(1, 10)
            if i == 5:
                return self.move(random.choice(['up', 'down', 'left', 'right']), map, heroPos)
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
        if misc.eDistance( self.home, (sX + mX, sY + mY)  ) <= self.roam:
            if map.getEntry(sX + mX, sY + mY) in range(25) and (sX + mX, sY + mY) != (hX, hY) and not map.isOccupied(sX + mX, sY + mY):
                self.setXY(sX + mX, sY + mY)
            else: self.moving = False
        else: self.moving = False

class Deer(Animal):
    
    def __init__(self, x, y, msg):
        Animal.__init__(self, x, y, msg, 'deer.bmp')