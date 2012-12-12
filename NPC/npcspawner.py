from NPC import npc, citizen, enemy, animal, inanimate

from SCRIPTS import npcScr

def newNpc( n, game):
    (x,y) = n[0]
    if n[1] == 'deer':
        return animal.Deer(x, y, n[2])
    elif n[1] == 'badger':
        return animal.Badger(x, y, n)
    elif n[1] == 'wilddog':
        return animal.wildDog(x, y, n)
    
    elif n[1] == 'blacksmith':
        return citizen.Blacksmith(x, y, n[2])
    elif n[1] == 'castleguard1':
        return citizen.CastleGuard1(x, y, n[2], game.Director)
    elif n[1] == 'guard':
        return citizen.Guard(x, y, n[2])
    elif n[1] == 'female':
        return citizen.Female(x, y, n[2], game.myHero.gender, game.myHero.level )
    elif n[1] == 'generichousewife':
        return citizen.genericHousewife(x, y, n[2])
    elif n[1] == 'tramp':
        return citizen.Tramp(x, y, n[2])
    elif n[1] == 'duke':
        return citizen.Duke(x, y, n[2], game.Director)
    elif n[1] == 'housewife':
        return citizen.Housewife(x, y, n[2], game.Director)
    elif n[1] == 'magician':
        return citizen.Magician(x, y, n[2])
    elif n[1] == 'shopkeep':
        return citizen.Shopkeep(x, y, n[2])
    elif n[1] == 'woodsman':
        return citizen.Woodsman(x, y, n[2], game.Director)
    
    elif n[1] == 'fireplace':
        return inanimate.Fireplace(x, y, n[2])
    elif n[1] == 'candleabra':
        return inanimate.Candleabra(x, y, n[2])
    # enemies
    elif n[1] == 'rattlehead':
        return enemy.rattleHead(x, y, 'Rattlehead', 'rattlehead.bmp', n, game.Director)
    else:
        i = npcScr.enemyDict[ n[1] ]
        return enemy.Enemy(x, y, i[0], i[1], n)