import pygame, random, pickle
from load_image import *
from const import *

class map():
    def __init__(self, badguys, filename):
        self.maptext = []
        self.loadMap()
        self.images = range(11)
        imageNames = ['floor.bmp','brick2.bmp','key.bmp','door.bmp','exit.bmp','fruit_s.bmp','hpotion.bmp','mpotion.bmp','spellbook.bmp','chest.bmp']
        self.images[0], self.rect = load_image(imageNames[0], -1)
        for i in range(1,10):
            self.images[i], self.rect = load_image(imageNames[i], None)
        
        self.fog = pygame.Surface( (30,30) )
        
        self.fog.fill( black )
        
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
    
    def getImages(self):
        return self.images
    
    def loadMap(self):
        save = open("map.dat", "r")
        grid = pickle.load(save)
        save.close()
        self.maptext = grid
    
    def getGrid(self):
        return self.maptext
    
    # returns distance between two points
    def distanceFunc(self, pos1, pos2):
        (x1,y1) = pos1
        (x2,y2) = pos2
        return max( abs(y2-y1), abs(x2-x1) )
    
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
    def redraw(self, heroLoc, heroRect, gameBoard):
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
        (rx, ry, r2x, r2y) = heroRect
        rx = rx/blocksize
        ry = ry/blocksize
        for x in range(HALFDIM):
            for y in range(HALFDIM):
                tile = self.getUnit(x+topX,y+topY)
                if tile < 10:
                    self.image = self.images[tile]
                    gameBoard.blit(self.image, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )
                    dist = self.distanceFunc( (x,y), (rx,ry) )
                    if dist == 1:
                        self.fog.set_alpha( 0 )
                        gameBoard.blit(self.fog, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )
                    elif dist == 2:
                        self.fog.set_alpha( 70 )
                        gameBoard.blit(self.fog, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )
                    elif dist == 3:
                        self.fog.set_alpha( 140 )
                        gameBoard.blit(self.fog, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )
                    elif dist >= 4:
                        self.fog.set_alpha( 210 )
                        gameBoard.blit(self.fog, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )
        

    def getItem(self, x, y):
        #updates map with empty space at collected item
        self.maptext[y] = self.maptext[y][:x]+[0]+self.maptext[y][x+1:]
        
    def updateUnit(self, x, y, type):
        #Updates one map unit to type at map coordinates x,y
        self.maptext[y] = self.maptext[y][:x]+[type]+self.maptext[y][x+1:]
    
    def getUnit(self,x,y):
        return self.maptext[y][x]
