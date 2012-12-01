import os
import pygame

def load_image(name, colorkey=None):
    fullname = os.path.join('IMG', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        if colorkey is 1:
            colorkey = [1,1,1]
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()