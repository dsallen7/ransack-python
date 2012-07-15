import pygame, random, pickle
from load_image import *
from const import *
from IMG import images

class miniMap():
    def __init__(self, maptext):
        self.maptext = maptext
        
        self.mapColors = [black,brickred,yellow,grey,red,white,brown,green,dkgreen]
        
        self.mapColorBlocks = range(9)
        
        for i in range(9):
            self.mapColorBlocks[i] = pygame.Surface( (miniblocksize,miniblocksize) )
            self.mapColorBlocks[i].fill( self.mapColors[i] )
        
        self.miniMapBoard = pygame.Surface( [300,300] )
        self.miniMapBoard.fill( black )
        
        self.colorDict = {0:0, 3:3, 4:3, 5:4, 6:4, 7:4, 8:3, 9:6, 10:5, 11:5, 12:7, 24:1, 25:1,
                          42:5, 42:5, 43:5, 44:5, 45:5, 46:5, 47:5, 48:1, 49:1, 50:1, 51:8, 52:8, 53:8, 55:3, 64:5, 92:4, 95:4, 98:2, 99:6, 
                          100:6, 116:3, 120:3, 121:3, 126:0, 127:5}
    
    def getEntry(self, x, y):
        return self.maptext[y][x]
    
    def drawMiniMap(self,screen):
        for i in range(DIM):
            for j in range(DIM):
                self.miniMapBoard.blit( self.mapColorBlocks[ self.colorDict[self.getEntry(i,j)] ], (i*miniblocksize, j*miniblocksize) )
        screen.blit(self.miniMapBoard, (75,75) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass

class map():
    def __init__(self, filename=None, mapball = None):
        images.load()
        self.maptext = []
        self.lineOfVision = 0
        if filename != None:
            self.loadMap(filename)
        
        if mapball != None:
            self.installBall(mapball)
        
        self.playerXY = self.startXY
        
        self.fog = pygame.Surface( (30,30) )
        self.fog.fill( black )
                
        self.topMapCorner = (0,0)
        
        self.myMiniMap = miniMap(self.maptext)
        
        self.images = images.mapImages
    
    def setLOV(self, num):
        self.lineOfVision = num
    
    def saveMap(self):
        grid = self.getGrid()
        save = open("map.dat", "w")
        pickle.dump(grid, save)
        save.close()
    
    def getImages(self):
        return self.images
    
    def installBall(self, ball):
        (grid, poe, poex, hs) = ball
        self.maptext = grid
        self.heroStart = hs
        self.startXY = poe
        self.pointOfEntry = poe
        self.pointOfExit = poex
    
    def loadMap(self, filename):
        try:
            save = open(filename, "r")
            ball = pickle.load(save)
            save.close()
            self.installBall(ball)
        except pygame.error, message:
            print 'Cannot load map:', name
            raise SystemExit, message
    
    def getGrid(self):
        return self.maptext
    
    def updateUnit(self, x, y, type):
        #Updates one map unit to type at map coordinates x,y
        self.maptext[y] = self.maptext[y][:x]+[type]+self.maptext[y][x+1:]
    
    def getUnit(self,x,y):
        if 0 <= x < DIM and 0 <= y < DIM:
            return self.maptext[y][x]
        else: return -1
    
    def getStartXY(self):
        return self.startXY
    
    def callDrawMiniMap(self, screen):
        self.myMiniMap.drawMiniMap(screen)
    
    def getPOE(self):
        print self.pointOfEntry
        return self.pointOfEntry
    
    def getPOEx(self):
        return self.pointOfExit
    
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
    # 4 : stairs up
    # 5 : stairs down
    # 6 : fruit
    # 7 : h potion
    # 8 : m potion
    # 9 : spellbook
    # 10 : chest 
    # ...
    # 64 : 

    def redraw(self, heroLoc, heroRect, gameBoard):
        oldX, oldY = self.playerXY
        #self.updateUnit(oldX,oldY,0)
        # Compute top map corner
        (px,py) = heroLoc
        px = px/blocksize
        py = py/blocksize
        #Erase old player
        self.playerXY = (px, py)
        #self.updateUnit(px,py,10)
        
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
                if tile != HEROSTART and tile != VOID:
                    self.image = self.images[tile]
                    gameBoard.blit(self.image, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )
                    dist = self.distanceFunc( (x,y), (rx,ry) )
                    if dist <= self.lineOfVision + 1:
                        self.fog.set_alpha( 0 )
                    elif dist == self.lineOfVision + 2:
                        self.fog.set_alpha( 70 )
                    elif dist == self.lineOfVision + 3:
                        self.fog.set_alpha( 140 )
                    elif dist >= self.lineOfVision + 4:
                        self.fog.set_alpha( 210 )
                    gameBoard.blit(self.fog, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )
    
