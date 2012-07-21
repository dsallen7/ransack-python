import pygame, random, math, os
from load_image import *
from const import *

from IMG import images
from OBJ import spell, item, weapon, armor

import Queue

class hero(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        images.load()
        self.images = images.heroImages
        self.imgIdx = 2
        self.image = self.images[self.imgIdx]
        self.rect = (blocksize, blocksize, blocksize, blocksize)
        
        self.dir = 'd'
        
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
        self.gainWeapon(0,0)
        self.equipWeapon(self.weapons[0])
        
        self.armor = []
        self.armorEquipped = [None,None,None]
        
        self.items = range(20)
        
        self.spells = []
        self.learnSpell(0)
        self.learnSpell(1)
        
        self.gold = 0
        
        self.step = False

    def takeStep(self):
        if self.step == True:
            self.imgIdx -= 1
            self.image = self.images[self.imgIdx]
            self.step = False
        else: 
            self.imgIdx += 1
            self.image = self.images[self.imgIdx]
            self.step = True

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
    def getItem(self, itype):
        if itype == KEY:
            self.keys += 1
            return
        entry = self.items[itype]
        if hasattr(entry, "__iter__"):
            self.items[itype].append( item.Item(itype+86) )
        else:
            self.items[itype] = [item.Item(itype+86)]
    def getItems(self):
        availableItems = []
        for i in self.items:
            if hasattr(i, "__iter__"):
                if len(i) > 0:
                    i[0].qty = len(i)
                    availableItems.append(i[0])
        return availableItems
    def useItem(self, item):
        if item == None:
            return
        item.execute(self)
        self.items[item.getType()-86].remove(item)
    
    def getWeapons(self):
        return self.weapons
    def getWeaponEquipped(self):
        return self.weaponEquipped
    # called when the player buys or finds a new weapon
    def gainWeapon(self, type, level):
        self.weapons.append(weapon.Weapon(type, level))
    def equipWeapon(self, weapon):
        self.weaponEquipped = weapon
        self.weapons.remove(weapon)
    
    def getArmor(self):
        return self.armor
    def getArmorEquipped(self):
        return self.armorEquipped
    def gainArmor(self, type, level):
        self.armor.append(armor.Armor(type, level))
    def equipArmor(self, armor):
        if self.armorEquipped[armor.getType()] == None:
            self.armorEquipped[armor.getType()] = armor
        else: 
            self.armor.append(self.armorEquipped[armor.getType()])
            self.armorEquipped[armor.getType()] = armor
    
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
    def castSpell(self, spell, battle=False):
        if spell == None:
            return
        if spell.getType() == 1 and battle==False:
            return -1
        spell.execute(self)
        return spell.getType()    
    def getSpells(self):
        return self.spells
    
    # for debugging purposes
    def showLocation(self, gameBoard):
        (x1,y1,x2,y2) = self.rect
        locBox = pygame.Surface( (350,50) )
        locBox.fill( grey )
        if pygame.font:
            font = pygame.font.SysFont("arial", 14)
            locText = font.render( "Self.X:"+str(self.X)+"Self.Y:"+str(self.Y)+"RectX:"+str(x1)+"RectY"+str(y1), 1, red, yellow )
            locBox.blit(locText, (10,10) )
        gameBoard.blit(locBox, (100, 300) )
        pygame.display.flip()
    
