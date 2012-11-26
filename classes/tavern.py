import pygame, cPickle, gzip
from load_image import *
from DISPLAY import menu, text
from IMG import images
import random, os
from OBJ import item
from SCRIPTS import shopScr

from UTIL import const, colors

from math import floor, ceil

class Tavern():
    
    def __init__(self, screen, interface, ticker, iH, menu):
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.screen = screen
        self.myInterface = interface
        self.ticker = ticker
        images.load()
        self.myMenu = menu
        self.images = range(2)
        self.images[0], r = load_image('cursor.bmp', -1)
        self.images[1], r = load_image( os.path.join('INT', 'inn.bmp'))
        self.storeScreen.fill( colors.black )
        self.storeScreen.blit( self.images[1], (0,0) )
        self.inputHandler = iH
        self.menuBox = pygame.Surface( ( int(ceil(124*2.4)), int(ceil(99*2.4)) ) )
    
    def drawStoreScreen(self):
        #self.myInterface.update()
        #self.screen.blit( pygame.transform.scale(self.storeScreen, (720, 720) ), (0, 0) )
        storeScreen_ = pygame.transform.scale(self.storeScreen, (720, 720) )
        storeScreen_.blit( self.menuBox, ( int(ceil(165*2.4)),
                                               int(ceil(190*2.4))) )
        self.screen.blit( storeScreen_, (0, 0) )
        pygame.display.flip()
    
    def getAction(self):
        options = ['Sleep', 'Return To Game']
        selection = 0
        while True:
            self.menuBox.fill( colors.gold )
            if pygame.font:
                for i in range(len(options)):
                    self.menuBox.blit( text.Text(options[i], os.getcwd()+"/FONTS/Squealer.ttf", const.shopTextFontSize), ( int(ceil(25*2.4)),
                                                                                                                      i*int(ceil(25*2.4)) ) )
            for event in pygame.event.get():
                event_ = self.inputHandler.getCmd(event)
                if event_ == pygame.K_UP:
                    selection -= 1
                    if selection == -1:
                        selection = len(options)-1
                if event_ == pygame.K_DOWN:
                    selection += 1
                    if selection == len(options):
                        selection = 0
                if event_ == pygame.K_RETURN:
                    return options[selection]
            self.menuBox.blit( self.images[0], (0, selection* int(ceil(25*2.4)) ) )
            #self.storeScreen.blit( menuBox, (165,190) )
            self.drawStoreScreen()
    
    def enterStore(self, hero, game, FX):
        self.storeScreen.blit( self.images[1], (0,0) )
        FX.scrollFromCenter(game.gameBoard, self.storeScreen)
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Return To Game':
                FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                return
            elif action == 'Sleep':
                if hero.takeGold( (hero.getMaxHP()-hero.getCurrHP()) /2 ):
                    game.textMessage('Your HP and MP are now full')
                    game.textMessage('Thank you for staying with us!')
                    hero.refillPts()
                    FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                    return
                else:
                    game.textMessage('Sorry! come back when you get paid!')
            self.drawStoreScreen()