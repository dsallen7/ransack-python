from UTIL import const

from random import randrange

battleOnlySpells = [const.DART, const.FRBL, const.ICBL, const.FBL2, const.IBL2]

heal = lambda s: [s[0] + randrange(5, 15) ] + s[1:]
heal2 = lambda s: [s[0] + randrange(10, 25) ] + s[1:]
heal3 = lambda s: [s[0] + randrange(25, 50) ] + s[1:]
heal4 = lambda s: [s[0] + randrange(50, 100) ] + s[1:]
heal5 = lambda s: [s[0] + randrange(100, 250) ] + s[1:]
nothing = lambda s: s

spellDict = { (const.HEAL): heal,
              (const.HEL2): heal2,
              (const.HEL3): heal3,
              (const.HEL4): heal4,
              (const.HEL5): heal5

                }

imgDict = {const.HEAL: 88,
           const.HEL2: 88,
           const.HEL3: 88,
           const.HEL4: 88,
           const.HEL5: 88,
           const.DART: 89,
           const.FRBL: 90,
           const.FBL2: 90,
           const.FBL3: 90,
           const.ICBL: 91,
           const.IBL2: 91,
           const.TLPT: 92,
           const.ASCD: 93
           
           }

descDict = {const.HEAL: 'Heal I',
            const.HEL2: 'Heal II',
            const.HEL3: 'Heal III',
            const.HEL4: 'Heal IV',
            const.HEL5: 'Heal V',
            
            const.DART: 'Magic Dart',
            const.FRBL: 'Fireball I',
            const.FBL2: 'Fireball II',
            const.FBL3: 'Fireball III',
            
            const.ICBL: 'Iceball I',
            const.ICBL: 'Iceball II',
            
            const.TLPT: 'Teleport',
            const.ASCD: 'Ascend I',
            
            const.EXTD: 'Exit Dungeon',
            const.RTRN: "Return to Village",
            const.ASCD: 'Ascend',
            const.GNCD: 'Genocide'
            }

costDict = { const.HEAL: 4,
             const.HEL2: 8,
             const.HEL3: 12,
             const.HEL4: 16,
             const.HEL5: 20,
             const.DART: 3,
             const.FRBL: 4,
             const.ICBL: 5,
             const.TLPT: 5,
             const.ASCD: 5
            }

timeDict = { const.HEAL: 60,
             const.HEL2: 90,
             const.HEL3: 120,
             const.HEL4: 150,
             const.HEL5: 180,
             const.DART: 30,
             const.FRBL: 30,
             const.ICBL: 30,
             const.TLPT: 60,
             const.ASCD: 60
            }
healingSpells =[const.HEAL,
                const.HEL2,
                const.HEL3,
                const.HEL4,
                const.HEL5
                 
                 ]
attackSpells = [const.DART, 
                const.FRBL, 
                const.FBL2, 
                const.ICBL, 
                const.IBL2
                ]
dungeonOnly = [const.ASCD,
               const.EXTD,
               const.RTRN
               ]
baseDmg = {const.DART : 5, 
                const.FRBL : 10, 
                const.FBL2 : 25, 
                const.ICBL : 15, 
                const.IBL2 : 30
           }

castMsgs = { const.HEAL: 'You feel a little better.',
             const.HEL2: 'You feel better.',
             const.HEL3: 'You feel much better.',
             const.HEL4: 'You feel great!',
             const.HEL5: 'You feel awesome!',
             const.DART: 'An electric dart stabs the enemy!',
             const.FRBL: 'A fireball materializes before your fingertips!',
             const.FBL2: 'A fireball materializes before your fingertips!',
             const.FBL3: 'A fireball materializes before your fingertips!',
             const.ICBL: 'A grim and frostbitten iceball emerges!',
             const.IBL2: 'A grim and frostbitten iceball emerges!',
             const.EXTD: 'Everything goes black... you wake up outside the dungeon.',
             const.RTRN: "You feel like you're leaving your body",
             const.TLPT: 'Your body disintegrates...',
             const.ASCD: 'You float up through the ceiling!',
             const.GNCD: 'A deadly feeling permeates the air!'
            }