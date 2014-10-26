import pygame
from UTIL import colors, const
from math import ceil, floor

from SCRIPTS import mapScr

# Main graphics engine for Ransack.

class Display():
    
    def __init__(self, screen, images):
        self.screen = screen
        self.images = images.mapImages
        self.accImages = images.accessories
        self.fog = pygame.Surface( (30,30) )
        self.fog.fill( colors.black )
        self.fog.set_alpha( 192 )
    
    def displayOneFrame(self, iFace, FX, board=None, game=None, dark=False, smooth=False):
        if game is not None:
            game.updateSprites()
            iFace.update(game)
            #board.blit( game.myHero.showLocation(), (0,50) )
        FX.update(self.screen)
        if board is not None:
            if game.myMap.type in const.darkMaps and dark:
                self.drawDarkness(game.myMap, board)
                #board.blit( self.SS_, (0, 0) )
            #pygame.time.delay(500)
            if smooth:
                pass
            '''
                self.screen.blit( pygame.transform.smoothscale(board, 
                                                           (int(ceil(300 * const.scaleFactor)), 
                                                            int(ceil(300 * const.scaleFactor)) ) ), (0,0) )
                                                            '''
            self.screen.blit( pygame.transform.scale(board, 
                                                           (int(ceil(300 * const.scaleFactor)), 
                                                            int(ceil(300 * const.scaleFactor)) ) ), (0,0) )
        pygame.display.flip()
    
    # Takes first two coordinates of hero rect, gameBoard and
    # draws darkness
    def drawDarkness(self, map, gameBoard, offset=(0,0) ):
        (oX, oY) = offset
        (topX, topY) = map.oldTopMapCorner
        (px, py) = map.playerXY
        tiles = map.litTiles
        for x in range( -1, map.WINDOWSIZE+1 ):
            for y in range( -1, map.WINDOWSIZE+1 ):
                if (x+topX, y+topY) not in tiles:
                    #AAfilledRoundedRect(surface,rect,color,radius=0.4)
                    gameBoard.blit(self.fog, 
                                   ( (x)*const.blocksize - oX, 
                                     (y)*const.blocksize - oY), 
                                   area=(0,0,const.blocksize,const.blocksize) )
    
    # Redraw map onto gameboard without redrawing tiles
    def redrawMap(self, map, hero, gameBoard):
        (rx,ry,rx2,ry2) = hero.getRect()
        rx = rx/const.blocksize
        ry = ry/const.blocksize
        #map.setPlayerXY(rx, ry)
        (topX, topY), (oldTopX, oldTopY) = map.updateWindowCoordinates(hero)
        gameBoard.blit( self.getMapWindow( (topX, topY), map.WINDOWSIZE ), (map.WINDOWOFFSET,map.WINDOWOFFSET) )
        if map.type in const.darkMaps:
            pass#self.drawDarkness(map, gameBoard  )
    
    # takes map coordinates, returns map window
    def getMapWindow(self, pos, wsize=10):
        (x1, y1) = pos
        window = pygame.Surface( (wsize*const.blocksize, wsize*const.blocksize) )
        window.blit( self.xGameBoard, ( -(x1*const.blocksize), -(y1*const.blocksize) ) )
        return window
    # takes pixel coordinates of top left corner of DIMxDIM window of xGameBoard, returns map window
    def getScrollingMapWindow(self, pos, wsize = 10):
        (x1,y1) = pos
        window = pygame.Surface( (wsize*const.blocksize, wsize*const.blocksize) )
        window.blit( self.xGameBoard, ( -x1, -y1 ) )
        return window
    
    # draws entire map to DIMxDIM Surface
    def redrawXMap(self, map, light, local=False):
        self.xGameBoard = pygame.Surface( (map.getDIM()*const.blocksize, map.getDIM()*const.blocksize) )
        if map.type in const.darkMaps:
            map.revealMap(light)
        if local:
            (tX, tY) = map.topMapCorner
            rX = range(tX-1, tX+const.HALFDIM+1)
            rY = range(tY-1, tY+const.HALFDIM+1)
        else:
            (rX, rY) = ( range(map.getDIM()), range(map.getDIM()) )
        for x in rX:
            for y in rY:
                fTile = map.getTileFG(x,y)
                bTile = map.getTileBG(x,y)
                if fTile != const.VOID and map.visDict[(x,y)]:
                    # draw background tile first
                    if bTile is not None:
                        self.xGameBoard.blit( self.images[ bTile ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    # then foreground
                    else: self.xGameBoard.blit( self.images[ map.defaultBkgd ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    '''
                    if tile > const.BRICK1:
                        shortList = [map.getEntry(tx, ty) for (tx, ty) in map.cardinalNeighbors((x,y))]
                        if const.VOID not in shortList:
                            self.xGameBoard.blit( self.images[ map.defaultBkgd ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    
                    if map.getEntry(x, y) == const.ITEMSDOOR:
                        self.xGameBoard.blit( self.images[128], (x*const.blocksize - const.blocksize, y*const.blocksize - 2*const.blocksize), area = self.images[128].get_rect() )
                    else: self.xGameBoard.blit( self.images[ tile ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    '''
                    self.xGameBoard.blit( self.images[ fTile ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    # make the trees look thicker
                    # whenever four adjacent trees are drawn one the map, draw
                    # another one in the center
                    
                    nbrL = map.getTileFG(x-1, y)
                    nbrU = map.getTileFG(x, y-1)
                    nbrUL = map.getTileFG(x-1, y-1)
                    if nbrL in mapScr.pines and nbrU in mapScr.pines and nbrUL in mapScr.pines and fTile in mapScr.pines:
                        self.xGameBoard.blit( self.images[ mapScr.pineDict[fTile] ], 
                                              ( (x*const.blocksize)-(const.blocksize/2), 
                                                (y*const.blocksize)-(const.blocksize/2) ) )
                    # put accessories on the table
                    if fTile in range(const.TABLE1, const.TABLE3+1):
                        try:
                            self.xGameBoard.blit( self.accImages[map.grid[x][y].accessory], 
                                                  ( x*const.blocksize+10,
                                                    y*const.blocksize+5) )
                        except AttributeError:
                            pass
        if map.type == 'village':
            for s in map.shops:
                (sX, sY) = s
                self.xGameBoard.blit( self.images[ mapScr.siteImgDict[ map.shops[s][0] ][0] ], 
                                      (sX*const.blocksize - const.blocksize, 
                                       sY*const.blocksize - (mapScr.siteImgDict[ map.shops[s][0] ][1]*const.blocksize)) )
    
    # draws all pending sprite movements
    def drawSprites(self, hero, map, gameBoard, game=None, dir=None, animated=True):
        DIMEN = map.getDIM()
        # by default, the hero is in the upper left corner of the map
        (newX,newY) = hero.getXY()
        map.setPlayerXY(newX/const.blocksize, newY/const.blocksize)
        #top-left corner of hero sprite location
        (oldX, oldY, c, d) = hero.getRect()
        scrolling = False
        # where is new on-screen location of hero?
        if DIMEN > const.HALFDIM:
            if (5*const.blocksize <= newX <= (DIMEN-5)*const.blocksize):
                newX = 5 * const.blocksize
                if dir in ['left','right'] and oldX == 5*const.blocksize:
                    scrolling = True
            if newX > (DIMEN-5)*const.blocksize:
                if map.getDIM() % 5 == 0:
                    newX = (5 * const.blocksize) + ( newX % (5 * const.blocksize) )# + const.blocksize
                else:
                    newX = (5 * const.blocksize) + ( newX % (5 * const.blocksize) ) + const.blocksize
            if (5*const.blocksize <= newY <= (DIMEN-5)*const.blocksize):
                newY = 5 * const.blocksize
                if dir in ['up','down'] and oldY == 5*const.blocksize:
                    scrolling = True
            if newY > (DIMEN-5)*const.blocksize:
                if map.getDIM() % 5 == 0:
                    newY = (5 * const.blocksize) + ( newY % (5 * const.blocksize) )# + const.blocksize
                else:
                    newY = (5 * const.blocksize) + ( newY % (5 * const.blocksize) ) + const.blocksize
        else:
            newX += (const.HALFDIM - DIMEN)/2*const.blocksize
            newY += (const.HALFDIM - DIMEN)/2*const.blocksize
        
        #make the move animated
        if animated:
            if not hero.moving:
                scrolling = False
            if scrolling:
                scrollX , scrollY = const.scrollingDict[dir]
            else: (scrollX , scrollY) = (0, 0)
            (px,py) = hero.getXY()
            pos, oldPos = map.updateWindowCoordinates( hero )
            (topX, topY) = pos
            if oldX == newX:
                xAxis = [oldX] * (const.blocksize)
            elif oldX < newX:
                xAxis = range(oldX, newX, 1)
            else:
                xAxis = range(oldX, newX, -1)
            if oldY == newY:
                yAxis = [oldY] * (const.blocksize/1)
            elif oldY < newY:
                yAxis = range(oldY, newY, 1)
            elif oldY > newY:
                yAxis = range(oldY, newY, -1)
            for (idx, (i, j)) in list( enumerate(zip(xAxis, yAxis), start=1) ):
                hero.setRect( i, j, const.blocksize, const.blocksize)
                for npc in game.NPCs:
                    if npc.moving:
                        npc.shiftOnePixel(npc.dir, -1)
                        if idx in [6,12,21,27]:
                            npc.takeStep()
                # compensate for scrolling
                if scrolling:
                    for npc in game.NPCs:
                        npc.shiftOnePixel(dir, 1)
                    #self.redrawMap(map, hero, )
                    gameBoard.blit( self.getScrollingMapWindow( ( (topX*const.blocksize)+(idx*scrollX)-(const.blocksize*scrollX), 
                                                                  (topY*const.blocksize)+(idx*scrollY)-(const.blocksize*scrollY) ) ), (0,0) )
                    
                else:
                    self.redrawMap(map, hero, gameBoard)
                
                if (idx % 3) == 0:
                    
                    if hero.moving:
                        if idx in [6,12,21,27]:
                            hero.takeStep()
                    self.displayOneFrame(game.myInterface, game.FX, game.gameBoard, game, True)
            hero.moving = False
        
        for npc in game.NPCs:
            npcdir = npc.dir
            (cX, cY) = npc.getXY()
            (tX, tY) = map.topMapCorner
            (oRX, oRY, oRX2, oRY2) = npc.getRect()
            nRX = cX*const.blocksize-(tX*const.blocksize)
            nRY = cY*const.blocksize-(tY*const.blocksize)
            npc.setRect(nRX, nRY, const.blocksize, const.blocksize)
            npc.moving = False
            if npc.dir == 'up':
                npc.dir = 'down'
        hero.setRect( newX, newY, const.blocksize, const.blocksize)
        
        if map.type in const.darkMaps:
            self.redrawXMap(map, 2 + hero.hasItem(const.LANTERN), True)
        #self.redrawMap(map, hero, gameBoard)