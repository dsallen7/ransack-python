import pygame, random, pickle
from load_image import *
from const import *

class map():
    def __init__(self, badguys, filename):
        self.maptext = []
        self.loadMap()
        self.images = range(10)
        imageNames = ['floor.bmp','brick2.bmp','key.bmp','door.bmp','exit.bmp','fruit_s.bmp','hpotion.bmp','spellbook.bmp','chest.bmp']
        self.images[0], self.rect = load_image(imageNames[0], -1)
        for i in range(1,9):
            self.images[i], self.rect = load_image(imageNames[i], None)
        
        self.image = self.images[0]
        
        for i in range(DIM):
            for j in range(DIM):
                if self.getUnit(i,j) == 9:
                    self.startXY = (i,j)
        
        self.topMapCorner = (0,0)
    
    def saveMap(self):
        grid = self.getGrid()
        save = open("map.dat", "w")
        pickle.dump(grid, save)
        save.close()
    
    def loadMap(self):
        save = open("map.dat", "r")
        grid = pickle.load(save)
        save.close()
        self.maptext = grid
    
    def getGrid(self):
        return self.maptext
    
    #working:
    # 0 : open space
    # 1 : wall
    # 2 : key
    # 3 : door
    # 4 : exit
    # 5 : fruit
    # 6 : h potion
    # 7 : spellbook
    # 8 : chest
    def redraw(self, heroLoc, gameBoard):
        # Compute top map corner
        (px,py) = heroLoc
        px = px/blocksize
        py = py/blocksize
        
        self.topMapCorner = ( (px%10 + (px/10)*10), (py%10 + (py/10)*10) )
        
        if px < 5:
            topX = 0
        elif 5 <= px <= 15:
            topX = px - 5
        else:
            topX = 10
        
        if py < 5:
            topY = 0
        elif 5 <= py <= 15:
            topY = py - 5
        else:
            topY = 10
        #Redraw map on screen from current map matrix
        #topX, topY = self.topMapCorner
        for x in range(HALFDIM):
            for y in range(HALFDIM):
                d = self.getUnit(x+topX,y+topY)
                if d < 9:
                    self.image = self.images[d]
                    gameBoard.blit(self.image, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )

    def getItem(self, x, y):
        #updates map with collected item
        self.maptext[y] = self.maptext[y][:x]+[0]+self.maptext[y][x+1:]
        
    def updateUnit(self, x, y, type):
        #Updates one map unit to type at map coordinates x,y
        self.maptext[y] = self.maptext[y][:x]+[type]+self.maptext[y][x+1:]
    
    def getUnit(self,x,y):
        return self.maptext[y][x]
