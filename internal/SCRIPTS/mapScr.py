from UTIL import const

wallDict = { (False, False, False, False) : 28, # center
             (False, False, False, True)  : const.ULWALL, # UL
             (False, False, True, False)  : const.LLWALL, # UL
             (False, False, True, True)   : const.EWWALL, # UL
             (False, True, False, False)  : const.LRWALL, # LR
             (False, True, False, True)   : const.ULWALL, # UR
             (False, True, True, False)   : const.URWALL,
             (False, True, True, True)    : const.URWALL,
             (True, False, False, False)  : const.LLWALL,
             (True, False, False, True)   : const.LLWALL,
             (True, False, True, False)   : const.LRWALL,
             (True, False, True, True)    : const.EWWALL,
             (True, True, False, False)   : const.NSWALL,
             (True, True, False, True)    : const.NSWALL,
             (True, True, True, False)    : const.URWALL,
             (True, True, True, True) : const.URWALL
            
            }

def getMappedNeighborList(L):
    L_ = []
    for l in L:
        if l == const.DFLOOR1 or l == const.VOID:
            L_.append(False)
        else: L_.append(True)
    return (L_[0], L_[1], L_[2], L_[3])

dirDict = { 'w':(-1,0), 'e':(1,0), 'n':(0,-1), 's':(0,1) }

siteImgDict = { 
               'itemshop'  : (256,2),
               'magicshop' : (257,2),
               'blacksmith': (258,2),
               'armory'    : (259,2),
               'tavern'    : (260,3),
               'townhall'  : (261,3),
               'house1'    : (262,2),
               'tower1'    : (263,3)
               }
# 'special' items behind secret doors
specialByLevel = { 1: [const.WSWORD, const.LSHIRT],
                   2: [const.WSWORD, const.LSHIRT],
                   3: [const.WSWORD, const.LSHIRT],
                   4: [const.WSWORD, const.LSHIRT],
                   5: [const.WSWORD, const.LMAIL],
                   6: [const.WSWORD, const.LMAIL],
                   7: [const.WSWORD, const.LMAIL, const.WSHIELD],
                   8: [const.SSWORD, const.LMAIL, const.WSHIELD],
                   9: [const.SSWORD, const.LMAIL, const.WSHIELD],
                  10: [const.SSWORD, const.LMAIL, const.WSHIELD]
                  
                  }

parchByLevel = {0 : [const.HEAL, const.DART], 
                1 : [const.HEAL, const.DART],
                 2 : [const.HEAL, const.DART],
                 3 : [const.HEAL, const.DART],
                 4 : [const.HEAL, const.DART, const.HEL2, const.FRBL],
                 5 : [const.HEAL, const.DART, const.HEL2, const.FRBL],
                 6 : [const.HEAL, const.DART, const.HEL2, const.FRBL],
                 7 : [const.HEL2, const.FRBL, const.ICBL, const.ASCD],
                 8 : [const.HEL2, const.FRBL, const.ICBL, const.ASCD],
                 9 : [const.HEL2, const.FRBL, const.HEL3, const.ICBL, const.ASCD],
                10 : [const.HEL2, const.FRBL, const.HEL3, const.ICBL, const.ASCD]
                }

lootByLevel = { 1: [ (2, const.GOLD),
                     (1, const.PARCHMENT) ],
               2: [ (2, const.GOLD),
                     (1, const.PARCHMENT) ],
               3: [ (2, const.GOLD),
                     (1, const.PARCHMENT) ],
               4: [ (3, const.GOLD),
                     (2, const.PARCHMENT) ],
               5: [ (3, const.GOLD),
                     (2, const.PARCHMENT) ],
               6: [ (3, const.GOLD),
                     (2, const.PARCHMENT) ],
               7: [ (8, const.GOLD),
                     (6, const.PARCHMENT) ],
               8: [ (8, const.GOLD),
                     (6, const.PARCHMENT) ],
               9: [ (8, const.GOLD),
                     (6, const.PARCHMENT) ],
              10: [ (8, const.GOLD),
                     (6, const.PARCHMENT) ]
               
               
               }
wildsTilesList = [ (8, const.GRASS1),
                   (3, const.PINE1) ]
fruitList = [const.FRUIT1,
             const.CHEESE,
             const.BREAD]

pines = [const.PINE1, const.PINE2, const.PINE3, const.PINE4]

pineDict = { const.PINE1 : const.PINE2,
             const.PINE2 : const.PINE3,
             const.PINE3 : const.PINE4,
             const.PINE4 : const.PINE1
            
            }

accessoryList = ['cards1','cards2','beer1','veggies','fish','beers','dinnerplate','chicken','ham','','','','','','','','','']

descriptions = {
                const.PINE1   : "They don't call it the Pinelands for nothing!",
                const.PINE2   : "They don't call it the Pinelands for nothing!",
                const.PINE3   : "They don't call it the Pinelands for nothing!",
                const.PINE4   : "They don't call it the Pinelands for nothing!",
                const.STAGHEAD : "A massive stag's head",
                const.WELLSP : "A village wellspring",
                const.COLUMN1 : "A tall marble column.",
                const.COLUMN2 : "A tall marble column.",
                const.BOOKSHELF : "Proud words on a dusty shelf...",
                const.CHINASHELF: "Fine china, the kind you never actually eat off!",
                const.CHAIR1  : "A sturdy hand-carved wooden chair.",
                const.CHAIR2  : "A sturdy hand-carved wooden chair.",
                const.TABLE1: "A massive oaken table",
                const.TABLE2: "A massive oaken table",
                const.TABLE3: "A massive oaken table",
                const.GVEG: "An assortment of fresh vegetables",
                const.GMEAT: "Meats and cheeses are on display",
                const.OCHEST : "The chest is empty."
                
                
                }