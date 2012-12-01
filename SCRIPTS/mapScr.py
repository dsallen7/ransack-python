from UTIL import const

wallDict = { (False, False, False, False) : 28, # center
             (False, False, False, True)  : const.ULWALL, # UL
             (False, False, True, False)  : const.LLWALL, # UL
             (False, False, True, True)   : const.ULWALL, # UL
             (False, True, False, False)  : const.LRWALL, # LR
             (False, True, False, True)   : const.URWALL, # UR
             (False, True, True, False)   : const.EWWALL,
             (False, True, True, True)    : const.URWALL,
             (True, False, False, False)  : const.LLWALL,
             (True, False, False, True)   : const.NSWALL,
             (True, False, True, False)   : const.LLWALL,
             (True, False, True, True)    : const.NSWALL,
             (True, True, False, False)   : const.LRWALL,
             (True, True, False, True)    : const.URWALL,
             (True, True, True, False)    : const.EWWALL,
             (True, True, True, True) : 28,
            
            }

parchByLevel = { 1 : [0, 1],
                 2 : [0, 1],
                 3 : [0, 1],
                 4 : [0, 1, 2],
                 5 : [0, 1, 2],
                 6 : [0, 1, 2],
                 7 : [0, 1, 2, 3],
                 8 : [0, 1, 2, 3],
                 9 : [0, 1, 2, 3],
                10 : [0, 1, 2, 3]
                }
wildsTilesList = [ (8, const.GRASS1),
                   (3, const.PINE1) ]
fruitList = [const.FRUIT1,
             const.CHEESE,
             const.BREAD]

pines = [const.PINE1, const.PINE2, const.PINE3, const.PINE4]

descriptions = {
                const.PINE1   : "They don't call it the Pine Barrens for nothing!",
                const.PINE2   : "They don't call it the Pine Barrens for nothing!",
                const.PINE3   : "They don't call it the Pine Barrens for nothing!",
                const.PINE4   : "They don't call it the Pine Barrens for nothing!",
                const.WELLSP : "A village wellspring",
                const.COLUMN : "A tall marble column.",
                const.CHAIR1  : "A sturdy hand-carved wooden chair.",
                const.CHAIR2  : "A sturdy hand-carved wooden chair.",
                const.OCHEST : "The chest is empty."
                
                
                }