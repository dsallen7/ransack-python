from UTIL import const, colors
import pygame

class miniMap():
    def __init__(self, grid):
        self.grid = grid
        self.mapColors = colors.mapColors
        self.DIM = len(self.grid)
        self.colorDict = colors.colorDict
    
    def getEntry(self, x, y):
        if x in range( len(self.grid) ) and y in range( len(self.grid) ):
            return self.grid[x][y].getFG()
        else: return -1
    
    def isMapped(self, coord):
        try:
            return self.visDict[coord]
        except KeyError:
            return False
    
    def drawMiniMap(self,screen, tx, ty, playerXY, visDict):
        miniMapBoard = pygame.Surface( [const.blocksize*const.HALFDIM,const.blocksize*const.HALFDIM] )
        miniMapBoard.fill(colors.black)
        for i in range(const.DIM):
            for j in range(const.DIM):
                mapColorBlock = pygame.Surface( (const.miniblocksize,const.miniblocksize) )
                if (i+tx,j+ty) == playerXY:
                    mapColorBlock.fill( self.mapColors[5] )
                    miniMapBoard.blit( mapColorBlock, ( i*const.miniblocksize, j*const.miniblocksize) )
                elif self.isMapped( (i+tx,j+ty) ):
                    try:
                        mapColorBlock.fill( self.mapColors[self.colorDict[self.getEntry(i+tx,j+ty)]] )
                    except KeyError:
                        mapColorBlock.fill( colors.ltgrey )
                    miniMapBoard.blit( mapColorBlock, ( i*const.miniblocksize, j*const.miniblocksize) )
        screen.blit(pygame.transform.scale(miniMapBoard, (720, 720) ), (0, 0) )
        pygame.display.flip()
    
    def event_handler(self, screen, playerXY, event_):
        if event_ == pygame.K_UP:
            if self.ty > 0:
                self.ty = self.ty - 1
                self.drawMiniMap(screen, self.tx, self.ty, playerXY, self.visDict)
        elif event_ == pygame.K_DOWN:
            if self.ty < self.DIM-const.DIM:
                self.ty = self.ty + 1
                self.drawMiniMap(screen, self.tx, self.ty, playerXY, self.visDict)
        elif event_ == pygame.K_LEFT:
            if self.tx > 0:
                self.tx = self.tx - 1
                self.drawMiniMap(screen, self.tx, self.ty, playerXY, self.visDict)
        elif event_ == pygame.K_RIGHT:
            if self.tx < self.DIM-const.DIM:
                self.tx = self.tx + 1
                self.drawMiniMap(screen, self.tx, self.ty, playerXY, self.visDict)
        elif event_ == pygame.K_m: return False
        elif event_ == pygame.K_ESCAPE: return False
        return True
    
    def callMiniMap(self, screen, playerXY, visDict, iH):
        self.visDict = visDict
        (px, py) = playerXY
        self.tx = px - const.HALFDIM
        self.ty = py - const.HALFDIM
        self.drawMiniMap(screen, self.tx, self.ty, playerXY, visDict)
        while True:
            for event in pygame.event.get():
                event_ = iH.getCmd(event)
                if not self.event_handler(screen, playerXY, event_):
                    return
            '''
            if pygame.mouse.get_pressed()[0]:
                event_ = iH.getCmd(None)
                if not self.event_handler(screen, playerXY, event_):
                    return
            '''