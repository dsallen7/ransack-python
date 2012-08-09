import pygame
import os
import random
import pickle

from classes import hero, hud, battle, menu, enemy, shop, tavern
from IMG import images
from DISPLAY import display
from const import *
from load_image import *

from MAP import map, mapgen
from UTIL import ticker

class game():
    
    def __init__(self, screen, clock, loadTicker=None, loadHero=None, loadDungeon=None, currentMap=2, levelDepth=0):
        self.Display = display.Display(screen)
        if loadTicker == None:
            self.Ticker = ticker.Ticker()
        else: self.Ticker = loadTicker
        if loadHero == None:
            self.myHero = hero.hero()
        else: self.myHero = hero.hero(load=loadHero)
        self.myMenu = menu.menu(screen)
        self.levelDepth = levelDepth
        self.currentMap = currentMap
        
        # a dungeon is just an array of maps
        self.myMap = None
        if loadDungeon == None:
            self.myDungeon = []
            for mapFileName in mapList:
                self.myDungeon += [map.map(mapFileName, type='village')]
        else: self.myDungeon = loadDungeon
        
        self.fortressMaps = []
        for mapFileName in fMapList:
            self.fortressMaps += [map.map(mapFileName, type='dungeon')]
        
        self.myMap = self.myDungeon[self.currentMap]
        
        self.screen = screen
        self.gameBoard = pygame.Surface( [300,300] )
        
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
        self.myBlacksmith = shop.Shop(screen, self.myHud, 1, 'blacksmith', self.Ticker)
        self.myArmory = shop.Shop(screen, self.myHud, 1, 'armory', self.Ticker)
        self.myItemShop = shop.Shop(screen, self.myHud, 1, 'itemshop', self.Ticker)
        self.myMagicShop = shop.Shop(screen, self.myHud, 1, 'magicshop', self.Ticker)
        self.myTavern = tavern.Tavern(screen, self.myHud, self.Ticker)
        self.myBattle = battle.battle(self.screen,self.myHud, self.Ticker)
        self.clock = clock
    
    #toggles switch to continue running game
    def gameOver(self):
        self.gameOn = False
    
    def generateMap(self, dimension):
        rndMap = mapgen.Map(dimension)
        rndMap.generateMap(20)
        newMap = map.map(None, rndMap.getMapBall(), level=self.levelDepth)
        return newMap
        
    def nextLevel(self):
        self.currentMap += 1
        if self.currentMap == len(self.myDungeon):
            self.levelDepth += 1
            if self.levelDepth == 5:
                self.myDungeon = self.myDungeon + self.fortressMaps
            else: self.myDungeon.append(self.generateMap(40))
            self.myMap = self.myDungeon[self.currentMap]
            self.Display.redrawXMap(self.myMap)
        else:
            self.myMap = self.myDungeon[self.currentMap]
            self.Display.redrawXMap(self.myMap)
            if self.myMap.getType() == 'dungeon':
                self.levelDepth += 1
        self.DIM = self.myMap.getDIM()
        (x,y) = self.myMap.getPOE()
        self.myHero.setXY( x*blocksize,y*blocksize )
        if self.myMap.getType() == 'dungeon':
            self.myMap.setLOV(0)
        else: self.myMap.setLOV(4)
    
    def prevLevel(self):
        self.currentMap -= 1
        self.myMap = self.myDungeon[self.currentMap]
        self.Display.redrawXMap(self.myMap)
        self.DIM = self.myMap.getDIM()
        (x,y) = self.myMap.getPOEx()
        self.myHero.setXY( x*blocksize,y*blocksize )
        if self.myMap.getType() == 'dungeon':
            self.myMap.setLOV(0)
        else: self.myMap.setLOV(4)
    
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
                if self.myHero.castSpell( self.myMenu.invMenu(self.myHero.getSpells(), "Spells:" ), self.myHud ) == -1:
                    self.textMessage('ThaT spell may only be casT in baTTle.')
            elif event.key == pygame.K_i:
                self.Ticker.tick( self.myHero.useItem( self.myMenu.invMenu(self.myHero.getItems(), "ITems:" ) ) )
            elif event.key == pygame.K_w:
                self.myHero.equipWeapon(self.myMenu.invMenu(self.myHero.getWeapons(), "Weapons:" ))
            elif event.key == pygame.K_a:
                self.myHero.equipArmor(self.myMenu.invMenu(self.myHero.getArmor(), "Armor:" ))
            elif event.key == pygame.K_t:
                self.screenShot()
            elif event.key == pygame.K_m:
                self.myMap.callDrawMiniMap(self.screen)
            elif event.key == pygame.K_SPACE:
                pass
                #action command
            else:
                if self.move(pygame.key.name(event.key)):
                    return 
    
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
            self.myBlacksmith.enterStore(self.myHero)
            return
        if i == ARMRYDOOR:
            self.myArmory.enterStore(self.myHero)
            return
        if i == 43:
            self.myItemShop.enterStore(self.myHero)
            return
        if i == 57:
            self.myMagicShop.enterStore(self.myHero)
        if i == 60:
            return self.myTavern.enterStore(self.myHero, self)
        if i == 38:
            self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize,19)
            self.Display.redrawXMap(self.myMap)
        if i == 81:
            self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize,18)
            self.Display.redrawXMap(self.myMap)
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
            self.myHero.getItem((i,1))
            self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize, 0)
            self.myHud.boxMessage(itemMsgs[i])
        # Stairs down
        if i == STAIRDN:
            self.nextLevel()
            self.Display.drawHero(x1,y1,self.myHero,self.myMap,self.gameBoard,animated=False)
            return
        # Stairs up
        if i == STAIRUP:
            self.prevLevel()
            self.Display.drawHero(x1,y1,self.myHero,self.myMap,self.gameBoard,animated=False)
            return
        # Chest
        if i == CHEST:
            chestlist = self.myMap.chests[(X + moveX)/blocksize, (Y + moveY)/blocksize]
            for item in self.myMenu.displayChest( chestlist ):
                self.myHero.getItem(item)
            self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize, OCHEST )
            self.Ticker
        #check if open space
        if ( (0 < X+moveX <= blocksize*self.DIM) and (0 < Y+moveY <= blocksize*self.DIM ) and i in range(24) ):
            self.myHero.moving = True
            X += moveX
            Y += moveY
            self.myHero.setXY(X,Y)
            self.Display.drawHero(x1,y1, self.myHero, self.myMap, self.gameBoard, self, direction)
            self.myHero.moving = False
            #roll the die to see if there will be a battle
            if self.rollDie(0,30) and self.myMap.type == 'dungeon':
                self.boxMessage("The baTTle is joined!")
                self.gameBoard.fill( black )
                g = self.myBattle.fightBattle(self.myHero, enemy.enemy(self.levelDepth))
                if g == True:
                    pass
                elif g == False:
                    self.gameOver()
                else: 
                    self.textMessage('You find '+str(g)+' gold pieces!')
                    self.myHero.addGold(g)
        self.Display.redrawXMap(self.myMap)
        self.Ticker.tick(1)
    
    def rollDie(self, target, range):
        d = random.randrange(range)
        if target >= d:
            return True
        else:
            return False

    # calls hud.boxMessage
    def boxMessage(self, msg):
        self.myHud.boxMessage(msg)
    
    # calls hud.txtMessage
    def textMessage(self, msg):
        self.myHud.txtMessage(msg)
    
    def getSaveBall(self):
        saveBall = (self.myHero.getSaveBall(), self.myDungeon, self.Ticker, self.currentMap)
        
        return saveBall
    
    def updateSprites(self):
        self.allsprites.update()
        rects = self.allsprites.draw(self.gameBoard)
        pygame.display.update(rects)
    
    def displayGameBoard(self):
        self.updateSprites()
        self.screen.blit( self.gameBoard, (75,75) )
        pygame.display.flip()

    def mainLoop(self):
        gameFrame, gameFrameRect = load_image('gamescreen600.bmp', None)
        self.screen.blit(gameFrame,(0,0))
        (X,Y) = self.myMap.getStartXY()
        self.myHero.setXY( X*blocksize,Y*blocksize )
        self.updateSprites()
        self.Display.drawHero( X*blocksize,Y*blocksize, self.myHero, self.myMap, self.gameBoard, animated=False)
        self.Display.redrawXMap(self.myMap)
        while self.gameOn:
            self.clock.tick(30)
            for event in pygame.event.get():
                self.event_handler(event)
                if event.type == pygame.QUIT:
                    os.sys.exit()
            self.gameBoard.fill(black)
            self.Display.redrawMap(self.myMap, self.myHero.getXY(), self.myHero.getRect(), self.gameBoard)
            self.myHud.update()
            #self.myHero.showLocation(self.gameBoard)
            self.displayGameBoard()
        return