import pygame, random, math, os
from UTIL import const, misc

from SCRIPTS import npcScr

from IMG import images

from npc import Npc

from random import choice

# Animals may be totally benign or may initial battle
# Some animals do not battle unless player initiates first.

class Animal(Npc):
    def __init__(self, x, y, name, filename, roam=5):
        Npc.__init__(self, x, y, name, filename)
        self.home = (x,y)
        self.roam = 5
        self.type = 'animal'
    
    def flee(self, map, heroPos):
        (sX, sY) = self.getXY()
        (hX, hY) = heroPos
        surroundings = filter( lambda x: map.getEntrySingle(x) < 18, map.cardinalNeighborsByCoords( (sX, sY) ) )
        
        moveTo = choice( surroundings )
        for (cX, cY), dir in zip( const.CARDINALS, ['up', 'down', 'left', 'right']):
            if (cX+sX, cY+sY) == moveTo and (cX+sX, cY+sY) != (hX, hY):
                self.move(dir, map, heroPos)
    
    def update(self, map, heroPos):
        (hX, hY) = heroPos
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        heroPos = (hX, hY)
        if misc.Distance(self.getXY(), heroPos) < 3:
            self.flee(map, heroPos)
            return True
        else:
            i = random.randrange(1, self.movingRate)
            if i == 1:
                self.move(random.choice(['up', 'down', 'left', 'right']), map, heroPos)
                return True
            else: return False
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
        return self.moving

class Deer(Animal):
    
    def __init__(self, x, y, msg):
        Animal.__init__(self, x, y, msg, 'deer.bmp')

class aggressiveAnimal(Animal):
    def __init__(self, x, y, n, filename):
        Animal.__init__(self, x, y, n[2], filename)
    
    def update(self, map, heroPos):
        (hX, hY) = heroPos
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        heroPos = (hX, hY)
        i = random.randrange(1, self.movingRate)
        if i == 1:
            self.move(random.choice(['up', 'down', 'left', 'right']), map, heroPos)
            return True
        else: return False
    def interact(self, interface, game):
        if interface.npcDialog(self.message, self.images[8]) == 'Yes':
            game.displayOneFrame()
            return 'battle'

class wildDog(aggressiveAnimal):
    
    def __init__(self, x, y, n):
        aggressiveAnimal.__init__(self, x, y, n, 'wilddog.bmp')
        self.message = 'Do you want to fight the Wild Dog?'
        self.movingRate = 50
        self.name = npcScr.enemyDict[n[1]][0]
        self.ID = n

class Badger(aggressiveAnimal):
    
    def __init__(self, x, y, n):
        aggressiveAnimal.__init__(self, x, y, n, 'badger.bmp')
        self.message = 'Do you want to fight the Badger?'
        self.movingRate = 50
        self.name = npcScr.enemyDict[n[1]][0]
        self.ID = n

class GardenBadger(Animal):
    
    def __init__(self, x, y, n):
        Animal.__init__(self, x, y, n[2], 'badger.bmp')
        self.message = 'Do you want to fight the Badger?'
        self.movingRate = 50
        self.name = npcScr.enemyDict[n[1]][0]
        self.ID = n
    def update(self, map, heroPos):
        (hX, hY) = heroPos
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        heroPos = (hX, hY)
        i = random.randrange(1, self.movingRate)
        if i == 1:
            self.move(random.choice(['up', 'down', 'left', 'right']), map, heroPos)
            return True
        else: return False
    def interact(self, interface, game):
        if game.Director.getQuestStatus(0) == 0:
            interface.npcMessage("It's a garden badger.", self.images[8] )
            return None
        if interface.npcDialog(self.message, self.images[8]) == 'Yes':
            game.displayOneFrame()
            return 'battle'