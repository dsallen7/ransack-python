import pygame
import os
import random
import pickle

from classes import hero, hud, battle, menu, enemy, store
from IMG import images
from const import *
from load_image import *

from MAP import map, mapgen

class game():
    def __init__(self, screen, clock):
        self.myHero = hero.hero()
        self.myMenu = menu.menu()
        self.myMap = None
        self.levelDepth = 2
        
        # a dungeon is just an array of maps
        self.myDungeon = []
        for mapFileName in mapList:
            self.myDungeon += [map.map(mapFileName)]
        
        self.myMap = self.myDungeon[self.levelDepth]
        
        self.screen = screen
        self.gameBoard = pygame.Surface( [300,300] )
        self.gameFrame, self.gameFrameRect = load_image('gamescreen600.bmp', -1)
        
        self.allsprites = pygame.sprite.RenderPlain((self.myHero))
        self.allsprites.clear(self.screen, self.gameBoard)
        
        #this is true while player is in a particular game
        self.gameOn = True
        self.DIM = DIM

        images.load()
        
        # 0 : camera
        # 1 : sword
        # 2 : miss
        self.sounds = range(3)
        self.sounds[0] = pygame.mixer.Sound(os.path.join('SND', 'camera.wav' ))
        self.sounds[1] = pygame.mixer.Sound(os.path.join('SND', 'sword1.wav' ))
        self.sounds[2] = pygame.mixer.Sound(os.path.join('SND', 'miss.wav' ))
        
        self.myHud = hud.hud(self.screen, self)
        self.myBlacksmith = store.Store(screen, self.myHud)
        self.myBattle = battle.battle(self.screen,self.myHud)
        self.clock = clock
    
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
        pygame.image.save(self.screen, "ransack"+str(serial)+".bmp")
        flash = pygame.Surface([450,450])
        flash.fill(white)
        self.screen.blit(flash,(75,75))
        self.clock.tick(100)
        self.sounds[0].play()
    
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_s:
                if self.myHero.castSpell( self.myMenu.invMenu(self.screen, self.myHero.getSpells(), "Spells:" ) ) == -1:
                    self.textMessage('That spell may only be cast in battle.')
            elif event.key == pygame.K_i:
                self.myHero.useItem( self.myMenu.invMenu(self.screen, self.myHero.getItems(), "Items:" ) )
            elif event.key == pygame.K_t:
                self.screenShot()
            elif event.key == pygame.K_m:
                self.myMap.callDrawMiniMap(self.screen)
            else:
                self.move(pygame.key.name(event.key))
    
    def rollDie(self, target, range):
        d = random.randrange(range)
        if target >= d:
            return True
        else:
            return False
    
    # called immediately after player makes a move or arrives in a new level
    # takes x,y of old myHero.rect location and finds new
    def drawHero(self,oldX,oldY, dir=None, animated=True):
        DIMEN = self.myMap.getDIM()
        (newX,newY) = self.myHero.getXY()
        scrolling = False
        if DIMEN > HALFDIM:
            if 5*blocksize < newX <= (DIMEN-5)*blocksize:
                newX = 5 * blocksize
                if dir in ['left','right']:
                    scrolling = True
            if newX > (DIMEN-5)*blocksize:
                newX = newX - (DIMEN/2)*blocksize
            if 5*blocksize < newY <= (DIMEN-5)*blocksize:
                newY = 5 * blocksize
                if dir in ['up','down']:
                    scrolling = True
            if newY > (DIMEN-5)*blocksize:
                newY = newY - (DIMEN/2)*blocksize
        else:
            newX += (HALFDIM - DIMEN)/2*blocksize
            newY += (HALFDIM - DIMEN)/2*blocksize
        
        #make the move animated
        if animated:
            if dir == None:
                scrolling = False
            else: scrollX , scrollY = scrollingDict[dir]
            (px,py) = self.myHero.getXY()
            pos, oldPos = self.myMap.updateWindowCoordinates( self.myHero.getXY(), self.myHero.getRect() )
            (topX, topY) = pos
            if oldX == newX:
                xAxis = [oldX]*blocksize
            elif oldX < newX:
                xAxis = range(oldX, newX)
            else:
                xAxis = range(oldX, newX, -1)
            if oldY == newY:
                yAxis = [oldY]*blocksize
            elif oldY < newY:
                yAxis = range(oldY, newY)
            elif oldY > newY:
                yAxis = range(oldY, newY, -1)
            for (idx, (i, j)) in list( enumerate(zip(xAxis, yAxis), start=1) ):
                self.clock.tick(100)
                self.myHero.setRect( i, j, blocksize, blocksize)
                if scrolling:
                    self.gameBoard.blit( self.myMap.getScrollingMapWindow( ( (topX*blocksize)+(idx*scrollX)-(blocksize*scrollX), (topY*blocksize)+(idx*scrollY)-(blocksize*scrollY) ) ), (0,0) )
                    self.myMap.drawDarkness( newX/blocksize, newY/blocksize, self.gameBoard )
                else: self.myMap.redraw(self.myHero.getXY(), self.myHero.getRect(), self.gameBoard)
                self.myHero.takeStep()
                self.displayGameBoard()
        
        self.myHero.setRect( newX, newY, blocksize, blocksize)
    
    # calls hud.boxMessage
    def boxMessage(self, msg):
        self.myHud.boxMessage(msg)
    
    # calls hud.txtMessage
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
        # detect blocking tiles first, otherwise they will be ignored
        #stores
        if i == BLKSMDOOR:
            self.myBlacksmith.enterStore()
            return
        if i == -1 or i in range(24,86):
            return
        # dungeon door
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
            self.myHud.boxMessage(itemMsgs[i])
        # Stairs down
        if i == STAIRDN:
            self.nextLevel()
            self.drawHero(x1,y1,animated=False)
            return
        # Stairs up
        if i == STAIRUP:
            self.prevLevel()
            self.drawHero(x1,y1,animated=False)
            return
        # Chest
        if i == CHEST:
            chestlist = self.myMap.chests[(X + moveX)/blocksize, (Y + moveY)/blocksize]
            for item in self.myMenu.displayChest( self.screen, chestlist ):
                self.myHero.getItem(item)
            self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize, OCHEST )
        #check if open space
        if ( (0 < X+moveX <= blocksize*self.DIM) and (0 < Y+moveY <= blocksize*self.DIM ) and i in range(24) ):
            self.myHero.moving = True
            X += moveX
            Y += moveY
            self.myHero.setXY(X,Y)
            self.drawHero(x1,y1, direction)
            self.myHero.moving = False
            #roll the die to see if there will be a battle
            if self.rollDie(0,30) and self.levelDepth > 2:
                self.boxMessage("The battle is joined!")
                self.gameBoard.fill( black )
                g = self.myBattle.fightBattle(self.myHero, enemy.enemy(self.levelDepth))
                if not g:
                    self.gameOver()
                else: 
                    self.textMessage('You find '+str(g)+' gold pieces!')
                    self.myHero.addGold(g)
        self.myMap.redrawXMap()
       
    def updateSprites(self):
        self.allsprites.update()
        rects = self.allsprites.draw(self.gameBoard)
        pygame.display.update(rects)
    
    def displayGameBoard(self):
        self.updateSprites()
        self.screen.blit( self.gameBoard, (75,75) )
        pygame.display.flip()
    
    def switchMap(self):
        pass

    def mainLoop(self, mapList):
        self.screen.blit(self.gameFrame,(0,0))
        (X,Y) = self.myMap.getStartXY()
        if self.levelDepth < 3:
            self.myMap.setLOV(4)
        self.myHero.setXY( X*blocksize,Y*blocksize )
        self.updateSprites()
        self.drawHero( X*blocksize,Y*blocksize, animated=False )
        while self.gameOn:
            self.clock.tick(30)
            for event in pygame.event.get():
                self.event_handler(event)
                if event.type == pygame.QUIT:
                    os.sys.exit()
            self.gameBoard.fill(black)
            self.myMap.redraw(self.myHero.getXY(), self.myHero.getRect(), self.gameBoard)
            self.myHud.update()
            self.displayGameBoard()