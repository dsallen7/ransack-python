import pygame, random, math, os
from load_image import *
from const import *

from IMG import images
from OBJ import spell, item, weapon, armor

import Queue

class hero(pygame.sprite.Sprite):
    
    def __init__(self, load=None):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        images.load()
        self.images = images.heroImages
        self.imgIdx = 2
        self.image = self.images[self.imgIdx]
        self.rect = (blocksize, blocksize, blocksize, blocksize)
        
        self.dir = 'd'
        
        if load == None:
            
            self.strength = random.randrange(5,10)
            self.intell = random.randrange(5,10)
            self.dex = random.randrange(5,10)
            
            self.X = blocksize
            self.Y = blocksize
            
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
            
            self.gold = 500
            self.isPoisoned = False
        else: self.installLoadedHero(load)
        
        self.step = False
        self.stepIdx = 1

    def takeStep(self):
        self.imgIdx = ( 1 - (self.imgIdx % 2) ) + (2 * (self.imgIdx / 2))
        self.image = self.images[self.imgIdx]
        '''
        if self.dir == 'up':
            if self.imgIdx == 0: self.imgIdx = 1
        if self.step == True:
            self.imgIdx -= 1
            self.image = self.images[self.imgIdx]
            self.step = False
        else:
            self.imgIdx += 1
            self.image = self.images[self.imgIdx]
            self.step = True
        '''

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
        if dir == 'up': self.imgIdx = 0; self.image = self.images[self.imgIdx]; return (0,-blocksize)
        elif dir == 'down': self.imgIdx = 2; self.image = self.images[self.imgIdx]; return (0,blocksize)
        elif dir == 'left': self.imgIdx = 4; self.image = self.images[self.imgIdx]; return (-blocksize,0)
        elif dir == 'right': self.imgIdx = 6; self.image = self.images[self.imgIdx]; return (blocksize,0)
    
    def getPlayerStats(self):
        return (self.currHP, self.maxHP, self.currMP, self.maxMP, self.strength, self.dex, self.intell, self.score, self.keys, self.currExp, self.nextExp)
    
    def setPlayerStats(self, stats):
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) = stats
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
    
    # increases level, next exp for lev up, max HP and MP and refills both
    def gainLevel(self):
        self.level += 1
        self.nextExp = int( math.ceil( self.nextExp * 2.5 ) )
        self.maxHP = int( math.ceil( self.maxHP * 1.15 ) )
        self.maxMP = int( math.ceil( self.maxMP * 1.15 ) )
        self.currHP = self.maxHP
        self.currMP = self.maxMP
    def increaseExp(self, exp):
        self.currExp += exp
        if self.currExp >= self.nextExp:
            self.gainLevel()
            return True
    
    def setItem(self, item, num=1):
        self.items[item] += num
    # Input: tile number denoting item
    def getItem(self, itm, level=None, spellNum=None):
        (itype, qty) = itm
        print itype+FRUIT1
        if itype == KEY or itype+FRUIT1 == KEY:
            self.keys += 1
            return
        elif itype+FRUIT1 == GOLD:
            self.addGold(qty)
            return
        elif itype+FRUIT1 in [112,113,114]:
            level = qty
            self.gainWeapon(itype, level)
            return
        elif itype+FRUIT1 in [117,118,119]:
            level = qty
            self.gainArmor(itype, level)
            return
        elif itype == SPELLBOOK or itype == PARCHMENT:
            newItem = item.Item( itype, level, spellNum )
            itype = itype - FRUIT1
        elif itype+FRUIT1 in range(86, 100): 
            newItem = item.Item(itype+FRUIT1)
        entry = self.items[itype]
        if hasattr(entry, "__iter__"):
            self.items[itype].append( newItem )
        else:
            self.items[itype] = [newItem]
    
    def getItems(self):
        availableItems = []
        for i in self.items:
            if hasattr(i, "__iter__"):
                if len(i) > 0:
                    i[0].qty = len(i)
                    availableItems.append(i[0])
        return availableItems
    def takeItem(self, type):
        self.items[type-86] = self.items[type-86][1:]
    def useItem(self, item):
        if item == None:
            return 0
        item.execute(self)
        self.takeItem(item.getType())
        return 60
    
    def getWeapons(self):
        return self.weapons
    def getWeaponEquipped(self):
        return self.weaponEquipped
    # called when the player buys or finds a new weapon
    def gainWeapon(self, type, level):
        self.weapons.append(weapon.Weapon(type, level))
    def loseWeapon(self, weapon):
        self.weapons.remove(weapon)        
    def equipWeapon(self, weapon):
        if weapon == None: return
        if self.weaponEquipped is not None:
            self.weapons.append(self.getWeaponEquipped() )
        self.weaponEquipped = weapon
        self.loseWeapon(weapon)
    
    def getArmor(self):
        return self.armor
    def getArmorEquipped(self):
        return self.armorEquipped
    def gainArmor(self, type, level):
        self.armor.append(armor.Armor(type, level))
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
    def castSpell(self, spell, hud, battle=False):
        if spell == None:
            return
        if spell.getType() in [1,2] and battle==False:
            return -1
        spell.execute(self, hud)
        return spell.getType()    
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
        return (str, itl, dex, X, Y, cHP, mHP, cMP, mMP, scr, kys, lvl, cXP, nXP, wpn, weq, arm, aeq, itm, spl, gld)
    
    def installLoadedHero(self, load):
        (str, itl, dex, X, Y, cHP, mHP, cMP, mMP, scr, kys, lvl, cXP, nXP, wpn, weq, arm, aeq, itm, spl, gld) = load
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
        
    
    # for debugging purposes
    def showLocation(self, gameBoard):
        (x1,y1,x2,y2) = self.rect
        locBox = pygame.Surface( (350,50) )
        locBox.fill( grey )
        if pygame.font:
            font = pygame.font.SysFont("arial", 14)
            locText = font.render( "Self.X:"+str(self.X)+"Self.Y:"+str(self.Y)+"RectX:"+str(x1)+"RectY"+str(y1), 1, red, yellow )
            locBox.blit(locText, (10,10) )
        gameBoard.blit(locBox, (0, 200) )
        pygame.display.flip()
    
