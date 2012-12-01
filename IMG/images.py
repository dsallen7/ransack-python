# Script for pre-loading all images used in Ransack

from spritesheet import *
from UTIL import const, load_image

import os

mHeroImages = range(9)
fHeroImages = range(9)
mapImages = range(263)
editorImages = range(7)

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
    siteImgs = ['itemSh.bmp', 'mShop.bmp', 'bSmith.bmp', 'armry.bmp', 'tavrn.bmp','townhall.bmp','house1.bmp']
    for i in range(256, 263):
        mapImages[i], r = load_image.load_image( os.path.join('EXT', siteImgs[i-256]), 1 )
    
    mHeroSpriteSheet = spritesheet( os.path.join('CHAR', 'mherosheet.bmp'))
    for i in range(9):
        mHeroImages[i] = mHeroSpriteSheet.image_at( (i*const.blocksize, 0, const.blocksize, const.blocksize), -1 )
        
    fHeroSpriteSheet = spritesheet( os.path.join('CHAR', 'fherosheet.bmp'))
    for i in range(9):
        fHeroImages[i] = fHeroSpriteSheet.image_at( (i*const.blocksize, 0, const.blocksize, const.blocksize), -1 )


def loadNPC(file):
    npcSS = spritesheet( os.path.join('CHAR', file) )
    npcImages = range(9)
    for i in range(9):
        npcImages[i] = npcSS.image_at( (i*const.blocksize, 0, const.blocksize, const.blocksize), 1 )
    return npcImages

siteImgDict = { 
               'itemshop'  : (256,2),
               'magicshop' : (257,2),
               'blacksmith': (258,2),
               'armory'    : (259,2),
               'tavern'    : (260,3),
               'townhall'  : (261,3),
               'house1'    : (262,2)
               }