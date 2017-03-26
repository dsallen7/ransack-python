from UTIL import const

itemShopsByLevel = { 
                    1: [const.FRUIT1,const.CHEESE,const.BREAD,const.LANTERN],
                    2: [const.ANTIDOTE,const.SHP,const.MHP,const.SMP,const.MMP]



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
townHallsByLevel = {1: [(const.CERTIFICATE,const.SAVECERT),
                          (const.CERTIFICATE,const.RETURNCERT)]
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
                          (const.PARCHMENT,const.DART),
                          (const.PARCHMENT,const.TLPT)],
                     3: [(const.SPELLBOOK,const.FRBL),
                          (const.PARCHMENT,const.FRBL),
                          (const.PARCHMENT,const.HEAL),
                          (const.PARCHMENT,const.DART),
                          (const.PARCHMENT,const.TLPT)]
                      
                      }