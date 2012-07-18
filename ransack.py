import pygame
import os
import random
import pickle

from classes import hero, hud, battle, menu, enemy
from IMG import images
from const import *
from load_image import *

from MAP import map, mapgen

class game():
    def __init__(self):
        self.myHero = hero.hero()
        self.myMenu = menu.menu()
        self.myMap = None
        self.levelDepth = 2
        # a dungeon is just an array of maps
        self.myDungeon = []
        for mapFileName in mapList:
            self.myDungeon += [map.map(mapFileName)]
        
        self.myMap = self.myDungeon[self.levelDepth]
        
        self.gameBoard = pygame.Surface( [450,450] )
        self.gameFrame, self.gameFrameRect = load_image('gamescreen600.bmp', -1)
        
        self.allsprites = pygame.sprite.LayeredDirty((self.myHero))
        self.allsprites.clear(screen, self.gameBoard)
        
        #this is true while player is in a particular game
        self.gameOn = True
        
        self.DIM = DIM
        
        # 0 : camera
        # 1 : sword
        # 2 : miss
        self.sounds = range(3)
        self.sounds[0] = pygame.mixer.Sound(os.path.join('SND', 'camera.wav' ))
        self.sounds[1] = pygame.mixer.Sound(os.path.join('SND', 'sword1.wav' ))
        self.sounds[2] = pygame.mixer.Sound(os.path.join('SND', 'miss.wav' ))
        
        self.myHud = hud.hud(screen, self)
        self.myBattle = battle.battle(screen,self.myHud)
    
    #toggles switch to continue running game
    def gameOver(self):
        self.gameOn = False
    
    def generateMap(self, dimension):
        rndMap = mapgen.Map(dimension)
        rndMap.generateMap(20)
        newMap = map.map(None, rndMap.getMapBall())
        return newMap
        
    def nextLevel(self):
        self.levelDepth += 1
        if self.levelDepth == len(self.myDungeon):
            self.myDungeon.append(self.generateMap(40))
            self.myMap = self.myDungeon[self.levelDepth]
        else:
            self.myMap = self.myDungeon[self.levelDepth]
        self.DIM = self.myMap.getDIM()
        (x,y) = self.myMap.getPOE()
        self.myHero.setXY( x*blocksize,y*blocksize )
        if self.levelDepth <= 2:
            self.myMap.setLOV(4)
        else: self.myMap.setLOV(0)
    
    def prevLevel(self):
        self.levelDepth -= 1
        self.myMap = self.myDungeon[self.levelDepth]
        self.DIM = self.myMap.getDIM()
        (x,y) = self.myMap.getPOEx()
        self.myHero.setXY( x*blocksize,y*blocksize )
        if self.levelDepth <= 2:
            self.myMap.setLOV(4)
        else: self.myMap.setLOV(0)
    
    #takes screen shot and saves as bmp in serial fashion, beginning with 1
    def screenShot(self):
        serial = 1
        while os.access("ransack"+str(serial)+".bmp", os.F_OK):
            serial += 1
        pygame.image.save(screen, "ransack"+str(serial)+".bmp")
        flash = pygame.Surface([450,450])
        flash.fill(white)
        screen.blit(flash,(75,75))
        clock.tick(100)
        self.sounds[0].play()
    
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_s:
                if self.myHero.castSpell( self.myMenu.invMenu(screen, self.myHero.getSpells(), "Spells:" ) ) == -1:
                    self.textMessage('That spell may only be cast in battle.')
            elif event.key == pygame.K_i:
                self.myHero.useItem( self.myMenu.invMenu(screen, self.myHero.getItems(), "Items:" ) )
            elif event.key == pygame.K_t:
                self.screenShot()
            elif event.key == pygame.K_m:
                self.myMap.callDrawMiniMap(screen)
            else:
                self.move(pygame.key.name(event.key))
    
    def rollDie(self, target, range):
        d = random.randrange(range)
        if target >= d:
            return True
        else:
            return False

    # takes x,y of old myHero.rect location and finds new
    def drawHero(self,x1,y1, animated=True):
        DIMEN = self.myMap.getDIM()
        (X,Y) = self.myHero.getXY()
        rectX = X
        rectY = Y
        if DIMEN > HALFDIM:
            if 5*blocksize <= X < (DIMEN-5)*blocksize:
                rectX = 5 * blocksize
            if X >= (DIMEN-5)*blocksize:
                rectX = X - (DIMEN/2)*blocksize
            if 5*blocksize <= Y < (DIMEN-5)*blocksize:
                rectY = 5 * blocksize
            if Y >= (DIMEN-5)*blocksize:
                rectY = Y - (DIMEN/2)*blocksize
        else:
            rectX += (HALFDIM - DIMEN)/2*blocksize
            rectY += (HALFDIM - DIMEN)/2*blocksize
        
        #make the move animated
        if animated:
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
                clock.tick(100)
                self.myHero.setRect( i, j, blocksize, blocksize)
                self.myHero.takeStep()
                #self.updateSprites()
                self.redrawGameBoard()
        
        self.myHero.setRect( rectX, rectY, blocksize, blocksize)
    
    # calls message
    def boxMessage(self, msg):
        self.myHud.boxMessage(msg)
    
    # calls msgSystem
    def textMessage(self, msg):
        self.myHud.txtMessage(msg)
    
    def move(self, direction):
        if direction not in ['up','down','left','right']: return
        x1,y1,x2,y2 = self.myHero.getRect()
        moveX = 0
        moveY = 0
        (X,Y) = self.myHero.getXY()
        (moveX,moveY) = self.myHero.changeDirection(direction)
        
        i = self.myMap.getUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize)
        if i == -1 or i in range(24,86):
            return
        #door
        if i == DOOR:
            if self.myHero.getPlayerStats()[8] == 0:
                self.boxMessage( "The door is locked!" )
                return
            else:
                self.boxMessage( "The door creaks open..." )
                self.myHero.takeKey()
                self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize,0)
        #item
        if i in range(86,109): 
            self.myHero.getItem(i)
            self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize, 0)
            self.myHud.msgSystem(self.gameBoard, itemMsgs[i])
        # Stairs down
        if i == STAIRDN:
            self.nextLevel()
            self.drawHero(x1,y1,False)
            return
        # Stairs up
        if i == STAIRUP:
            self.prevLevel()
            self.drawHero(x1,y1,False)
            return
        # Chest
        if i == CHEST:
            chestlist = self.myMap.chests[(X + moveX)/blocksize, (Y + moveY)/blocksize]
            for item in self.myMenu.displayChest( screen, chestlist ):
                self.myHero.getItem(item)
            self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize, OCHEST )
        #check if open space
        if ( (0 < X+moveX <= blocksize*self.DIM) and (0 < Y+moveY <= blocksize*self.DIM ) and i in range(24) ):
            X += moveX
            Y += moveY
            self.myHero.setXY(X,Y)
            self.drawHero(x1,y1)
            #roll the die to see if there will be a battle
            if self.rollDie(0,40) and self.levelDepth > 2:
                self.boxMessage("The battle is joined!")
                self.gameBoard.fill( black )
                if not self.myBattle.fightBattle(self.myHero, enemy.enemy(self.levelDepth)):
                    self.gameOver()
       
    def updateSprites(self):
        self.allsprites.update()
        rects = self.allsprites.draw(self.gameBoard)
        pygame.display.update(rects)
        pygame.display.flip()
    
    def redrawGameBoard(self):
        self.myMap.redraw(self.myHero.getXY(), self.myHero.getRect(), self.gameBoard)
        self.updateSprites()
        screen.blit( self.gameBoard, (75,75) )
        pygame.display.flip()
    
    def switchMap(self):
        pass

    def mainLoop(self, mapList):
        screen.blit(self.gameFrame,(0,0))
        (X,Y) = self.myMap.getStartXY()
        if self.levelDepth < 3:
            self.myMap.setLOV(4)
        self.myHero.setXY( X*blocksize,Y*blocksize )
        self.updateSprites()
        self.drawHero( X*blocksize,Y*blocksize, False )
        while self.gameOn:
            clock.tick(15)
            for event in pygame.event.get():
                self.event_handler(event)
                if event.type == pygame.QUIT:
                    os.sys.exit()
            self.gameBoard.fill(black)
            self.myHud.update()
            self.redrawGameBoard()

# Set the height and width of the screen
screenSize=[600,600]
screen=pygame.display.set_mode(screenSize)

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

if not pygame.font: print 'Warning, fonts disabled'

pygame.display.set_caption("Ransack")

background = pygame.Surface([250,250])
background = background.convert()
background.fill((0,0,0))

pygame.init()
clock = pygame.time.Clock()
random.seed()

images.load()

def main():    
    titleScreen = pygame.Surface(screenSize)
    
    titleScreen.fill(black)
    
    titleImg, titleRect = load_image('titlescreen.bmp', -1)
    
    titleScreen.blit(titleImg, (50,50) )
    
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