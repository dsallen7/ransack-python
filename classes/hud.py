import pygame
from load_image import *
from const import *
import random

class hud():
    def __init__(self, screen):
        self.textBox1 = pygame.Surface((100, 250))
        self.textBox1.fill( yellow )
        self.textBox2 = pygame.Surface((300, 100))
        self.textBox2.fill( yellow )
        self.playerkeys = 0
        
        #for displaying messages or menus
        self.screen = screen
        
        self.invItems = []
        
        self.frameBox1, r = load_image("hudBox1.bmp",-1)
        self.frameBox2, r = load_image("hudBox2.bmp",-1)
        
        self.scrollText = ['']*3

    def displayStats(self, gameBoard, stats):
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) = stats
        self.textBox1 = pygame.Surface((100, 250))
        self.textBox1.fill( yellow )
        self.frameBox1 = self.frameBox1.copy()
        if pygame.font:
            font = pygame.font.SysFont("arial", 18)
            scoretext = font.render( "Score: "+str(scr), 1, white, yellow )
            self.textBox1.blit(scoretext, (0,0) )
            lifetext = font.render( "HP: "+str(cHP)+"/"+str(mHP), 1, white, yellow)
            self.textBox1.blit(lifetext, (0,25) )
            magtext = font.render( "MP: "+str(cMP)+"/"+str(mMP), 1, white, yellow)
            self.textBox1.blit(magtext, (0,50) )
            magtext = font.render( "Int: "+str(itl), 1, white, yellow)
            self.textBox1.blit(magtext, (0,75) )
            magtext = font.render( "Str: "+str(sth), 1, white, yellow)
            self.textBox1.blit(magtext, (0,100) )
            magtext = font.render( "Dex: "+str(dex), 1, white, yellow)
            self.textBox1.blit(magtext, (0,125) )
            magtext = font.render( "Exp: "+str(cEX)+"/"+str(nEX), 1, white, yellow)
            self.textBox1.blit(magtext, (0,150) )
            keytext = font.render( "Keys: "+str(kys), 1, white, yellow)
            self.textBox1.blit(keytext, (0,175) )
        self.frameBox1.blit(self.textBox1,(25,25))
        gameBoard.blit(self.frameBox1, (blocksize*10, 0) )
        gameBoard.blit(self.frameBox2, (0, blocksize*10) )
    
    def msgSystem(self,gameBoard, msg):
        self.textBox2 = pygame.Surface((500, 100))
        self.textBox2.fill( yellow )
        self.scrollText[0] = self.scrollText[1]
        self.scrollText[1] = self.scrollText[2]
        self.scrollText[2] = msg
        if pygame.font:
            font = pygame.font.SysFont("arial", 18)
            for i in range(3):
                Msg = font.render( self.scrollText[i], 1, white, yellow)
                self.textBox2.blit(Msg, (0,20*i) )
        self.frameBox2.blit(self.textBox2, (25,25) )
        gameBoard.blit(self.frameBox2, (0, blocksize*10) )

    def hurt(self):
        if self.playerlife > 10:
            self.playerlife -= 10
        else:
            self.newGame.gameover()
            
    def takeKey(self):
        self.playerkeys -= 1
        self.message("The door unlocks")

    def getItem(self,type,stats):
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) = stats
        if type == 5:
            if cHP < mHP:
                cHP += 10
            else:
                cHP = mHP
            scr += 10
        if type == 2:
            kys += 1
            self.message("You got a key")
        if type == 6:
            self.invItems += ['hp']
            self.message("You found a healing potion")
        if type == 7:
            self.invItems += ['mp']
            self.message("You found a magic potion")
        return (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX)
    
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
            font = pygame.font.SysFont("arial", 18)
            msgText = font.render( text, 1, white, yellow )
            msgBox.blit(msgText, (10,10) )
        borderBox.blit( msgBox, (5, 5) )
        self.screen.blit(borderBox, (100, 200) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass