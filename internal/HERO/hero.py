import pygame, random, math, os

from types import *

from IMG import images
from OBJ import spell, item, weapon, armor
from UTIL import const, colors, queue
from SCRIPTS import itemScr, spellScr
import Queue

from math import floor, ceil

class hero(pygame.sprite.Sprite):
    
    def __init__(self, load=None, pos=None):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        
        self.dir = 'down'
        
        self.armorClass = 0
        self.weaponClass = 0
        
        #self.weaponEquipped = None
        #self.armorEquipped = [None,None,None]
        
        self.hasLantern = False
        
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
        self.moveQueue = queue.Queue()
        
    def takeStep(self):
        self.imgIdx = self.imgIdx + const.walkingList[self.stepIdx]
        self.stepIdx = ( self.stepIdx + 1 ) % 4
        self.image = self.images[self.imgIdx]
    def moveFromQueue(self):
        d = self.moveQueue.pop()
        if d == 0:
            return 'right'
        elif d == 1:
            return 'down'
        elif d == 2:
            return 'left'
        elif d == 3:
            return 'up'
        elif d == 4:
            return None
    def moveEnqueue(self, moves):
        for c in moves:
            self.moveQueue.push(int(c))

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
    def drinkWater(self, qty=None):
        if self.thirst == 0:
            return False
        if qty is None:
            self.thirst = 0
            return True
        else:
            self.thirst = max(0, self.thirst-qty)
            return True
    
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
    def getItem(self, gItem):
        if gItem.getType() in const.GAMEITEMS:
            if gItem.getType() == const.LANTERN:
                self.hasLantern = True
        if gItem.getType() == const.KEY:
            self.keys += 1
            return 'A dungeon key'
        elif gItem.getType() == const.GOLD:
            self.addGold( gItem.qty )
            return str(gItem.qty)+' gold pieces'
        elif gItem.getType() in range(const.WSWORD, const.RING):
            return self.gainWeapon(gItem.getType(), [gItem.plusStr, gItem.plusItl, gItem.plusDex] )
        elif gItem.getType() in range(const.RING, const.SSHIELD+1):
            return self.gainArmor( gItem )
        itype = gItem.getID()
        entry = self.items[ itype ]
        if hasattr(entry, "__iter__"):
            self.items[itype].append( gItem )
        else:
            self.items[itype] = [gItem]
        return gItem.getDesc()
    
    def getItems(self):
        availableItems = []
        for it in self.items:
            if type(it) is not IntType:
                if hasattr(it, "__iter__"):
                    if len(it) > 0:
                        for i in it:
                            i.qty = len(it)
                        availableItems.append(it[0])
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
        try:
            if tItem.getName() == 'weapon':
                self.loseWeapon(tItem)
                return
            elif tItem.getName() == 'armor':
                self.loseArmor(tItem)
                return
        except AttributeError as e:
            print 'AttributeError in takeItem: ', e
        if type(tItem) == IntType:
            tItem = item.Item( tItem )
        try:
            self.items[ tItem.getID() ] = self.items[ tItem.getID() ][1:]
            if self.items[ tItem.getID()] == []:
                self.items[ tItem.getID() ] = 0
            return True
        except ValueError as e:
            print 'ValueError in takeItem: ', e
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
        if item.getType() in const.GAMEITEMS:
            game.textMessage( item.execute(self) )
            game.Ticker.tick(60)
            return
        if item.getType() == const.CERTIFICATE:
            if item.certNum == const.SAVECERT:
                if game.saveGame( 'ransack0.sav'):
                    game.textMessage('Game Saved')
                else: game.textMessage('File Error o_O')
            elif item.certNum == const.RETURNCERT:
                game.portalMove(*item.loc)
            self.takeItem(item)
            return
        if item.getName() == 'parchment':
            mySpell = spell.Spell( item.spellNum )
            d = self.castSpell(mySpell, game, battle, True)
            if d != False:
                self.takeItem(item)
                game.Ticker.tick(mySpell.cost)
            return d
        item.execute(self)
        self.takeItem(item)
        if item.type in itemScr.foodItems:
            self.hunger = max(0, self.hunger-itemScr.foodValue[item.type])
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
        print self.weaponClass
        print weapon.level
        self.weaponClass = self.weaponClass + self.weaponEquipped.level
        if weapon in self.weapons:
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
    def equipArmor(self, newArmor, slot):
        oldArmor = self.armorEquipped[slot]
        if newArmor == None: return
        if self.armorEquipped[slot] == None:
            self.armorEquipped[slot] = newArmor
            self.armorClass += (newArmor.getLevel())
            if newArmor.enh == 'Plus HP':
                self.currHP = int(ceil( self.currHP*( self.maxHP + newArmor.enhAmt)/self.maxHP ))
                self.maxHP += newArmor.enhAmt
            elif newArmor.enh == 'Plus MP':
                self.currMP = int(ceil( self.currMP*( self.maxMP + newArmor.enhAmt)/self.maxMP ))
                self.maxMP += newArmor.enhAmt
            elif newArmor.enh == 'Plus WP':
                self.weaponClass += newArmor.enhAmt
        else:
            self.armorClass -= (oldArmor.getLevel())
            self.armorClass += (newArmor.getLevel())
            self.armor.append(oldArmor)
            self.armorEquipped[slot] = newArmor
            if oldArmor.enh == 'Plus HP':
                self.maxHP += newArmor.enhAmt
                self.currHP = min( self.currHP, self.maxHP )
            if oldArmor.enh == 'Plus MP':
                self.maxMP += oldArmor.enhAmt
                self.currMP = min( self.currMP, self.maxMP )
            if oldArmor.enh == 'Plus WP':
                self.weaponClass -= oldArmor.enhAmt
            if newArmor.enh == 'Plus HP':
                self.currHP = int(ceil( self.currHP*( self.maxHP + armor.enhAmt)/self.maxHP ))
                self.maxHP += newArmor.enhAmt
            if newArmor.enh == 'Plus MP':
                self.currMP = int(ceil( self.currMP*( self.maxMP + armor.enhAmt)/self.maxMP ))
                self.maxMP += newArmor.enhAmt
            if newArmor.enh == 'Plus WP':
                self.weaponClass += newArmor.enhAmt
        if newArmor in self.armor:
            self.loseArmor(newArmor)
    
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
    
    def castSpell(self, spell, game, battle=False, isItem=False):
        if spell == None:
            #game.textMessage('')
            return False
        elif (spell.getType() in spellScr.attackSpells and battle==False):
            game.textMessage('That spell may only be cast in battle')
            return False
        elif (spell.getType() in [3] and battle == True):
            game.textMessage('That spell may not be cast in battle')
            return False
        elif (spell.getType() in spellScr.dungeonOnly and game.myMap.getType() not in ['dungeon', 'maze', 'fortress']):
            #game.textMessage('You must be in the Dungeon to cast that spell')
            game.textMessage('That spell may only be cast in the dungeon.')
            return False
        elif spell.cost > self.currMP:
            if item == False:
                game.textMessage("You don't have enough MP!")
                return False
        else:
            if isItem == False:
                self.takeMP(spell.cost)
        #scripted spells
        if spell.getType() == const.TLPT:
            game.textMessage( spell.getCastMsg() )
            loc1 = self.getXY()
            (x, y) = game.myMap.getRandomTile()
            x = x*const.blocksize
            y = y*const.blocksize
            self.setXY( x, y )
            loc2 = (x, y)
            game.myMap.playerXY = loc2
            #game.Display.mapJump(self, game.myMap, game.gameBoard, game, loc1, loc2)
            game.Display.drawSprites(self, game.myMap, game.gameBoard, game, animated=False)
            game.myMap.revealMap()
            game.Display.redrawXMap(game.myMap)
            game.Display.redrawMap(game.myMap, self, game.gameBoard)
            game.displayOneFrame()
            game.textMessage('...and re-integrates!')
            return
        if spell.getType() == const.ASCD:
            loc = game.myWorld.upLevel()
            game.transition(loc)
            game.Display.drawSprites(game.myHero,
                                     game.myMap,
                                     game.gameBoard,
                                     game,
                                     animated=False)
            return
        elif spell.getType() in spellScr.attackSpells:
            spell.execute(self, battle)
            game.textMessage(spell.getCastMsg())
            game.Ticker.tick(spell.getCastTime() )
            dmg = spellScr.baseDmg[spell.getType()]+random.randrange(self.intell-5,self.intell+5)/2
            game.textMessage('You hit the monster for '+str(dmg)+' points!')
            return dmg
        spell.execute(self, battle)
        game.Ticker.tick(spell.getCastTime() )
        game.textMessage(spell.getCastMsg())
        return True
    def getSpells(self):
        return self.spells
    
    def notchKill(self):
        self.slain += 1
    
    def updateStatus(self, game):
        if self.hungerAt == 0:
            self.hungerAt = game.Ticker.getTicks()
        elif game.Ticker.getTicks() >= self.hungerAt + (14400 * game.Ticker.timeRate):
            self.hunger += 1
            if self.hunger > 10:
                game.txtMessage("You have starved to death!")
                return False
        if self.thirstAt == 0:
            self.thirstAt = game.Ticker.getTicks()
        elif game.Ticker.getTicks() >= self.thirstAt + (14400 * game.Ticker.timeRate):
            self.thirst += 1
            if self.thirst > 10:
                game.txtMessage("You have died of thirst!")
                return False
                
        if self.isPoisoned:
            game.Ticker.tick(5)
            if game.Ticker.getTicks() - self.poisonedAt >= 120 * game.Ticker.timeRate:
                # poison, damnation last for 2 "minutes"
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
        flv = self.faithLevel
        
        str = self.strength
        itl = self.intell
        dex = self.dex
        
        hng = self.hunger
        thr = self.thirst
        
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
        sts = [self.isPoisoned, self.isDamned, self.hasLantern]
        sln = self.slain
        nm = self.name
        return (gnd, fth, flv,
                str, itl, dex,
                hng, thr,
                X, Y, 
                cHP, mHP, cMP, mMP, 
                scr, kys, lvl, cXP, nXP, 
                wpn, weq, arm, aeq, 
                itm, spl, gld, sts, sln, nm)
    
    def installLoadedHero(self, load):
        (gnd, fth, flv,
         str, itl, dex,
         hng, thr,
         X, Y,
         cHP, mHP, cMP, mMP,
         scr, kys, lvl, cXP, nXP,
         wpn, weq, arm, aeq,
         itm, spl, gld, sts, sln, nm) = load
         
        self.gender = gnd
        self.faith = fth
        self.faithLevel = flv
        self.strength = str
        self.intell = itl
        self.dex = dex
        
        self.hunger = hng
        self.thirst = thr
        self.hungerAt = 0
        self.thirstAt = 0
        
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
                self.equipArmor(aeq[i], i)
        
        self.items = itm
        
        self.spells = spl
        
        self.gold = gld
        self.isPoisoned = sts[0]
        self.isDamned = sts[1]
        self.hasLantern = sts[2]
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
