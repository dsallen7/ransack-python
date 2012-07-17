import pygame, random, math, os
from load_image import *
from const import *
import spells, items

import Queue

class hero(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.images = range(6)
        self.images[0], self.rect = load_image('link_u.bmp', -1)
        self.images[1], self.rect = load_image('link_d.bmp', -1)
        self.images[2], self.rect = load_image('link_l.bmp', -1)
        self.images[3], self.rect = load_image('link_r.bmp', -1)

        self.image = self.images[1]
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
        
        # first dimension of array is weapon level
        # second is type: Sword, axe, spear, hammer
        self.weapons = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        # (level, type)
        self.weaponEquipped = (0,0)
        
        #same as above
        #Breastplate, helmet, shield
        self.armor = [[1,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        # types are in order as above, level is indicated
        self.armorEquipped = [0,None,0]
        
        #hpot, mpot,?
        self.items = range(20)
        #healing, fireball
        self.spells = []
        self.learnSpell(0)
        self.learnSpell(1)
        
        self.gold = 0

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
        if dir == 'up': self.image = self.images[0]; return (0,-blocksize)
        elif dir == 'down': self.image = self.images[1]; return (0,blocksize)
        elif dir == 'left': self.image = self.images[2]; return (-blocksize,0)
        elif dir == 'right': self.image = self.images[3]; return (blocksize,0)
    
    def getPlayerStats(self):
        return (self.currHP, self.maxHP, self.currMP, self.maxMP, self.strength, self.dex, self.intell, self.score, self.keys, self.currExp, self.nextExp)
    
    def setPlayerStats(self, stats):
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) = stats
        if cHP > mHP:
            cHP = mHP
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
    
    def getSpells(self):
        return self.spells
    
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
        entry = self.items[itype]
        if hasattr(entry, "__iter__"):
            self.items[itype].append( items.Item(itype+86) )
        else:
            self.items[itype] = [items.Item(itype+86)]
    
    def getItems(self):
        availableItems = []
        for i in self.items:
            if hasattr(i, "__iter__"):
                if len(i) > 0:
                    i[0].qty = len(i)
                    availableItems.append(i[0])
        return availableItems
    
    def getSpells(self):
        return self.spells
    
    def getWeapons(self):
        return self.weapons
    
    def getWeaponEquipped(self):
        return self.weaponEquipped
    
    def getArmor(self):
        return self.armor
    
    def getArmorEquipped(self):
        return self.armorEquipped
    
    def addGold(self, amt):
        self.gold += amt
    
    def learnSpell(self, num):
        self.spells += [spells.Spell( num )]
    
    def castSpell(self, spell, battle=False):
        if spell == None:
            return
        if spell.getType() == 1 and battle==False:
            return -1
        spell.execute(self)
        return spell.getType()
    
    def useItem(self, item):
        if item == None:
            return
        item.execute(self)
        self.items[item.getType()-86].remove(item)


    #There is duplicate code here. at some point it would be wise to implement
    #a project-wide messaging/menu utility.
    #UPDATE: done.

    
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
    
