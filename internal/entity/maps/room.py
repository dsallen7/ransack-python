from UTIL import const, colors
from MAP import tile


class Room():

    def __init__(self, xdim, ydim, pos=(0, 0), shape='square'):
        self.pos = pos
        self.xdim = xdim
        self.ydim = ydim
        self.grid = [range(xdim) for _ in range(ydim)]
        for i in range(xdim):
            for j in range(ydim):
                self.grid[j][i] = tile.Tile(i, j, const.DFLOOR1, const.DFLOOR1)
        self.entrances = []
        self.neighbors = []
        self.secret = False

        if shape == 'square':
            (xpos, ypos) = self.getPos()
            (xdim, ydim) = self.getDimensions()
            for i in range(1, xdim - 1):
                self.setGrid(i, 0, const.EWWALL)
                self.setGrid(i, ydim - 1, const.EWWALL)
            for i in range(1, ydim - 1):
                self.setGrid(0, i, const.NSWALL)
                self.setGrid(xdim - 1, i, const.NSWALL)
            self.setGrid(0, 0, const.ULWALL)
            self.setGrid(xdim - 1, 0, const.URWALL)
            self.setGrid(0, ydim - 1, const.LLWALL)
            self.setGrid(xdim - 1, ydim - 1, const.LRWALL)
            for i in range(1, xdim - 1):
                for j in range(1, ydim - 1):
                    self.setGrid(i, j, 0)
        if shape == 'round':
            (xpos, ypos) = self.getPos()
            self.xdim = 9
            self.ydim = 9
            self.grid = [range(self.xdim) for _ in range(self.ydim)]
            layout = [[const.VOID, const.VOID, const.ULWALL,
                       const.EWWALL, const.EWWALL, const.EWWALL,
                       const.URWALL, const.VOID, const.VOID],
                           [const.VOID, const.ULWALL, const.LRWALL,
                           const.DFLOOR1, const.DFLOOR1, const.DFLOOR1,
                           const.LLWALL, const.URWALL, const.VOID],
                           [const.ULWALL, const.LRWALL, const.DFLOOR1,
                           const.DFLOOR1, const.DFLOOR1, const.DFLOOR1,
                           const.DFLOOR1, const.LLWALL, const.URWALL],
                           [const.NSWALL, const.DFLOOR1, const.DFLOOR1,
                           const.DFLOOR1, const.DFLOOR1, const.DFLOOR1,
                           const.DFLOOR1, const.DFLOOR1, const.NSWALL],
                           [const.NSWALL, const.DFLOOR1, const.DFLOOR1,
                           const.DFLOOR1, const.DFLOOR1, const.DFLOOR1,
                           const.DFLOOR1, const.DFLOOR1, const.NSWALL],
                           [const.NSWALL, const.DFLOOR1, const.DFLOOR1,
                           const.DFLOOR1, const.DFLOOR1, const.DFLOOR1,
                           const.DFLOOR1, const.DFLOOR1, const.NSWALL],
                           [const.LLWALL, const.URWALL, const.DFLOOR1,
                           const.DFLOOR1, const.DFLOOR1, const.DFLOOR1,
                           const.DFLOOR1, const.ULWALL, const.LRWALL],
                           [const.VOID, const.LLWALL, const.URWALL,
                           const.DFLOOR1, const.DFLOOR1, const.DFLOOR1,
                           const.ULWALL, const.LRWALL, const.VOID],
                           [const.VOID, const.VOID, const.LLWALL,
                           const.EWWALL, const.EWWALL, const.EWWALL,
                           const.LRWALL, const.VOID, const.VOID]
                        ]
            for i in range(self.xdim):
                for j in range(self.ydim):
                    self.grid[j][i] = tile.Tile(
                        i, j, layout[j][i], const.DFLOOR1)

    def getDimensions(self):
        return (self.xdim, self.ydim)

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def setGrid(self, x, y, e):
        #self.grid[y] = self.grid[y][:x] + [e] + self.grid[y][x+1:]
        self.grid[y][x].setFG(e)

    def getGrid(self, x, y):
        return self.grid[y][x]
