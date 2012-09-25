import numpy as np
from numpy.random import random_integers as rnd
import matplotlib.pyplot as plt

from random import choice, randrange

from MAP import map, tile

from SCRIPTS import mapScr, enemyScr

import itertools

from UTIL import load_image, const


class Generator():
    def __init__(self, DIM, level):
        self.DIM = DIM
        self.map = map.genMap(self.DIM, 1)
        self.level = level

    def maze(self, width=40, height=40, complexity=.75, density =.75):
        # Only odd shapes
        shape = ((height//2)*2+1, (width//2)*2+1)
        # Adjust complexity and density relative to maze size
        complexity = int(complexity*(5*(shape[0]+shape[1])))
        density    = int(density*(shape[0]//2*shape[1]//2))
        # Build actual maze
        Z = np.zeros(shape, dtype=bool)
        # Fill borders
        Z[0,:] = Z[-1,:] = 1
        Z[:,0] = Z[:,-1] = 1
        # Make isles
        for i in range(density):
            x, y = rnd(0,shape[1]//2)*2, rnd(0,shape[0]//2)*2
            Z[y,x] = 1
            for j in range(complexity):
                neighbours = []
                if x > 1:           neighbours.append( (y,x-2) )
                if x < shape[1]-2:  neighbours.append( (y,x+2) )
                if y > 1:           neighbours.append( (y-2,x) )
                if y < shape[0]-2:  neighbours.append( (y+2,x) )
                if len(neighbours):
                    y_,x_ = neighbours[rnd(0,len(neighbours)-1)]
                    if Z[y_,x_] == 0:
                        Z[y_,x_] = 1
                        Z[y_+(y-y_)//2, x_+(x-x_)//2] = 1
                        x, y = x_, y_
        return Z
    
    def getMatrixEntry(self, x, y):
        if not ( (0 <= x and x < self.DIM ) or (0 <= y and y < self.DIM)  ):
            return None
        return self.Z[x][y]
    
    def rollDie(self, target, range):
        d = randrange(range)
        if target >= d:
            return True
        else:
            return False
        
    def getRandomTile(self, type):
        if type == 'open':
            x = randrange(1, self.DIM-1)
            y = randrange(1, self.DIM-1)
            while not ( not self.getMatrixEntry(x, y) and 
                        not self.getMatrixEntry(x, y-1) and 
                        not self.getMatrixEntry(x-1, y) and 
                        not self.getMatrixEntry(x+1, y) and 
                        not self.getMatrixEntry(x, y+1) ) :
                x = randrange(1, self.DIM-1)
                y = randrange(1, self.DIM-1)
            return (x,y)
        elif type == 'doorway':
            pass
        elif type == "closed":
            x = randrange(1, self.DIM-1)
            y = randrange(1, self.DIM-1)
            while not ( ( self.getMatrixEntry(x, y-1),
                    self.getMatrixEntry(x-1, y),
                    self.getMatrixEntry(x+1, y),
                    self.getMatrixEntry(x, y+1)
                   ) in list(itertools.permutations([True, True, True, False])) and not self.getMatrixEntry(x, y) ):
                x = randrange(1, self.DIM-1)
                y = randrange(1, self.DIM-1)
            return (x,y)
    
    def matrixToMap(self, mat):
        for i in range(1, self.DIM-1):
            
            if self.getMatrixEntry(i, 1):
                self.map.setEntry(i, 0, 27)
            else:
                self.map.setEntry(i, 0, 30)
            self.map.setEntry(i, self.DIM-1, 30)
            
            
            if self.getMatrixEntry(self.DIM-2, i):
                self.map.setEntry(self.DIM-1, i, 27)
            else:
                self.map.setEntry(self.DIM-1, i, 31)
            self.map.setEntry(0, i, 31)
            
            for j in range(1, self.DIM-1):
                if self.getMatrixEntry(i, j):
                    self.map.setEntry(i, j, mapScr.wallDict[( self.getMatrixEntry(i, j-1), self.getMatrixEntry(i-1, j), self.getMatrixEntry(i+1, j), self.getMatrixEntry(i, j+1) )]   )
                else: self.map.setEntry(i, j, 0)
    
    def generateMap(self):
        self.Z = self.maze()
        self.matrixToMap(self.Z)
        
        while not self.map.pathfinder( (1, self.DIM-2), (self.DIM-2, 1) ):
            self.Z = self.maze()
            self.matrixToMap(self.Z)
        
        self.map.setEntry(0, 0, 40)
        self.map.setEntry( 1, self.DIM-2, const.STAIRDN)
        self.map.pointOfExit = ( 1, self.DIM-2 )
        self.map.setEntry( self.DIM-2, 1, const.STAIRUP)
        self.map.pointOfEntry = ( self.DIM-2, 1)
        self.map.heroStart = ( self.DIM-2, 1 )
        
        i = 0
        while i < 15:
            tile = self.getRandomTile('open')
            if tile == None:
                pass
            else:
                self.map.NPCs.append( ( tile, choice(enemyScr.enemiesByLevel[self.map.level] ) ) )
                i += 1
        i = 0
        chestList = []
        while i < 5:
            chestItems = []
            tile = self.getRandomTile('closed')
            if tile == None:
                pass
            else:
                chestItems.append( (const.PARCHMENT-const.FRUIT1, choice(mapScr.parchByLevel[self.level]) ) )
                if self.rollDie(0, 2):
                    chestItems.append( (13, choice( range(15, 50)+range(15,30) ) ))
                chestList.append( (tile, chestItems) )
                (x,y) = tile
                self.map.setEntry( x, y, 110)
                i += 1
        self.map.chests = dict(chestList)

    def getMapBall(self):
        return self.map.getMapBall()

#plt.figure(figsize=(10,10))
#M = maze(40,40)
#print M
#plt.imshow(M,cmap=plt.cm.binary,interpolation='nearest')
#plt.xticks([]),plt.yticks([])
#plt.show()