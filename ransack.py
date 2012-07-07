import pygame
import os
import random
import pickle

from classes import hero, map, hud, battle, menu, enemy
from const import *
from load_image import *

import numpy as np
from numpy.random import random_integers as rnd
import matplotlib.pyplot as plt

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=500,height=500):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))

class game():
    def __init__(self):
        self.badguys = []
        self.myHero = hero.hero()
        self.myHud = hud.hud(screen)
        self.myMenu = menu.menu()
        self.myBattle = battle.battle()
        self.myMap = None
        
        self.allsprites = pygame.sprite.RenderPlain((self.myHero, self.badguys))
        
        #this is true while player is in a particular game
        self.gameOn = True
        
        #this is true while player is in a particular level
        self.levelOn = True        
        
        self.gameBoard = pygame.Surface( [450,450] )
        self.gameScreen, self.gameScreenRect = load_image('gamescreen600.bmp', -1)
        self.spriteLayer = pygame.Surface( [450,450] )
        
        self.spellImages = range(2)
        spellNames = ['heart.bmp','fireball.bmp']
        for i in range(2):
            self.spellImages[i],r = load_image(spellNames[i],-1)
    
    def gameOver(self):
        self.gameOn = False
        
    def nextLevel(self):
        self.levelOn = False
        
    def screenShot(self):
        serial = 1
        while os.access("ransack"+str(serial)+".bmp", os.F_OK):
            serial += 1
        pygame.image.save(screen, "ransack"+str(serial)+".bmp")
    
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
                '''
                (x,y,a,b) = self.rect
                self.newGame.mySword.attack(x,y,self.dir)
                '''
            elif event.key == pygame.K_s:
                self.castSpell( self.myMenu.invMenu(screen, self.myHero.getSpells(), self.spellImages, "Spells:" ) )
            elif event.key == pygame.K_i:
                self.useItem( self.myMenu.invMenu(screen, self.myHud.getItemsList(), self.myMap.getImages(), "Items:" ) )
            elif event.key == pygame.K_t:
                self.screenShot()
            else:
                self.move(pygame.key.name(event.key))
    
    def rollDie(self, target, range):
        d = random.randrange(range)
        if target >= d:
            return True
        else:
            return False
    
    def castSpell(self, spell):
        if spell == 'heal':
            if self.myHero.takeMP(5):
                self.myHero.takeDmg(-5)
                self.myHud.msgSystem(self.gameBoard, "You feel better!")
            else:
                self.myHud.msgSystem(self.gameBoard, "Not enough MP!")
    
    def useItem(self,item):
        if item == 'hp':
            self.myHero.takeDmg(-5)
            self.myHud.msgSystem(self.gameBoard, "You feel better!")
        elif item == 'mp':
            self.myHero.takeMP(-5)
            self.myHud.msgSystem(self.gameBoard, "You feel magical!")
    
    def fightBattle(self):
        engagedEnemy = enemy.enemy()
        while engagedEnemy.getHP() > 0:
            clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    #you attack
                    if event.key == pygame.K_f:
                        if self.rollDie(1,2):
                            dmg = random.randrange(1,5)
                            self.myHud.msgSystem(self.gameBoard, "You hit the monster for "+str(dmg)+" points!")
                            engagedEnemy.takeDmg(dmg)
                        else:
                            self.myHud.msgSystem(self.gameBoard, "You missed the monster!")
                    #enemy attacks
                    if self.rollDie(1,2):
                        dmg = random.randrange(1,5)
                        self.myHud.msgSystem(self.gameBoard, "The monster hits you for "+str(dmg)+" points!")
                        if self.myHero.takeDmg(dmg) < 1:
                            self.myHud.msgSystem(self.gameBoard, "You have died!")
                            self.gameOver()
                            return
                    else:
                        self.myHud.msgSystem(self.gameBoard, "The monster missed you!")
                    self.myHud.displayStats(self.gameBoard, self.myHero.getPlayerStats())
                    self.redrawScreen()
                    pygame.display.flip()
        self.myHud.msgSystem(self.gameBoard, "The monster is dead!")
        if self.myHero.increaseExp(5):
            self.myHud.msgSystem(self.gameBoard, "Congratulations! You have gained a level!")
    
    def drawHero(self):
        (X,Y) = self.myHero.getXY()
        rectX = X
        rectY = Y
        if 5*blocksize <= X < 15*blocksize:
            rectX = 5 * blocksize
        if X >= 15*blocksize:
            rectX = X - HALFDIM*blocksize
        if 5*blocksize <= Y < 15*blocksize:
            rectY = 5 * blocksize
        if Y >= 15*blocksize:
            rectY = Y - HALFDIM*blocksize
        '''
        #make the move animated
        if x1 == rectX:
            xAxis = [x1]*blocksize
        elif x1 < rectX:
            xAxis = range(x1, rectX)
        else:
            xAxis = range(x1, rectX, -1)
        if y1 == rectY:
            yAxis = [y1]*blocksize
        elif y1 < rectY:
            yAxis = range(y1, rectY)
        elif y1 > rectY:
            yAxis = range(y1, rectY, -1)
        for (i, j) in zip(xAxis, yAxis):
            self.myHero.setRect( i, j, x2, y2)
            self.updateSprites()
            self.redrawScreen()
        '''
        self.myHero.setRect( rectX, rectY, blocksize, blocksize)
            
    
    def move(self, direction):
        noGoList = [1,8]
        x1,y1,x2,y2 = self.myHero.getRect()
        moveX = 0
        moveY = 0
        (X,Y) = self.myHero.getXY()
        if direction == 'up':
            self.myHero.changeDirection(0,'u')
            moveY = -blocksize
        elif direction == 'down':
            self.myHero.changeDirection(1,'d')
            moveY = blocksize
        elif direction == 'left':
            self.myHero.changeDirection(2,'l')
            moveX = -blocksize
        elif direction == 'right':
            self.myHero.changeDirection(3,'r')
            moveX = blocksize
        
        i = self.myMap.getUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize)
        #door
        if i == DOOR:
            if self.myHero.getPlayerStats()[8] == 0:
                self.myHud.message( "The door is locked!" )
                return
            else:
                self.myHud.message( "The door creaks open..." )
                self.myHero.takeKey()
                self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize,0)
        #item
        if i == KEY or i == FRUIT or i == HPOTION or i == MPOTION:
            self.myHero.setPlayerStats( self.myHud.getItem(i, self.myHero.getPlayerStats() ) )
            self.myMap.getItem( (X + moveX)/blocksize, (Y + moveY)/blocksize)
        #exit
        if i == EXIT:
            self.myHud.message( "Onto the next level!" )
            self.nextLevel()
        #check if open space
        if ( (0 < X+moveX <= blocksize*DIM) and (0 < Y+moveY <= blocksize*DIM ) and i not in noGoList ):
            X += moveX
            Y += moveY
            self.myHero.setXY(X,Y)
            self.drawHero()
            #roll the die to see if there will be a battle
            if self.rollDie(0,50):
                self.myHud.message("The battle is joined!")
                self.myBattle.commence(screen)
                self.fightBattle()
       
    def updateSprites(self):
        #self.allsprites.clear(self.spriteLayer, self.gameBoard)
        self.allsprites.update()
        self.allsprites.draw(self.gameBoard)
    
    def redrawScreen(self):
        screen.blit( self.gameScreen, (0,0) )
        #self.myHero.showLocation(self.gameBoard)
        screen.blit( self.gameBoard, (75,75) )
        #screen.blit( self.spriteLayer, (75,75) )
        pygame.display.flip()
        

    def mainLoop(self, mapList):
        #while self.gameOn == True:
        for mapFileName in mapList:
            self.levelOn = True
            self.myMap = map.map(mapFileName)
            (X,Y) = self.myMap.getStartXY()
            print X,Y
            self.myHero.setXY( X*blocksize,Y*blocksize )
            self.drawHero()
            while self.levelOn and self.gameOn:
                self.gameBoard.fill(black)
                clock.tick(15)
                for event in pygame.event.get():
                    self.event_handler(event)
                    if event.type == pygame.QUIT:
                        os.sys.exit()
                self.myMap.redraw(self.myHero.getXY(), self.myHero.getRect(), self.gameBoard)
                self.myHud.displayStats(self.gameBoard, self.myHero.getPlayerStats())
                self.updateSprites()
                #self.myHero.showLocation(self.gameBoard)
                self.redrawScreen()

# Set the height and width of the screen
size=[600,600]
screen=pygame.display.set_mode(size)

if not pygame.font: print 'Warning, fonts disabled'

pygame.display.set_caption("Ransack")

background = pygame.Surface([250,250])
background = background.convert()
background.fill((0,0,0))

pygame.init()
clock = pygame.time.Clock()
random.seed()


def main():
    mapList = ['map.dat', 'map2.dat']    
    
    titleScreen = pygame.Surface([500,500])
    
    titleScreen.fill(black)
    
    
    titleImg, titleRect = load_image('titlescreen.bmp', -1)
    
    titleScreen.blit(titleImg, (0,0) )
    
    screen.blit(titleScreen, (0,0))
    while True:
        screen.blit(titleScreen, (0,0))
        clock.tick(20)
    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    os.sys.exit()
                if event.key == pygame.K_SPACE:
                    newGame = game()
                    newGame.mainLoop(mapList)
        pygame.display.flip()
    
main()