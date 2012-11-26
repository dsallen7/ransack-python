import pygame
from IMG import images
from UTIL import colors, const
from math import ceil, floor

# Main graphics engine for Ransack.

class Display():
    
    def __init__(self, screen):
        self.screen = screen
        images.load()
        self.images = images.mapImages
        self.fog = pygame.Surface( (30,30) )
        self.fog.fill( colors.offblack )
    
    def displayOneFrame(self, iFace, FX, board=None, game=None, dark=False):
        if game is not None:
            game.updateSprites()
            iFace.update(game)
            #board.blit( game.myHero.showLocation(), (0,50) )
        FX.update(self.screen)
        if board is not None:
            if dark:
                self.drawDarkness(game.myMap, board)
                #board.blit( self.SS_, (0, 0) )
            self.screen.blit( pygame.transform.scale(board, 
                                                     (int(ceil(300 * 2.4)), 
                                                      int(ceil(300 * 2.4)) ) ), (0,0) )
        pygame.display.flip()
    
    # Takes first two coordinates of hero rect, gameBoard and
    # draws darkness
    def drawDarkness(self, map, gameBoard):
        (topX, topY) = map.topMapCorner
        (px, py) = map.playerXY
        tiles = map.litTiles
        for x in range( map.WINDOWSIZE ):
            for y in range( map.WINDOWSIZE ):
                if (x+topX, y+topY) in tiles:
                    self.fog.set_alpha( 0 )
                else:
                    self.fog.set_alpha( 192 )
                gameBoard.blit(self.fog, 
                               ( (x)*const.blocksize, (y)*const.blocksize), 
                               area=(0,0,const.blocksize,const.blocksize) )
    
    # Redraw map onto gameboard without redrawing tiles
    def redrawMap(self, map, hero, gameBoard):
        (rx,ry,rx2,ry2) = hero.getRect()
        rx = rx/const.blocksize
        ry = ry/const.blocksize
        #map.setPlayerXY(rx, ry)
        (topX, topY), (oldTopX, oldTopY) = map.updateWindowCoordinates(hero)
        gameBoard.blit( self.getMapWindow( (topX, topY), map.WINDOWSIZE ), (map.WINDOWOFFSET,map.WINDOWOFFSET) )
    
    # takes map coordinates, returns map window
    def getMapWindow(self, pos, wsize=10):
        (x1, y1) = pos
        window = pygame.Surface( (wsize*const.blocksize, wsize*const.blocksize) )
        window.blit( self.xGameBoard, ( -(x1*const.blocksize), -(y1*const.blocksize) ) )
        return window
    # takes pixel coordinates of top left corner of DIMxDIM window of xGameBoard, returns map window
    def getScrollingMapWindow(self, pos, wsize = 10, darkness=True):
        (x1,y1) = pos
        window = pygame.Surface( (wsize*const.blocksize, wsize*const.blocksize) )
        window.blit( self.xGameBoard, ( -x1, -y1 ) )
        #self.drawDarkness
        return window
    # draws entire map to DIMxDIM Surface
    def redrawXMap(self, map):
        self.xGameBoard = pygame.Surface( (map.getDIM()*const.blocksize, map.getDIM()*const.blocksize) )
        if map.type in ['dungeon', 'maze', 'fortress']:
            map.revealMap()
        for x in range(map.getDIM()):
            for y in range(map.getDIM()):
                tile = map.getEntry(x,y)
                if tile != const.VOID and map.visDict[(x,y)]:
                    self.xGameBoard.blit( self.images[ map.defaultBkgd ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    '''
                    if tile > 24:
                        shortList = [map.getEntry(tx, ty) for (tx, ty) in map.neighbors((x,y))]
                        if const.VOID not in shortList:
                            self.xGameBoard.blit( self.images[ map.defaultBkgd ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    
                    if map.getEntry(x, y) == const.ITEMSDOOR:
                        self.xGameBoard.blit( self.images[128], (x*const.blocksize - const.blocksize, y*const.blocksize - 2*const.blocksize), area = self.images[128].get_rect() )
                    else: self.xGameBoard.blit( self.images[ tile ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    '''
                    self.xGameBoard.blit( self.images[ tile ], ( (x*const.blocksize), (y*const.blocksize) ) )
        if map.type == 'village':
            for s in map.shops:
                (sX, sY) = s
                self.xGameBoard.blit( self.images[ images.siteImgDict[ map.shops[s][0] ][0] ], 
                                      (sX*const.blocksize - const.blocksize, 
                                       sY*const.blocksize - (images.siteImgDict[ map.shops[s][0] ][1]*const.blocksize)) )
    
    # draws all pending sprite movements
    def drawSprites(self, hero, map, gameBoard, game=None, dir=None, animated=True):
        DIMEN = map.getDIM()
        # by default, the hero is in the upper left corner of the map
        (newX,newY) = hero.getXY()
        map.setPlayerXY(newX/const.blocksize, newY/const.blocksize)
        (oldX, oldY, c, d) = hero.getRect()
        scrolling = False
        delta = int( ceil( float(DIMEN)/2.) )
        if map.getDIM() % 2 == 0:
            delta = delta + 1
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
        
        
        # use this to control speed of animation
        
        # speedFactor of 1 is normal speed, 2 is 2x as fast, etc.
        
        speedFactor = 1
       
        #make the move animated
        if animated:
            if not hero.moving:
                scrolling = False
            else: scrollX , scrollY = const.scrollingDict[dir]
            (px,py) = hero.getXY()
            pos, oldPos = map.updateWindowCoordinates( hero )
            (topX, topY) = pos
            if oldX == newX:
                xAxis = [oldX] * (const.blocksize/speedFactor)
            elif oldX < newX:
                xAxis = range(oldX, newX, speedFactor)
            else:
                xAxis = range(oldX, newX, -speedFactor)
            if oldY == newY:
                yAxis = [oldY] * (const.blocksize/speedFactor)
            elif oldY < newY:
                yAxis = range(oldY, newY, speedFactor)
            elif oldY > newY:
                yAxis = range(oldY, newY, -speedFactor)
            for (idx, (i, j)) in list( enumerate(zip(xAxis, yAxis), start=1) ):
                hero.setRect( i, j, const.blocksize, const.blocksize)
                for npc in game.NPCs:
                    if npc.moving:
                        npc.shiftOnePixel(npc.dir, -1)
                        npc.takeStep()
                if scrolling:
                    for npc in game.NPCs:
                        npc.shiftOnePixel(dir, 1)
                    
                    gameBoard.blit( self.getScrollingMapWindow( ( (topX*const.blocksize)+(idx*scrollX)-(const.blocksize*scrollX), (topY*const.blocksize)+(idx*scrollY)-(const.blocksize*scrollY) ) ), (0,0) )
                    
                else:
                    self.redrawMap(map, hero, gameBoard)
                if hero.moving: hero.takeStep()
                if (idx % 5) == 0:
                    self.displayOneFrame(game.myInterface, game.FX, game.gameBoard, game, map.type in ['dungeon', 'maze', 'fortress'])
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
        hero.setRect( newX, newY, const.blocksize, const.blocksize)
        self.redrawXMap(map)
        self.redrawMap(map, hero, gameBoard)