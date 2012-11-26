import pygame, random, cPickle, ppov, gzip, os
from UTIL import queue, const, colors, load_image, misc
from types import *

from MAP import map, mapgen#, mazegen

class World():
    
    def __init__(self, context, wBall=None):
        if context == 'editor':
            self.worldArray = []
            self.addMap( None, map.edMap() )
            self.currentMap = self.worldArray[0]
            #self.initialMap = self.currentMap.name
            # number of maps in array
            # by default, world must have at least 1 map
            self.worldSize = 1
        elif context == 'game':
            if wBall is not None:
                self.installWorldBall(wBall, context)
            else: self.loadWorld('game')
            #installWorldBall(loadBall, context)
    
    def loadWorld(self, context):
        try:
            loadedWorld = gzip.GzipFile(os.getcwd()+'/MAP/WORLDS/MainWorld', 'rb')
            ball = cPickle.load(loadedWorld)
            loadedWorld.close()
            self.installWorldBall(ball, context)
        except IOError, message:
            print 'Cannot load world:', filename
            return
    
    def getWorldBall(self):
        ballList = []
        for map in self.worldArray:
            ballList.append( map.getMapBall() )
        return (ballList, self.initialMap.getName(), self.currentMap.getName() )
    
    def setInitialMap(self, name):
        self.getMapByName(name)
    
    def installWorldBall(self, ball, context):
        self.worldArray = []
        if context == 'editor':
            for mB in ball[0]:
                self.worldArray.append( map.edMap(mB, None) )
            self.initialMap = self.getMapByName( ball[1] )
            self.currentMap = self.getMapByName( ball[1] )
        elif context == 'game':
            for mB in ball[0]:
                self.worldArray.append( map.gameMap(mB) )
            self.initialMap = self.getMapByName( ball[1] )
            self.currentMap = self.getMapByName( ball[2] )
            #self.currentMap.setPlayerXY
    
    def getMapByName(self, name):
        for map in self.worldArray:
            if map.getName() == name:
                return map
    
    def removeMapByName(self, name):
        for map in self.worldArray[:]:
            if map.getName() == name:
                self.worldArray.remove( self.getMapByName(name) )
    
    def getMapList(self):
        L = []
        for map in self.worldArray:
            L.append(map.getName())
        return L

    # adds new map to world array
    def addMap(self, title=None, nMap=None):
        if nMap is not None:
            self.worldArray.append(nMap)
        elif title is not None:
            self.worldArray.append( map.edMap(None, title) )
    
    # generates map but does not add it to world
    def generateMap(self, dimension, level, type):
        if type == 'dungeon':
            MG = mapgen.Generator(dimension, level)
            MG.generateMap(20)
            newMap = map.gameMap(MG.getMapBall(), level)
        elif type == 'maze':
            MG = mazegen.Generator(dimension, level)
            MG.generateMap()
            newMap = map.gameMap(self.inputHandler, None, MG.getMapBall(), level=self.levelDepth)
        return newMap

    # in-game only
    def upLevel(self):
        self.currentMap = self.getMapByName( self.currentMap.up[0] )
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
                newMap = self.generateMap(40, self.currentMap.level+1, type = 'dungeon')
                newMap.up = ( self.currentMap.getName(),)
                down_ = self.currentMap.down
                self.currentMap.down = ( newMap.getName(), )
                self.addMap(None, newMap )
                self.currentMap = self.getMapByName( newMap.getName() )
                self.currentMap.down = down_
                return newMap.pointOfEntry
                # generate new level
                # set self.currentMap
        else:
            self.currentMap = self.getMapByName( self.currentMap.down[0] )
            return self.currentMap.pointOfEntry
    
    # in-game only
    # takes location (tiles not pixels) at which player is attempting to leave current map,
    def changeMap(self, dir, loc):
        if dir == 0: # north
            if self.currentMap.neighbors[0] is not '':
                if self.getMapByName( self.currentMap.neighbors[0] ).getTileFG(loc[0], 
                                                                               self.getMapByName( self.currentMap.neighbors[0] ).getDIM()-1  ) in range(24):
                    self.currentMap = self.getMapByName( self.currentMap.neighbors[0] )
                    return (loc[0], self.currentMap.getDIM()-1)
                else: return False
            else: return False
        elif dir == 1: # south
            if self.currentMap.neighbors[1] is not '':
                if self.getMapByName( self.currentMap.neighbors[1] ).getTileFG(loc[0], 0  ) in range(24):
                    self.currentMap = self.getMapByName( self.currentMap.neighbors[1] )
                    return (loc[0], 0)
                else: return False
            else: return False
        elif dir == 2: # east
            if self.currentMap.neighbors[2] is not '':
                if self.getMapByName( self.currentMap.neighbors[2] ).getTileFG(0, loc[1] ) in range(24):
                    self.currentMap = self.getMapByName( self.currentMap.neighbors[2] )
                    return (0, loc[1])
                else: return False
            else: return False
        elif dir == 3: # west
            if self.currentMap.neighbors[3] is not '':
                if self.getMapByName( self.currentMap.neighbors[3] ).getTileFG(self.getMapByName( self.currentMap.neighbors[3] ).getDIM()-1, 
                                                                               loc[1] ) in range(24):
                    self.currentMap = self.getMapByName( self.currentMap.neighbors[3] )
                    return (self.currentMap.getDIM()-1, loc[1])
                else: return False
            else: return False