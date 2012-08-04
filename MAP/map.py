import pygame, random, pickle, ppov
from load_image import *
from const import *
from UTIL import queue
from types import *

class miniMap():
    def __init__(self, maptext):
        self.maptext = maptext
        self.mapColors = [black,brickred,yellow,grey,red,white,brown,green,dkgreen,blue,ltgrey]
                
        self.colorDict = {-1:0, 0:0, 3:3, 4:3, 5:4, 6:4, 7:4, 8:10, 9:6, 10:5, 11:5, 12:7, 13:7, 
                          16:6, 20:10, 21:10, 22:10, 23:10, 24:1, 25:1, 28:3, 29:10, 32:3, 33:3, 34:3, 35:3, 36:3, 37:3, 41:1,
                          42:5, 42:5, 43:5, 44:5, 45:5, 46:5, 47:5, 48:1, 49:1, 50:1, 51:8, 52:8, 53:8, 55:3, 59:1, 60:8, 61:3, 62:3, 63:1, 64:5, 
                          65:9, 66:9, 67:9, 68:9, 69:9, 70:9, 72:5, 73:5, 92:4, 95:4, 98:2, 99:6, 
                          100:6, 110:6, 111:6, 112:3, 116:3, 117:3, 118:3, 120:3, 121:3, 126:0, 127:5}
    
    def getEntry(self, x, y):
        if x in range( len(self.maptext) ) and y in range( len(self.maptext) ):
            return self.maptext[y][x]
        else: return -1
    
    def isMapped(self, coord):
        try:
            return self.visDict[coord]
        except KeyError:
            return False
    
    def drawMiniMap(self,screen, topCorner, playerXY, visDict):
        miniMapBoard = pygame.Surface( [300,300] )
        miniMapBoard.fill(black)
        self.visDict = visDict
        if len(self.maptext) <= DIM:
            topCorner = (0,0)
        (tx, ty) = topCorner
        (px, py) = playerXY
        tx = px - HALFDIM
        ty = py - HALFDIM
        for i in range(DIM):
            for j in range(DIM):
                mapColorBlock = pygame.Surface( (miniblocksize,miniblocksize) )
                if (i+tx,j+ty) == playerXY:
                    mapColorBlock.fill( self.mapColors[5] )
                    miniMapBoard.blit( mapColorBlock, ( i*miniblocksize, j*miniblocksize) )
                elif self.isMapped( (i+tx,j+ty) ):
                    mapColorBlock.fill( self.mapColors[self.colorDict[self.getEntry(i+tx,j+ty)]] )
                    miniMapBoard.blit( mapColorBlock, ( i*miniblocksize, j*miniblocksize) )
        screen.blit(miniMapBoard, (75,75) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass

class map():
    def __init__(self, filename=None, mapball = None, level=0, type='dungeon'):
        self.maptext = []
        self.level = level
        self.lineOfVision = 0
        if filename != None:
            self.loadMap(filename)
        self.BFSQueue = queue.Queue()
        
        if mapball != None:
            self.installBall(mapball)
        
        self.playerXY = self.startXY
        self.type = type
                
        self.topMapCorner = (0,0)
        self.DIM = len(self.maptext)
        self.visDict = {}
        for i in range( self.DIM ):
            for j in range( self.DIM ):
                if self.type == 'dungeon': self.visDict[ (i,j) ] = False
                else: self.visDict[ (i,j) ] = True
        self.myMiniMap = miniMap(self.maptext)
    
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
        self.startXY = hs
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
    def getPOE(self):
        return self.pointOfEntry
    def getPOEx(self):
        return self.pointOfExit
    def getType(self):
        return self.type
    
    def callDrawMiniMap(self, screen):
        self.myMiniMap.drawMiniMap(screen, self.topMapCorner, self.playerXY, self.visDict)
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
    def revealMap(self):
        litTiles = self.getLitTiles()
        self.litTiles = litTiles
        if litTiles == None: return
        for tile in litTiles:
            self.visDict[ tile ] = True
        return
    
    def flatten(self, x):
        result = []
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, basestring) and type(el) is not TupleType and type(el) is not NoneType:
                result.extend(self.flatten(el))
            elif type(el) is TupleType:
                result.append(el)
        return result
    
    #@tail_call_optimized
    def litBFS(self,start):
        (x,y) = start
        if self.getUnit(x,y) in range(24,86):
            return (x,y)
        entryList = []
        for (Cx,Cy) in CARDINALS:
            if (x+Cx,y+Cy) not in self.visited and ~self.BFSQueue.has( (x+Cy, y+Cy) ):
                self.BFSQueue.push( (x+Cx, y+Cy) )
                entryList += [ (x+Cx,y+Cy) ]
                self.visited += [ (x+Cx,y+Cy) ]
        if len( entryList ) <= 1:
            return (x,y)
        else:
            returnList = []
            for i in range( len( entryList ) ): 
                returnList += [ self.litBFS(self.BFSQueue.pop()) ]
            return [ (x,y) ] + returnList
    
    def getLitTiles(self):
        (px, py) = self.playerXY
        self.BFSQueue.reset()
        self.visited = []
        litTiles = self.flatten( self.litBFS( (px,py) ) )
        litTiles = list( set( litTiles) )
        return litTiles
    
