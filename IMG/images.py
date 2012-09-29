# Script for pre-loading all images used in Ransack

from spritesheet import *
from UTIL import const

import os

heroImages = range(8)
mapImages = range(133)
editorImages = range(7)

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
    return image

def load(path=''):

    mapSpriteSheet = spritesheet('mastersheet.bmp')
    for i in range(128):
        mapImages[i] = mapSpriteSheet.image_at( ( (i*const.blocksize)%240, (i/8)*const.blocksize, const.blocksize, const.blocksize), 1 )
    siteImgs = ['house1.bmp', 'mShop.bmp', 'bSmith.bmp', 'armry.bmp', 'tavrn.bmp']
    for i in range(128, 133):
        mapImages[i] = load_image( os.path.join('EXT', siteImgs[i-128]), 1 )
    
    heroSpriteSheet = spritesheet( os.path.join('CHAR', 'herosheet.bmp'))
    for i in range(8):
        heroImages[i] = heroSpriteSheet.image_at( (i*const.blocksize, 0, const.blocksize, const.blocksize), -1 )
    
    editorSpriteSheet = spritesheet('editorsheet.bmp')
    for i in range(7):
        editorImages[i] = editorSpriteSheet.image_at((i*const.blocksize, 0, const.blocksize, const.blocksize), -1 )

def loadNPC(file):
    npcSS = spritesheet( os.path.join('CHAR', file) )
    npcImages = range(9)
    for i in range(9):
        npcImages[i] = npcSS.image_at( (i*const.blocksize, 0, const.blocksize, const.blocksize), -1 )
    return npcImages