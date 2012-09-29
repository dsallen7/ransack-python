import pygame, os

from DISPLAY import text
from UTIL import load_image, const, colors

class Creator():
    
    def __init__(self):
        self.displayField, r = load_image.load_image("createBox.bmp")
        self.HP = 50
        self.MP = 50
        self.str = 8
        self.itl = 8
        self.dex = 8
        self.slider = 4
        
        self.cursor, r = load_image.load_image("cursor.bmp", -1)
    
    # Displays string-formatted statistic
    def displayStat(self, stat, loc):
        (x,y) = loc
        statT = text.Text( stat, os.getcwd()+"/FONTS/devinne.ttf", 18, colors.white, colors.black, transparent=True )
        self.displayField.blit( statT, (x,y) )
        
    def slide(self, screen):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    return
                elif event.type == pygame.MOUSEMOTION:
                    (mX, mY) = pygame.mouse.get_pos()
                    if 307 <= mY < 397:
                        self.slider = (mY - 307) / 10
            self.updateDisplay(screen)
    
    def updateDisplay(self, screen):
        self.HP = 30 + (9 - self.slider) * 10
        self.MP = 20 + self.slider * 10 
        self.displayField, r = load_image.load_image("createBox.bmp")
        self.displayStat( str(self.HP), (150,62) )
        self.displayStat( str(self.MP), (200,62) )
        self.displayStat( str(self.str), (150,102) )
        self.displayStat( str(self.itl), (200,102) )
        self.displayStat( str(self.dex), (250,102) )
        self.displayField.blit(self.cursor, (216, 145+(self.slider*10)) )
        screen.blit(self.displayField, (150,150) )
        pygame.display.flip()
    
    def mainLoop(self, screen):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mX, mY) = pygame.mouse.get_pos()
                    if 369 <= mX < 387 and 302+(self.slider*10) <= mY < 318+(self.slider*10):
                        self.slide(screen)
                    # done
                    elif 291 <= mX < 340 and 387 <= mY < 416:
                        return (self.str, 
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
                                50, [False, False] ) #gold, stats
                elif event.type == pygame.QUIT:
                    os.sys.exit()
            self.updateDisplay(screen)
        while (pygame.event.wait().type != pygame.KEYDOWN): pass