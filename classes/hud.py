import pygame
from load_image import *
from const import *
import random

#import threading
import Queue

class hud( ):
    def __init__(self, screen, game):
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
        
        self.weaponImg = range(4)
        self.weaponImg[0], r = load_image("sword.bmp",-1)
        
        self.armorImg = range(3)
        self.armorImg[0], r = load_image("bplate.bmp",None)
        self.armorImg[2], r = load_image("shield.bmp",None)
        
        self.scrollText = ['']*3
        
        self.game = game
        self.gameBoard = game.gameBoard
        
        self.On = True
        
        #self.Queue = Q
        #self.queueLock = QL
        
        #threading.Thread.__init__ ( self )
    
    def writeText(self, surface, loc, text, fgc, bgc, size=18, font="arial"):
        font = pygame.font.SysFont(font, size)
        surface.blit( font.render(text, 1, fgc, bgc), loc )
        
    def update( self ):
        stats = self.game.myHero.getPlayerStats()
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) = stats
        (armor, weapon) = ( self.game.myHero.getArmorEquipped(), self.game.myHero.getWeaponEquipped() )
        self.textBox1 = pygame.Surface((100, 250))
        self.textBox1.fill( yellow )
        self.frameBox1 = self.frameBox1.copy()
        if pygame.font:
            self.writeText(self.textBox1, (0,0), "Score: "+str(scr), white, yellow)
            self.writeText(self.textBox1, (0,25), "HP: "+str(cHP)+"/"+str(mHP), white, yellow)
            self.writeText(self.textBox1, (0,50), "MP: "+str(cMP)+"/"+str(mMP), white, yellow)
            self.writeText(self.textBox1, (0,75), "Int: "+str(itl), white, yellow,12)
            self.writeText(self.textBox1, (25,75), "Str: "+str(sth), white, yellow,12)
            self.writeText(self.textBox1, (50,75), "Dex: "+str(dex), white, yellow,12)
            self.writeText(self.textBox1, (0,150), "Exp: "+str(cEX)+"/"+str(nEX), white, yellow)
            self.writeText(self.textBox1, (0,175), "Keys: "+str(kys), white, yellow)
        self.frameBox1.blit(self.textBox1,(25,25))
        #show equipped armor and weapon
        weaponCopy = self.weaponImg[weapon[1]]
        self.writeText(weaponCopy, (20,20), str(weapon[0]), white, black, 8)
        self.frameBox1.blit(weaponCopy, (25, 250))
        
        armorLocList = [(60,250), (25,290), (60,290)]
        for A in range( len(armor) ):
            if armor[A] == None:
                pass
            else:
                armorCopy = self.armorImg[ A ]
                self.writeText(armorCopy, (20,20), str(armor[A]), white, black,8)
                self.frameBox1.blit(armorCopy, armorLocList[A])
        '''
        # check for messages
        self.queueLock.acquire()
        if not self.Queue.empty():
            data = self.Queue.get()
            (fn, msg) = data
            if fn == 0:
                self.boxMessage(msg)
            else: self.txtMessage(msg)
            self.queueLock.release()
        else:
            self.queueLock.release()
        '''
        self.gameBoard.blit(self.frameBox1, (blocksize*10, 0) )
        self.gameBoard.blit(self.frameBox2, (0, blocksize*10) )
        self.screen.blit(self.gameBoard, (75,75) )

    
    def txtMessage(self, msg):
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
        self.gameBoard.blit(self.frameBox2, (0, blocksize*10) )
        self.screen.blit(self.gameBoard, (75,75) )
    
   
    def boxMessage(self, text):
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