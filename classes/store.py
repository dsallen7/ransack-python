import pygame
import menu
from load_image import *
from const import *
from classes import menu
from IMG import images
import random

class Store():
    
    def __init__(self, screen, hud):
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.screen = screen
        self.myHud = hud
        images.load()
        self.myMenu = menu.menu(screen)
        self.images = range(2)
        self.images[0], r = load_image('cursor.bmp')
    
    def drawStoreScreen(self):
        self.screen.blit( self.storeScreen, (75,75) )
        
        #enemyHPBox = pygame.Surface( (100,50) )
        #self.writeText( enemyHPBox, (0,0), 
        pygame.display.flip()
        
    # displays battle menu and waits for player to select choice,
    # returns choice to fightBattle()
    def getAction(self):
        menuBox = pygame.Surface( (60,75) )
        options = ['Buy', 'Sell', 'Exit']
        selection = 0
        while True:
            menuBox.fill( yellow )
            if pygame.font:
                font = pygame.font.SysFont("URW Chancery L", 14)
                for i in range(3):
                    menuBox.blit( font.render(options[i], 1, white, yellow), (25,i*25) )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection -= 1
                        if selection == -1:
                            selection = 2
                    if event.key == pygame.K_DOWN:
                        selection += 1
                        if selection == 3:
                            selection = 0
                    if event.key == pygame.K_RETURN:
                        return options[selection]
            menuBox.blit( self.images[0], (0, selection*25) )            
            self.storeScreen.blit( menuBox, (200,150) )
            self.drawStoreScreen()
    
    def sell(self):
        pass
    
    def buy(self):
        pass
    
    def enterStore(self):
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit':
                return
            elif action == 'Buy':
                self.buy()
            elif action == 'Sell':
                self.sell()