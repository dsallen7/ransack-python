# Script for pre-loading all images used in Ransack

from spritesheet import *
from const import *

mapImages = range(12)
itemImages = range(3)
spellImages = range(2)

def load():
    mapSpriteSheet = spritesheet('mapsheet.bmp')

    for i in range(12):
        mapImages[i] = mapSpriteSheet.image_at( (i*blocksize, 0, blocksize, blocksize) )

    itemSpriteSheet = spritesheet('itemsheet.bmp')

    for i in range(3):
        itemImages[i] = itemSpriteSheet.image_at( (i*blocksize, 0, blocksize, blocksize) )
    
    spellSpriteSheet = spritesheet('spellsheet.bmp')
    
    for i in range(2):
        spellImages[i] = spellSpriteSheet.image_at( (i*blocksize, 0, blocksize, blocksize) )