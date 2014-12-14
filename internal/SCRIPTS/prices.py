from UTIL import const

itemPrices = { const.FRUIT1: 5, const.CHEESE: 8, const.BREAD: 10, const.ANTIDOTE: 30, 
              const.SHP : 25, const.MHP : 50, const.LHP: 75,
               const.SMP: 25, const.MMP: 50,  const.LMP: 75,
               const.CERTIFICATE: 25, const.LANTERN: 100 }

weaponPrices = { const.WSWORD: 50,
                 const.SSWORD: 100,
                 const.AXE: 150,
                 const.LSWORD: 250,
                 const.TSWORD: 500,
                 const.VAXE: 1000,
                 const.GSWORD: 2000
                }



armorPrices = {
                const.LSHIRT: 50,
                const.LMAIL: 100,
                const.CMAIL: 200,
                const.RING:  200,
                const.SPLATE: 500,
                const.TPLATE: 1000,
                const.WSHIELD: 75,
                const.ISHIELD: 250,
                const.SSHIELD: 500
                }

resistPrices = {'Fire': 100,
                'Ice' : 100,
                'Electric' : 100,
                None : 0
                }

ringStatusEnhancementPrices = {
                               
                               }

magicPrices = { (const.SPELLBOOK,const.DART): 100,
               (const.SPELLBOOK,const.FRBL): 250,
               (const.SPELLBOOK,const.HEL2): 100,
                (const.SPELLBOOK,const.TLPT): 500,
                (const.SPELLBOOK,const.HEL3): 250,
                (const.SPELLBOOK,const.ICBL): 500,
                (const.SPELLBOOK,const.ASCD): 100,
                (const.SPELLBOOK,const.HEL4): 500,
                (const.SPELLBOOK,const.EXTD): 1000,
                (const.SPELLBOOK,const.FBL2): 1000,
                (const.SPELLBOOK,const.HEL5): 750,
                (const.SPELLBOOK,const.RTRN): 1500,
                (const.SPELLBOOK,const.IBL2): 1500,
                (const.SPELLBOOK,const.FBL3): 1750,
                (const.SPELLBOOK,const.GNCD): 2000,
                
                (const.PARCHMENT,const.HEAL): 10,
                (const.PARCHMENT,const.DART): 10,
               (const.PARCHMENT,const.FRBL): 25,
               (const.PARCHMENT,const.HEL2): 10,
                (const.PARCHMENT,const.TLPT): 50,
                (const.PARCHMENT,const.HEL3): 25,
                (const.PARCHMENT,const.ICBL): 50,
                (const.PARCHMENT,const.ASCD): 10,
                (const.PARCHMENT,const.HEL4): 50,
                (const.PARCHMENT,const.EXTD): 100,
                (const.PARCHMENT,const.FBL2): 100,
                (const.PARCHMENT,const.HEL5): 75,
                (const.PARCHMENT,const.RTRN): 150,
                (const.PARCHMENT,const.IBL2): 150,
                (const.PARCHMENT,const.FBL3): 175,
                (const.PARCHMENT,const.GNCD): 200,
                }

def priceItem(item):
    if item.name == 'armor':
        if item.type == const.RING:
            return armorPrices[item.type] + resistPrices[item.resist] + 5* item.enhAmt
        else: return armorPrices[item.type] + resistPrices[item.resist]
    elif item.name == 'weapon':
        enh = item.getEnhancements()
        return weaponPrices[item.type] + 25*enh[0] + 25*enh[1] + 25*enh[2]
    elif item.name == 'spellbook' or item.name == 'parchment':
        return magicPrices[ (item.type, item.spellNum) ]
    else:
        return itemPrices[item.type]