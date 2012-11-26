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

npcList = ['female',
           'firepit',
           'guard',
           'housewife',
           'king',
           'tramp',
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

femaleToFemaleLinesByLevel = { 1 : ["What are you staring at?",
                                   "Look what the cat dragged in!"],
                               2 : ["This town sucks, I can't wait to move out! ",
                                    "God, I'm so bored!" ]
               }

femaleToMaleLinesByLevel = { 1 : ["Get away from me, creep!",
                                  "Not if you were the last dude on earth.",
                                  "Whatever..."],
                            2 : ["So how you doin?",
                                  "Nice sword..."],
                            3 : ["So you work for the government?"] }
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