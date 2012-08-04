import pygame
from load_image import *
from const import *
import random

from IMG import images

#import threading
import Queue

class hud( ):
    def __init__(self, screen, game):
        self.textBox1 = pygame.Surface((100, 250))
        self.textBox1.fill( gold )
        self.textBox2 = pygame.Surface((300, 100))
        self.textBox2.fill( gold )
        self.playerkeys = 0
        
        #for displaying messages or menus
        self.screen = screen
        
        self.invItems = []
        
        self.frameBox1, r = load_image("hudBox1.bmp",None)
        self.frameBox2, r = load_image("hudBox2.bmp",None)
        
        self.scrollText = ['']*5
        
        self.game = game
        self.gameBoard = game.gameBoard
        
        self.On = True
        
        images.load()
    
    def writeText(self, surface, loc, text, fgc, bgc, size=14, font=os.getcwd()+"/FONTS/gothic.ttf"):
        font = pygame.font.Font(font, size)
        surface.blit( font.render(text, 1, fgc, bgc), loc )
    
    def boxStat(self, stat, mStat, fgCol, bgCol):
        pass
        
    def update( self ):
        stats = self.game.myHero.getPlayerStats()
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) = stats
        (armor, weapon) = ( self.game.myHero.getArmorEquipped(), self.game.myHero.getWeaponEquipped() )
        self.textBox1 = pygame.Surface((100, 75))
        self.textBox1.fill( gold )
        self.frameBox1 = self.frameBox1.copy()
        if pygame.font:
            #self.writeText(self.textBox1, (0,0), "Score: "+str(scr), white, gold)
            #self.writeText(self.textBox1, (0,25), "HP: "+str(cHP)+"/"+str(mHP), white, gold)
            #self.writeText(self.textBox1, (0,50), "MP: "+str(cMP)+"/"+str(mMP), white, gold)
            self.writeText(self.textBox1, (0,0), "INT: "+str(itl), white, gold,12)
            self.writeText(self.textBox1, (30,0), "STR: "+str(sth), white, gold,12)
            self.writeText(self.textBox1, (60,0), "DEX: "+str(dex), white, gold,12)
            self.writeText(self.textBox1, (0,25), "EXP: "+str(cEX)+"/"+str(nEX), white, gold)
            self.writeText(self.textBox1, (0,50), "Keys: "+str(kys), white, gold)
        self.frameBox1.blit(self.textBox1,(25,100))
        #show equipped armor and weapon
        weaponCopy = pygame.Surface( (30,30) )
        weaponCopy.blit( images.mapImages[ weapon.getImg() ], (0,0) )
        self.writeText(weaponCopy, (17,17), 'L'+str(weapon.getLevel()), white, black, 10)
        self.frameBox1.blit(weaponCopy, (30, 180))
        
        armorLocList = [(70,180), (30,220), (70,220)]
        for A in range( len(armor) ):
            if armor[A] == None:
                pass
            else:
                armorCopy = images.mapImages[ armor[A].getImgNum() ]
                self.writeText(armorCopy, (20,20), 'L'+str(armor[A].getLevel()), white, black,10)
                self.frameBox1.blit(armorCopy, armorLocList[A])
        goldBox = pygame.Surface( (30,30) )
        goldBox.blit( images.mapImages[109], (0,0) )
        self.writeText(goldBox, (5,17), '$'+str(self.game.myHero.getGold()), white, black,10)
        self.frameBox1.blit( goldBox, (30, 260) )
        self.screen.blit(self.frameBox1, (blocksize*10+75, 75) )
        self.screen.blit(self.frameBox2, (75, blocksize*10+75) )
        self.screen.blit(self.gameBoard, (75,75) )

    
    def txtMessage(self, msg):
        self.textBox2 = pygame.Surface((400, 100))
        self.textBox2.fill( gold )
        self.scrollText[0] = self.scrollText[1]
        self.scrollText[1] = self.scrollText[2]
        self.scrollText[2] = self.scrollText[3]
        self.scrollText[3] = self.scrollText[4]
        self.scrollText[4] = msg
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 18)
            for i in range(5):
                Msg = font.render( self.scrollText[i], 1, white, gold)
                self.textBox2.blit(Msg, (0,20*i) )
        self.frameBox2.blit(self.textBox2, (25,25) )
        self.gameBoard.blit(self.frameBox2, (0, blocksize*10) )
        self.screen.blit(self.gameBoard, (75,75) )
    
   
    def boxMessage(self, text):
        for i in range(88):
            borderBox = pygame.Surface( ( ((i*2)+5 ), 60) )
            borderBox.fill( grey )
            msgBox = pygame.Surface( (i*2, 50 ) )
            msgBox.fill( gold )
            borderBox.blit(msgBox, (5, 5) )
            self.screen.blit(borderBox, (188-i, 200) )
            pygame.display.flip()
            
        borderBox = pygame.Surface( ( 186, 60 ) )
        borderBox.fill( grey )
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 18)
            msgText = font.render( text, 1, white, gold )
            msgBox.blit(msgText, (10,10) )
        borderBox.blit( msgBox, (5, 5) )
        self.screen.blit(borderBox, (100, 200) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass