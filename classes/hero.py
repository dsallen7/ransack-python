import pygame, random, math
from load_image import *
from const import *

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
        
        #Sword, axe, spear, hammer
        self.weapons = [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.weaponEquipped = (0,1)
        
        #Breastplate, helmet, shield
        self.armor = [[1,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.armorEquipped = [(0,1),None,None]
        
        #hp, mp,?
        self.items = [0,0,0]
        #healing, fireball
        self.spells = ['heal']

    def getXY(self):
        return (self.X,self.Y)
    
    def setXY(self,x,y):
        self.X = x
        self.Y = y
        
    def getRect(self):
        return self.rect
    
    def setRect(self,x1,y1,x2,y2):
        self.rect = (x1,y1,x2,y2)
    
    def changeDirection(self, imgNum, dir):
        self.image = self.images[imgNum]
        self.dir = dir
    
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
    
    def gainLevel(self):
        self.level += 1
        self.nextExp = int( math.ceil( self.nextExp * 2.5 ) )
        self.maxHP = int( math.ceil( self.maxHP * 1.15 ) )
        self.currHP = self.maxHP
    
    def increaseExp(self, exp):
        self.currExp += exp
        if self.currExp >= self.nextExp:
            self.gainLevel()
            return True
    
    def getItems(self):
        return self.items


    #There is duplicate code here. at some point it would be wise to implement
    #a project-wide messaging/menu utility.    

    
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
    
