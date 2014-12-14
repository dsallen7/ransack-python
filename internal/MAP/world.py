import pygame, random, cPickle, ppov, gzip, os
from UTIL import queue, const, colors, load_image, misc
from types import *

from MAP import generalmap, mapgen#, mazegen

class World():
    
    def __init__(self, context, myWorldBall=None, loadWorld=None):
        if context == 'editor':
            self.worldArray = []
            self.addMap( None, generalmap.edMap() )
            self.currentMap = self.worldArray[0]
            #self.initialMap = self.currentMap.name
            # number of maps in array
            # by default, world must have at least 1 map
            self.worldSize = 1
        elif context == 'game':
            if loadWorld is not None:
                self.installWorldBall(context, myWorldBall, loadWorld, )
            else: self.installWorldBall(context, myWorldBall, None, )
    
    def loadWorld(self, context):
        try:
            loadedWorld = gzip.GzipFile(os.getcwd()+'/MAP/WORLDS/MainWorld', 'rb', 1)
            ball = cPickle.load(loadedWorld)
            loadedWorld.close()
            self.installWorldBall(ball, context)
        except IOError, message:
            print 'Cannot load world:', filename
            return
    
    def getWorldBall(self, context):
        ballList = []
        if context == 'game':
            for thismap in self.worldArray:
                if thismap.getName()[:7]=='Dungeon' and thismap.getType() == 'dungeon':
                    ballList.append( thismap.getMapBall() )
        elif context == 'editor':
            for thismap in self.worldArray:
                ballList.append( thismap.getMapBall() )
        ball = (ballList, self.initialMap.getName(), self.currentMap.getName() )
        return ball
    
    def setInitialMap(self, name):
        self.getMapByName(name)
    
    def installWorldBall(self, context, myWorldBall, loadBall=None ):
        #print myWorldBall
        self.worldArray = []
        if context == 'editor':
            for mB in myWorldBall[0]:
                self.worldArray.append( generalmap.edMap(mB) )
            self.initialMap = self.getMapByName( myWorldBall[1] )
            self.currentMap = self.getMapByName( myWorldBall[1] )
        elif context == 'game':
            for mB in myWorldBall[0]:
                #print mB
                self.worldArray.append( generalmap.gameMap(mB, None) )
            if loadBall is not None:
                for mB in loadBall[0]:
                    newMap = generalmap.gameMap(mB)
                    self.worldArray.append( newMap )
                    if newMap.up[0] != 'dungeon':
                        self.getMapByName(newMap.up[0]).down = ( newMap.getName(), )
                    if newMap.down[0] != 'dungeon':
                        self.getMapByName(newMap.down[0]).up = ( newMap.getName(), )
                self.initialMap = self.getMapByName( loadBall[1] )
                self.currentMap = self.getMapByName( loadBall[2] )
            else:
                self.initialMap = self.getMapByName( myWorldBall[1] )
                self.currentMap = self.getMapByName( myWorldBall[2] )
    
    def getMapByName(self, name):
        for thismap in self.worldArray:
            if thismap.getName() == name:
                return thismap
    
    def removeMapByName(self, name):
        for thismap in self.worldArray[:]:
            if thismap.getName() == name:
                self.worldArray.remove( self.getMapByName(name) )
    
    def getMapList(self):
        L = []
        for thismap in self.worldArray:
            L.append(thismap.getName())
        return L

    # adds new map to world array
    def addMap(self, title=None, nMap=None):
        if nMap is not None:
            self.worldArray.append(nMap)
        elif title is not None:
            self.worldArray.append( generalmap.edMap(None, title) )
    
    # generates map but does not add it to world
    def generateMap(self, dimension, level, type):
        if type == 'dungeon':
            MG = mapgen.Generator(dimension, level)
            MG.generateMap(20)
            newMap = generalmap.gameMap(MG.getMapBall(), level)
        elif type == 'maze':
            MG = mazegen.Generator(dimension, level)
            MG.generateMap()
            newMap = generalmap.gameMap(self.inputHandler, None, MG.getMapBall(), level=self.levelDepth)
        return newMap

    # in-game only
    def upLevel(self):
        self.currentMap = self.getMapByName( self.currentmap.up[0] )
        return self.currentMap.pointOfExit
    
    # in-game only
    def downLevel(self):
        if self.currentMap.down[0] == 'dungeon':
            if self.currentMap.level == self.currentMap.down[1]:
                # next up is fortress
                dName = self.currentMap.getName()
                newMap = self.getMapByName( self.currentMap.down[2] ) #first one after dungeon ends
                self.currentMap.down = ( self.currentMap.down[2], )   # last floor of dungeon
                self.currentMap = newMap
                self.currentMap.up = ( dName, )
                return newMap.pointOfEntry
            else:
                # dungeon
                # generate new level
                newMap = self.generateMap(40, self.currentMap.level+1, type = 'dungeon')
                newMap.up = ( self.currentMap.getName(),)
                down_ = self.currentMap.down
                self.currentMap.down = ( newMap.getName(), )
                self.addMap(None, newMap )
                # set self.currentMap
                self.currentMap = self.getMapByName( newMap.getName() )
                self.currentMap.down = down_
                return newMap.pointOfEntry
        else:
            self.currentMap = self.getMapByName( self.currentMap.down[0] )
            return self.currentMap.pointOfEntry
    
    # in-game only
    # takes location (tiles not pixels) at which player is attempting to leave current map,
    def changeMap(self, dir, loc):
        if dir == 0: # north
            if self.currentMap.neighbors[0] is not '':
                if self.getMapByName( self.currentMap.neighbors[0] ).getTileFG(loc[0], 
                                                                               self.getMapByName( self.currentMap.neighbors[0] ).getDIM()-1  ) in range(const.BRICK1):
                    self.currentMap = self.getMapByName( self.currentMap.neighbors[0] )
                    return (loc[0], self.currentMap.getDIM()-1)
                else: return False
            else: return False
        elif dir == 1: # south
            if self.currentMap.neighbors[1] is not '':
                if self.getMapByName( self.currentMap.neighbors[1] ).getTileFG(loc[0], 0  ) in range(const.BRICK1):
                    self.currentMap = self.getMapByName( self.currentMap.neighbors[1] )
                    return (loc[0], 0)
                else: return False
            else: return False
        elif dir == 2: # east
            if self.currentMap.neighbors[2] is not '':
                if self.getMapByName( self.currentMap.neighbors[2] ).getTileFG(0, loc[1] ) in range(const.BRICK1):
                    self.currentMap = self.getMapByName( self.currentMap.neighbors[2] )
                    return (0, loc[1])
                else: return False
            else: return False
        elif dir == 3: # west
            if self.currentMap.neighbors[3] is not '':
                if self.getMapByName( self.currentMap.neighbors[3] ).getTileFG(self.getMapByName( self.currentMap.neighbors[3] ).getDIM()-1, 
                                                                               loc[1] ) in range(const.BRICK1):
                    self.currentMap = self.getMapByName( self.currentMap.neighbors[3] )
                    return (self.currentMap.getDIM()-1, loc[1])
                else: return False
            else: return False