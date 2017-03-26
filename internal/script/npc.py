# Used for creating in-game non-player characters from names provided in map
# identifier: (display name, NPC image file)
enemyDict = { 
             'badger'    : ('Badger', 'badger.bmp'),
             'gardenbadger'    : ('Garden Badger', 'badger.bmp'),
             'wilddog'    : ('Wild Dog', 'wilddog.bmp'),
              'skeleton'  : ('Skeleton', 'skeleton.bmp'),
              'dskeleton' : ('Dark Skeleton', 'skeleton.bmp'),
              
              'orc'       : ('Orc', 'orc.bmp'),
              'orcsgt'    : ('Orc Sergeant', 'orc.bmp'),
              'dguard'    : ('Dark Guard', 'darkguard.bmp'),
                            
              'zombie'    : ('Zombie', 'zombie.bmp'),
              'cobra'     : ('Cobra', 'cobra.bmp'),
              'vampire'   : ('Vampire', 'vampire.bmp'),
              'cwolf'     : ('Carpathian Wolf', 'cwolf.bmp'),
              'wolf'      : ('Wolf', 'wolf.bmp')
             }

npcList = [
           # animals (enemy status optional)
           'badger',
           'deer',
           'gardenbadger',
           'wilddog',
           # citizens
           'blacksmith',
           'castleguard1',
           'darkguard',
           'dungeonguard',
           'female',
           'gardener',
           'generichousewife',
           'guard',
           'housewife',
           'duke',
           'magician',
           'shopmagician',
           'shopkeep',
           'tramp',
           'woodsman',
           # inanimate
           'firepit',
           'fireplace',
           'candleabra',
           # enemies
           'cobra',
           'cwolf',
           'orc',
           'orcsgt',
           'skeleton',
           'dskeleton',
           'rattlehead',
           'vampire',
           'wolf',
           'zombie'
           ]

femaleToFemaleLines = [["What are you staring at?",
                        "What's your problem?",
                        "Look what the cat dragged in!"],
                       ["This town sucks, I can't wait to move out! ",
                        "God, I'm so bored!" ],
                       ["We should totally hang out!",
                        "I wanna be like you someday!"]
                       ]

femaleToFemaleLinesByLevel = { 1 : femaleToFemaleLines[0],
                               2 : femaleToFemaleLines[0],
                               3 : femaleToFemaleLines[0],
                               4 : femaleToFemaleLines[1],
                               5 : femaleToFemaleLines[1],
                               6 : femaleToFemaleLines[1],
                               7 : femaleToFemaleLines[2],
                               8 : femaleToFemaleLines[2],
                               9 : femaleToFemaleLines[2]
               }

femaleToMaleLines = [["Get away from me, creep!",
                      "Not if you were the last dude on earth.",
                      "Whatever..."],
                     ["Hi there...",
                      "So you like, work for the government?"],
                     [ "Nice sword...",
                      "Doing anything tonight? ;)"],
                     
                     ]

femaleToMaleLinesByLevel = { 1 : femaleToMaleLines[0],
                             2 : femaleToMaleLines[0],
                             3 : femaleToMaleLines[0],
                             4 : femaleToMaleLines[1],
                             5 : femaleToMaleLines[1],
                             6 : femaleToMaleLines[1],
                             7 : femaleToMaleLines[2],
                             8 : femaleToMaleLines[2],
                             9 : femaleToMaleLines[2] }

# question, YES response, NO response

genericHousewifeDialogs = ["Lovely day, isn't it?",
                           "Fish stew for breakfast, lunch and dinner. I hate my life.",
                           "I bet my husband's down at that tavern again. He's gonna get it when he gets home!",
                           "That Duke, what a typical politician. Takes our very last scrap of gold while he sits around getting fat..."
                           
                           ]

trampDialogs = [
               
               ('Hey there, looking for a good time?',
                "Hehe, you can't afford it!",
                "Aw, that's too bad! ;)"),
               
               ('Wanna come back to my place?',
                "Well you can't! Hah! :-P",
                "Come on, you know you want to! ;)"),
                
                ("How about you and me blow this joint?",
                 "LOL JK you thought I was for real!",
                 "Come on, you know you want to! ;)")
               
               ]
               
               
               
''' 

----all NPC types

----blacksmith
----female
----housewife
----tramp
----king
----guard
----shopkeep

----skeleton
----dskeleton

----orc
----orcsgt

----zombie
----cobra
----vampire
----wolf

'''