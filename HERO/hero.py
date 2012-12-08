import pygame, random, math, os

from types import *

from IMG import images
from OBJ import spell, item, weapon, armor
from UTIL import const, colors
from SCRIPTS import spellScr
import Queue



class hero(pygame.sprite.Sprite):
    
    def __init__(self, load=None, pos=None):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        
        self.dir = 'down'
        
        self.armorClass = 0
        self.weaponClass = 0
        
        #self.weaponEquipped = None
        #self.armorEquipped = [None,None,None]
        
        self.installLoadedHero(load)
        if pos is not None:
            (self.X, self.Y) = pos
        if self.gender == 'male':
            self.images = images.mHeroImages
        else: self.images = images.fHeroImages
        self.imgIdx = 2
        self.image = self.images[self.imgIdx]
        self.rect = (const.blocksize, const.blocksize, const.blocksize, const.blocksize)
        
        if self.weaponEquipped == None:
            self.gainWeapon(const.WSWORD)
            self.equipWeapon(self.weapons[0])
        if self.spells == []:
            self.learnSpell(0)
        
        self.step = False
        self.moving = False
        self.stepIdx = 0

    def takeStep(self):
        self.imgIdx = self.imgIdx + const.walkingList[self.stepIdx]
        self.stepIdx = ( self.stepIdx + 1 ) % 4
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
    def refillPts(self, rMP=False):
        self.currHP = self.maxHP
        if rMP:
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
        if item.getType() == const.KEY:
            self.keys += 1
            return 'A dungeon key'
        elif item.getType() == const.GOLD:
            self.addGold( item.qty )
            return str(item.qty)+' gold pieces'
        elif item.getType() in range(const.WSWORD, const.RING):
            return self.gainWeapon(item.getType(), [item.plusStr, item.plusItl, item.plusDex] )
        elif item.getType() in range(const.HELMET, const.SSHIELD+1):
            return self.gainArmor(item.getType() )
        itype = item.getID()
        entry = self.items[ itype ]
        if hasattr(entry, "__iter__"):
            self.items[itype].append( item )
        else:
            self.items[itype] = [item]
        return item.getDesc()
    
    def getItems(self):
        availableItems = []
        for it in self.items:
            if type(it) is not IntType:
                if hasattr(it, "__iter__"):
                    if len(it) > 0:
                        for i in it:
                            i.qty = len(it)
                        availableItems.append(it)
                else: 
                    it.qty = 1
                    availableItems.append( it )
        return availableItems
        for i in self.items:
            if hasattr(i, "__iter__"):
                if len(i) > 0:
                    i[0].qty = len(i)
                    availableItems.append(i[0])
        return availableItems
    def takeItem(self, tItem):
        if type(tItem) == IntType:
            tItem = item.Item( tItem )
        try:
            self.items[ tItem.getID() ].remove(tItem)
            if self.items[ tItem.getID()] == []:
                self.items[ tItem.getID() ] = 0
            return True
        except ValueError:
            return False
    
    def hasItem(self, item, qty = 1):
        if hasattr( self.items[item-const.FRUIT1], "__iter__" ):
            if len(self.items[item-const.FRUIT1]) == qty:
                return True
            else: return False
        else: return False
    
    def useItem(self, item, game, battle=False):
        if item == None:
            return 0
        if hasattr(item, "__iter__"):
            item = item[0]
        if item.getName() == 'parchment':
            mySpell = spell.Spell( item.spellNum )
            d = self.castSpell(mySpell, game, battle, True)
            if d > 0:
                self.takeItem(item)
                self.currMP = self.currMP + mySpell.cost
                game.Ticker.tick(mySpell.cost)
                return d
            else: return 0
        item.execute(self)
        self.takeItem(item)
        game.Ticker.tick(60)
    
    def getWeapons(self):
        return self.weapons
    def getWeaponEquipped(self):
        return self.weaponEquipped
    # called when the player buys or finds a new weapon
    def gainWeapon(self, type, mods=None):
        newW = weapon.Weapon(type, mods)
        self.weapons.append(newW)
        return newW.getDesc()
    def loseWeapon(self, weapon):
        self.weapons.remove(weapon)        
    def equipWeapon(self, weapon):
        if weapon == None: return
        if self.weaponEquipped is not None:
            self.strength = self.strength - self.weaponEquipped.plusStr
            self.intell = self.intell - self.weaponEquipped.plusItl
            self.dex = self.dex - self.weaponEquipped.plusDex
            self.weaponClass = self.weaponClass - self.weaponEquipped.level
            self.weapons.append(self.getWeaponEquipped() )
        self.weaponEquipped = weapon
        self.strength = self.strength + weapon.plusStr
        self.intell = self.intell + weapon.plusItl
        self.dex = self.dex + weapon.plusDex
        self.weaponClass = self.weaponClass + self.weaponEquipped.level
        if self.weapons != []:
            self.loseWeapon(weapon)
    
    def getArmor(self):
        return self.armor
    def getArmorEquipped(self):
        return self.armorEquipped
    def gainArmor(self, newA):
        #newA = armor.Armor(type)
        #newA.resist = resist
        self.armor.append(newA)
        return newA.getDesc()
    def loseArmor(self, armor):
        self.armor.remove(armor)
    def equipArmor(self, armor, slot):
        if armor == None: return
        if self.armorEquipped[slot] == None:
            self.armorEquipped[slot] = armor
            self.armorClass += (armor.getLevel())
        else:
            self.armorClass -= (self.armorEquipped[slot].getLevel())
            self.armorClass += (armor.getLevel())
            self.armor.append(self.armorEquipped[slot])
            self.armorEquipped[slot] = armor
        if self.armor != []:
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
    
    def castSpell(self, spell, game, battle=False, item=False):
        if spell == None:
            #game.textMessage('')
            return
        elif (spell.getType() in spellScr.attackSpells and battle==False):
            game.textMessage('That spell may only be cast in battle')
            return False
        elif (spell.getType() in [3] and battle == True):
            game.textMessage('That spell may not be cast in battle')
            return False
        elif spell.cost > self.currMP:
            if item == False:
                game.textMessage("You don't have enough MP!")
                return
        else:
            if not item:
                self.takeMP(spell.cost)
        if spell.getType() == const.TLPT:
            game.textMessage( spell.getCastMsg() )
            (x,y) = game.myMap.getRandomTile()
            self.setXY( x*const.blocksize, y*const.blocksize )
            game.myMap.playerXY = (x, y)
            game.Display.drawSprites(self, game.myMap, game.gameBoard, game, animated=False)
            game.myMap.revealMap()
            game.Display.redrawXMap(game.myMap)
            game.Display.redrawMap(game.myMap, self, game.gameBoard)
            game.displayOneFrame()
            game.textMessage('...and re-integrates!')
        elif spell.getType() in spellScr.attackSpells:
            spell.execute(self, battle)
            game.textMessage(spell.getCastMsg())
            game.Ticker.tick(spell.getCastTime() )
            dmg = spellScr.baseDmg[spell.getType()]+random.randrange(self.intell-5,self.intell+5)/2
            game.textMessage('You hit the monster for '+str(dmg)+' points!')
            return dmg
        #spell.execute(self, battle)
        game.Ticker.tick(spell.getCastTime() )
        game.textMessage(spell.getCastMsg())
        return True
    def getSpells(self):
        return self.spells
    
    def notchKill(self):
        self.slain += 1
    
    def updateStatus(self, game):
        if self.isPoisoned:
            game.Ticker.tick(5)
            if game.Ticker.getTicks() - self.poisonedAt >= 120 * game.Ticker.timeRate:
                game.textMessage('The poison has left your system.')
                self.isPoisoned = False
            else:
                game.textMessage('The poison hurts you...')
                if self.takeDmg(1) < 1:
                    game.txtMessage("You have died!")
                    return False
        if self.isDamned:
            game.Ticker.tick(5)
            if game.Ticker.getTicks() - self.damnedAt >= 120 * game.Ticker.timeRate:
                game.textMessage('You are no longer damned.')
                self.isDamned = False
            else:
                game.textMessage('The damnation siphons your lifepower...')
                if self.takeDmg(1) < 1:
                    game.textMessage("You have died!")
                    return False
        return True
        
    
    def getSaveBall(self):
        gnd = self.gender
        fth = self.faith
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
        sts = [self.isPoisoned, self.isDamned]
        sln = self.slain
        nm = self.name
        return (gnd, fth, str, itl, dex, X, Y, cHP, mHP, cMP, mMP, scr, kys, lvl, cXP, nXP, wpn, weq, arm, aeq, itm, spl, gld, sts, sln, nm)
    
    def installLoadedHero(self, load):
        (gnd, fth, str, itl, dex, X, Y, cHP, mHP, cMP, mMP, scr, kys, lvl, cXP, nXP, wpn, weq, arm, aeq, itm, spl, gld, sts, sln, nm) = load
        self.gender = gnd
        self.faith = fth
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
        self.weaponEquipped = None
        self.equipWeapon(weq)
        
        self.armor = arm
        self.armorEquipped = [None,None,None,
                              None,None,None,
                              None,None,None]
        for i in range(len(aeq)):
            if aeq[i] != None:
                self.equipArmor(a, i)
        
        self.items = itm
        
        self.spells = spl
        
        self.gold = gld
        self.isPoisoned = sts[0]
        self.isDamned = sts[1]
        self.slain = sln
        self.name = nm
        
    
    # for debugging purposes
    def showLocation(self):
        (x1,y1,x2,y2) = self.rect
        locBox = pygame.Surface( (350,50) )
        locBox.fill( colors.grey )
        if pygame.font:
            font = pygame.font.SysFont("arial", 14)
            locText = font.render( "Self.X:"+str(self.X)+"Self.Y:"+str(self.Y)+"RectX:"+str(x1)+"RectY"+str(y1), 1, colors.red, colors.yellow )
            locBox.blit(locText, (10,10) )
        return locBox
