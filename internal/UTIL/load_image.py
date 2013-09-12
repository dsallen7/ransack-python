import os
import pygame

try:
    import android
except ImportError:
    android = False
    print "No Android in load_image"

def load_image(name, colorkey=None):
    if android:
        fileobj = android.assets.open(os.path.join('IMG', name))
    else: fileobj = os.path.join('../assets/IMG', name)
    try:
        image = pygame.image.load(fileobj)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        if colorkey is 1:
            colorkey = [1,1,1]
        if colorkey is 2:
            colorkey = [255,0,255]
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()