import pygame, random, pickle, ppov
from load_image import *
from UTIL import queue, const, colors
from types import *
from MAP import tile

class miniMap():
    def __init__(self, grid):
        self.grid = grid
        self.mapColors = colors.mapColors
                
        self.colorDict = {-1:0, 0:10, 1:11, 3:3, 4:3, 5:4, 6:4, 7:4, 8:10, 9:6, 10:5, 11:5, 12:7, 13:7, 14:8, 15:8,
                          16:6, 18:-1, 19:11, 20:10, 21:10, 22:10, 23:10, 24:1, 25:1, 27:3, 28:3, 29:10, 
                          30:3, 31:3, 32:3, 33:3, 34:3, 35:3, 36:3, 37:3, 38:6, 40:3, 41:1, 42:5, 42:5, 
                          43:5, 44:5, 45:5, 46:5, 47:5, 48:1, 49:1, 50:1, 51:3, 52:8, 53:8, 55:3, 56:10, 57:11, 
                          58:1, 59:1, 60:8, 61:3, 62:3, 63:1, 64:5, 65:9, 66:9, 67:9, 68:9, 69:9, 70:9, 
                          72:5, 73:5, 74:6, 75:3, 81:3, 92:4, 95:4, 98:2, 99:6, 100:6, 110:6, 111:6, 112:3, 
                          116:3, 117:3, 118:3, 120:3, 121:3, 126:0, 127:5}
    
    def getEntry(self, x, y):
        if x in range( len(self.grid) ) and y in range( len(self.grid) ):
            return self.grid[x][y].getFG()
        else: return -1
    
    def isMapped(self, coord):
        try:
            return self.visDict[coord]
        except KeyError:
            return False
    
    def drawMiniMap(self,screen, topCorner, playerXY, visDict):
        miniMapBoard = pygame.Surface( [300,300] )
        miniMapBoard.fill(colors.black)
        self.visDict = visDict
        if len(self.grid) <= const.DIM:
            topCorner = (0,0)
        (tx, ty) = topCorner
        (px, py) = playerXY
        tx = px - const.HALFDIM
        ty = py - const.HALFDIM
        for i in range(const.DIM):
            for j in range(const.DIM):
                mapColorBlock = pygame.Surface( (const.miniblocksize,const.miniblocksize) )
                if (i+tx,j+ty) == playerXY:
                    mapColorBlock.fill( self.mapColors[5] )
                    miniMapBoard.blit( mapColorBlock, ( i*const.miniblocksize, j*const.miniblocksize) )
                elif self.isMapped( (i+tx,j+ty) ):
                    mapColorBlock.fill( self.mapColors[self.colorDict[self.getEntry(i+tx,j+ty)]] )
                    miniMapBoard.blit( mapColorBlock, ( i*const.miniblocksize, j*const.miniblocksize) )
        screen.blit(miniMapBoard, (75,75) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass

class map():
    def __init__(self, DIM=20, dFG=const.DFLOOR1):
        self.grid = []
        self.DIM = DIM
        self.chests = {}
        self.defaultBkgd = 0
        self.shops = []
        self.NPCs = []
    
    def getDIM(self):
        return self.DIM
    def setEntry(self, x, y, fg):
    #Updates one map Entry to type at map coordinates x,y
        #self.grid[y] = self.grid[y][:x]+[type]+self.grid[y][x+1:]
        self.grid[x][y].setFG(fg)
    def getEntry(self,x,y):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            return self.grid[x][y].getFG()
        else: return const.VOID
    def getTileFG(self, x, y):
        return self.grid[x][y].getFG()
    def setTileFG(self, x, y, fg):
        self.grid[x][y].setFG(fg)
    
    def getGrid(self):
        return self.grid
    def getMapBall(self):
        return (self.grid, self.defaultBkgd, self.pointOfEntry, self.pointOfExit, self.heroStart, self.shops, self.chests, self.NPCs)

    def installBall(self, ball):
        (grid, DBGD, poe, poex, hs, shops, chests, npcs) = ball
        self.grid = grid
        self.DIM = len(grid)
        self.heroStart = hs
        self.pointOfEntry = poe
        self.pointOfExit = poex
        self.chests = chests
        self.shops = shops
        self.defaultBkgd = DBGD
        self.NPCs = npcs
    
    def mapCut(self, pos1, pos2):
        (x1, y1) = pos1
        (x2, y2) = pos2
        return
        grid = [range(x2-x1)]*(y2-y1)
        for i in range(x2-x1):
            for j in range(y2-y1):
                grid[j][i] = self.getEntry(x1+i, y1+j)
                self.setEntry(x1+i, y1+j, 0)
        self.copyText = grid
    
    def mapCopy(self, pos1, pos2):
        (x1, y1) = pos1
        (x2, y2) = pos2
        grid = [range(x2-x1)]*(y2-y1)
        for i in range(x2-x1):
            for j in range(y2-y1):
                grid[j][i] = self.getEntry(x1+i, y1+j)
                self.setEntry(x1+i, y1+j, 0)
        self.copyText = grid
        
    def mapPaste(self, pos):
        (sX, sY) = pos
        copyText = self.copyText
        for i in range( len(copyText[0]) ):
            for j in range( len(copyText) ):
                self.grid[i+sX][j+sY] = copyText[j][i]
                self.grid[i+sX][j+sY].setXY(i+sX, j+sY)


class gameMap(map):
    
    def __init__(self, filename=None, mapball = None, level=0, type='dungeon'):
        map.__init__(self)
        
        self.level = level
        self.lineOfVision = 0
        if filename != None:
            self.loadMap(filename)
        self.BFSQueue = queue.Queue()
        
        if mapball != None:
            self.installBall(mapball)
        
        self.playerXY = self.heroStart
        self.type = type
                
        self.topMapCorner = (0,0)
        self.visDict = {}
        for i in range( self.DIM ):
            for j in range( self.DIM ):
                if self.type == 'dungeon': 
                    self.visDict[ (i,j) ] = False
                    self.grid[i][j].visible = False
                else:
                    self.visDict[ (i,j) ] = True
                    self.grid[i][j].visible = True
        self.myMiniMap = miniMap(self.grid)
        
        self.litTiles = []
    
    def setLOV(self, num):
        self.lineOfVision = num
    
    def saveMap(self):
        grid = self.getGrid()
        save = open("map.dat", "w")
        pickle.dump(grid, save)
        save.close()
    def getImages(self):
        return self.images
    def loadMap(self, filename):
        try:
            save = open(os.getcwd()+'/MAP/LEVELS/'+filename, "r")
            ball = pickle.load(save)
            save.close()
            self.installBall(ball)
        except pygame.error, message:
            print 'Cannot load map:', name
            raise SystemExit, message
        
    def getGrid(self):
        return self.grid
    def getPlayerXY(self):
        return self.playerXY
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
    def neighbors(self, tile):
        returnList = []
        (x,y) = tile
        for (Cx, Cy) in const.CARDINALS:
            returnList.append((Cx+x, Cy+y))
        return returnList
    def getRandomTile(self):
        x = random.randrange(0, self.DIM)
        y = random.randrange(0, self.DIM)
        while ( self.getEntry(x, y) not in range(0, 25) ):
            x = random.randrange(0, self.DIM)
            y = random.randrange(0, self.DIM)
        return x, y
            
    # calculate location of map window based on hero location and hero sprite rect
    def updateWindowCoordinates(self, hero):
        DIMEN = self.getDIM()
        oldX, oldY = self.playerXY
        # Compute top map corner
        (px,py) = hero.getXY()
        px = px/const.blocksize
        py = py/const.blocksize
        self.playerXY = (px, py)
        
        if DIMEN <= const.HALFDIM:
            topX = 0
            topY = 0
            self.WINDOWOFFSET = (const.HALFDIM - DIMEN)/2
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
            self.WINDOWSIZE = const.HALFDIM
            self.WINDOWOFFSET = 0
        oldTopX, oldTopY = self.topMapCorner
        self.topMapCorner = (topX, topY)
        return (topX, topY), (oldTopX, oldTopY)
    
    # complete list of tiles is in tiles1.txt
    def revealMap(self):
        if self.type == 'dungeon':
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
        if self.getEntry(x,y) in range(24,86):
            returnList = [(x,y)]
            for (Cx, Cy) in const.CARDINALS:
                if self.getEntry(x+Cx,y+Cy) in range(24, 86):
                    count = 0
                    for (Nx, Ny) in const.CARDINALS:
                        if self.visDict[ (x+Cx+Nx, y+Cy+Ny) ]:
                            count += 1
                    if count >= 2:
                        returnList.append((x+Cx,y+Cy))
            return returnList
        entryList = []
        for (Cx,Cy) in const.CARDINALS:
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
        self.litTiles = litTiles
        return litTiles
    
    def isVisible(self, x, y):
        if (x, y) in self.litTiles:
            return True
        else: return False

# inherited map class to be used by map generator
class edMap(map):
    def __init__(self):
        map.__init__(self, 2*const.DIM)
        self.defaultBkgd = const.DFLOOR1
        for i in range(self.DIM):
            self.grid += [range(self.DIM)]
            for j in range(self.DIM):
                self.grid[i][j] = tile.Tile(i, j, const.DFLOOR1, self.defaultBkgd)
        self.heroStart = None
        self.pointOfEntry = None
        self.pointOfExit = None
        
        self.itemShop = None
        self.magicShop = None
        self.Armory = None
        self.Blacksmith = None
        self.Tavern = None
        
        self.portals = []
        # location : (type, level)
        self.shops = {}
    
    def addChest(self, loc, chest):
        self.chests[loc] = chest
    
    # overridden from parent class
    def setEntry(self, x, y, e, level=None):
        if e == const.HEROSTART:
            if self.heroStart == None:
                self.heroStart = (x,y)
            else:
                (px,py) = self.heroStart
                self.setEntry(px,py,self.defaultBkgd)
                self.heroStart = (x,y)
                return
        if e == const.STAIRUP:
            if self.pointOfEntry == None:
                self.pointOfEntry = (x,y)
            else:
                (px,py) = self.pointOfEntry
                self.setEntry(px,py,self.defaultBkgd)
                self.pointOfEntry = (x,y)
        if e == const.STAIRDN:
            if self.pointOfExit == None:
                self.pointOfExit = (x,y)
            else:
                (px,py) = self.pointOfExit
                self.setEntry(px,py,self.defaultBkgd)
                self.pointOfExit = (x,y)
        if e == const.ITEMSDOOR:
            if self.itemShop == None:
                self.itemShop = (x, y)
                self.shops[(x,y)] = ('itemshop', level )
            else:
                (px, py) = self.itemShop
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px,py))
                self.shops[(x,y)] = ('itemshop', level )
                self.itemShop = (x, y)
        if e == const.ARMRYDOOR:
            if self.Armory == None:
                self.Armory = (x, y)
                self.shops[(x,y)] = ( 'armory', level )
            else:
                (px, py) = self.Armory
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px,py))
                self.shops[(x,y)] = ('armory', level )
                self.Armory = (x, y)
        if e == const.BLKSMDOOR:
            if self.Blacksmith == None:
                self.Blacksmith = (x, y)
                self.shops[(x,y)] = ( 'blacksmith', level )
            else:
                (px, py) = self.Blacksmith
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px,py))
                self.shops[(x,y)] = ( 'blacksmith', level )
                self.Blacksmith = (x, y)
        if e == const.MAGICDOOR:
            if self.magicShop == None:
                self.magicShop = (x, y)
                self.shops[(x,y)] = ( 'magicshop', level )
            else:
                (px, py) = self.magicShop
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px,py))
                self.shops[(x,y)] = ( 'magicshop', level )
                self.magicShop = (x, y)
        if e == const.TAVRNDOOR:
            if self.Tavern == None:
                self.Tavern = (x, y)
                self.shops[(x,y)] = ( 'tavern', level )
            else:
                (px, py) = self.Tavern
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px,py))
                self.shops[(x,y)] = ( 'tavern', level )
                self.Tavern = (x, y)
        self.grid[x][y].setFG(e)
    def changeDimensions(self, nDim):
        newGrid = [[0 for i in range(nDim)] for j in range(nDim)]
        # expanding
        if nDim > self.DIM:
            for i in range(nDim):
                if i < self.DIM:
                    for j in range(nDim):
                        if j < self.DIM:
                            newGrid[i][j] = self.grid[i][j]
                        else: newGrid[i][j] = tile.Tile(i, j, const.DFLOOR1, self.defaultBkgd)
                else:
                    for j in range(nDim):
                        newGrid[i][j] = tile.Tile(i, j, const.DFLOOR1, self.defaultBkgd)
            self.grid = newGrid
        #shrinking
        elif self.DIM > nDim:
            self.grid = self.grid[:nDim]
            for i in range(nDim):
                self.grid[i] = self.grid[i][:nDim]
        #same
        else: return
        self.DIM = nDim
        self.cursorPos = (0,0)
    
    def mapMove(self, source, size, dest):
        (sX, sY) = source
        (dX, dY) = dest
        (xDim, yDim) = size
        tmpGrid = [range(xDim) for _ in range(yDim)]
        for i in range(xDim):
            for j in range(yDim):
                tmpGrid[j][i] = self.getEntry(i+sX, j+sY)
        for i in range(xDim):
            for j in range(yDim):
                self.setEntry(i+sX, j+sY, 0)
        for i in range(xDim):
            for j in range(yDim):
                self.setEntry(i+dX, j+dY, tmpGrid[j][i])
    
    def mapErase(self):
        pass

# inherited map class to be used by map generator
class genMap(map):
    
    def __init__(self, DIM, level ):
        map.__init__(self, DIM, const.VOID)
        self.level = level
        for i in range(self.DIM):
            self.grid += [range(self.DIM)]
            for j in range(self.DIM):
                self.grid[i][j] = tile.Tile(i, j, const.VOID, const.VOID)