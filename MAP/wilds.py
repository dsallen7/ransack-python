import os, pygame, cPickle

from random import choice, randrange
from MAP import map, tile, room
from UTIL import const, colors

from SCRIPTS import mEnemyScr, mapScr

from IMG import images

#from IMG import images

dirDict = { 'w':(-1,0), 'e':(1,0), 'n':(0,-1), 's':(0,1) }
DefaultWallTile = 12

DEFAULTBKGD = 0

class Generator():
    
    def __init__(self, DIM, level):
        self.map = map.genMap(DIM, level, 'Wilderness' )
        self.map.type = 'wilds'
        self.copyText = []
        self.level = level
        images.load()
    
    def rollDie(self, target, range):
        d = randrange(range)
        if target >= d:
            return True
        else:
            return False
    
    def weightedChoice(self, choices):
        choicesList = []
        for c in choices:
            choicesList += [c[1]]*c[0]
        return choice(choicesList)
    
    def getTileByNumber(self, tile):
        rX = randrange( 1, self.map.getDIM()-1 )
        rY = randrange( 1, self.map.getDIM()-1 )
        while self.map.getEntry(rX, rY) != tile:
            print 'Searching for '+str(tile)
            rX = randrange( 1, self.map.getDIM()-1 )
            rY = randrange( 1, self.map.getDIM()-1 )
        return rX, rY
    
    def generateMap(self):
        for x in range( 0, self.map.getDIM() ):
            self.map.setEntry(x, 0, const.PINE)
            self.map.setEntry(x, self.map.getDIM()/2, const.PINE)
            for y in range( 1, self.map.getDIM()/2 ):
                if x == 0 or x == self.map.getDIM()-1:
                    self.map.setEntry(x, y, const.GRASS1 )
                else: self.map.setEntry(x, y, self.weightedChoice(mapScr.wildsTilesList) )
        #self.draw()
        self.map.pointOfEntry = None
        self.map.pointOfExit = None
        self.map.heroStart = None
        #add chests
        chestlist = []
        i = 0
        while i < 5:
            # get random empty tile
            (rX, rY) = self.getTileByNumber(const.GRASS1)
            chestItems = []
            
            if self.rollDie(0, 2):
                chestItems.append( (randrange(26,29), self.level/4,
                                                               [randrange( (self.level/4)+1, (self.level/4)+3 ),
                                                                randrange( (self.level/4)+1, (self.level/4)+3 ),
                                                                randrange( (self.level/4)+1, (self.level/4)+3 )] ) )
            else: chestItems.append( (randrange(31,34), self.level/4, randrange(0, 3) ) )
            
            if self.rollDie(0, 8):
                chestItems.append( (randrange(26,29),self.level/4, # weapon level
                                    [randrange( (self.level/4)+1, (self.level/4)+3 ),     # plus str
                                     randrange( (self.level/4)+1, (self.level/4)+3 ),     # plus int
                                     randrange( (self.level/4)+1, (self.level/4)+3 )] ) ) # plus dex
            elif self.rollDie(0, 5):
                chestItems.append( (const.PARCHMENT-const.FRUIT1, choice(mapScr.parchByLevel[self.level]) ) )
            elif self.rollDie(0, 3):
                chestItems.append( (13, choice( range(15, 50)+range(15,30) ) ))
            else:
                chestItems.append( (self.weightedChoice( zip( [randrange(1,3),randrange(1,3),randrange(1,3)],
                                                               mapScr.fruitList ) ), 
                                    1 ) )
            self.map.setEntry( rX, rY, 110)
            chestlist += [( (rX, rY), chestItems )]
            
            i += 1
            
        self.map.chests = dict(chestlist)
        '''
        # add enemies
        while len(rooms) > 0:
            room = choice(rooms)
            (xpos, ypos) = room.getPos()
            (xdim, ydim) = room.getDimensions()
            self.map.NPCs.append( (( xpos + xdim/2, ypos + ydim/2), choice(mEnemyScr.enemiesByLevel[self.map.level] ) ) )
            rooms.remove(room)
        '''
        #(rX, rY) = self.getTileByNumber(const.GRASS1)
    def getMapBall(self):
        return self.map.getMapBall()
    
    def draw(self):
        gridField = pygame.Surface(( self.map.getDIM()*const.blocksize, 
                                     self.map.getDIM()*const.blocksize ))
        gridField.fill( [0,0,0] )
        for i in range(self.map.getDIM()):
            for j in range(self.map.getDIM()):
                gridField.blit( images.mapImages[self.map.getEntry(i,j)], (i*const.blocksize,j*const.blocksize) )

        screen.blit(gridField, (0,0) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass