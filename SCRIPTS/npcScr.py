# Used for creating in-game non-player characters from names provided in map

enemyDict = { 'skeleton'  : ('Skeleton', 'skeleton.bmp'),
              'dskeleton' : ('Dark Skeleton', 'skeleton.bmp'),
              
              'orc'       : ('Orc', 'orc.bmp'),
              'orcsgt'    : ('Orc Sergeant', 'orc.bmp'),
                            
              'zombie'    : ('Zombie', 'zombie.bmp'),
              'cobra'     : ('Cobra', 'cobra.bmp'),
              'vampire'   : ('Vampire', 'vampire.bmp'),
              'wolf'      : ('Wolf', 'wolf.bmp')
             }

npcList = [
           # animals (non-enemy)
           'deer',
           # citizens
           'blacksmith',
           'female',
           'guard',
           'housewife',
           'king',
           'magician',
           'shopkeep',
           'tramp',
           'woodsman',
           # inanimate
           'firepit',
           'fireplace',
           # enemies
           'cobra',
           'orc',
           'orcsgt',
           'skeleton',
           'dskeleton',
           'skeletonking',
           'vampire',
           'wolf',
           'zombie'
           ]

femaleToFemaleLines = [["What are you staring at?",
                                   "Look what the cat dragged in!"],
                       ["This town sucks, I can't wait to move out! ",
                                    "God, I'm so bored!" ]
                       ]

femaleToFemaleLinesByLevel = { 1 : femaleToFemaleLines[0],
                               2 : femaleToFemaleLines[0],
                               3 : femaleToFemaleLines[1],
                               4 : femaleToFemaleLines[1]
               }

femaleToMaleLines = [["Get away from me, creep!",
                      "Not if you were the last dude on earth.",
                      "Whatever..."],
                     ["So how you doin?",
                      "Nice sword..."],
                     ["So you work for the government?"]
                     ]

femaleToMaleLinesByLevel = { 1 : femaleToMaleLines[0],
                             2 : femaleToMaleLines[0],
                             3 : femaleToMaleLines[1],
                             4 : femaleToMaleLines[1] }
''' 

----all NPC types

----female
----tramp
----king
----guard

----skeleton
----dskeleton

----orc
----orcsgt

----zombie
----cobra
----vampire
----wolf

'''