import pygame, random, math, os
from load_image import *
from const import *

from types import *

from IMG import images
from OBJ import spell, item, weapon, armor
from UTIL import const, colors

import Queue

class hero(pygame.sprite.Sprite):
    
    def __init__(self, load=None):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.images = images.loadNPC('herosheet.bmp')
        self.imgIdx = 2
        self.image = self.images[self.imgIdx]
        self.rect = (const.blocksize, const.blocksize, const.blocksize, const.blocksize)
        
        self.dir = 'down'
        
        self.armorClass = 0
        self.weaponClass = 0
        
        if load == None:
            
            self.strength = random.randrange(5,10)
            self.intell = random.randrange(5,10)
            self.dex = random.randrange(5,10)
            
            self.X = const.blocksize
            self.Y = const.blocksize
            
            self.currHP = 50
            self.maxHP = 50
            
            self.currMP = 20
            self.maxMP = 20
            
            self.score = 0
            self.keys = 0
            
            self.level = 1
            self.currExp = 0
            self.nextExp = 20
            
            self.weapons = []
            self.weaponEquipped = None
            self.gainWeapon(26,0)
            self.equipWeapon(self.weapons[0])
            
            self.armor = []
            self.armorEquipped = [None,None,None]
            
            self.items = range(20)
            
            self.spells = []
            self.learnSpell(0)
            self.learnSpell(1)
            
            self.gold = 5000
            self.isPoisoned = False
        else: self.installLoadedHero(load)
        
        self.step = False
        self.moving = False
        self.stepIdx = 1

    def takeStep(self):
        self.imgIdx = ( 1 - (self.imgIdx % 2) ) + (2 * (self.imgIdx / 2))
        self.image = self.images[self.imgIdx]

    def getXY(self):
        return (self.X,self.Y)
    
    def setXY(self,x,y):
        self.X = x
        self.Y = y
        
    def getRect(self):
        return self.rect
    
    def setRect(self,x1,y1,x2,y2):
        self.rect = (x1,y1,x2,y2)
    
    def changeDirection(self, dir):
        self.dir = dir
        if dir == 'up': self.imgIdx = 0; self.image = self.images[self.imgIdx]; return (0,-const.blocksize)
        elif dir == 'down': self.imgIdx = 2; self.image = self.images[self.imgIdx]; return (0,const.blocksize)
        elif dir == 'left': self.imgIdx = 4; self.image = self.images[self.imgIdx]; return (-const.blocksize,0)
        elif dir == 'right': self.imgIdx = 6; self.image = self.images[self.imgIdx]; return (const.blocksize,0)
    
    def getPlayerStats(self):
        return (self.currHP, self.maxHP, self.currMP, self.maxMP, self.strength, self.dex, self.intell, self.score, self.keys, self.currExp, self.nextExp, self.isPoisoned)
    
    def setPlayerStats(self, stats):
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn) = stats
        if cHP > mHP:
            cHP = mHP
        if cMP > mMP:
            cMP = mMP
        self.currHP = cHP
        self.currMP = cMP
        self.strength = sth
        self.dex = dex
        self.intell = itl
        self.score = scr
        self.keys = kys
        self.isPoisoned = psn
    
    def takeKey(self):
        self.keys -= 1
    
    def takeDmg(self,dmg):
        self.currHP -= dmg
        return self.currHP
    
    def takeMP(self, mp):
        if self.currMP - mp >= 0:
            self.currMP -= mp
            return True
        else:
            return False
    
    def getCurrHP(self):
        return self.currHP
    def getMaxHP(self):
        return self.maxHP
    def refillPts(self):
        self.currHP = self.maxHP
        self.currMP = self.maxMP
    
    # increases level, next exp for lev up, max HP and MP and refills both
    def gainLevel(self):
        self.level += 1
        self.nextExp = int( math.ceil( self.nextExp * 2.5 ) )
        self.maxHP = int( math.ceil( self.maxHP * 1.15 ) )
        self.maxMP = int( math.ceil( self.maxMP * 1.15 ) )
        self.refillPts()
    def increaseExp(self, exp):
        self.currExp += exp
        if self.currExp >= self.nextExp:
            self.gainLevel()
            return True
    
    def setItem(self, item, num=1):
        self.items[item] += num
    # Input: tile number denoting item
    def getItem(self, item):
        if item.getType() == KEY or item.getType() == KEY:
            self.keys += 1
            return 'A dungeon key'
        elif item.getType() == GOLD:
            self.addGold( item.qty )
            return str(item.qty)+' gold pieces'
        elif item.getType() in [112,113,114]:
            level = qty
            return self.gainWeapon(itype, level)
        elif item.getType() in [117,118,119]:
            return self.gainArmor(itype, level)
        elif item.getType() == const.SPELLBOOK or item.getType() == const.PARCHMENT:
            pass
        elif item.getType() in range(86, 100): 
            pass
        itype = item.getType()-const.FRUIT1
        entry = self.items[ itype ]
        if hasattr(entry, "__iter__"):
            self.items[itype].append( item )
        else:
            self.items[itype] = [item]
        return item.getDesc()
    
    def getItems(self):
        availableItems = []
        for it in self.items:
            #print it
            if type(it) is not IntType:
                if hasattr(it, "__iter__"):
                    if len(it) > 0:
                        for i in it:
                            i.qty = len(it)
                        availableItems.append(it)
                else: 
                    it.qty = 1
                    availableItems.append( it )
        print availableItems
        return availableItems
        for i in self.items:
            if hasattr(i, "__iter__"):
                if len(i) > 0:
                    i[0].qty = len(i)
                    availableItems.append(i[0])
        return availableItems
    def takeItem(self, type):
        self.items[type-const.FRUIT1] = self.items[type-const.FRUIT1][1:]
    def useItem(self, item, game, battle=False):
        if item == None:
            return 0
        if hasattr(item, "__iter__"):
            item = item[0]
        if item.getName() == 'parchment':
            mySpell = spell.Spell( item.spellNum )
            if self.castSpell(mySpell, game, battle):
                self.takeItem(item.getType())
                self.currMP = self.currMP + mySpell.cost
                return mySpell.getCastTime()
            else: return 0
        item.execute(self)
        self.takeItem(item.getType())
        return 60
    
    def getWeapons(self):
        return self.weapons
    def getWeaponEquipped(self):
        return self.weaponEquipped
    # called when the player buys or finds a new weapon
    def gainWeapon(self, type, level):
        newW = weapon.Weapon(type, level)
        self.weapons.append(newW)
        return newW.getDesc()
    def loseWeapon(self, weapon):
        self.weapons.remove(weapon)        
    def equipWeapon(self, weapon):
        if weapon == None: return
        if self.weaponEquipped is not None:
            self.strength = self.strength - weapon.plusStr
            self.intell = self.intell - weapon.plusItl
            self.dex = self.dex - weapon.plusDex
            self.weapons.append(self.getWeaponEquipped() )
        self.weaponEquipped = weapon
        self.strength = self.strength + weapon.plusStr
        self.intell = self.intell + weapon.plusItl
        self.dex = self.dex + weapon.plusDex
        self.loseWeapon(weapon)
    
    def getArmor(self):
        return self.armor
    def getArmorEquipped(self):
        return self.armorEquipped
    def gainArmor(self, type, level):
        newA = armor.Armor(type, level)
        self.armor.append(newA)
        return newA.getDesc()
    def loseArmor(self, armor):
        self.armor.remove(armor)
    def equipArmor(self, armor):
        if armor == None: return
        print armor.getType()
        if self.armorEquipped[armor.getType()-31] == None:
            self.armorEquipped[armor.getType()-31] = armor
        else: 
            self.armor.append(self.armorEquipped[armor.getType()])
            self.armorEquipped[armor.getType()-31] = armor
        self.loseArmor(armor)
    
    def addGold(self, amt):
        self.gold += amt
    def getGold(self):
        return self.gold
    def takeGold(self, amt):
        if self.gold >= amt:
            self.gold -= amt
            return True
        else:
            return False
    
    def learnSpell(self, num):
        self.spells += [spell.Spell( num )]
    def castSpell(self, spell, game, battle=False):
        if spell == None:
            #game.textMessage('')
            return
        elif (spell.getType() in [1,2] and battle==False):
            game.textMessage('That spell may only be cast in battle')
            return False
        elif (spell.getType() in [3] and battle == True):
            game.textMessage('That spell may not be cast in battle')
            return False
        elif spell.cost > self.currMP:
            game.textMessage("You don't have enough MP!")
            return
        if spell.getType() == const.TLPT:
            (x,y) = game.myMap.getRandomTile()
            self.setXY( x*const.blocksize, y*const.blocksize )
            game.myMap.playerXY = (x, y)
            game.Display.drawSprites(self, game.myMap, game.gameBoard, game, animated=False)
            game.myMap.revealMap()
            game.Display.redrawXMap(game.myMap)
            game.Display.redrawMap(game.myMap, self, game.gameBoard)
            game.displayGameBoard()
            game.textMessage( spell.getCastMsg() )
        elif spell.getType() == const.FRBL:
            spell.execute(self, game.myHud, battle)
            game.textMessage(spell.getCastMsg())
            game.Ticker.tick(spell.getCastTime() )
            dmg = random.randrange(self.intell,2*self.intell)
            game.textMessage('The fireball hits the monster for '+str(dmg)+' points!')
            return dmg
        elif spell.getType() == const.ICBL:
            spell.execute(self, game.myHud, battle)
            game.textMessage(spell.getCastMsg())
            game.Ticker.tick(spell.getCastTime() )
            dmg = random.randrange(self.intell,2*self.intell)
            game.textMessage('The iceball hits the monster for '+str(dmg)+' points!')
            return dmg
        spell.execute(self, game.myHud, battle)
        game.Ticker.tick(spell.getCastTime() )
        game.textMessage(spell.getCastMsg())
        return True
    def getSpells(self):
        return self.spells
    
    def getSaveBall(self):
        str = self.strength
        itl = self.intell
        dex = self.dex
        
        X = self.X
        Y = self.Y
        
        cHP = self.currHP
        mHP = self.maxHP
        
        cMP = self.currMP
        mMP = self.maxMP
        
        scr = self.score
        kys = self.keys
        
        lvl = self.level
        cXP = self.currExp
        nXP = self.nextExp
        
        wpn = self.weapons
        weq = self.weaponEquipped
        
        arm = self.armor
        aeq = self.armorEquipped
        
        itm = self.items
        spl = self.spells
        gld = self.gold
        psn = self.isPoisoned
        return (str, itl, dex, X, Y, cHP, mHP, cMP, mMP, scr, kys, lvl, cXP, nXP, wpn, weq, arm, aeq, itm, spl, gld, psn)
    
    def installLoadedHero(self, load):
        (str, itl, dex, X, Y, cHP, mHP, cMP, mMP, scr, kys, lvl, cXP, nXP, wpn, weq, arm, aeq, itm, spl, gld, psn) = load
        self.strength = str
        self.intell = itl
        self.dex = dex
        
        self.X = X
        self.Y = Y
        
        self.currHP = cHP
        self.maxHP = mHP
        
        self.currMP = cMP
        self.maxMP = mMP
        
        self.score = scr
        self.keys = kys
        
        self.level = lvl
        self.currExp = cXP
        self.nextExp = nXP
        
        self.weapons = wpn
        self.weaponEquipped = weq
        
        self.armor = arm
        self.armorEquipped = aeq
        
        self.items = itm
        
        self.spells = spl
        
        self.gold = gld
        self.isPoisoned = psn
        
    
    # for debugging purposes
    def showLocation(self, screen):
        (x1,y1,x2,y2) = self.rect
        locBox = pygame.Surface( (350,50) )
        locBox.fill( grey )
        if pygame.font:
            font = pygame.font.SysFont("arial", 14)
            locText = font.render( "Self.X:"+str(self.X)+"Self.Y:"+str(self.Y)+"RectX:"+str(x1)+"RectY"+str(y1), 1, red, yellow )
            locBox.blit(locText, (10,10) )
        screen.blit(locBox, (0, 0) )
        pygame.display.flip()
    
