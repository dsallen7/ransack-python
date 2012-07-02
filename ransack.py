import pygame
import os
import random
import pickle

import numpy as np
from numpy.random import random_integers as rnd
import matplotlib.pyplot as plt

def load_image(name, colorkey=None):
    fullname = os.path.join('IMG', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

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

class sword(pygame.sprite.Sprite):
    
    def __init__(self, nGame):
        self.images = range(4)
        self.images[0], self.rect = load_image('sword_d.bmp', -1)
        
        self.image = self.images[0]
        
        self.swordTimer = 0
        self.swordLoc = (0,0)
        self.swordDir = 'd'
        
        self.newGame = nGame
        
    
    def drawSword(self):
        self.swordTimer -= 1
        x,y = self.swordLoc
        if self.swordDir == 'd':
            self.newGame.gameBoard.blit(self.images[0], (x,y) )
        elif self.swordDir == 'u':
            self.newGame.gameBoard.blit(self.images[0], (x,y) )
        elif self.swordDir == 'l':
            self.newGame.gameBoard.blit(self.images[0], (x,y) )
        elif self.swordDir == 'r':
            self.newGame.gameBoard.blit(self.images[0], (x,y) )

    def attack(self, x, y, direction):
        swordX = 0
        swordY = 0
        if direction == 'd':
            swordY = blocksize
        if direction == 'u':
            swordY = -blocksize
        if direction == 'l':
            swordX = -blocksize
        if direction == 'r':
            swordX = blocksize
        
        self.swordLoc = (x + swordX, y + swordY)
        self.swordTimer = 5
        self.swordDir = direction
        for b in self.newGame.badguys:
            (x2,y2) = b.location
            if (x + swordX) == x2 and (y + swordY) == y2:
                b.die()
                self.newGame.badguys.remove(b)


class hero(pygame.sprite.Sprite):
    
    def __init__(self, nGame):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.images = range(6)
        self.images[0], self.rect = load_image('link_u.bmp', -1)
        self.images[1], self.rect = load_image('link_d.bmp', -1)
        self.images[2], self.rect = load_image('link_l.bmp', -1)
        self.images[3], self.rect = load_image('link_r.bmp', -1)

        self.image = self.images[1]
        self.rect = (blocksize, blocksize, blocksize, blocksize)
        #Height: 23
        #Width: 17
        
        self.dir = 'd'
        
        self.strength = random.randrange(5,10)
        self.intell = random.randrange(5,10)
        self.dex = random.randrange(5,10)
        
        self.X = blocksize
        self.Y = blocksize
        
        self.newGame = nGame

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                (x,y,a,b) = self.rect
                self.newGame.mySword.attack(x,y,self.dir)
            elif event.key == pygame.K_s:
                self.openSpellMenu()
            elif event.key == pygame.K_i:
                self.invMenu()
            else:
                self.move(pygame.key.name(event.key))

    def checkMap(self, x, y):
        i = self.newGame.myMap.getUnit(x/blocksize,y/blocksize)
        return i
    
    def getXY(self):
        return (self.X,self.Y)
    
    def setXY(self,x,y):
        self.X = x*blocksize
        self.Y = y*blocksize

    def move(self, direction):
        noGoList = [1,8]
        x1,y1,x2,y2 = self.rect
        moveX = 0
        moveY = 0
        if direction == 'up':
            self.image = self.images[0]
            self.dir = 'u'
            moveY = -blocksize
        elif direction == 'down':
            self.image = self.images[1]
            self.dir = 'd'
            moveY = blocksize
        elif direction == 'left':
            self.image = self.images[2]
            self.dir = 'l'
            moveX = -blocksize
        elif direction == 'right':
            self.image = self.images[3]
            self.dir = 'r'
            moveX = blocksize
        
        i = self.checkMap( (self.X + moveX), (self.Y + moveY))
        #door
        if i == 3:
            if self.newGame.myHud.playerkeys == 0:
                self.newGame.myHud.message( "The door is locked!" )
                return
            else:
                self.newGame.myHud.takeKey()
                self.newGame.myMap.updateUnit( (self.X + moveX)/blocksize, (self.Y + moveY)/blocksize,0)
        #item
        if i == 2 or i == 5 or i == 6:
            self.newGame.myMap.getItem( (self.X + moveX)/blocksize, (self.Y + moveY)/blocksize)
        #exit
        if i == 4:
            self.newGame.myHud.message( "Onto the next level!" )
            self.newGame.nextLevel()
        #open space
        if ( (0 < self.X <= 540) and (0 < self.Y <= 540 ) and i not in noGoList ):
            self.X = self.X + moveX
            self.Y = self.Y + moveY
            rectX = self.X
            rectY = self.Y
            if 5*blocksize <= self.X <= 15*blocksize:
                rectX = 5 * blocksize
            if self.X > 15*blocksize:
                rectX = self.X - HALFDIM*blocksize
            if 5*blocksize <= self.Y <= 15*blocksize:
                rectY = 5 * blocksize
            if self.Y > 15*blocksize:
                rectY = self.Y - HALFDIM*blocksize
            self.rect = ( rectX, rectY, x2, y2)
    #There is duplicate code here. at some point it would be wise to implement
    #a project-wide messaging/menu utility.    

    
    def showLocation(self):
        (x1,y1,x2,y2) = self.rect
        locBox = pygame.Surface( (350,50) )
        locBox.fill( grey )
        if pygame.font:
            font = pygame.font.SysFont("arial", 24)
            locText = font.render( "Self.X:"+str(self.X)+"Self.Y:"+str(self.Y)+"RectX:"+str(x1)+"RectY"+str(y1), 1, red, yellow )
            locBox.blit(locText, (10,10) )
        self.newGame.gameBoard.blit(locBox, (100, 500) )
        pygame.display.flip()
    
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
        items = self.newGame.myHud.getItemsList()
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

class hud():
    def __init__(self, nGame):
        self.box = pygame.Surface((80, 250))
        self.box.fill( yellow )
        self.playerscore = 0
        self.playerlife = 50
        self.playerkeys = 0
        
        self.invItems = []
        
        self.newGame = nGame

    def update(self):
        self.box = self.box.copy()
        if pygame.font:
            font = pygame.font.SysFont("arial", 24)
            scoretext = font.render( "Score: "+str(self.playerscore), 1, red, yellow )
            self.box.blit(scoretext, (0,0) )
            lifetext = font.render( "Life: ", 1, red, yellow)
            self.box.blit(lifetext, (0,25) )
            keytext = font.render( "Keys: "+str(self.playerkeys), 1, red, yellow)
            self.box.blit(keytext, (0,80) )
        backbar = pygame.Surface((100,10))
        lifebar = pygame.Surface((self.playerlife,10))
        backbar.fill( yellow )
        lifebar.fill(red)
        self.box.blit(backbar, (0,55) )
        self.box.blit(lifebar, (0,55) )
        self.newGame.gameBoard.blit(self.box, (blocksize*10, 0) )

    def hurt(self):
        if self.playerlife > 10:
            self.playerlife -= 10
        else:
            self.newGame.gameover()
            
    def takeKey(self):
        self.playerkeys -= 1
        self.message("The door unlocks")

    def getItem(self,type):
        if type == 5:
            if self.playerlife < 90:
                self.playerlife += 10
            else:
                self.playerlife = 100
            self.playerscore += 10
        if type == 2:
            self.playerkeys += 1
            self.message("You got a key")
        if type == 6:
            self.invItems += ['hp']
            self.message("You found a healing potion")
    
    def getItemsList(self):
        return self.invItems
    
    def message(self, text):
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
            msgText = font.render( text, 1, red, yellow )
            msgBox.blit(msgText, (10,10) )
        borderBox.blit( msgBox, (5, 5) )
        screen.blit(borderBox, (100, 200) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass

class map():
    def __init__(self, badguys, filename, nGame):
        self.maptext = []
        self.loadMap()
        self.images = range(10)
        imageNames = ['floor.bmp','brick2.bmp','key.bmp','door.bmp','exit.bmp','fruit_s.bmp','hpotion.bmp','spellbook.bmp','chest.bmp']
        self.images[0], self.rect = load_image(imageNames[0], -1)
        for i in range(1,9):
            self.images[i], self.rect = load_image(imageNames[i], None)
        
        self.newGame = nGame
        
        self.image = self.images[0]
        
        for i in range(DIM):
            for j in range(DIM):
                if self.getUnit(i,j) == 9:
                    self.newGame.myHero.setXY(i,j)
        
        self.topMapCorner = (0,0)
    
    def saveMap(self):
        grid = self.getGrid()
        save = open("map.dat", "w")
        pickle.dump(grid, save)
        save.close()
    
    def loadMap(self):
        save = open("map.dat", "r")
        grid = pickle.load(save)
        save.close()
        self.maptext = grid
    
    def getGrid(self):
        return self.maptext
    
    #working:
    # 0 : open space
    # 1 : wall
    # 2 : key
    # 3 : door
    # 4 : exit
    # 5 : fruit
    # 6 : h potion
    # 7 : spellbook
    # 8 : chest
    def redraw(self):
        # Compute top map corner
        (px,py) = self.newGame.myHero.getXY()
        px = px/blocksize
        py = py/blocksize
        
        self.topMapCorner = ( (px%10 + (px/10)*10), (py%10 + (py/10)*10) )
        
        if px < 5:
            topX = 0
        elif 5 <= px <= 15:
            topX = px - 5
        else:
            topX = 10
        
        if py < 5:
            topY = 0
        elif 5 <= py <= 15:
            topY = py - 5
        else:
            topY = 10
        #Redraw map on screen from current map matrix
        #topX, topY = self.topMapCorner
        for x in range(HALFDIM):
            for y in range(HALFDIM):
                d = self.getUnit(x+topX,y+topY)
                if d < 9:
                    self.image = self.images[d]
                    self.newGame.gameBoard.blit(self.image, (x*blocksize,y*blocksize), area=(0,0,blocksize,blocksize) )

    def getItem(self, x, y):
        #updates map with collected item and calls HUD
        self.newGame.myHud.getItem(self.getUnit(x,y))
        self.maptext[y] = self.maptext[y][:x]+[0]+self.maptext[y][x+1:]
        
    def updateUnit(self, x, y, type):
        #Updates one map unit to type at map coordinates x,y
        self.maptext[y] = self.maptext[y][:x]+[type]+self.maptext[y][x+1:]
    
    def getUnit(self,x,y):
        return self.maptext[y][x]

class item():
    def __init__(self):
        self.type = None
        
class badguy(pygame.sprite.Sprite):
    def __init__(self,x,y, nGame):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('goomba.bmp', -1)
        self.location = (x,y)
        self.rect = (x,y,blocksize,blocksize)
        
        self.newGame = nGame
        
    def checkMap(self, x, y):
        (a,b,c,d) = self.newGame.myHero.rect
        if x == a and y == b:
            return 'p'
        if self.newGame.myMap.maptext[x/blocksize][y/blocksize] == 0:
            return False

    def hurtPlayer(self):
        self.newGame.myHud.hurt()
        
    def die(self):
        x,y = self.location
        self.newGame.myMap.updateUnit(x/blocksize,y/blocksize,'o')
        
    def move(self):
        n = random.randrange(1,5)
        if n != 2:
            #to slow badguys down
            return
        x,y = self.location
        m = random.randrange(1,5)
        moveX = 0
        moveY = 0
        if m == 1: # up
            moveY = -blocksize
        elif m == 2: # down
            moveY = blocksize
        elif m == 3: # left
            moveX = -blocksize
        elif m == 4: # right
            moveX = blocksize
        
        if self.checkMap( (x + moveX), (y + moveY) ) == 'p':
            self.hurtPlayer()
        elif (0 < y < 500) and (0 < x < 500) and (self.checkMap( (x + moveX), (y + moveY) ) == False):
            self.newGame.myMap.updateUnit(x/blocksize,y/blocksize,'o')
            self.location = ( (x + moveX), (y + moveY) )
            self.newGame.myMap.updateUnit( (x + moveX)/blocksize,(y + moveY)/blocksize,'b')
        
        x,y = self.location
        self.rect = (x,y, blocksize, blocksize)
    
    #move in direction of player
    def seek(self):
        pass

class game():
    def __init__(self):
        self.badguys = []
        self.myHero = hero(self)
        self.myHud = hud(self)
        self.mySword = sword(self)
        self.myMap = None
        
        #this is true while player is in a particular game
        self.gameOn = True
        
        #this is true while player is in a particular level
        self.levelOn = True        
        
        self.gameBoard = pygame.Surface( [400,300] )
        
        self.gameScreen, self.gameScreenRect = load_image('gamescreen600.bmp', -1)
    
    def gameover(self):
        self.gameOn = False
        
    def nextLevel(self):
        self.levelOn = False

    def mainLoop(self, mapList):
        #while self.gameOn == True:
        for mapFileName in mapList:
            self.levelOn = True
            self.myMap = map(self.badguys, mapFileName, self)
            while self.levelOn == True:
                self.gameBoard.fill(black)
                allsprites = pygame.sprite.RenderPlain((self.myHero, self.badguys))
                clock.tick(15)
                for event in pygame.event.get():
                    self.myHero.event_handler(event)
                    if event.type == pygame.QUIT:
                        os.sys.exit()
                if self.mySword.swordTimer > 0:
                    self.mySword.drawSword()
                allsprites.update()
                allsprites.draw(self.gameBoard)
                self.myMap.redraw()
                self.myHud.update()
                for b in self.badguys:
                    b.move()
                screen.blit( self.gameScreen, (0,0) )
                screen.blit( self.gameBoard, (75,75) )
                pygame.display.flip()

# Set the height and width of the screen
size=[600,600]
screen=pygame.display.set_mode(size)

#Height and width of a "block" unit
blocksize = 30

if not pygame.font: print 'Warning, fonts disabled'

pygame.display.set_caption("Ransack")

background = pygame.Surface([250,250])
background = background.convert()
background.fill((0,0,0))

pygame.init()
clock = pygame.time.Clock()
random.seed()

DIM = 20

HALFDIM = 10

# Define the colors we will use in RGB format
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]
yellow = [127, 127, 0]
grey = [32, 32, 32]

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