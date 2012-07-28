import pygame, random, pickle
from load_image import *
from const import *
from IMG import images

class miniMap():
    def __init__(self, maptext):
        self.maptext = maptext
        
        self.mapColors = [black,brickred,yellow,grey,red,white,brown,green,dkgreen,blue,ltgrey]
        
        self.mapColorBlocks = range(11)
        
        for i in range(11):
            self.mapColorBlocks[i] = pygame.Surface( (miniblocksize,miniblocksize) )
            self.mapColorBlocks[i].fill( self.mapColors[i] )
        
        self.miniMapBoard = pygame.Surface( [300,300] )
        self.miniMapBoard.fill( black )
        
        self.colorDict = {-1:0, 0:0, 3:3, 4:3, 5:4, 6:4, 7:4, 8:10, 9:6, 10:5, 11:5, 12:7, 13:7, 
                          16:6, 20:10, 21:10, 22:10, 23:10, 24:1, 25:1, 28:3, 29:10, 32:3, 33:3, 34:3, 35:3, 36:3, 37:3, 41:1,
                          42:5, 42:5, 43:5, 44:5, 45:5, 46:5, 47:5, 48:1, 49:1, 50:1, 51:8, 52:8, 53:8, 55:3, 59:1, 60:8, 61:3, 62:3, 63:1, 64:5, 
                          65:9, 66:9, 67:9, 68:9, 69:9, 70:9, 72:5, 73:5, 92:4, 95:4, 98:2, 99:6, 
                          100:6, 110:6, 111:6, 112:3, 116:3, 117:3, 118:3, 120:3, 121:3, 126:0, 127:5}
    
    def getEntry(self, x, y):
        if x in range( len(self.maptext) ) and y in range( len(self.maptext) ):
            return self.maptext[y][x]
        else: return -1
    
    def drawMiniMap(self,screen, topCorner, playerXY):
        if len(self.maptext) <= DIM:
            topCorner = (0,0)
        (tx, ty) = topCorner
        (px, py) = playerXY
        tx = px - HALFDIM
        ty = py - HALFDIM
        for i in range(DIM):
            for j in range(DIM):
                if (i+tx,j+ty) == playerXY:
                    self.miniMapBoard.blit( self.mapColorBlocks[ 5 ], ( i*miniblocksize, j*miniblocksize) )
                else: self.miniMapBoard.blit( self.mapColorBlocks[ self.colorDict[self.getEntry(i+tx,j+ty)] ], ( i*miniblocksize, j*miniblocksize) )
        screen.blit(self.miniMapBoard, (75,75) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass

class map():
    def __init__(self, filename=None, mapball = None, level=0):
        images.load()
        self.maptext = []
        self.level = level
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
        
        self.DIM = len(self.maptext)
        
        self.xGameBoard = pygame.Surface( (self.DIM*blocksize, self.DIM*blocksize) )
        
        self.redrawXMap()
    
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
        (grid, poe, poex, hs, chests) = ball
        self.maptext = grid
        self.heroStart = hs
        self.startXY = poe
        self.pointOfEntry = poe
        self.pointOfExit = poex
        self.chests = chests
    
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
    
    def getDIM(self):
        return self.DIM
    
    def updateUnit(self, x, y, type):
        #Updates one map unit to type at map coordinates x,y
        self.maptext[y] = self.maptext[y][:x]+[type]+self.maptext[y][x+1:]
    
    def getUnit(self,x,y):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            return self.maptext[y][x]
        else: return 126
    
    def getStartXY(self):
        return self.startXY
    
    def callDrawMiniMap(self, screen):
        self.myMiniMap.drawMiniMap(screen, self.topMapCorner, self.playerXY)
    
    def getPOE(self):
        return self.pointOfEntry
    
    def getPOEx(self):
        return self.pointOfExit
    
    # returns distance between two points
    def distanceFunc(self, pos1, pos2):
        (x1,y1) = pos1
        (x2,y2) = pos2
        return max(abs(y2-y1), abs(x2-x1), abs(y2-y1) + abs(x2-x1))
    
    # calculate location of map window based on hero location and hero sprite rect
    def updateWindowCoordinates(self, heroLoc, heroRect):
        DIMEN = self.getDIM()
        oldX, oldY = self.playerXY
        # Compute top map corner
        (px,py) = heroLoc
        px = px/blocksize
        py = py/blocksize
        self.playerXY = (px, py)
        
        if DIMEN <= HALFDIM:
            topX = 0
            topY = 0
            self.WINDOWOFFSET = (HALFDIM - DIMEN)/2
            self.WINDOWSIZE = DIMEN
        else:
            if px < 5:
                topX = 0
            elif 5 <= px <= DIMEN - 5:
                topX = px - 5
            else:
                topX = DIMEN - 10
            
            if py < 5:
                topY = 0
            elif 5 <= py <= DIMEN - 5:
                topY = py - 5
            else:
                topY = DIMEN - 10
            self.WINDOWSIZE = HALFDIM
            self.WINDOWOFFSET = 0
        oldTopX, oldTopY = self.topMapCorner
        self.topMapCorner = (topX, topY)
        return (topX, topY), (oldTopX, oldTopY)
    
    # complete list of tiles is in tiles1.txt
    
    # takes map coordinates, returns map window
    def getMapWindow(self, pos, wsize=10):
        (x1, y1) = pos
        window = pygame.Surface( (wsize*blocksize, wsize*blocksize) )
        window.blit( self.xGameBoard, ( -(x1*blocksize), -(y1*blocksize) ) )
        return window
    
    # takes pixel coordinates of top left corner of DIMxDIM window of xGameBoard, returns map window
    def getScrollingMapWindow(self, pos, wsize = 10, darkness=True):
        (x1,y1) = pos
        window = pygame.Surface( (wsize*blocksize, wsize*blocksize) )
        window.blit( self.xGameBoard, ( -x1, -y1 ) )
        #self.drawDarkness
        return window
    
    # draws entire map to DIMxDIM Surface
    def redrawXMap(self):
        for x in range(self.getDIM()):
            for y in range(self.getDIM()):
                tile = self.getUnit(x,y)
                if tile != VOID:
                    self.xGameBoard.blit( self.images[ tile ], ( (x*blocksize), (y*blocksize) ) )
    
    def scroll(self,x,y):
        self.xGameBoard.scroll(x,y)
    
    # Takes first two coordinates of hero rect, gameBoard and
    # draws darkness
    def drawDarkness(self, rx, ry, gameBoard):
        for x in range(self.WINDOWSIZE):
            for y in range(self.WINDOWSIZE):
                dist = self.distanceFunc( (x,y), (rx,ry) )
                if dist <= self.lineOfVision + 2:
                    self.fog.set_alpha( 0 )
                elif dist == self.lineOfVision + 3:
                    self.fog.set_alpha( 70 )
                elif dist == self.lineOfVision + 4:
                    self.fog.set_alpha( 140 )
                elif dist >= self.lineOfVision + 5:
                    self.fog.set_alpha( 210 )
                gameBoard.blit(self.fog, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )
    
    def redraw(self, heroLoc, heroRect, gameBoard):
        # Redraw map on screen from current map matrix
        (rx,ry,rx2,ry2) = heroRect
        rx = rx/blocksize
        ry = ry/blocksize
        (topX, topY), (oldTopX, oldTopY) = self.updateWindowCoordinates(heroLoc, heroRect)
        gameBoard.blit( self.getMapWindow( (topX, topY), self.WINDOWSIZE ), (self.WINDOWOFFSET,self.WINDOWOFFSET) )
        if self.level >= 1:
            self.drawDarkness(rx, ry, gameBoard)
    
