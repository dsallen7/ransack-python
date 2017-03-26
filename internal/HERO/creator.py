import pygame
import os

from DISPLAY import text
from UTIL import load_image, const, colors, slider, eztext
from IMG import images
from random import randrange
from math import ceil, floor

try:
    import android
except ImportError as e:
    print ("in HERO.creator: {}".format(e))
    android = False


class Creator():
    
    def __init__(self):
        self.displayField, r = load_image.load_image(os.path.join('MENU', "createBox.png"))
        self.baseHP = randrange(25, 35)
        self.baseMP = randrange(15, 25)
        self.bStr = randrange(6, 10)
        self.bItl = randrange(8, 10)
        self.bDex = randrange(8, 10)
        self.sliders = [slider.Slider(216, 145),  # Warrior/Wizard
                        slider.Slider(172, 145),  # Lawful/neutral/chaotic
                        slider.Slider(101, 61, 0, 1),  # Male/female
                        slider.Slider(81, 134, 0, 1)  # Faith
                        ]
        self.gender = 'male'
        self.faith = 'xtian'
        self.faithLevel = 5
        self.images = range(3)
        self.images[0], r = load_image.load_image( os.path.join('MENU', "cursor.png" ), -1)
        self.images[1], r = load_image.load_image( os.path.join('MENU', 'cursor_l.png'), -1)
        
        images.load()

    def getInput(self, screen, msg):
        #get file name
        input = None
        txtbx = eztext.Input(font=pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf",56),
                             maxlength=12,
                             color=(255,255,255),
                             prompt='')
        inputWindow = pygame.Surface( (int(ceil(223*const.scaleFactor)),
                                       int(ceil(36*const.scaleFactor))) )
        while input is None:

            # events for txtbx
            events = pygame.event.get()
            # process other events
            for event in events:
                # close it x button is pressed
                if event.type == pygame.QUIT:
                        os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input = txtbx.getValue()

            # clear the screen
            inputWindow.fill((25,25,25))
            # update txtbx
            txtbx.update(events)
            # blit txtbx on the sceen
            txtbx.draw(inputWindow)
            screen.blit(inputWindow, ( int(ceil(38*const.scaleFactor)), int(ceil(73*const.scaleFactor)) ) )
            # refresh the display
            pygame.display.flip()
        return input
    
    # Displays string-formatted statistic
    def displayStat(self, stat, loc):
        (x,y) = loc
        statT = text.Text( stat, os.getcwd()+"/FONTS/devinne.ttf", 9, colors.white, colors.black, transparent=True )
        self.displayField.blit( statT, (x,y) )
        
    def slide(self, sldr, screen):
        if sldr.getMax() == 1:
            sldr.setValue(1-sldr.getValue())
            return
        sldr.sliding = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    sldr.sliding = False
                    return
                elif event.type == pygame.MOUSEMOTION:
                    (mX, mY) = pygame.mouse.get_pos()
                    #if int(floor(sldr.getYLoc()*const.scaleFactor)) <= mY <= int(ceil(sldr.getYLoc() + sldr.getMax()*10*const.scaleFactor)):
                    if sldr.getYLoc()*const.scaleFactor <= mY <= (sldr.getYLoc() + sldr.getMax()*12)*const.scaleFactor:
                        sldr.setValue( int( floor( ( (mY - (sldr.getYLoc())*const.scaleFactor ) / 12 ) / const.scaleFactor ) ) )
                    else:
                        sldr.sliding = False
                        return
            self.updateDisplay(screen, 'stats')
            
    def calculateStats(self):
        # goes up with
        self.HP = self.baseHP + (self.sliders[0].getMax() - self.sliders[0].getValue() ) * 10
        # goes down with
        self.MP = self.baseMP + self.sliders[0].getValue() * 10
        self.str = self.bStr + ((((self.sliders[0].getMax() - self.sliders[1].getValue()) * 10 ) / 2) / 5) + 2 * (1 - self.sliders[2].getValue())
        self.itl = self.bItl + ((self.sliders[1].getValue() * 10) / 4) / 5
        self.dex = self.bDex + (((self.sliders[1].getValue() * 10) / 2) / 5) + 2 * self.sliders[2].getValue()
    
    def updateDisplay(self, screen, step):
        if step == 'stats':
            self.displayField, r = load_image.load_image(os.path.join('MENU', "createBox.png") )
            self.calculateStats()
            self.displayField, self.displayField.copy
            self.displayStat( str(self.HP), (146,65) )
            self.displayStat( str(self.MP), (197,65) )
            self.displayStat( str(self.str), (150,102) )
            self.displayStat( str(self.itl), (202,102) )
            self.displayStat( str(self.dex), (247,102) )
            for s in self.sliders:
                if s.sliding:
                    self.displayField.blit(self.images[1], (s.getXLoc(), s.getYLoc()+(s.getValue()*10)) )
                else: self.displayField.blit(self.images[0], (s.getXLoc(), s.getYLoc()+(s.getValue()*10)) )
            if self.sliders[2].getValue() == 0:
                self.gender = 'male'
                self.displayField.blit(images.mHeroImages[8], (40 , 59))
            else:
                self.gender = 'female'
                self.displayField.blit(images.fHeroImages[8], (40 , 59))
            
            if self.sliders[3].getValue() == 0:
                self.faith = 'xtian'
                self.displayField.blit(images.mapImages[246], (40 , 134))
            else:
                self.faith = 'asatru'
                self.displayField.blit(images.mapImages[245], (40 , 134))
            screen.blit(pygame.transform.scale(self.displayField, (720, 720)), (0, 0))
            pygame.display.flip()
        elif step == 'name':
            self.displayField, r = load_image.load_image(os.path.join('MENU', "createBox2.png"))
            screen.blit(pygame.transform.scale(self.displayField, (720, 720) ), (0, 0) )
            pygame.display.flip()
            
    def getBall(self):
        if android:
            android.hide_keyboard()
        return (self.gender, self.faith, self.faithLevel,
                self.str, self.itl, self.dex, 
                1, 1,             # hunger, thirst
                const.blocksize,  # img dimensions
                const.blocksize,
                self.HP, self.HP, # max, current
                self.MP, self.MP,
                0, 10,             # score, keys
                3, 0, 50,         # level, current XP, XP for next lev
                [], None,         # weapons, eq. weapons
                [], [None, None, None,  #armor, eq. armor (helmet, plate, shield,
                     None, None, None,  #ring, ring, amulet, 
                     None, None, None], #cloak, boots, ?)
                range(100),        # items
                [],                # spells
                100, [False, False, False], 0, #gold, stats, slain
                self.name )
    def mainLoop(self, screen):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mX, mY) = pygame.mouse.get_pos()
                    for s in self.sliders:
                        if s.getXLoc()* const.scaleFactor <= mX < (s.getXLoc() + 24) * const.scaleFactor and (s.getYLoc()+(s.getValue()*10)) * const.scaleFactor <= mY < (s.getYLoc()+(s.getValue()*10) + 24 )* const.scaleFactor:
                            self.slide(s, screen)
                    # done
                    if int(floor(33*const.scaleFactor)) <= mX < int(ceil(82*const.scaleFactor)) and int(floor(237*const.scaleFactor)) <= mY < int(ceil(266*const.scaleFactor)):
                        self.displayField, r = load_image.load_image(os.path.join('MENU', "createBox2.png") )
                        self.updateDisplay(screen, 'name')
                        if android:
                            android.show_keyboard()
                        self.name = self.getInput(screen, '')
                        return self.getBall()
                elif event.type == pygame.QUIT:
                    os.sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.displayField, r = load_image.load_image(os.path.join('MENU', "createBox2.png"))
                        self.updateDisplay(screen, 'name')
                        if android:
                            android.show_keyboard()
                        self.name = self.getInput(screen, '')
                        return self.getBall()
                    elif event.key == pygame.K_ESCAPE:
                        os.sys.exit()
            self.updateDisplay(screen, 'stats')
        while (pygame.event.wait().type != pygame.KEYDOWN):
            pass
