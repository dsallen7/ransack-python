import pygame, os
from DISPLAY import text
from UTIL import const, colors
from math import floor, ceil

class Button:
    
    def __init__(self, loc, msg, font = os.getcwd()+"/FONTS/devinne.ttf", size=18, invisible = False ):
        (x, y) = loc
        self.msg = msg
        self.locX = x
        self.locY = y
        #self.img = text.Text(msg, font, size, colors.white, colors.gold, True)
        if invisible:
            self.img = text.Text(msg, font, size, colors.white, colors.white, True)
            self.sizeX = int(ceil(3.6*const.blocksize))
            self.sizeY = int(ceil(3.6*const.blocksize))
        else: 
            self.img = text.Text(msg, font, size, colors.white, colors.gold, True)
            self.sizeX = self.img.get_width()
            self.sizeY = self.img.get_height()
        self.type = 'button'
        
        '''
        self.area = ( (self.locX, self.locY),
                      (self.locX, self.locY+size[1]),
                      (self.locX+size[0], self.locY+size[1]),
                      (self.locX+size[0], self.locY) )
        '''
    
    def hit(self, x, y):
        if self.locX <= x < self.locX+self.sizeX and self.locY <= y < self.locY+self.sizeY:
            return True
        else: return False