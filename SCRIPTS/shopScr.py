from UTIL import const

itemShopsByLevel = { 
                    1: [0,1,4],
                    2: [5,6,7,9,10]



}

blacksmithShopsByLevel = {
                            1: [ (26,0),(27,0),(28,0) ],
                            2: [ (26,0),(27,0),(28,0),(26,1),(27,1),(28,1) ]

}

armoriesByLevel = { 
                   1: [ (31,0),(32,0),(33,0)],
                   2: [ (31,0),(32,0),(33,0),(31,1),(32,1),(33,1)]


}

# 100: spellbook
# 101: parchment
# level, spellnum
magicShopsByLevel = { 
                     1: [(const.SPELLBOOK,0,1),
                          (const.PARCHMENT,0,0),
                          (const.PARCHMENT,0,1)],
                     2: [(const.SPELLBOOK,0,2),
                          (const.SPELLBOOK,0,3),
                          (const.PARCHMENT,0,0),
                          (const.PARCHMENT,0,1),
                          (const.PARCHMENT,0,3)]
                      
                      }