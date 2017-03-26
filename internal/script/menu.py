from math import ceil, floor
from UTIL import const
menuBoxPositions = [ ( int(ceil(80*const.scaleFactor)), int(ceil(80*const.scaleFactor)) ), 
                     ( int(ceil(115*const.scaleFactor)), int(ceil(80*const.scaleFactor)) ), 
                     ( int(ceil(150*const.scaleFactor)), int(ceil(80*const.scaleFactor)) ), 
                     ( int(ceil(185*const.scaleFactor)), int(ceil(80*const.scaleFactor)) ),
                     ( int(ceil(80*const.scaleFactor)), int(ceil(115*const.scaleFactor)) ), 
                     ( int(ceil(115*const.scaleFactor)), int(ceil(115*const.scaleFactor)) ), 
                     ( int(ceil(150*const.scaleFactor)), int(ceil(115*const.scaleFactor)) ), 
                     ( int(ceil(185*const.scaleFactor)), int(ceil(115*const.scaleFactor)) ) ]
boxPointsFn = lambda x: ( (x[0],x[1]), 
                          (x[0],x[1] + int(ceil(const.blocksize*const.scaleFactor)) ), 
                          (x[0] + int(ceil(const.blocksize*const.scaleFactor)), x[1]+int(ceil(const.blocksize*const.scaleFactor)) ), 
                          (x[0] + int(ceil(const.blocksize*const.scaleFactor)), x[1]) )
armorLocList = [( 242, 29 ), # 0 helmet
                ( 31, 202 ), # 1 mail
                ( 169, 245 ),# 2 shield
                ( 31, 112 ),
                ( 240, 115),
                (109, 51),
                (219, 181),
                (76, 243)]