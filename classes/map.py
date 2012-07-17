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
        
        self.colorDict = {-1:0, 0:0, 3:3, 4:3, 5:4, 6:4, 7:4, 8:3, 9:6, 10:5, 11:5, 12:7, 13:7, 16:6, 24:1, 25:1, 29:10,
                          42:5, 42:5, 43:5, 44:5, 45:5, 46:5, 47:5, 48:1, 49:1, 50:1, 51:8, 52:8, 53:8, 55:3, 64:5, 
                          65:9, 66:9, 67:9, 68:9, 69:9, 70:9, 72:5, 73:5, 92:4, 95:4, 98:2, 99:6, 
                          100:6, 110:6, 111:6, 116:3, 120:3, 121:3, 126:0, 127:5}
    
    def getEntry(self, x, y):
        if x in range( len(self.maptext) ) and y in range( len(self.maptext) ):
            return self.maptext[y][x]
        else: return -1
    
    def drawMiniMap(self,screen, topCorner):
        (tx, ty) = topCorner
        for i in range(DIM):
            for j in range(DIM):
                self.miniMapBoard.blit( self.mapColorBlocks[ self.colorDict[self.getEntry(i+tx,j+ty)] ], ( i*miniblocksize, j*miniblocksize) )
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
        
        self.DIM = len(self.maptext)
        print self.DIM
    
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
        self.myMiniMap.drawMiniMap(screen, self.topMapCorner)
    
    def getPOE(self):
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
        DIMEN = self.getDIM()
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
        
        if DIMEN <= HALFDIM:
            topX = 0
            topY = 0
            WINDOWOFFSET = (HALFDIM - DIMEN)/2
            WINDOWSIZE = DIMEN
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
            WINDOWSIZE = HALFDIM
            WINDOWOFFSET = 0
        #Redraw map on screen from current map matrix
        self.topMapCorner = (topX, topY)
        (rx, ry, r2x, r2y) = heroRect
        rx = rx/blocksize
        ry = ry/blocksize
        for x in range(WINDOWSIZE):
            for y in range(WINDOWSIZE):
                tile = self.getUnit(x+topX,y+topY)
                if tile != HEROSTART and tile != VOID:
                    self.image = self.images[tile]
                    gameBoard.blit(self.image, ( (x+WINDOWOFFSET)*blocksize, (y+WINDOWOFFSET)*blocksize), area=(0,0,blocksize,blocksize) )
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
    
