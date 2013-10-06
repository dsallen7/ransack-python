pEnemies = ['Cobra', 'Scorpion']
dEnemies = ['Zombie','Skeleton', 'Vampire']

healthDict = { 
              # Undead
              'Skeleton'       : 30,
              'Dark Skeleton'  : 80,
              'Rattlehead'     : 250,
              'Zombie'         : 50,
              'Vampire'        : 75,
              
              # Humanoid
              'Orc'            : 25,
              'Orc Sergeant'   : 75,
              'Dark Guard'     : 100,
              
              # Animal
              'Wild Dog'       : 25,
              'Garden Badger'  : 15,
              'Badger'         : 20,
              'Cobra'          : 30,
              'Carpathian Wolf': 60,
              'Wolf'           : 40
              }

attackDict = { 
              # Undead
              'Skeleton'       : 10,
              'Dark Skeleton'  : 17,
              'Rattlehead'     : 25,
              'Zombie'         : 13,
              'Vampire'        : 15,
              
              # Humanoid
              'Orc'            : 10,
              'Orc Sergeant'   : 18,
              'Dark Guard'     : 20,
              
              # Animal
              'Wild Dog'       : 7,
              'Badger'         : 5,
              'Garden Badger'  : 3,
              'Cobra'          : 7,
              'Carpathian Wolf': 20,
              'Wolf'           : 15
              }

expDict = { 
              # Undead
              'Skeleton'       : 10,
              'Dark Skeleton'  : 50,
              'Rattlehead'     : 250,
              'Zombie'         : 30,
              'Vampire'        : 40,
              
              # Humanoid
              'Orc'            : 10,
              'Orc Sergeant'   : 50,
              'Dark Guard'     : 60,
              
              # Animal
              'Wild Dog'       : 5,
              'Badger'         : 5,
              'Garden Badger'  : 3,
              'Cobra'          : 8,
              'Carpathian Wolf': 50,
              'Wolf'           : 35
              }
'''
imgFileDict = { 
              # Undead
              'Skeleton'       : ['rattlehead1.bmp', 'rattlehead2.bmp'],
              'Dark Skeleton'  : ['rattlehead1.bmp', 'rattlehead2.bmp'],
              'Rattlehead'     : ['rattlehead1.bmp', 'rattlehead2.bmp'],
              'Zombie'         : ['cobra1.bmp', 'cobra2.bmp'],
              'Vampire'        : ['cobra1.bmp', 'cobra2.bmp'],
              
              # Humanoid
              'Orc'            : ['orc1.bmp', 'orc2.bmp'],
              'Orc Sergeant'   : ['orc1.bmp', 'orc2.bmp'],
              
              # Animal
              'Wild Dog'       : ['cobra1.bmp', 'cobra2.bmp'],
              'Badger'         : ['cobra1.bmp', 'cobra2.bmp'],
              'Garden Badger'  : ['cobra1.bmp', 'cobra2.bmp'],
              'Cobra'          : ['cobra1.bmp', 'cobra2.bmp'],
              'Carpathian Wolf': ['cobra1.bmp', 'cobra2.bmp'],
              'Wolf'           : ['cobra1.bmp', 'cobra2.bmp']
               }
'''
lootDict = { 
              # Undead
              'Skeleton'     : 10,
              'Dark Skeleton': 50,
              'Rattlehead'   : 250,
              'Zombie'       : 30,
              'Vampire'      : 45,
              
              # Humanoid
              'Orc'          : 15,
              'Orc Sergeant' : 75,
              'Dark Guard'   : 80,
              
              # Animal
              'Wild Dog'     : 5,
              'Badger'       : 5,
              'Garden Badger': 3,
              'Cobra'        : 5,
              'Carpathian Wolf': 7,
              'Wolf'         : 5
              }

enemiesByDungeonLevel = {
                         1: ['skeleton', 'orc', 'cobra'],
                         2: ['skeleton', 'orc', 'cobra'],
                         3: ['skeleton', 'orc', 'cobra'],
                         4: ['skeleton', 'orc', 'cobra', 'zombie', 'wolf'],
                         5: ['skeleton', 'orc', 'cobra', 'zombie', 'wolf'],
                         6: ['skeleton', 'orc', 'cobra', 'zombie', 'wolf'],
                         7: ['zombie', 'cwolf', 'vampire'],
                         8: ['zombie', 'cwolf', 'vampire'],
                         9: ['zombie', 'cwolf', 'vampire', 'dguard'],
                        10: ['zombie', 'cwolf', 'vampire', 'dguard']
}

# badger badger badger badger badger badger  &c 

enemiesByWildsLevel = { 0: ['badger', 'wilddog'],
                       1: ['orc', 'orc', 'orc', 'wolf']
                       
                       
                       }