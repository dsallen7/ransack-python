import pygame
import os
import random
import pickle

from classes import hero, map, hud, battle, menu, enemy
from IMG import images
from const import *
from load_image import *

from MAP import mapgen


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
        self.myBattle = battle.battle(screen)
        self.myMap = None
        self.levelDepth = 1
        # a dungeon is just an array of maps
        self.myDungeon = []
        for mapFileName in mapList:
            self.myDungeon += [map.map(mapFileName)]
        
        self.myMap = self.myDungeon[self.levelDepth]
        
        self.allsprites = pygame.sprite.RenderPlain((self.myHero, self.badguys))
        
        #this is true while player is in a particular game
        self.gameOn = True
        
        #this is true while player is in a particular level
        self.levelOn = True        
        
        self.gameBoard = pygame.Surface( [450,450] )
        self.gameFrame, self.gameFrameRect = load_image('gamescreen600.bmp', -1)
        
        # 0 : camera
        # 1 : sword
        # 2 : miss
        self.sounds = range(3)
        self.sounds[0] = pygame.mixer.Sound(os.path.join('SND', 'camera.wav' ))
        self.sounds[1] = pygame.mixer.Sound(os.path.join('SND', 'sword1.wav' ))
        self.sounds[2] = pygame.mixer.Sound(os.path.join('SND', 'miss.wav' ))
    
    #toggles switch to continue running game
    def gameOver(self):
        self.gameOn = False
    
    def generateMap(self, DIM):
        rndMap = mapgen.Map(DIM)
        rndMap.generateMap(5)
        newMap = map.map(None, rndMap.getMapBall())
        return newMap
        
    def nextLevel(self):
        print self.myDungeon
        self.levelDepth += 1
        if self.levelDepth == len(self.myDungeon):
            self.myDungeon.append(self.generateMap(DIM))
            self.myMap = self.myDungeon[self.levelDepth]
        else:
            self.myMap = self.myDungeon[self.levelDepth]
        (x,y) = self.myMap.getPOE()
        self.myHero.setXY( x*blocksize,y*blocksize )
        if self.levelDepth <= 1:
            self.myMap.setLOV(4)
        else: self.myMap.setLOV(0)
    
    def prevLevel(self):
        self.levelDepth -= 1
        self.myMap = self.myDungeon[self.levelDepth]
        (x,y) = self.myMap.getPOEx()
        self.myHero.setXY( x*blocksize,y*blocksize )
        if self.levelDepth <= 1:
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
                '''
                (x,y,a,b) = self.rect
                self.newGame.mySword.attack(x,y,self.dir)
                '''
            elif event.key == pygame.K_s:
                self.castSpell( self.myMenu.invMenu(screen, self.myHero.getSpells(), images.spellImages, "Spells:" ) )
            elif event.key == pygame.K_i:
                self.useItem( self.myMenu.invMenu(screen, self.myHero.getItems(), "Items:" ) )
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
    
    def castSpell(self, spell):
        if spell == HEAL:
            if self.myHero.takeMP(5):
                self.myHero.takeDmg(-5)
                self.myHud.msgSystem(self.gameBoard, "You feel better!")
            else:
                self.myHud.msgSystem(self.gameBoard, "Not enough MP!")
    
    # this 
    def useItem(self,item):
        print item
        if item == None:
            return
        elif item+86 == SHP:
            self.myHero.takeDmg(-5)
            self.myHud.msgSystem(self.gameBoard, "You feel better!")
        elif item+86 == SMP:
            self.myHero.takeMP(-5)
            self.myHud.msgSystem(self.gameBoard, "You feel magical!")
        self.myHero.setItem(item, -1)
    
    # this controls all the logic of what goes on in an actual battle
    def fightBattle(self):
        engagedEnemy = enemy.enemy()
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) = self.myHero.getPlayerStats()
        while engagedEnemy.getHP() > 0:
            clock.tick(15)
            action = self.myBattle.getAction()
            if action == 'Fight':
                #hero attacks
                if self.rollDie(0,2):
                    dmg = random.randrange(sth/2,sth)
                    self.myHud.msgSystem(self.gameBoard, "You hit the monster for "+str(dmg)+" points!")
                    self.sounds[1].play()
                    engagedEnemy.takeDmg(dmg)
                else:
                    self.myHud.msgSystem(self.gameBoard, "You missed the monster!")
                    self.sounds[2].play()
            elif action == 'Magic':
                self.castSpell( self.myMenu.invMenu(screen, self.myHero.getSpells(), images.spellImages, "Spells:" ) )
            elif action == 'Item':
                self.useItem( self.myMenu.invMenu(screen, self.myHero.getItems(), images.itemImages, "Items:" ) )
            elif action == 'Flee':
                if self.rollDie(1,3):
                    self.myHud.msgSystem(self.gameBoard, "You escaped safely.")
                    return
                else:
                    self.myHud.msgSystem(self.gameBoard, "You can't escape!")                    
            #enemy attacks
            if engagedEnemy.getHP() > 0:
                if self.rollDie(0,2):
                    dmg = random.randrange(1,5)
                    self.myHud.msgSystem(self.gameBoard, "The monster hits you for "+str(dmg)+" points!")
                    self.sounds[1].play()
                    if self.myHero.takeDmg(dmg) < 1:
                        self.myHud.msgSystem(self.gameBoard, "You have died!")
                        self.gameOver()
                        return
                else:
                    self.myHud.msgSystem(self.gameBoard, "The monster missed you!")
                    self.sounds[2].play()
            self.myHud.displayStats(self.gameBoard, self.myHero.getPlayerStats(),self.myHero.getArmorEquipped(), self.myHero.getWeaponEquipped() )
            self.redrawScreen()
            pygame.display.flip()
        self.myHud.msgSystem(self.gameBoard, "The monster is dead!")
        if self.myHero.increaseExp(5):
            self.myHud.msgSystem(self.gameBoard, "Congratulations! You have gained a level!")
    
    #takes x,y of old myHero.rect location and finds new
    def drawHero(self,x1,y1, animated=True):
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
                self.myHero.setRect( i, j, blocksize, blocksize)
                self.updateSprites()
                self.redrawScreen()
        
        self.myHero.setRect( rectX, rectY, blocksize, blocksize)
            
    
    def move(self, direction):
        if direction not in ['up','down','left','right']: return
        noGoList = [1,3,10]
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
                self.myHud.message( "The door is locked!" )
                return
            else:
                self.myHud.message( "The door creaks open..." )
                self.myHero.takeKey()
                self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize,0)
        #item
        if i in range(86,101): 
            self.myHero.getItem(i)
            self.myMap.updateUnit( (X + moveX)/blocksize, (Y + moveY)/blocksize, 0)
            self.myHud.msgSystem(self.gameBoard, itemMsgs[i])
        # Stairs down
        if i == STAIRDN:
            self.myHud.message( "Onto the next level!" )
            self.nextLevel()
            self.drawHero(x1,y1,False)
            return
        # Stairs up
        if i == STAIRUP:
            self.prevLevel()
            self.drawHero(x1,y1,False)
            return
        #check if open space
        if ( (0 < X+moveX <= blocksize*DIM) and (0 < Y+moveY <= blocksize*DIM ) and i in range(24) ):
            X += moveX
            Y += moveY
            self.myHero.setXY(X,Y)
            self.drawHero(x1,y1)
            #roll the die to see if there will be a battle
            if self.rollDie(0,40) and self.levelDepth > 1:
                self.myHud.message("The battle is joined!")
                #self.myBattle.commence(screen)
                self.gameBoard.fill( black )
                self.fightBattle()
       
    def updateSprites(self):
        #self.allsprites.clear(self.spriteLayer, self.gameBoard)
        self.allsprites.update()
        self.allsprites.draw(self.gameBoard)
    
    def redrawScreen(self):
        #screen.blit( self.gameFrame, (0,0) )
        #self.myHero.showLocation(self.gameBoard)
        screen.blit( self.gameBoard, (75,75) )
        #screen.blit( self.spriteLayer, (75,75) )
        pygame.display.flip()
    
    def switchMap(self):
        pass

    def mainLoop(self, mapList):
        screen.blit(self.gameFrame,(0,0))
        (X,Y) = self.myMap.getStartXY()
        self.myHero.setXY( X*blocksize,Y*blocksize )
        self.updateSprites()
        self.drawHero( X*blocksize,Y*blocksize, False )
        while self.levelOn and self.gameOn:
            clock.tick(15)
            for event in pygame.event.get():
                self.event_handler(event)
                if event.type == pygame.QUIT:
                    os.sys.exit()
            self.gameBoard.fill(black)
            self.myMap.redraw(self.myHero.getXY(), self.myHero.getRect(), self.gameBoard)
            self.myHud.displayStats(self.gameBoard, self.myHero.getPlayerStats(),self.myHero.getArmorEquipped(), self.myHero.getWeaponEquipped())
            self.updateSprites()
            self.redrawScreen()

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