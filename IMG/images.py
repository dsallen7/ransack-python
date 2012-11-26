# Script for pre-loading all images used in Ransack

from spritesheet import *
from UTIL import const, load_image

import os

mHeroImages = range(9)
fHeroImages = range(9)
mapImages = range(135)
editorImages = range(7)

def load(path=''):

    mapSpriteSheet = spritesheet('mastersheet.bmp')
    for i in range(128):
        mapImages[i] = mapSpriteSheet.image_at( ( (i*const.blocksize)%240, (i/8)*const.blocksize, const.blocksize, const.blocksize), 1 )
    siteImgs = ['itemSh.bmp', 'mShop.bmp', 'bSmith.bmp', 'armry.bmp', 'tavrn.bmp','townhall.bmp','house1.bmp']
    for i in range(128, 135):
        mapImages[i], r = load_image.load_image( os.path.join('EXT', siteImgs[i-128]), 1 )
    
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
               'itemshop'  : (128,2),
               'magicshop' : (129,2),
               'blacksmith': (130,2),
               'armory'    : (131,2),
               'tavern'    : (132,3),
               'townhall'  : (133,3),
               'house1'    : (134,2)
               }