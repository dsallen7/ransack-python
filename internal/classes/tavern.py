import pygame, cPickle, gzip
from DISPLAY import menu, text
import random, os
from OBJ import item
from SCRIPTS import shopScr
from shop import Shop
from UTIL import const, colors, load_image

from math import floor, ceil

class Tavern(Shop):
    
    def __init__(self, screen, interface, ticker, iH, menu):
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.screen = screen
        self.myInterface = interface
        self.ticker = ticker
        self.myMenu = menu
        self.images = range(2)
        self.images[0], r = load_image.load_image( os.path.join('MENU', "cursor.png" ), -1)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'inn.bmp'))
        self.storeScreen.fill( colors.black )
        self.storeScreen.blit( self.images[1], (0,0) )
        self.inputHandler = iH
        self.menuBox = pygame.Surface( ( int(ceil(124*const.scaleFactor)), int(ceil(99*const.scaleFactor)) ) )

    def enterStore(self, hero, game, FX):
        self.gameboard_copy = game.gameBoard
        self.storeScreen.blit( self.images[1], (0,0) )
        FX.scrollFromCenter(game.gameBoard, self.storeScreen)
        self.drawStoreScreen(game)
        while True:
            action = self.getAction(['Sleep', 'Return To Game'], game)
            if action == 'Return To Game':
                FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                return
            elif action == 'Sleep':
                if hero.takeGold( (hero.getMaxHP()-hero.getCurrHP()) /2 ):
                    game.textMessage('Your HP and MP are now full')
                    game.textMessage('Thank you for staying with us!')
                    hero.refillPts(True)
                    FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                    return
                else:
                    game.textMessage('Sorry! come back when you get paid!')
            self.drawStoreScreen(game)