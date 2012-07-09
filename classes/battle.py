import pygame
from load_image import *
from const import *
import random

# this class will be used to draw the animation occuring in the battle.

class battle():
    
    def __init__(self, screen):
        self.battleField = pygame.Surface( (300,300) )
        self.battleField.fill( black )
        self.images = range(3)
        
        self.screen = screen
        
        self.images[0], r = load_image('cursor.bmp')
    
    def drawBattleScreen(self):
        self.screen.blit( self.battleField, (75,75) )
        pygame.display.flip()
    
    # displays battle menu and waits for player to select choice,
    # returns choice to fightBattle()
    def getAction(self):
        menuBox = pygame.Surface( (50,100) )
        options = ['Fight', 'Magic', 'Item', 'Flee']
        selection = 0
        while True:
            menuBox.fill( yellow )
            if pygame.font:
                font = pygame.font.SysFont("arial", 10)
                for i in range(4):
                    menuBox.blit( font.render(options[i], 1, white, yellow), (25,i*25) )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection -= 1
                        if selection == -1:
                            selection = 3
                    if event.key == pygame.K_DOWN:
                        selection += 1
                        if selection == 4:
                            selection = 0
                    if event.key == pygame.K_RETURN:
                        return options[selection]
            menuBox.blit( self.images[0], (0, selection*25) )            
            self.battleField.blit( menuBox, (200,150) )
            self.drawBattleScreen()
    
    def commence(self, screen):
        while (pygame.event.wait().type != pygame.KEYDOWN): pass