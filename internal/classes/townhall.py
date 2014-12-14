import pygame
from DISPLAY import menu, text
import random, os
from OBJ import item
from SCRIPTS import shopScr, prices
from shop import Shop
from UTIL import const, colors, load_image
from math import floor, ceil

class Townhall(Shop):
    
    def __init__(self, screen, interface, ticker, iH, menu):
        Shop.__init__(self, screen, interface, 'townhall', ticker, iH, menu)
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.images = range(2)
        self.images[0], r = load_image.load_image( os.path.join('MENU', "cursor.png" ), -1)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'inn.bmp'))
        self.storeScreen.fill( colors.black )
        self.storeScreen.blit( self.images[1], (0,0) )
        self.menuBox = pygame.Surface( ( int(ceil(124*const.scaleFactor)), int(ceil(99*const.scaleFactor)) ) )
        self.name = 'townhall'
    
    def stockStore(self, level):
        itemsList = shopScr.townHallsByLevel[ level ]
        
        self.prices[level] = {}
        self.items[level] = []
        for i in itemsList:
            iT = item.Item( *i )
            iT.priceID = i
            self.items[level].append( iT )
            self.prices[level][i] = prices.priceItem(iT)
    
    def save(self, fileName, game, FX):
        return game.saveGame(fileName)
    
    def load(self, fileN):
        pass
    # loc is: (mapname, playerX, playerY )
    def enterStore(self, hero, game, FX, level, loc):
        self.gameboard_copy = game.gameBoard
        self.stockStore(level)
        self.storeScreen.blit( self.images[1], (0,0) )
        FX.scrollFromCenter(game.gameBoard, self.storeScreen)
        self.drawStoreScreen(game)
        while True:
            action = self.getAction(['Buy', 'Save', 'Return To Game', 'Exit Game'], game)
            if action == 'Return To Game':
                FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                return
            elif action == 'Save':
                #game.gameOn = False
                if self.save( 'ransack0.sav', game, FX):
                    game.textMessage('Game Saved')
                else: game.textMessage('File Error o_O')
                FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                return
            elif action == 'Buy':                
                self.ticker.tick(60)
                purchase = self.buy(game, self.items[level], self.prices[level])
                if purchase == None: pass
                elif hero.takeGold( self.prices[level][purchase.priceID] ):
                    if purchase.certNum == const.RETURNCERT:
                        purchase.loc = (loc[0], loc[1][0], loc[1][1])
                    hero.getItem( purchase )
                    self.stockStore(level)
                else: game.textMessage("You don't have enough money!")
            elif action == 'Load':
                game.gameOn = False
                game.exitCode = 1
                filename = self.getFile()
                self.load( filename )
                game.loadFileName = filename
                FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                return
            elif action == 'Exit Game':
                game.gameOn = False
                game.exitCode = 0
                game.loadFileName = None
                return
            self.drawStoreScreen(game)