import pygame
from load_image import *
from const import *
import random

class hud():
    def __init__(self, screen):
        self.box = pygame.Surface((80, 250))
        self.box.fill( yellow )
        self.playerscore = 0
        self.playerlife = 50
        self.playerkeys = 0
        
        #for displaying messages or menus
        self.screen = screen
        
        self.invItems = []

    def update(self, gameBoard):
        self.box = self.box.copy()
        if pygame.font:
            font = pygame.font.SysFont("arial", 24)
            scoretext = font.render( "Score: "+str(self.playerscore), 1, red, yellow )
            self.box.blit(scoretext, (0,0) )
            lifetext = font.render( "Life: ", 1, red, yellow)
            self.box.blit(lifetext, (0,25) )
            keytext = font.render( "Keys: "+str(self.playerkeys), 1, red, yellow)
            self.box.blit(keytext, (0,80) )
        backbar = pygame.Surface((100,10))
        lifebar = pygame.Surface((self.playerlife,10))
        backbar.fill( yellow )
        lifebar.fill(red)
        self.box.blit(backbar, (0,55) )
        self.box.blit(lifebar, (0,55) )
        gameBoard.blit(self.box, (blocksize*10, 0) )

    def hurt(self):
        if self.playerlife > 10:
            self.playerlife -= 10
        else:
            self.newGame.gameover()
            
    def takeKey(self):
        self.playerkeys -= 1
        self.message("The door unlocks")

    def getItem(self,type):
        if type == 5:
            if self.playerlife < 90:
                self.playerlife += 10
            else:
                self.playerlife = 100
            self.playerscore += 10
        if type == 2:
            self.playerkeys += 1
            self.message("You got a key")
        if type == 6:
            self.invItems += ['hp']
            self.message("You found a healing potion")
    
    def getItemsList(self):
        return self.invItems
    
    def message(self, text):
        for i in range(88):
            borderBox = pygame.Surface( ( ((i*2)+5 ), 60) )
            borderBox.fill( grey )
            msgBox = pygame.Surface( (i*2, 50 ) )
            msgBox.fill( yellow )
            borderBox.blit(msgBox, (5, 5) )
            self.screen.blit(borderBox, (188-i, 200) )
            pygame.display.flip()
            
        borderBox = pygame.Surface( ( 186, 60 ) )
        borderBox.fill( grey )
        if pygame.font:
            font = pygame.font.SysFont("arial", 24)
            msgText = font.render( text, 1, red, yellow )
            msgBox.blit(msgText, (10,10) )
        borderBox.blit( msgBox, (5, 5) )
        self.screen.blit(borderBox, (100, 200) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass