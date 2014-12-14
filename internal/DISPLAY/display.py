import pygame
from IMG import images
from UTIL import colors, const
from math import ceil
from SCRIPTS import mapScr


class Display():

    def __init__(self, screen, images):
        self.screen = screen
        #images.load()
        self.images = images.mapImages
        #self.images = images
        self.fog = pygame.Surface((30, 30))
        self.fog.fill(colors.black)

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
            '''
            self.screen.blit( pygame.transform.scale(board,
                                                           (int(ceil(300 * const.scaleFactor)),
                                                            int(ceil(300 * const.scaleFactor)) ) ), (100,100) )'''
        pygame.display.flip()

    def drawShade(self, map, gameBoard):
        """Takes first two coordinates of hero rect, gameBoard and
        draws darkness
        """
        (topX, topY) = map.topMapCorner
        (px, py) = map.playerXY
        tiles = map.litTiles
        for x in range(map.WINDOWSIZE):
            for y in range(map.WINDOWSIZE):
                if (x + topX, y + topY) in tiles:
                    self.fog.set_alpha(0)
                else:
                    self.fog.set_alpha(140)
                gameBoard.blit(self.fog, ((x) * const.blocksize,
                    (y) * const.blocksize), area=(0, 0, const.blocksize,
                    const.blocksize))

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

    def redrawMap(self, map, hero, gameBoard):
        """Redraw map on screen from current map matrix
        """
        #self.revealMap()
        (rx, ry, rx2, ry2) = hero.getRect()
        rx = rx / const.blocksize
        ry = ry / const.blocksize
        (topX, topY), (oldTopX, oldTopY) = map.updateWindowCoordinates(hero)
        gameBoard.blit(self.getMapWindow((topX, topY),
            map.WINDOWSIZE), (map.WINDOWOFFSET, map.WINDOWOFFSET))
        if map.type in ['dungeon', 'maze', 'fortress']:
            self.drawShade(map, gameBoard)
            #self.drawDarkness(rx, ry, gameBoard)

    def getMapWindow(self, pos, wsize=10):
        """takes map coordinates, returns map window
        """
        (x1, y1) = pos
        window = pygame.Surface((
            wsize * const.blocksize, wsize * const.blocksize))
        window.blit(self.xGameBoard, (-(x1 * const.blocksize),
                                      -(y1 * const.blocksize)))
        return window

    def getScrollingMapWindow(self, pos, wsize=10, darkness=True):
        """ takes pixel coordinates of top left corner of
        DIMxDIM window of xGameBoard, returns map window
        """
        (x1, y1) = pos
        window = pygame.Surface((wsize * const.blocksize,
                                 wsize * const.blocksize))
        window.blit(self.xGameBoard, (-x1, -y1))
        #self.drawDarkness
        return window

    def redrawXMap(self, thismap, light, local=False):
        """draws entire map to DIMxDIM Surface
            light: number of tiles visible from player
        """
        self.xGameBoard = pygame.Surface((thismap.getDIM() * const.blocksize,
             thismap.getDIM() * const.blocksize))
        if thismap.type in const.darkMaps:
            thismap.revealMap(light)
        if local:
            (tX, tY) = thismap.topMapCorner
            rX = range(tX-1, tX+const.HALFDIM+1)
            rY = range(tY-1, tY+const.HALFDIM+1)
        else:
            (rX, rY) = ( range(thismap.getDIM()), range(thismap.getDIM()) )
        for x in rX:
            for y in rY:
                fTile = thismap.getTileFG(x,y)
                bTile = thismap.getTileBG(x,y)
                if fTile != const.VOID and thismap.visDict[(x,y)]:
                    # draw background tile first
                    if bTile is not None:
                        self.xGameBoard.blit( self.images[ bTile ], ( (x*const.blocksize), (y*const.blocksize) ) )
                    # then foreground
                    else: self.xGameBoard.blit( self.images[ thismap.defaultBkgd ], ( (x*const.blocksize), (y*const.blocksize) ) )
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

                    nbrL = thismap.getTileFG(x-1, y)
                    nbrU = thismap.getTileFG(x, y-1)
                    nbrUL = thismap.getTileFG(x-1, y-1)
                    if nbrL in mapScr.pines and nbrU in mapScr.pines and nbrUL in mapScr.pines and fTile in mapScr.pines:
                        self.xGameBoard.blit( self.images[ mapScr.pineDict[fTile] ],
                                              ( (x*const.blocksize)-(const.blocksize/2),
                                                (y*const.blocksize)-(const.blocksize/2) ) )
                    # put accessories on the table
                    if fTile in range(const.TABLE1, const.TABLE3+1):
                        try:
                            self.xGameBoard.blit( self.accImages[thismap.grid[x][y].accessory],
                                                  ( x*const.blocksize+10,
                                                    y*const.blocksize+5) )
                        except AttributeError:
                            pass
            '''
        for x in range(thismap.getDIM()):
            for y in range(thismap.getDIM()):
                tile = thismap.getEntry(x, y)
                if tile != const.VOID and thismap.visDict[(x, y)]:

                    if tile > 24:
                        shortList = [thismap.getEntry(tx, ty) for (
                            tx, ty) in thismap.neighbors((x, y))]
                        if const.VOID not in shortList:
                            self.xGameBoard.blit(
                                self.images[thismap.defaultBkgd], ((
                                x * const.blocksize), (
                                y * const.blocksize)))
                    if thismap.getEntry(x, y) == const.ITEMSDOOR:
                        self.xGameBoard.blit(self.images[128],
                            (x * const.blocksize - const.blocksize,
                            y * const.blocksize - 2 * const.blocksize),
                            area=self.images[128].get_rect())
                    else:
                        self.xGameBoard.blit(self.images[tile],
                            ((x * const.blocksize), (y * const.blocksize)))'''
        if thismap.type == 'village':
            for s in thismap.shops:
                if thismap.shops[s][0] == 'itemshop':
                    (sX, sY) = s
                    self.xGameBoard.blit(self.images[128],
                        (sX * const.blocksize - const.blocksize,
                         sY * const.blocksize - (2 * const.blocksize)))
                if thismap.shops[s][0] == 'magicshop':
                    (sX, sY) = s
                    self.xGameBoard.blit(self.images[129],
                        (sX * const.blocksize - const.blocksize,
                        sY * const.blocksize - (2 * const.blocksize)))
                if thismap.shops[s][0] == 'blacksmith':
                    (sX, sY) = s
                    self.xGameBoard.blit(self.images[130],
                        (sX * const.blocksize - const.blocksize,
                         sY * const.blocksize - (2 * const.blocksize)))
                if thismap.shops[s][0] == 'armory':
                    (sX, sY) = s
                    self.xGameBoard.blit(self.images[131],
                        (sX * const.blocksize - const.blocksize,
                        sY * const.blocksize - (2 * const.blocksize)))
                if thismap.shops[s][0] == 'tavern':
                    (sX, sY) = s
                    self.xGameBoard.blit(self.images[132],
                        (sX * const.blocksize - const.blocksize,
                         sY * const.blocksize - (3 * const.blocksize)))

    def drawSprites(self, hero, map, gameBoard, game=None, dir=None,
            animated=True):
        """draws all pending sprite movements
        """
        DIMEN = map.getDIM()
        # by default, the hero is in the upper left corner of the map
        (newX, newY) = hero.getXY()
        map.setPlayerXY(newX / const.blocksize, newY / const.blocksize)
        (oldX, oldY, c, d) = hero.getRect()
        scrolling = False
        delta = int(ceil(float(DIMEN) / 2.))
        if map.getDIM() % 2 == 0:
            delta = delta + 1
        if DIMEN > const.HALFDIM:
            if (5 * const.blocksize <= newX <= (DIMEN - 5) * const.blocksize):
                newX = 5 * const.blocksize
                if dir in ['left', 'right'] and oldX == 5 * const.blocksize:
                    scrolling = True
            if newX > (DIMEN - 5) * const.blocksize:
                newX = newX - delta * const.blocksize
                if newX > const.HALFDIM * const.blocksize:
                    newX = newX - 300
            if (5 * const.blocksize <= newY <= (DIMEN - 5) * const.blocksize):
                newY = 5 * const.blocksize
                if dir in ['up', 'down'] and oldY == 5 * const.blocksize:
                    scrolling = True
            if newY > (DIMEN - 5) * const.blocksize:
                newY = newY - delta * const.blocksize
                if newY > const.HALFDIM * const.blocksize:
                    newY = newY - 300
        else:
            newX += (const.HALFDIM - DIMEN) / 2 * const.blocksize
            newY += (const.HALFDIM - DIMEN) / 2 * const.blocksize

        #make the move animated
        if animated:
            if not hero.moving:
                scrolling = False
            else:
                scrollX, scrollY = const.scrollingDict[dir]
            (px, py) = hero.getXY()
            pos, oldPos = map.updateWindowCoordinates(hero)
            (topX, topY) = pos
            if oldX == newX:
                xAxis = [oldX] * const.blocksize
            elif oldX < newX:
                xAxis = range(oldX, newX)
            else:
                xAxis = range(oldX, newX, -1)
            if oldY == newY:
                yAxis = [oldY] * const.blocksize
            elif oldY < newY:
                yAxis = range(oldY, newY)
            elif oldY > newY:
                yAxis = range(oldY, newY, -1)
            for (idx, (i, j)) in list(enumerate(zip(xAxis, yAxis), start=1)):

                game.clock.tick(200)
                hero.setRect(i, j, const.blocksize, const.blocksize)
                for npc in game.NPCs:
                    if npc.moving:
                        npc.shiftOnePixel(npc.dir, -1)
                        if (idx % 2 == 0):
                            npc.takeStep()
                if scrolling:
                    for npc in game.NPCs:
                        npc.shiftOnePixel(dir, 1)

                    gameBoard.blit(self.getScrollingMapWindow(((
                        topX * const.blocksize) + (idx * scrollX) -
                        (const.blocksize * scrollX), (topY * const.blocksize) +
                        (idx * scrollY) - (const.blocksize * scrollY))),
                            (0, 0))

                    if map.type in ['dungeon', 'maze', 'fortress']:
                        self.drawShade(map, gameBoard)
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
            nRX = cX * const.blocksize - (tX * const.blocksize)
            nRY = cY * const.blocksize - (tY * const.blocksize)
            npc.setRect(nRX, nRY, const.blocksize, const.blocksize)
            npc.moving = False
        hero.setRect(newX, newY, const.blocksize, const.blocksize)
        self.redrawXMap(map, 2)
        self.redrawMap(map, hero, gameBoard)
