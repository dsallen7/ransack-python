import pygame
import os
import random
import pickle

from classes import hero
from classes import map
from classes import hud
from classes import sword
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

class item():
    def __init__(self):
        self.type = None
        

    


class game():
    def __init__(self):
        self.badguys = []
        self.myHero = hero.hero()
        self.myHud = hud.hud(screen)
        self.mySword = sword.sword()
        self.myMap = None
        
        #this is true while player is in a particular game
        self.gameOn = True
        
        #this is true while player is in a particular level
        self.levelOn = True        
        
        self.gameBoard = pygame.Surface( [400,400] )
        
        self.gameScreen, self.gameScreenRect = load_image('gamescreen600.bmp', -1)
    
    def gameover(self):
        self.gameOn = False
        
    def nextLevel(self):
        self.levelOn = False
    
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
                '''
                (x,y,a,b) = self.rect
                self.newGame.mySword.attack(x,y,self.dir)
                '''
            elif event.key == pygame.K_s:
                self.openSpellMenu()
            elif event.key == pygame.K_i:
                self.invMenu()
            else:
                self.move(pygame.key.name(event.key))
    
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
        if i == 3:
            if self.myHud.playerkeys == 0:
                self.myHud.message( "The door is locked!" )
                return
            else:
                self.myHud.takeKey()
                self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize,0)
        #item
        if i == 2 or i == 5 or i == 6:
            self.myHud.getItem(i)
            self.myMap.getItem( (X + moveX)/blocksize, (Y + moveY)/blocksize)
        #exit
        if i == 4:
            self.myHud.message( "Onto the next level!" )
            self.nextLevel()
        #open space
        if ( (0 < X+moveX <= 540) and (0 < Y+moveY <= 540 ) and i not in noGoList ):
            X += moveX
            Y += moveY
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
            self.myHero.setXY(X,Y)
            self.myHero.setRect( rectX, rectY, x2, y2)
    
    def openSpellMenu(self):
        for i in range(88):
            borderBox = pygame.Surface( ( ((i*2)+5 ), 60) )
            borderBox.fill( grey )
            msgBox = pygame.Surface( (i*2, 50 ) )
            msgBox.fill( yellow )
            borderBox.blit(msgBox, (5, 5) )
            screen.blit(borderBox, (188-i, 200) )
            pygame.display.flip()
            
        borderBox = pygame.Surface( ( 186, 60 ) )
        borderBox.fill( grey )
        if pygame.font:
            font = pygame.font.SysFont("arial", 24)
            msgText = font.render( "Spell menu:", 1, red, yellow )
            msgBox.blit(msgText, (10,10) )
        borderBox.blit( msgBox, (5, 5) )
        screen.blit(borderBox, (100, 200) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
        
    def invMenu(self):
        for i in range(88):
            borderBox = pygame.Surface( ( ((i*2)+5 ), 120) )
            borderBox.fill( grey )
            msgBox = pygame.Surface( (i*2, 110 ) )
            msgBox.fill( yellow )
            borderBox.blit(msgBox, (5, 5) )
            screen.blit(borderBox, (188-i, 100) )
            pygame.display.flip()
            
        borderBox = pygame.Surface( ( 186, 120 ) )
        borderBox.fill( grey )
                
        if pygame.font:
            font = pygame.font.SysFont("arial", 24)
            msgText = font.render( "Inventory:", 1, red, yellow )
            msgBox.blit(msgText, (10,10) )
        
        #draw available items in window
        items = self.myHud.getItemsList()
        w = 10 #var to draw items across screen
        #hPosList = []
        for item in items:
            if item == 'hp':
                itemBox = pygame.Surface( (23, 29) )
                itemBox.fill( black )
                itemBox.blit( self.newGame.myMap.images[5], (5, 5) )
                
            msgBox.blit( itemBox, (w, 30) )
            w += 10
            #hPosList += [w]
        hPos = 10 #horizontal position of selection box
        hPosList = [10, 30, 50]
        boxPoints = ( (hPos, 30), (hPos, 59), (hPos+23, 59), (hPos+23, 30) )
        pygame.draw.lines( msgBox, white, True, boxPoints, 1 )
        
        borderBox.blit( msgBox, (5, 5) )
        screen.blit(borderBox, (100, 100) )        
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        pygame.draw.lines( msgBox, yellow, True, boxPoints, 1 )
                        hPosList = hPosList[1:]+[hPosList[0]]
                        hPos = hPosList[0]
                        boxPoints = ( (hPos, 30), (hPos, 59), (hPos+23, 59), (hPos+23, 30) )
                        pygame.draw.lines( msgBox, white, True, boxPoints, 1 )
                    if event.key == pygame.K_LEFT:
                        pygame.draw.lines( msgBox, yellow, True, boxPoints, 1 )
                        hPosList = [hPosList[2]]+hPosList[:2]
                        hPos = hPosList[0]
                        boxPoints = ( (hPos, 30), (hPos, 59), (hPos+23, 59), (hPos+23, 30) )
                        pygame.draw.lines( msgBox, white, True, boxPoints, 1 )
                    if event.key == pygame.K_ESCAPE:
                        return
            borderBox.blit( msgBox, (5, 5) )
            screen.blit(borderBox, (100, 100) ) 
            pygame.display.flip()
        #while (pygame.event.wait().type != pygame.KEYDOWN): pass

    def mainLoop(self, mapList):
        #while self.gameOn == True:
        for mapFileName in mapList:
            self.levelOn = True
            self.myMap = map.map(self.badguys, mapFileName)
            while self.levelOn == True:
                self.gameBoard.fill(black)
                allsprites = pygame.sprite.RenderPlain((self.myHero, self.badguys))
                clock.tick(15)
                for event in pygame.event.get():
                    self.event_handler(event)
                    if event.type == pygame.QUIT:
                        os.sys.exit()
                if self.mySword.swordTimer > 0:
                    self.mySword.drawSword()
                allsprites.update()
                allsprites.draw(self.gameBoard)
                self.myMap.redraw(self.myHero.getXY(), self.gameBoard)
                self.myHud.update(self.gameBoard)
                for b in self.badguys:
                    b.move()
                screen.blit( self.gameScreen, (0,0) )
                self.myHero.showLocation(self.gameBoard)
                screen.blit( self.gameBoard, (75,75) )
                pygame.display.flip()

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
    
    clearScreen = pygame.Surface([500,500])
    
    clearScreen.fill(black)
    
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
                    screen.blit(clearScreen, (0,0))
                    newGame.mainLoop(mapList)
        pygame.display.flip()
    
main()