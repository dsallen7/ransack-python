# Script for pre-loading all images used in Ransack

from spritesheet import *
from const import *

heroImages = range(8)
mapImages = range(128)
editorImages = range(7)

def load():

    mapSpriteSheet = spritesheet('mastersheet.bmp')
    for i in range(128):
        mapImages[i] = mapSpriteSheet.image_at( ( (i*blocksize)%240, (i/8)*blocksize, blocksize, blocksize) )
    
    heroSpriteSheet = spritesheet('herosheet.bmp')
    for i in range(8):
        heroImages[i] = heroSpriteSheet.image_at( (i*blocksize, 0, blocksize, blocksize), -1 )
    
    editorSpriteSheet = spritesheet('editorsheet.bmp')
    for i in range(7):
        editorImages[i] = editorSpriteSheet.image_at((i*blocksize, 0, blocksize, blocksize), -1 )