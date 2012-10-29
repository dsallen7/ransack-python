import pygame, os

from DISPLAY import text
from UTIL import load_image, const, colors, slider

from IMG import images

from random import randrange

class Creator():
    
    def __init__(self):
        self.displayField, r = load_image.load_image("createBox.bmp")
        self.baseHP = randrange(25, 35)
        self.baseMP = randrange(15, 25)
        self.bStr = randrange(6, 10)
        self.bItl = randrange(8, 10)
        self.bDex = randrange(8, 10)
        self.sliders = [slider.Slider(216, 145),slider.Slider(172, 131),slider.Slider(101, 61, 0, 1)]
        self.gender = 'male'
        self.cursor, r = load_image.load_image("cursor.bmp", -1)
        
        images.load()
    
    # Displays string-formatted statistic
    def displayStat(self, stat, loc):
        (x,y) = loc
        statT = text.Text( stat, os.getcwd()+"/FONTS/devinne.ttf", 18, colors.white, colors.black, transparent=True )
        self.displayField.blit( statT, (x,y) )
        
    def slide(self, sldr, screen):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    return
                elif event.type == pygame.MOUSEMOTION:
                    (mX, mY) = pygame.mouse.get_pos()
                    if 150 + sldr.getYLoc() <= mY <= 150 + sldr.getYLoc() + sldr.getMax()*10:
                        sldr.setValue( (mY - (150 + sldr.getYLoc()) ) / 10 )
            self.updateDisplay(screen)
            
    def calculateStats(self):
        # goes up with
        self.HP = self.baseHP + (self.sliders[0].getMax() - self.sliders[0].getValue() ) * 10
        # goes down with
        self.MP = self.baseMP + self.sliders[0].getValue() * 10
        self.str = self.bStr + ( ( ( (self.sliders[0].getMax() -  self.sliders[1].getValue() ) * 10 ) / 2 ) / 5 ) + 2*(1-self.sliders[2].getValue())
        self.itl = self.bItl + (       ( self.sliders[1].getValue()   * 10 ) / 4 ) / 5
        self.dex = self.bDex + ( (     ( self.sliders[1].getValue()   * 10 ) / 2 ) / 5 ) + 2*self.sliders[2].getValue()
    
    def updateDisplay(self, screen):
        self.calculateStats()
        self.displayField, r = load_image.load_image("createBox.bmp")
        self.displayStat( str(self.HP), (150,62) )
        self.displayStat( str(self.MP), (200,62) )
        self.displayStat( str(self.str), (150,102) )
        self.displayStat( str(self.itl), (200,102) )
        self.displayStat( str(self.dex), (250,102) )
        for s in self.sliders:
            self.displayField.blit(self.cursor, (s.getXLoc(), s.getYLoc()+(s.getValue()*10)) )
        if self.sliders[2].getValue() == 0:
            self.gender = 'Male'
            self.displayField.blit(images.mHeroImages[8], (40 , 59) )
        else:
            self.gender = 'Female'
            self.displayField.blit(images.fHeroImages[8], (40 , 59) )
        screen.blit(pygame.transform.scale(self.displayField, (500, 500) ), (60, 60) )
        pygame.display.flip()
    
    def mainLoop(self, screen):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mX, mY) = pygame.mouse.get_pos()
                    for s in self.sliders:
                        if 153 + s.getXLoc() <= mX < 171 + s.getXLoc() and 145+s.getYLoc()+(s.getValue()*10) <= mY < 161+s.getYLoc()+(s.getValue()*10):
                            self.slide(s, screen)
                    # done
                    if 410 <= mX < 641 and 504 <= mY < 686:
                        return (self.gender,
                                self.str, 
                                self.itl, 
                                self.dex, 
                                const.blocksize, 
                                const.blocksize,
                                self.HP, self.HP, # max, current
                                self.MP, self.MP,
                                0, 0,             # score, keys
                                1, 0, 20,         # level, current XP, XP for next lev
                                [], None,         # weapons, eq. weapons
                                [], [None,None,None], #armor, eq. armor
                                range(20),        # items
                                [],               # spells
                                50, [False, False], 0 ) #gold, stats, slain
                elif event.type == pygame.QUIT:
                    os.sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return (self.gender,
                                self.str, 
                                self.itl, 
                                self.dex, 
                                const.blocksize, 
                                const.blocksize,
                                self.HP, self.HP, # max, current
                                self.MP, self.MP,
                                0, 0,             # score, keys
                                1, 0, 20,         # level, current XP, XP for next lev
                                [], None,         # weapons, eq. weapons
                                [], [None,None,None], #armor, eq. armor
                                range(20),        # items
                                [],               # spells
                                50, [False, False], 0 ) #gold, stats, slain
            self.updateDisplay(screen)
        while (pygame.event.wait().type != pygame.KEYDOWN): pass