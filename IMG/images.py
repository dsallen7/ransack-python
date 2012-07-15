# Script for pre-loading all images used in Ransack

from spritesheet import *
from const import *

mapSpriteSheet = None
villageSpriteSheet = None
mapImages = range(128)
spellImages = range(2)
villageImages = range(14)

def load():

    mapSpriteSheet = spritesheet('mastersheet.bmp')
    for i in range(128):
        mapImages[i] = mapSpriteSheet.image_at( ( (i*blocksize)%240, (i/8)*blocksize, blocksize, blocksize) )
    
    spellSpriteSheet = spritesheet('spellsheet.bmp')
    
    for i in range(2):
        spellImages[i] = spellSpriteSheet.image_at( (i*blocksize, 0, blocksize, blocksize) )
    
    villageSpriteSheet = spritesheet('villagesheet.bmp')
    
    for i in range(14):
        villageImages[i] = villageSpriteSheet.image_at( (i*blocksize, 0, blocksize, blocksize) )