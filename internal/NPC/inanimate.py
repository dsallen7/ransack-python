import pygame, random, math, os
from UTIL import const, misc

from SCRIPTS import npcScr

from IMG import images

from npc import Npc

from random import choice

class Inanimate(Npc):
    def __init__(self, x, y, name, filename):
        Npc.__init__(self, x, y, name, filename)

class Fireplace(Inanimate):
    def __init__(self, x, y, name):
        Inanimate.__init__(self, x, y, name, 'fireplace.bmp')
        self.message = 'The fire glows brightly.'
        self.flicker = 0
        self.type = 'inanimate'
    
    def update(self, map, hero):
        if self.flicker == 4:
            self.imgIdx = ( self.imgIdx + 1 ) % 8
            self.image = self.images[self.imgIdx]
        self.flicker = ( self.flicker + 1 ) % 5

class Firepit(Inanimate):
    def __init__(self, x, y, name):
        Inanimate.__init__(self, x, y, name, 'firepit.bmp')
        self.message = 'The fire glows brightly.'
        self.flicker = 0
        self.type = 'inanimate'
    
    def update(self, map, hero):
        if self.flicker == 4:
            self.imgIdx = ( self.imgIdx + 1 ) % 8
            self.image = self.images[self.imgIdx]
        self.flicker = ( self.flicker + 1 ) % 5
        
class Candleabra(Inanimate):
    def __init__(self, x, y, name):
        Inanimate.__init__(self, x, y, name, 'candleabra.bmp')
        self.message = 'The candles cast an eerie glow over the room!'
        self.flicker = 0
    
    def update(self, map, hero):
        if self.flicker == 4:
            self.imgIdx = ( self.imgIdx + 1 ) % 8
            self.image = self.images[self.imgIdx]
        self.flicker = ( self.flicker + 1 ) % 5