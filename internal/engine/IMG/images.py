# Script for pre-loading all images used in Ransack

from spritesheet import *
from UTIL import const, load_image

import os

mHeroImages = range(18)
fHeroImages = range(18)
mapImages = range(264)
editorImages = range(7)
accessories = range(18)

def load(path=''):

    mapSpriteSheet = spritesheet('mastersheet.bmp')
    for i in range(128):
        mapImages[i] = mapSpriteSheet.image_at( ( (i*const.blocksize)%240, 
                                                  (i/8)*const.blocksize, 
                                                  const.blocksize, 
                                                  const.blocksize), 
                                               1 )
        
    for i in range(128, 256):
        #print (i*const.blocksize)%240 + 240
        mapImages[i] = mapSpriteSheet.image_at( ( (i*const.blocksize)%240 + 240, 
                                                  ( (i-128) /8)*const.blocksize, 
                                                  const.blocksize, 
                                                  const.blocksize), 
                                               1 )
    siteImgs = ['itemSh.bmp', 'mShop.bmp', 'bSmith.bmp', 'armry.bmp', 'tavrn.bmp','townhall.bmp','house1.bmp', 'tower1.bmp']
    for i in range(256, 264):
        mapImages[i], r = load_image.load_image( os.path.join('EXT', siteImgs[i-256]), 1 )
    for i in range(18):
        accessories[i] = pygame.Surface((15,10))
        accessories[i].set_colorkey([255,128,128], pygame.RLEACCEL)
        accessories[i].blit( mapImages[242 + (i/6) ], ( ((i%6)/3)*-15, (i%3)*-10) )
    mHeroSpriteSheet = spritesheet( os.path.join('CHAR', 'mherosheet.bmp'))
    for i in range(18):
        mHeroImages[i] = mHeroSpriteSheet.image_at( ((i*const.blocksize)%270, 
                                                     (i/9)*const.blocksize, 
                                                     const.blocksize, 
                                                     const.blocksize), -1 )
    fHeroSpriteSheet = spritesheet( os.path.join('CHAR', 'fherosheet.bmp'))
    for i in range(18):
        fHeroImages[i] = fHeroSpriteSheet.image_at( ((i*const.blocksize)%270, 
                                                     (i/9)*const.blocksize, 
                                                     const.blocksize, 
                                                     const.blocksize), -1 )

def loadNPC(file):
    npcSS = spritesheet( os.path.join('CHAR', file) )
    npcImages = range(18)
    for i in range(18):
        npcImages[i] = npcSS.image_at( ((i*const.blocksize)%270, 
                                                     (i/9)*const.blocksize, 
                                                     const.blocksize, 
                                                     const.blocksize), -1 )
    return npcImages

def getMHero():
    return