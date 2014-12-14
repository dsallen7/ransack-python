import pygame
import random
import pickle
import ppov
import gzip
import os
from UTIL import queue, const, colors, load_image, misc
from types import *
from MAP import tile, minimap, submap


class generalmap():
    def __init__(self, DIM=const.DIM, dFG=const.DFLOOR1):
        self.grid = []
        self.DIM = DIM
        self.chests = {}
        self.defaultBkgd = 0
        self.shops = []
        self.NPCs = []

    def getDIM(self):
        return self.DIM

    def setEntry(self, x, y, fg):
        """Updates one map Entry to type at map coordinates x, y
        """
        #self.grid[y] = self.grid[y][:x]+[type]+self.grid[y][x+1:]
        self.grid[x][y].setFG(fg)

    def getEntry(self, x, y):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            return self.grid[x][y].getFG()
        else:
            return const.VOID

    def getTileFG(self, x, y):
        return self.grid[x][y].getFG()

    def setTileFG(self, x, y, fg):
        self.grid[x][y].setFG(fg)

    def getGrid(self):
        return self.grid

    def getMapBall(self):
        return (self.grid, self.defaultBkgd, self.pointOfEntry,
            self.pointOfExit, self.heroStart, self.shops,
            self.chests, self.NPCs)

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
        grid = [range(x2 - x1)] * (y2 - y1)
        for i in range(x2 - x1):
            for j in range(y2 - y1):
                grid[j][i] = self.getEntry(x1 + i, y1 + j)
                self.setEntry(x1 + i, y1 + j, 0)
        self.copyText = grid

    def mapCopy(self, pos1, pos2):
        (x1, y1) = pos1
        (x2, y2) = pos2
        grid = [range(x2 - x1)] * (y2 - y1)
        for i in range(x2 - x1):
            for j in range(y2 - y1):
                grid[j][i] = self.getEntry(x1 + i, y1 + j)
                self.setEntry(x1 + i, y1 + j, 0)
        self.copyText = grid

    def mapPaste(self, pos):
        (sX, sY) = pos
        copyText = self.copyText
        for i in range(len(copyText[0])):
            for j in range(len(copyText)):
                self.grid[i + sX][j + sY] = copyText[j][i]
                self.grid[i + sX][j + sY].setXY(i + sX, j + sY)


class gameMap(generalmap):

    def __init__(self, filename=None, mapball=None, level=0, type='dungeon'):
        generalmap.__init__(self)

        self.level = level
        self.lineOfVision = 0
        if filename is not None:
            self.loadMap(filename)
        self.BFSQueue = queue.Queue()

        if mapball is not None:
            self.installBall(mapball)

        self.playerXY = self.heroStart
        self.type = type

        self.topMapCorner = (0, 0)
        self.visDict = {}
        for i in range(self.DIM):
            for j in range(self.DIM):
                if self.type in ['dungeon', 'maze', 'fortress']:
                    self.visDict[(i, j)] = False
                    self.grid[i][j].visible = False
                else:
                    self.visDict[(i, j)] = True
                    self.grid[i][j].visible = True
        self.myMiniMap = minimap.miniMap(self.grid)

        self.litTiles = []

    def setLOV(self, num):
        self.lineOfVision = num

    def getImages(self):
        return self.images

    def loadMap(self, filename):
        try:
            save = gzip.GzipFile(
                os.getcwd() + '/MAP/LEVELS/' + filename, "rb")
            ball = pickle.load(save)
            save.close()
            self.installBall(ball)
        except pygame.error, message:
            print 'Cannot load map:', name
            raise SystemExit(message)

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
        self.myMiniMap.callMiniMap(screen, self.playerXY, self.visDict)

    def distanceFunc(self, pos1, pos2):
        """returns distance between two points
        """
        (x1, y1) = pos1
        (x2, y2) = pos2
        return max(abs(y2 - y1), abs(x2 - x1), abs(y2 - y1) + abs(x2 - x1))

    def neighbors(self, tile):
        returnList = []
        (x, y) = tile
        for (Cx, Cy) in const.CARDINALS:
            returnList.append((Cx + x, Cy + y))
        return returnList

    def getRandomTile(self):
        x = random.randrange(0, self.DIM)
        y = random.randrange(0, self.DIM)
        while (self.getEntry(x, y) not in range(0, 25)):
            x = random.randrange(0, self.DIM)
            y = random.randrange(0, self.DIM)
        return x, y

    def setPlayerXY(self, x, y):
        self.playerXY = (x, y)

    def updateWindowCoordinates(self, hero):
        """calculate location of map window based on hero location
           and hero sprite rect
        """
        DIMEN = self.getDIM()
        oldX, oldY = self.playerXY
        # Compute top map corner
        (px, py) = hero.getXY()
        px = px / const.blocksize
        py = py / const.blocksize
        self.playerXY = (px, py)

        if DIMEN <= const.HALFDIM:
            topX = 0
            topY = 0
            self.WINDOWOFFSET = (const.HALFDIM - DIMEN) / 2
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

    def revealMap(self):
        """complete list of tiles is in tiles1.txt
        """
        if self.type in ['dungeon', 'maze', 'fortress']:
            litTiles = self.getLitTiles()
            self.litTiles = litTiles
            if litTiles is None:
                return
            for tile in litTiles:
                self.visDict[tile] = True
        return

    #@tail_call_optimized
    def litBFS(self, start, d=0):
        if self.type == 'maze':
            if d > 2:
                return start
        (x, y) = start
        if self.getEntry(x, y) in [18, 19]:
            return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                     (x - 1, y), (x, y), (x + 1, y),
                     (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        if self.getEntry(x, y) in range(18, 86):
            returnList = [(x, y)]
            for (Cx, Cy) in const.CARDINALS:
                if self.getEntry(x + Cx, y + Cy) in range(18, 86):
                    count = 0
                    for (Nx, Ny) in const.CARDINALS:
                        try:
                            if self.visDict[(x + Cx + Nx, y + Cy + Ny)]:
                                count += 1
                        except KeyError:
                            pass
                    if count >= 2:
                        returnList.append((x + Cx, y + Cy))
            return returnList
        entryList = []
        for (Cx, Cy) in const.CARDINALS:
            if (x + Cx, y + Cy) not in self.visited and ~self.BFSQueue.has(
                    (x + Cy, y + Cy) and
                    self.getEntry(x + Cx, y + Cy) in range(18)):
                self.BFSQueue.push((x + Cx, y + Cy))
                entryList += [(x + Cx, y + Cy)]
                self.visited += [(x + Cx, y + Cy)]
        if len(entryList) < 1:
            return (x, y)
        else:
            returnList = []
            for i in range(len(entryList)):
                returnList += [self.litBFS(self.BFSQueue.pop(), d + 1)]
            return [(x, y)] + returnList

    def getLitTiles(self):
        (px, py) = self.playerXY
        self.BFSQueue.reset()
        self.visited = []
        litTiles = misc.flatten(self.litBFS((px, py)))
        litTiles = list(set(litTiles))
        self.litTiles = litTiles
        return litTiles

    def isVisible(self, x, y):
        if (x, y) in self.litTiles:
            return True
        else:
            return False

    def isOccupied(self, x, y):
        return self.grid[x][y].occupied


class edMap(generalmap):
    """inherited map class to be used by map generator
    """
    def __init__(self):
        generalmap.__init__(self, 2 * const.DIM)
        self.defaultBkgd = const.DFLOOR1
        for i in range(self.DIM):
            self.grid += [range(self.DIM)]
            for j in range(self.DIM):
                self.grid[i][j] = tile.Tile(i, j, const.DFLOOR1,
                    self.defaultBkgd)
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

    def setEntry(self, x, y, e, level=None):
        """overridden from parent class
        """
        if e == const.HEROSTART:
            if self.heroStart is None:
                self.heroStart = (x, y)
            else:
                (px, py) = self.heroStart
                self.setEntry(px, py, self.defaultBkgd)
                self.heroStart = (x, y)
                return
        if e == const.STAIRUP:
            if self.pointOfEntry is None:
                self.pointOfEntry = (x, y)
            else:
                (px, py) = self.pointOfEntry
                self.setEntry(px, py, self.defaultBkgd)
                self.pointOfEntry = (x, y)
        if e == const.STAIRDN:
            if self.pointOfExit is None:
                self.pointOfExit = (x, y)
            else:
                (px, py) = self.pointOfExit
                self.setEntry(px, py, self.defaultBkgd)
                self.pointOfExit = (x, y)
        if e == const.ITEMSDOOR:
            if self.itemShop is None:
                self.itemShop = (x, y)
                self.shops[(x, y)] = ('itemshop', level)
            else:
                (px, py) = self.itemShop
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px, py))
                self.shops[(x, y)] = ('itemshop', level)
                self.itemShop = (x, y)
        if e == const.ARMRYDOOR:
            if self.Armory is None:
                self.Armory = (x, y)
                self.shops[(x, y)] = ('armory', level)
            else:
                (px, py) = self.Armory
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px, py))
                self.shops[(x, y)] = ('armory', level)
                self.Armory = (x, y)
        if e == const.BLKSMDOOR:
            if self.Blacksmith is None:
                self.Blacksmith = (x, y)
                self.shops[(x, y)] = ('blacksmith', level)
            else:
                (px, py) = self.Blacksmith
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px, py))
                self.shops[(x, y)] = ('blacksmith', level)
                self.Blacksmith = (x, y)
        if e == const.MAGICDOOR:
            if self.magicShop is None:
                self.magicShop = (x, y)
                self.shops[(x, y)] = ('magicshop', level)
            else:
                (px, py) = self.magicShop
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px, py))
                self.shops[(x, y)] = ('magicshop', level)
                self.magicShop = (x, y)
        if e == const.TAVRNDOOR:
            if self.Tavern is None:
                self.Tavern = (x, y)
                self.shops[(x, y)] = ('tavern', level)
            else:
                (px, py) = self.Tavern
                self.setEntry(px, py, self.defaultBkgd)
                self.shops.pop((px, py))
                self.shops[(x, y)] = ('tavern', level)
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
                        else:
                            newGrid[i][j] = tile.Tile(i, j, const.DFLOOR1,
                                self.defaultBkgd)
                else:
                    for j in range(nDim):
                        newGrid[i][j] = tile.Tile(i, j, const.DFLOOR1,
                            self.defaultBkgd)
            self.grid = newGrid
        #shrinking
        elif self.DIM > nDim:
            self.grid = self.grid[:nDim]
            for i in range(nDim):
                self.grid[i] = self.grid[i][:nDim]
        #same
        else:
            return
        self.DIM = nDim
        self.cursorPos = (0, 0)

    def mapMove(self, source, size, dest):
        (sX, sY) = source
        (dX, dY) = dest
        (xDim, yDim) = size
        tmpGrid = [range(xDim) for _ in range(yDim)]
        for i in range(xDim):
            for j in range(yDim):
                tmpGrid[j][i] = self.getEntry(i + sX, j + sY)
        for i in range(xDim):
            for j in range(yDim):
                self.setEntry(i + sX, j + sY, 0)
        for i in range(xDim):
            for j in range(yDim):
                self.setEntry(i + dX, j + dY, tmpGrid[j][i])

    def mapErase(self):
        pass


class genMap(generalmap):
    """inherited map class to be used by map generator
    """

    def __init__(self, DIM, level):
        generalmap.__init__(self, DIM, const.VOID)
        self.level = level
        self.BFSQueue = queue.Queue()
        for i in range(self.DIM):
            self.grid += [range(self.DIM)]
            for j in range(self.DIM):
                self.grid[i][j] = tile.Tile(i, j, const.VOID, const.VOID)

    def pathfinderBFS(self, start):
        (x, y) = start
        entryList = []
        self.visited += [(x, y)]
        self.BFSQueue.push((x, y))
        while not self.BFSQueue.isEmpty():
            (x, y) = self.BFSQueue.pop()
            for (Cx, Cy) in const.CARDINALS:
                if ((x + Cx, y + Cy) not in self.visited
                        and not self.BFSQueue.has((x + Cx, y + Cy))
                        and self.getEntry(x + Cx, y + Cy) in range(24)):
                    self.BFSQueue.push((x + Cx, y + Cy))
                    self.visited += [(x + Cx, y + Cy)]
        return self.visited

    def pathfinder(self, t1, t2):
        self.visited = []
        self.BFSQueue.reset()
        tiles = self.pathfinderBFS(t1)
        if t2 in tiles:
            return True
        else:
            return False