from UTIL import const

# Master armor dictionary containing information in the following format:
# (Description, Level, Category, Img Num)

#descDict
armorDict = { 
             const.LSHIRT:  ('Leather Shirt',1,1,const.LSHIRT),
             const.LMAIL:   ('Leather Cuirass',2,1,const.LMAIL),
             const.CMAIL:   ('Chainmail',4,1,const.CMAIL),
             const.SPLATE:  ('Steel Plate',8,1,const.SPLATE),
             const.TPLATE:  ('Titanium Plate',10,1,const.TPLATE),
             
             const.WSHIELD: ('Wooden Shield',2,0,const.WSHIELD),
             const.ISHIELD: ('Iron Shield',4,0,const.ISHIELD),
             const.SSHIELD: ('Steel Shield',8,0,const.SSHIELD),
             
             const.HELMET:  ('Iron Helmet',4,2,const.HELMET),
             
             const.RING: ('Enchanted Ring',1,3,const.RING),
             const.AMULET: ('Enchanted Amulet',1, 4,const.AMULET), # amulet
             const.CLOAK:   ('Cloak',1,5,const.CLOAK), # cloak
             const.BOOTS:   ('Leather Boots',1,6,const.BOOTS)  # boots
            }

resists = ['Fire', 'Ice', 'Electric']

# Slots:
# 0 : helmet
# 1 : mail
# 2 : shield
# 3 : ring
# 4 : ring
# 5 : amulet
# 6 : cloak
# 7 : boots

# Categories:
# 0 : shield
# 1 : mail
# 2 : helmet
# 3 : ring
# 4 : amulet
# 5 : cloak
# 6 : boots

# mapping of slots to categories
slotCategories = {0:2, 1:1, 2:0,
                  3:3, 4:3, 5:4,
                  6:5, 7:6
                  }