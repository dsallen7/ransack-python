from UTIL import const, colors
import pygame


class miniMap():

    def __init__(self, grid):
        self.grid = grid
        self.mapColors = colors.mapColors
        self.DIM = len(self.grid)

        self.colorDict = {-1: 0, 0: 10, 1: 11, 3: 3, 4: 11, 5: 11, 6: 11,
                          7: 11, 8: 10, 9: 6, 10: 5, 11: 5, 12: 7, 13: 7,
                          14: 8, 15: 8, 16: 6, 18: -1, 19: 11, 20: 10, 21: 10,
                          22: 10, 23: 10, 24: 1, 25: 1, 27: 3, 28: 3, 29: 10,
                          30: 3, 31: 3, 32: 3, 33: 3, 34: 3, 35: 3, 36: 3,
                          37: 3, 38: 6, 39: 3, 40: 3, 41: 1, 42: 5, 42: 5,
                          43: 5, 44: 5, 45: 5, 46: 5, 47: 5, 48: 1, 49: 1,
                          50: 1, 51: 3, 52: 8, 53: 8, 55: 3, 56: 10, 57: 11,
                          58: 1, 59: 1, 60: 8, 61: 3, 62: 3, 63: 1, 64: 5,
                          65: 9, 66: 9, 67: 9, 68: 9, 69: 9, 70: 9, 71: 4,
                          72: 5, 73: 5, 74: 6, 75: 3, 80: 3, 81: 3, 92: 4,
                          95: 4, 98: 2, 99: 6, 100: 6, 110: 6, 111: 6, 112: 3,
                          116: 3, 117: 3, 118: 3, 120: 3, 121: 3,
                          126: 0, 127: 5}

    def getEntry(self, x, y):
        if x in range(len(self.grid)) and y in range(len(self.grid)):
            return self.grid[x][y].getFG()
        else:
            return -1

    def isMapped(self, coord):
        try:
            return self.visDict[coord]
        except KeyError:
            return False

    def drawMiniMap(self, screen, tx, ty, playerXY, visDict):
        miniMapBoard = pygame.Surface(
            [const.blocksize * const.HALFDIM, const.blocksize * const.HALFDIM])
        miniMapBoard.fill(colors.black)
        for i in range(const.DIM):
            for j in range(const.DIM):
                mapColorBlock = pygame.Surface((const.miniblocksize,
                                                const.miniblocksize))
                if (i + tx, j + ty) == playerXY:
                    mapColorBlock.fill(self.mapColors[5])
                    miniMapBoard.blit(mapColorBlock,
                        (i * const.miniblocksize, j * const.miniblocksize))
                elif self.isMapped((i + tx, j + ty)):
                    mapColorBlock.fill(
                        self.mapColors[self.colorDict[self.getEntry(
                        i + tx, j + ty)]])
                    miniMapBoard.blit(mapColorBlock,
                        (i * const.miniblocksize, j * const.miniblocksize))
        screen.blit(miniMapBoard, (const.gameBoardOffset,
            const.gameBoardOffset))
        pygame.display.flip()

    def callMiniMap(self, screen, playerXY, visDict):
        self.visDict = visDict
        (px, py) = playerXY
        tx = px - const.HALFDIM
        ty = py - const.HALFDIM
        self.drawMiniMap(screen, tx, ty, playerXY, visDict)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if ty > 0:
                            ty = ty - 1
                            self.drawMiniMap(screen, tx, ty, playerXY, visDict)
                    elif event.key == pygame.K_DOWN:
                        if ty < self.DIM - const.DIM:
                            ty = ty + 1
                            self.drawMiniMap(screen, tx, ty, playerXY, visDict)
                    elif event.key == pygame.K_LEFT:
                        if tx > 0:
                            tx = tx - 1
                            self.drawMiniMap(screen, tx, ty, playerXY, visDict)
                    elif event.key == pygame.K_RIGHT:
                        if tx < self.DIM - const.DIM:
                            tx = tx + 1
                            self.drawMiniMap(screen, tx, ty, playerXY, visDict)
                    else:
                        return
