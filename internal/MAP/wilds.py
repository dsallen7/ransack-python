import os
import pygame
import cPickle

from random import choice, randrange
from MAP import generalmap, tile
from UTIL import const, colors, misc
from SCRIPTS import enemyScr, mapScr
from IMG import images


dirDict = {'w':(-1,0), 'e':(1,0), 'n':(0,-1), 's':(0,1)}
DefaultWallTile = 12

DEFAULTBKGD = 0

class Generator():
    
    def __init__(self, DIM, level):
        self.generalmap = generalmap.genMap(DIM, level, 'Wilderness' )
        self.generalmap.type = 'wilds'
        self.copyText = []
        self.level = level
        images.load()
    
    def rollDie(self, target, range):
        d = randrange(range)
        if target >= d:
            return True
        else:
            return False
    
    def getTileByNumber(self, tile):
        rX = randrange( 1, self.generalmap.getDIM()-1 )
        rY = randrange( 1, self.generalmap.getDIM()-1 )
        while self.generalmap.getEntry(rX, rY) != tile:
            print 'Searching for '+str(tile)
            rX = randrange( 1, self.generalmap.getDIM()-1 )
            rY = randrange( 1, self.generalmap.getDIM()-1 )
        return rX, rY
    
    def generateMap(self, orientation):
        if orientation == 'h':
            for x in range( 0, self.generalmap.getDIM() ):
                self.generalmap.setEntry(x, 0, const.PINE1)
                self.generalmap.setTileBG(x, 0, const.GRASS3)
                self.generalmap.setEntry(x, self.generalmap.getDIM()/2, const.PINE1)
                self.generalmap.setTileBG(x, self.generalmap.getDIM()/2, const.GRASS3)
                for y in range( 1, self.generalmap.getDIM()/2 ):
                    if x == 0 or x == self.generalmap.getDIM()-1:
                        self.generalmap.setEntry(x, y, const.GRASS1 )
                    else: self.generalmap.setEntry(x, y, misc.weightedChoice(mapScr.wildsTilesList) )
                    self.generalmap.setTileBG(x, y, const.GRASS3)
        elif orientation == 'v':
            for x in range( 0, self.generalmap.getDIM() ):
                self.generalmap.setEntry(0, x, const.PINE1)
                self.generalmap.setTileBG(0, x, const.GRASS3)
                self.generalmap.setEntry(self.generalmap.getDIM()/2, x, const.PINE1)
                self.generalmap.setTileBG(self.generalmap.getDIM()/2, x, const.GRASS3)
                for y in range( 1, self.generalmap.getDIM()/2 ):
                    if x == 0 or x == self.generalmap.getDIM()-1:
                        self.generalmap.setEntry(y, x, const.GRASS1 )
                    else: self.generalmap.setEntry(y, x, misc.weightedChoice(mapScr.wildsTilesList) )
                    self.generalmap.setTileBG(y, x, const.GRASS3)
        #self.draw()
        self.generalmap.pointOfEntry = None
        self.generalmap.pointOfExit = None
        self.generalmap.heroStart = None
        #add chests
        chestlist = []
        i = 0
        while i < 5:
            # get random empty tile
            (rX, rY) = self.getTileByNumber(const.GRASS1)
            chestItems = []
            
            if misc.rollDie(0, 2):
                chestItems.append( (randrange(const.WSWORD,const.HELMET), self.level/4,
                                                               [randrange( (self.level/4)+1, (self.level/4)+3 ),
                                                                randrange( (self.level/4)+1, (self.level/4)+3 ),
                                                                randrange( (self.level/4)+1, (self.level/4)+3 )] ) )
            else: chestItems.append( (randrange(31,34), self.level/4, randrange(0, 3) ) )
            
            if misc.rollDie(0, 8):
                chestItems.append( (randrange(26,29),self.level/4, # weapon level
                                    [randrange( (self.level/4)+1, (self.level/4)+3 ),     # plus str
                                     randrange( (self.level/4)+1, (self.level/4)+3 ),     # plus int
                                     randrange( (self.level/4)+1, (self.level/4)+3 )] ) ) # plus dex
            elif misc.rollDie(0, 5):
                chestItems.append( (const.PARCHMENT-const.FRUIT1, choice(mapScr.parchByLevel[self.level]) ) )
            elif misc.rollDie(0, 3):
                chestItems.append( (const.GOLD, choice( range(15, 50)+range(15,30) ) ))
            else:
                chestItems.append( (misc.weightedChoice( zip( [randrange(1,3),randrange(1,3),randrange(1,3)],
                                                               mapScr.fruitList ) ), 
                                    1 ) )
            self.generalmap.setEntry( rX, rY, const.CHEST)
            chestlist += [( (rX, rY), chestItems )]
            
            i += 1
            
        self.generalmap.chests = dict(chestlist)
        '''
        # add enemies
        while len(rooms) > 0:
            room = choice(rooms)
            (xpos, ypos) = room.getPos()
            (xdim, ydim) = room.getDimensions()
            self.generalmap.NPCs.append( (( xpos + xdim/2, ypos + ydim/2), choice(enemyScr.enemiesByLevel[self.generalmap.level] ) ) )
            rooms.remove(room)
        '''
        #(rX, rY) = self.getTileByNumber(const.GRASS1)
    def getMapBall(self):
        return self.generalmap.getMapBall()
    
    def draw(self):
        gridField = pygame.Surface(( self.generalmap.getDIM()*const.blocksize, 
                                     self.generalmap.getDIM()*const.blocksize ))
        gridField.fill( [0,0,0] )
        for i in range(self.generalmap.getDIM()):
            for j in range(self.generalmap.getDIM()):
                gridField.blit( images.mapImages[self.generalmap.getEntry(i,j)], (i*const.blocksize,j*const.blocksize) )

        screen.blit(gridField, (0,0) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
