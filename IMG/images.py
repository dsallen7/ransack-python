# Script for pre-loading all images used in Ransack

from spritesheet import *
from const import *

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

def load():

    mapSpriteSheet = spritesheet('mastersheet.bmp')
    for i in range(128):
        mapImages[i] = mapSpriteSheet.image_at( ( (i*blocksize)%240, (i/8)*blocksize, blocksize, blocksize), 1 )
    mapImages[128] = load_image('house1.bmp', 1)
    mapImages[129] = load_image('mShop.bmp', 1)
    mapImages[130] = load_image('bSmith.bmp', 1)
    mapImages[131] = load_image('armry.bmp', 1)
    mapImages[132] = load_image('tavrn.bmp', 1)
    
    heroSpriteSheet = spritesheet('herosheet.bmp')
    for i in range(8):
        heroImages[i] = heroSpriteSheet.image_at( (i*blocksize, 0, blocksize, blocksize), -1 )
    
    editorSpriteSheet = spritesheet('editorsheet.bmp')
    for i in range(7):
        editorImages[i] = editorSpriteSheet.image_at((i*blocksize, 0, blocksize, blocksize), -1 )

def loadNPC(file):
    npcSS = spritesheet(file)
    npcImages = range(8)
    for i in range(8):
        npcImages[i] = npcSS.image_at( (i*blocksize, 0, blocksize, blocksize), -1 )
    return npcImages