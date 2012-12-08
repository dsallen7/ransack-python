pEnemies = ['Cobra', 'Scorpion']
dEnemies = ['Zombie','Skeleton', 'Vampire']

healthDict = { 
              # Undead
              'Skeleton'     : 30,
              'Dark Skeleton': 80,
              'Skeleton King': 250,
              'Zombie'       : 50,
              'Vampire'      : 75,
              
              # Humanoid
              'Orc'          : 25,
              'Orc Sergeant' : 75,
              
              # Animal
              'Cobra'        : 30,
              'Wolf'         : 40
              }

attackDict = { 
              # Undead
              'Skeleton'     : 10,
              'Dark Skeleton': 17,
              'Skeleton King': 25,
              'Zombie'       : 13,
              'Vampire'      : 15,
              
              # Humanoid
              'Orc'          : 10,
              'Orc Sergeant' : 18,
              
              # Animal
              'Cobra'        : 7,
              'Wolf'         : 15
              }

imgFileDict = { 
              # Undead
              'Skeleton'     : ['rattlehead1.bmp', 'rattlehead2.bmp'],
              'Dark Skeleton': ['rattlehead1.bmp', 'rattlehead2.bmp'],
              'Skeleton King': ['rattlehead1.bmp', 'rattlehead2.bmp'],
              'Zombie'       : ['cobra1.bmp', 'cobra2.bmp'],
              'Vampire'      : ['cobra1.bmp', 'cobra2.bmp'],
              
              # Humanoid
              'Orc'          : ['orc1.bmp', 'orc2.bmp'],
              'Orc Sergeant' : ['orc1.bmp', 'orc2.bmp'],
              
              # Animal
              'Cobra'        : ['cobra1.bmp', 'cobra2.bmp'],
              'Wolf'         : ['cobra1.bmp', 'cobra2.bmp']               
               }

lootDict = { 
              # Undead
              'Skeleton'     : 10,
              'Dark Skeleton': 50,
              'Skeleton King': 250,
              'Zombie'       : 30,
              'Vampire'      : 45,
              
              # Humanoid
              'Orc'          : 15,
              'Orc Sergeant' : 75,
              
              # Animal
              'Cobra'        : 5,
              'Wolf'         : 5
              }

enemiesByLevel = {  1: ['skeleton', 'orc', 'cobra'],
                    2: ['skeleton', 'orc', 'cobra'],
                    3: ['skeleton', 'orc', 'cobra'],
                    4: ['skeleton', 'orc', 'cobra', 'zombie', 'wolf'],
                    5: ['skeleton', 'orc', 'cobra', 'zombie', 'wolf'],
                    6: ['skeleton', 'orc', 'cobra', 'zombie', 'wolf'],
                    7: ['zombie', 'wolf', 'vampire'],
                    8: ['zombie', 'wolf', 'vampire'],
                    9: ['zombie', 'wolf', 'vampire'],
                   10: ['zombie', 'wolf', 'vampire']
}
