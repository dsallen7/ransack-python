from MAP import tile


class subMap():
    def __init__(self, dX, dY, defaultFloor):
        self.DIMX = dX
        self.DIMY = dY
        self.grid = []
        self.portal = (0,0)
        for i in range(self.DIMX):
            for j in range(self.DIMY):
                self.grid[i][j] = tile.Tile(i, j, defaultFloor)
        for i in range(self.DIMX):
            self.grid[i][0] = tile.Tile(i, j, 0)