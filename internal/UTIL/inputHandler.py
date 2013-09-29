import pygame

from math import floor, ceil

from UTIL import const

'''
            (left bound of button, top bound of button + size of gameboard) : key
'''

class inputHandler():
    
    def __init__(self, FX):
        self.keyDict = {(int(floor(173*2.4)), 
                         int(ceil(106*2.4))+int(ceil(300*2.4)))      : pygame.K_c,      # upper left   (7) cast spell
                        (int(floor(173*2.4)), 
                         int(ceil(143*2.4))+int(ceil(300*2.4)))      : pygame.K_LEFT,   # middle left  (4) left
                        (int(floor(173*2.4)), 
                         1 + int(ceil(180*2.4))+int(ceil(300*2.4)))  : pygame.K_m,      # lower left   (1) map *
                        (int(floor(210*2.4)), 
                         int(ceil(106*2.4))+int(ceil(300*2.4)))      : pygame.K_UP,     # upper center (8) up
                        (int(floor(210*2.4)), 
                         int(ceil(143*2.4))+int(ceil(300*2.4)))      : pygame.K_RETURN, # middle center(5) action
                        (int(floor(210*2.4)), 
                         1 + int(ceil(180*2.4))+int(ceil(300*2.4)))  : pygame.K_DOWN,   # lower center (2) down *
                        (int(ceil(247*2.4)), 
                         int(ceil(106*2.4))+int(ceil(300*2.4)))      : pygame.K_i,      # upper right  (9) item *
                        (int(ceil(247*2.4)), 
                         int(ceil(143*2.4))+int(ceil(300*2.4)))      : pygame.K_RIGHT,  # middle right (6) right *
                        (int(ceil(247*2.4)), 
                         1 + int(ceil(180*2.4))+int(ceil(300*2.4)))  : pygame.K_s,      # lower right  (3) hero stats *
                           
                        (int(floor(135*2.4)), int(ceil(143*2.4))+int(ceil(300*2.4))) : pygame.K_e,      # armor
                        (int(floor(135*2.4)), int(ceil(180*2.4))+int(ceil(300*2.4))+1) : pygame.K_e,      # weapons
                           
                        (int(floor(78*2.4)), int(ceil(143*2.4))+int(ceil(300*2.4))) : pygame.K_h        # help
                           
                        }
        self.FX = FX
    
    def getMouseCmd(self, mEvent):
        (mX, mY) = pygame.mouse.get_pos()
        if int(floor(173*2.4)) <= mX < int(floor(275*2.4)) and int(ceil(106*2.4))+int(ceil(300*2.4)) <= mY < int(ceil(208*2.4))+int(ceil(300*2.4)):
            # keypad
            mX_ = int(floor(173*2.4)) + ( ( (mX - int(floor(173*2.4))) / 89 ) * 89 )
            mY_ = int(ceil(106*2.4))+int(ceil(300*2.4)) + ( ( (mY - (int(ceil(106*2.4))+int(ceil(300*2.4)))) / 89 ) * 89 )
        elif int(floor(135*2.4)) <= mX < int(floor(163*2.4)) and int(ceil(143*2.4))+int(ceil(300*2.4)) <= mY < int(ceil(208*2.4))+int(ceil(300*2.4)):
            # armor/weapons
            return pygame.K_e
            mX_ = int(floor(135*2.4)) + ( ( (mX - int(floor(135*2.4))) / 89 ) * 89 )
            mY_ = int(ceil(143*2.4))+int(ceil(300*2.4)) + ( ( (mY - (int(ceil(143*2.4))+int(ceil(300*2.4)) )) / 89 ) * 89 )
        elif int(floor(78*2.4)) <= mX < int(floor(125*2.4)) and int(floor(143*2.4))+int(ceil(300*2.4)) <= mY < int(floor(154*2.4))+int(ceil(300*2.4)):
            # help
            return pygame.K_h
        elif mY < int( ceil( 300*2.4 ) ):
            return ( int(floor(mX/2.4))/const.blocksize, int(floor(mY/2.4))/const.blocksize)
        else: return None
        try:
            self.FX.drawKeyFlash( self.keyDict[(mX_, mY_)] )
            return self.keyDict[(mX_, mY_)]
        except KeyError:
            return None

    def getCmd(self, event):
        if event == None:
            if pygame.mouse.get_pressed()[0]:
                return self.getMouseCmd(event)
            else:
                return None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self.getMouseCmd(event)
        elif event.type == pygame.QUIT:
            return pygame.QUIT
        elif event.type == pygame.KEYDOWN:
            return event.key