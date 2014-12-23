import pygame, random, cPickle, ppov, gzip, os
from UTIL import queue, const, colors, load_image, misc
from types import *
from MAP import tile, minimap, submap, ppov as PPOV

from math import sqrt

from SCRIPTS import enemyScr

class generalmap():
    def __init__(self, DIM=const.DIM, dFG=const.DFLOOR1):
        self.grid = []
        self.DIM = DIM
        self.chests = {}
        self.defaultBkgd = 0
        self.shops = []
        self.NPCs = []
        self.neighbors = [ 
                            '', # North
                            '', # South
                            '', # East
                            ''  # West
        ]
        self.up = ('',)
        self.down = ('',)
        self.type = ''
        self.visDict = {}
    
    def getDIM(self):
        return self.DIM
    def setEntry(self, x, y, fg):
    #Updates one map Entry to type at map coordinates x,y
        self.grid[x][y].setFG(fg)
    def getEntry(self,x,y):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            if self.grid[x][y] is not None:
                return self.grid[x][y].getFG()
            else: return const.VOID
        else: return const.VOID
        
    def getEntrySingle(self, pos):
        (x,y) = pos
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            if self.grid[x][y] is not None:
                return self.grid[x][y].getFG()
            else: return const.VOID
        else: return const.VOID
        
    def getTileFG(self, x, y):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            if self.grid[x][y] is not None:
                return self.grid[x][y].getFG()
            else: return const.VOID
        else: return const.VOID
    def setTileFG(self, x, y, fg):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            if self.grid[x][y] is not None:
                self.grid[x][y].setFG(fg)
        
    def getTileBG(self, x, y):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            if self.grid[x][y] is not None:
                return self.grid[x][y].getBG()
            else: return const.VOID
        else: return const.VOID
    def setTileBG(self, x, y, bg):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            if self.grid[x][y] is not None:
                self.grid[x][y].setBG(bg)
    
    def getName(self):
        return self.name[0]

    def setName(self, name):
        self.name = (name,)
    
    
    def cardinalNeighbors(self, tile):
        returnList = []
        (x,y) = tile
        for (Cx, Cy) in const.CARDINALS:
            returnList.append( self.getTileFG(Cx+x, Cy+y) )
        return returnList
    def cardinalNeighborsByCoords(self, tile):
        returnList = []
        (x,y) = tile
        for (Cx, Cy) in const.CARDINALS:
            returnList.append( (Cx+x, Cy+y) )
        return returnList
    
    def allNeighbors(self, tile):
        returnList = []
        (x,y) = tile
        for (Cx, Cy) in const.ALLNBRS:
            returnList.append( self.getTileFG(Cx+x, Cy+y) )
        return returnList
    
    def getGrid(self):
        return self.grid

    def getMapBall(self):
        for x in range( self.getDIM() ):
            for y in range( self.getDIM() ):
                if self.getEntry(x, y) == const.VOID:
                    if y + 1 == self.getDIM():
                        self.grid[x] = self.grid[x][:y] + [ None ]
                    else: self.grid[x] = self.grid[x][:y] + [ None ] + self.grid[x][y+1:]
        return (self.grid,
                self.defaultBkgd,
                self.pointOfEntry,
                self.pointOfExit,
                self.heroStart,
                self.shops,
                self.chests,
                self.NPCs,
                self.neighbors,
                self.up,
                self.down,
                self.name,
                self.type,
                self.level,
                self.visDict)

    def installBall(self, ball):
        (grid, DBGD, poe, poex, hs, shops, chests, npcs, nbrs, up, dn, nm, tp, lv, vd) = ball
        self.grid = grid
        self.DIM = len(grid)
        self.heroStart = hs
        self.pointOfEntry = poe
        self.pointOfExit = poex
        self.chests = chests
        self.shops = shops
        self.defaultBkgd = DBGD
        self.NPCs = npcs
        self.neighbors = nbrs
        self.up = up
        self.down = dn
        self.name = nm
        self.type = tp
        self.level = lv
        self.visDict = vd
            
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
                #self.setEntry(x1+i, y1+j, 0)
        self.copyText = grid
        
    def mapPaste(self, pos):
        copyText = self.copyText
        for i in range( len(copyText[0]) ):
            for j in range( len(copyText) ):
                self.grid[i+sX][j+sY] = copyText[j][i]
                self.grid[i+sX][j+sY].setXY(i+sX, j+sY)


class gameMap(generalmap):
    def __init__(self, mapball = None, level=0):
        generalmap.__init__(self)
        
        self.level = level
        self.BFSQueue = queue.Queue()
        
        self.newNPCs = []
        
        if mapball is not None:
            self.installBall(mapball)
        
        for i in range( self.DIM ):
            for j in range( self.DIM ):
                if self.grid[i][j] is not None:
                    if self.type in const.darkMaps:
                        if (i,j) not in self.visDict:
                            self.visDict[ (i,j) ] = False
                            self.grid[i][j].visible = False
                    else:
                        self.visDict[ (i,j) ] = True
                        self.grid[i][j].visible = True
        
        if self.heroStart is not None:
            self.playerXY = self.heroStart
        else: self.playerXY = self.getPOE()
                
        self.topMapCorner = (0,0)

        self.myMiniMap = minimap.miniMap(self.grid)
        
        self.litTiles = []
    
    def addMonster(self):
        (x,y) = self.getRandomTile(True)
        if self.type in ['dungeon','maze']:
            newEnemy = random.choice( enemyScr.enemiesByDungeonLevel[self.level] )
        elif self.type == 'wilds': newEnemy = random.choice( enemyScr.enemiesByWildsLevel[self.level] )
        self.newNPCs.append( ( (x,y),  newEnemy, '') )
    
    # used for performing tasks like adding monsters to map, etc
    
    def update(self, npcCount):
        if self.type in ['dungeon', 'wilds', 'maze']:
            if npcCount < 5:
                self.addMonster()
                return 'newNPCs'
        else: return None
    
    def getImages(self):
        return self.images
    def loadMap(self, filename):
        try:
            save = gzip.GzipFile(os.getcwd()+'/MAP/LEVELS/'+filename, "rb")
            ball = cPickle.load(save)
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
    def callDrawMiniMap(self, screen, iH):
        self.myMiniMap.callMiniMap(screen, self.playerXY, self.visDict, iH)
    # returns distance between two points
    def distanceFunc(self, pos1, pos2):
        (x1,y1) = pos1
        (x2,y2) = pos2
        return int( sqrt( (x2-x1)**2 + (y2-y1)**2 ) )
        #return max(abs(y2-y1), abs(x2-x1), abs(y2-y1) + abs(x2-x1))
    
    def getRandomTile(self, offscreen=False):
        x = random.randrange(0, self.DIM)
        y = random.randrange(0, self.DIM)
        if offscreen:
            while ( self.getEntry(x, y) not in range(0, 25) ) or self.isOccupied(x, y) or self.distanceFunc( (x,y), self.playerXY) < 10:
                x = random.randrange(0, self.DIM)
                y = random.randrange(0, self.DIM)
            return x, y
        else:
            while (self.getEntry(x, y) not in range(0, 25)) or self.isOccupied(x, y):
                x = random.randrange(0, self.DIM)
                y = random.randrange(0, self.DIM)
            return x, y
    def setPlayerXY(self, x, y):
        self.playerXY = (x,y)
            
    # calculate location of map window based on hero location and hero sprite rect
    def updateWindowCoordinates(self, hero):
        DIMEN = self.getDIM()
        oldX, oldY = self.getPlayerXY()
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
        self.oldTopMapCorner = self.topMapCorner
        oldTopX, oldTopY = self.topMapCorner # old top map corner
        self.topMapCorner = (topX, topY)     # new top map corner
        return (topX, topY), (oldTopX, oldTopY)
    
    # complete list of tiles is in tiles1.txt
    def revealMap(self, light):
        if self.type in const.darkMaps:
            litTiles = self.getLitTiles(light)
            self.litTiles = litTiles
            if litTiles == None: return
            for tile in litTiles:
                self.visDict[ tile ] = True
        return
    
    def minBFS(self,start, d=0):
        (x,y) = start
        if d == 3:
            return (x, y)
        entryList = []
        if self.getEntry(x, y) in const.SOLIDS:
            (px, py) = self.playerXY
            if (x, y) in [ (px-1,py-1), (px,py-1), (px+1,py-1),
                     (px-1,py), (px,py), (px+1,py),
                     (px-1,py+1), (px,py+1), (px+1,py+1)]:
                self.visited += [ (x, y) ]
                return (x, y)
            else:
                self.visited += [ (x, y) ]
                return []
        for (Cx,Cy) in const.CARDINALS:
            if (x+Cx,y+Cy) not in self.visited and ~self.BFSQueue.has( (x+Cy, y+Cy)  ):
                self.BFSQueue.push( (x+Cx, y+Cy) )
                entryList += [ (x+Cx,y+Cy) ]
                self.visited += [ (x+Cx,y+Cy) ]
        if len( entryList ) < 1:
            return (x,y)
        else:
            returnList = []
            for i in range( len( entryList ) ): 
                returnList += [ self.minBFS(self.BFSQueue.pop(), d+1) ]
            return [ (x,y) ] + returnList
    
    #gets list of tiles 'visible' from current player pos
    def litBFS(self,start, d=0):
        (x,y) = start
        if self.type in ['cave']:
            return [ (x-1,y-1), (x,y-1), (x+1,y-1),
                     (x-1,y), (x,y), (x+1,y),
                     (x-1,y+1), (x,y+1), (x+1,y+1)]
        if self.type in ['maze']:
            if d > 2:
                return start
        elif d > 5:
            return start
        (x,y) = start
        # if standing in doorway, return 8-tile section around door
        if self.getEntry(x,y) in [const.EWDOORO, const.NSDOORO]:
            return [ (x-1,y-1), (x,y-1), (x+1,y-1),
                     (x-1,y), (x,y), (x+1,y),
                     (x-1,y+1), (x,y+1), (x+1,y+1)]
        if self.getEntry(x,y) in range(128, 192): # dungeon solids
            returnList = [(x,y)]
            for (Cx, Cy) in const.CARDINALS:
                if self.getEntry(x+Cx,y+Cy) in range(128, 192):
                    count = 0
                    for (Nx, Ny) in const.CARDINALS:
                        try:
                            if self.visDict[ (x+Cx+Nx, y+Cy+Ny) ]:
                                count += 1
                        except KeyError:
                            pass
                    if count >= 2:
                        returnList.append((x+Cx,y+Cy))
            return returnList
        entryList = []
        for (Cx,Cy) in const.CARDINALS:
            if (x+Cx,y+Cy) not in self.visited and ~self.BFSQueue.has( (x+Cy, y+Cy) and self.getEntry(x+Cx,y+Cy) in range(18) ):
                self.BFSQueue.push( (x+Cx, y+Cy) )
                entryList += [ (x+Cx,y+Cy) ]
                self.visited += [ (x+Cx,y+Cy) ]
        if len( entryList ) < 1:
            return (x,y)
        else:
            returnList = []
            for i in range( len( entryList ) ): 
                returnList += [ self.litBFS(self.BFSQueue.pop(), d+1) ]
            return [ (x,y) ] + returnList
    
    def getLitTiles(self, l):
        (px, py) = self.playerXY
        self.BFSQueue.reset()
        self.visited = []
        if self.type == 'cave':
            self.getPPOV(px, py, l)
            #litTiles = misc.flatten( self.minBFS( (px,py) ) )
            return self.visited
        else:
            self.getPPOV(px, py, l)
            #litTiles = misc.flatten( self.minBFS( (px,py) ) )
            return self.visited
            litTiles = misc.flatten( self.litBFS( (px,py) ) )
        litTiles = list( set( litTiles) )
        self.litTiles = litTiles
        return litTiles
    
    def visitTile(self, x, y):
        self.visited += [(x, y)]
    
    def isVisited(self, x, y):
        return (x, y) in self.visited
    def isSolid(self, x, y):
        return self.getEntry(x, y) in const.SOLIDS
    
    def getPPOV(self, x, y, l = 2):
        PPOV.fieldOfView(x, y, self.DIM, self.DIM, l, self.visitTile, self.isSolid)
        #print self.visited
    
    def isVisible(self, x, y):
        if self.type not in const.darkMaps:
            return True
        if (x, y) in self.litTiles:
            return True
        else: return False
    
    def isOccupied(self, x, y):
        return self.grid[x][y].occupied
    def setOccupied(self, x, y):
        self.grid[x][y].occupied = True
    def clearOccupied(self, x, y):
        self.grid[x][y].occupied = False
    
    def getBinaryMap(self):
        bMap = [[0 for i in range(self.DIM)] for j in range(self.DIM)]
        for i in range(self.DIM):
            for j in range(self.DIM):
                if self.getTileFG(i, j) in const.SOLIDS:
                    bMap[j][i] = 1
                else: bMap[j][i] = 0
        return bMap

# inherited map class to be used by level editor
class edMap(generalmap):
    def __init__(self, mBall=None, name=None):
        generalmap.__init__(self, 2*const.DIM)
        if mBall is not None:
            self.installBall(mBall)
        else:
            self.defaultBkgd = const.DFLOOR1
            for i in range(self.DIM):
                self.grid += [range(self.DIM)]
                for j in range(self.DIM):
                    self.grid[i][j] = tile.Tile(i, j, const.DFLOOR1, self.defaultBkgd)
            self.heroStart = None
            self.pointOfEntry = None
            self.pointOfExit = None
                        
            self.portals = []
            # location : (type, level)
            self.shops = {}
            self.setName('Untitled')
            self.level = 0
        self.itemShop = None
        self.magicShop = None
        self.Armory = None
        self.Blacksmith = None
        self.Tavern = None
        self.Townhall = None
        for s in self.shops:
            if self.shops[s][0] == 'armory':
                self.Armory = s
            elif self.shops[s][0] == 'blacksmith':
                self.Blacksmith = s
            elif self.shops[s][0] == 'magicshop':
                self.magicShop = s
            elif self.shops[s][0] == 'itemshop':
                self.itemShop = s
            elif self.shops[s][0] == 'tavern':
                self.Tavern = s
            elif self.shops[s][0] == 'townhall':
                self.Townhall = s
    
    def addChest(self, loc, chest):
        self.chests[loc] = chest
    
    def changeEntry(self, x, y, entry, shop=False):
        if entry is not None:
            (px,py) = entry
            self.setEntry(px,py,self.defaultBkgd)
        return (x,y)
    
    # overridden from parent class
    def setEntry(self, x, y, e, param=None):
        if self.shops != []:
            try:
                self.shops.pop( (x, y) )
            except KeyError:
                pass
        if e == const.HEROSTART:
            self.heroStart = self.changeEntry(x, y, self.heroStart)
            return
        elif e == const.STAIRUP:
            self.pointOfEntry = self.changeEntry(x, y, self.pointOfEntry)
        elif e == const.STAIRDN:
            self.pointOfExit = self.changeEntry(x, y, self.pointOfExit)
        elif e == const.TOWERDOOR:
            self.shops[ self.changeEntry(x, y, self.itemShop, True) ] = ('tower1', param )
        elif e == const.ITEMSDOOR:
            self.shops[ self.changeEntry(x, y, self.itemShop, True) ] = ('itemshop', param )
        elif e == const.ARMRYDOOR:
            self.shops[ self.changeEntry(x, y, self.Armory, True) ] = ('armory', param )
        elif e == const.BLKSMDOOR:
            self.shops[ self.changeEntry(x, y, self.Blacksmith, True) ] = ('blacksmith', param )
        elif e == const.MAGICDOOR:
            self.shops[ self.changeEntry(x, y, self.magicShop, True) ] = ('magicshop', param )
        elif e == const.TAVRNDOOR:
            self.shops[ self.changeEntry(x, y, self.Tavern, True) ] = ('tavern', param )
        elif e == const.TOWNHALLDOOR:
            self.shops[ self.changeEntry(x, y, self.Townhall, True) ] = ('townhall', param )
        elif e == const.HOUSEDOOR1:
            self.shops[ (x, y) ] = ('house1', param )
        elif e == const.SIGN:
            self.grid[x][y].setMsgText(param)
        try:
            self.grid[x][y].setFG(e)
        except AttributeError:
            pass
    
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
class genMap(generalmap):
    
    def __init__(self, DIM, level, name):
        generalmap.__init__(self, DIM, const.VOID)
        self.level = level
        self.BFSQueue = queue.Queue()
        for i in range(self.DIM):
            self.grid += [range(self.DIM)]
            for j in range(self.DIM):
                self.grid[i][j] = tile.Tile(i, j, const.VOID, const.VOID)
        self.setName(name)
    
    def setEntry(self, x, y, fg, roomN=None):
    #Updates one map Entry to type at map coordinates x,y
    # Overridden for gen class with room SN
        self.grid[x][y].setFG(fg)
        self.grid[x][y].setBG(const.DFLOOR1)
        if roomN != None:
            self.grid[x][y].roomN = roomN
        
    def mapPaste(self, pos, roomN):
        (sX, sY) = pos
        copyText = self.copyText
        for i in range( len(copyText[0]) ):
            for j in range( len(copyText) ):
                self.setEntry(i+sX, j+sY, copyText[j][i].getFG(), roomN)
                self.grid[i+sX][j+sY].setXY(i+sX, j+sY)
    
    def getRoomN(self, x, y):
        try:
            return self.grid[x][y].roomN
        except AttributeError:
            return None
    
    def pathfinderBFS(self, start):
        (x,y) = start
        entryList = []
        self.visited += [ (x, y) ]
        self.BFSQueue.push( (x, y) )
        while not self.BFSQueue.isEmpty():
            (x, y) = self.BFSQueue.pop()
            for (Cx,Cy) in const.CARDINALS:
                if (x+Cx,y+Cy) not in self.visited and  not self.BFSQueue.has( (x+Cx, y+Cy) ) and self.getEntry(x+Cx,y+Cy) in range(const.BRICK1):
                    self.BFSQueue.push( (x+Cx, y+Cy) )
                    self.visited += [ (x+Cx,y+Cy) ]
        return self.visited
        
    def pathfinder(self, t1, t2):
        self.visited = []
        self.BFSQueue.reset()
        tiles = self.pathfinderBFS( t1 )
        if t2 in tiles:
            return True
        else:
            return False
