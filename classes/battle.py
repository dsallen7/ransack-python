import pygame
from load_image import *
from const import *
import random

# this class will be used to draw the animation occuring in the battle.

class battle():
    
    def __init__(self):
        self.battleField = pygame.Surface( (300,300) )
        self.battleField.fill( black )
    
    
    def commence(self, screen):
        screen.blit( self.battleField, (75,75) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass