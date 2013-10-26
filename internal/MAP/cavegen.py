import os, pygame, cPickle

from random import choice, randrange
from MAP import map, tile
from ROOM import room, roomtools
from UTIL import const, colors, misc

from SCRIPTS import enemyScr, mapScr

#from IMG import images

DefaultWallTile = 29

DEFAULTBKGD = 0

class Generator():
    
    def __init__(self, DIM, level=1):
        self.map = map.genMap(DIM, level, 'Cave' )
        self.map.type = 'cave'
        self.copyText = []
        self.level = level
    
    def singlePass(self):
        for i in range(self.map.DIM):
            for j in range(self.map.DIM):
                if self.map.getEntry(i,j) == const.CAVEWALL1:
                    count = 1
                else: count = 0
                for n in self.map.cardinalNeighbors( (i,j) ):
                    if n == const.CAVEWALL1 or n == const.VOID:
                        count += 1
                if count >= 5:
                    self.map.setEntry(i,j, const.CAVEWALL1)
                elif count <= 2:
                    self.map.setEntry(i,j, const.DFLOOR1)
    
    def generateMap(self):
        for i in range(self.map.DIM):
            for j in range(self.map.DIM):
                if misc.rollDie(50,100):
                    self.map.setEntry(i,j, const.DFLOOR1)
                else:
                    self.map.setEntry(i,j, const.CAVEWALL1)
        #borders
        for i in range(self.map.DIM):
            self.map.setEntry(i,0, const.CAVEWALL1)
            self.map.setEntry(i,self.map.DIM-1, const.CAVEWALL1)
            self.map.setEntry(0,i, const.CAVEWALL1)
            self.map.setEntry(self.map.DIM-1,i, const.CAVEWALL1)
        for i in range(4):
            self.singlePass()
            #self.draw()
        self.map.pointOfEntry = ( 0,0 )
        self.map.pointOfExit = ( 0,0 )
        self.map.heroStart = ( 0,0 )

    
    def getMapBall(self):
        return self.map.getMapBall()
 
    
    def draw(self):
        gridField.fill( [0,0,0] )
        for i in range(DIM):
            for j in range(DIM):
                gridField.blit( images.mapImages[myMap.getMapEntry(i,j)], (i*blocksize,j*blocksize) )

        screen.blit(gridField, (0,0) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass