from UTIL import const

itemShopsByLevel = { 
                    1: [0,1,4],
                    2: [5,6,7,9,10]



}

blacksmithShopsByLevel = {
                            1: [ const.WSWORD, const.SSWORD ],
                            2: [ const.SSWORD, const.AXE ]

}

armoriesByLevel = { 
                   1: [ const.LSHIRT, const.LMAIL, const.WSHIELD ],
                   2: [ const.LMAIL, const.CMAIL, const.RING ]
}


enhancementsByLevel = {
                       1: [ 'plusWP' ],
                       2: [ 'plusHP', 'plusMP', 'plusWP' ]
                       
                       }

# 100: spellbook
# 101: parchment
# level, spellnum
magicShopsByLevel = { 
                     1: [(const.SPELLBOOK,const.DART),
                          (const.PARCHMENT,const.DART),
                          (const.PARCHMENT,const.HEAL)],
                     2: [(const.SPELLBOOK,const.FRBL),
                          (const.PARCHMENT,const.FRBL),
                          (const.PARCHMENT,const.HEAL),
                          (const.PARCHMENT,const.DART)]
                      
                      }