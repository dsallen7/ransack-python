import pygame, flash

from UTIL import const, colors

from math import floor, ceil

from DISPLAY import text

import os

class effects():
    def __init__(self, clock, screen):
        self.clock = clock
        self.screen = screen
        self.keyFlash = None
        self.flashImg = None
        
        self.flashDict = { pygame.K_c      : (int(floor(173*const.scaleFactor)), int(ceil(106*const.scaleFactor))+int(ceil(300*const.scaleFactor))),    # upper left   (7) cast spell
                           pygame.K_LEFT   : (int(floor(173*const.scaleFactor)), int(ceil(143*const.scaleFactor))+int(ceil(300*const.scaleFactor))),    # middle left  (4) left
                           pygame.K_m      : (int(floor(173*const.scaleFactor)), 1 + int(ceil(180*const.scaleFactor))+int(ceil(300*const.scaleFactor))),# lower left   (1) map *
                           pygame.K_UP     : (int(floor(210*const.scaleFactor)), int(ceil(106*const.scaleFactor))+int(ceil(300*const.scaleFactor))),     # upper center (8) up
                           pygame.K_RETURN : (int(floor(210*const.scaleFactor)), int(ceil(143*const.scaleFactor))+int(ceil(300*const.scaleFactor))), # middle center(5) action
                           pygame.K_DOWN   : (int(floor(210*const.scaleFactor)), 1 + int(ceil(180*const.scaleFactor))+int(ceil(300*const.scaleFactor))),   # lower center (2) down *
                           pygame.K_i      : (int(ceil(247*const.scaleFactor)),  int(ceil(106*const.scaleFactor))+int(ceil(300*const.scaleFactor))),      # upper right  (9) item *
                           pygame.K_RIGHT  : (int(ceil(247*const.scaleFactor)),  int(ceil(143*const.scaleFactor))+int(ceil(300*const.scaleFactor))),  # middle right (6) right *
                           pygame.K_s      : (int(ceil(247*const.scaleFactor)),  1 + int(ceil(180*const.scaleFactor))+int(ceil(300*const.scaleFactor))),      # lower right  (3) hero stats *
                           
                           pygame.K_a      : (int(floor(135*const.scaleFactor)), int(ceil(143*const.scaleFactor))+int(ceil(300*const.scaleFactor))),      # armor
                           pygame.K_w      : (int(floor(135*const.scaleFactor)), int(ceil(180*const.scaleFactor))+int(ceil(300*const.scaleFactor))),      # weapons
                           
                           pygame.K_h      : (int(floor(78*const.scaleFactor)), int(ceil(143*const.scaleFactor))+int(ceil(300*const.scaleFactor)))        # help
                          
                          }

    def fadeOut(self, size):
        fadeScreen = pygame.Surface( (int(ceil(300 * const.scaleFactor)) - 2*size, 
                                      int(ceil(300 * const.scaleFactor)) - 2*size) )
        fadeScreen.fill( colors.black )
        for i in range(0, 255, 5):
            fadeScreen.set_alpha(i)
            self.clock.tick(40)
            self.screen.blit(fadeScreen, (size, size) )
            pygame.display.flip()
    
    def scrollFromCenter(self, screenOne, screenTwo):
        if screenOne.get_rect() != screenTwo.get_rect():
            print 'Mismatch'
            return
        self.screen.blit(screenOne, (0,0) )
        for i in range(0, screenTwo.get_width()/2, 5):
            screenOne_ = screenOne.copy()
            screenOne_.blit(screenTwo,                          # source 
                           ( (screenOne.get_width()/2)-i, 0 ), # dest
                           ( 0,0, 2*i, 300 )                     # area
                           )
            #pygame.time.wait(10)
            self.screen.blit(pygame.transform.scale(screenOne_, (int(ceil(300 * const.scaleFactor)), 
                                                                int(ceil(300 * const.scaleFactor))) ), (0, 0) )
            pygame.display.flip()
    
    def drawKeyFlash(self, key):
        self.flashImg = pygame.Surface((70, 70))
        self.flashImg.fill( colors.white )
        self.keyFlash = flash.Flash( self.flashDict[key], 30, 15  )
        (x,y)=self.flashDict[key]
        #print 'New flash at'+str(x)+', '+str(y)
        
    def update(self, screen):
        if self.keyFlash is not None:
            self.flashImg.set_alpha(self.keyFlash.alpha)
            screen.blit(self.flashImg, self.keyFlash.loc  )
            if not self.keyFlash.cycle():
                self.keyFlash = None
        else:
            return
    
    def displayLoadingMessage(self, board, message):
        board_ = board.copy()
        msgBox = text.Text(message, os.getcwd()+"/FONTS/DevinneSwashShadow.ttf", 18, colors.white, colors.black, True)
        board_.blit( msgBox, ( (board_.get_width()/2-msgBox.get_width()/2), 
                                    (self.screen.get_width()/2-msgBox.get_height())  ) )
        self.screen.blit( board_, (0, 0) )
        pygame.display.flip()