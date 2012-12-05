from UTIL import const

descDict = { 
             const.LSHIRT:  'Leather Shirt',
             const.LMAIL:   'Leather Cuirass',
             const.CMAIL:   'Chainmail',
             const.SPLATE:  'Steel Plate',
             const.TPLATE:  'Titanium Plate',
             const.WSHIELD: 'Wooden Shield',
             const.ISHIELD: 'Iron Shield',
             const.SSHIELD: 'Steel Shield',
             
             const.HELMET:  'Iron Helmet'
            }

aLevels = { 
             const.LSHIRT:  1,
             const.LMAIL:   2,
             const.CMAIL:   4,
             const.SPLATE:  8,
             const.TPLATE:  10,
             const.WSHIELD: 2,
             const.ISHIELD: 4,
             const.SSHIELD: 8,
             
             const.HELMET:  4
            }

categories = {
             const.WSHIELD: 0, # shield
             const.ISHIELD: 0,
             const.SSHIELD: 0,
             const.LSHIRT:  1, # plate
             const.LMAIL:   1,
             const.CMAIL:   1,
             const.SPLATE:  1,
             const.TPLATE:  1,
              
             const.HELMET:  2 # helmet
              }