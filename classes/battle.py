import pygame
import menu
from load_image import *
from const import *
import random

# this class will be used to draw the animation occuring in the battle.

class battle():
    
    def __init__(self, screen, hud):
        self.battleField = pygame.Surface( (300,300) )
        self.battleField.fill( black )
        self.images = range(3)
        
        self.screen = screen
        
        self.myMenu = menu.menu()
        
        self.images[0], r = load_image('cursor.bmp')
        
        self.myHud = hud
    
    def writeText(self, surface, loc, text, fgc, bgc, size=18, font="arial"):
        font = pygame.font.SysFont(font, size)
        surface.blit( font.render(text, 1, fgc, bgc), loc )
        
    def drawBattleScreen(self):
        self.screen.blit( self.battleField, (75,75) )
        
        enemyHPBox = pygame.Surface( (100,50) )
        #self.writeText( enemyHPBox, (0,0), 
        pygame.display.flip()
    
    # displays battle menu and waits for player to select choice,
    # returns choice to fightBattle()
    def getAction(self):
        menuBox = pygame.Surface( (60,100) )
        options = ['Fight', 'Magic', 'Item', 'Flee']
        selection = 0
        while True:
            menuBox.fill( yellow )
            if pygame.font:
                font = pygame.font.SysFont("arial", 10)
                for i in range(4):
                    menuBox.blit( font.render(options[i], 1, white, yellow), (25,i*25) )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection -= 1
                        if selection == -1:
                            selection = 3
                    if event.key == pygame.K_DOWN:
                        selection += 1
                        if selection == 4:
                            selection = 0
                    if event.key == pygame.K_RETURN:
                        return options[selection]
            menuBox.blit( self.images[0], (0, selection*25) )            
            self.battleField.blit( menuBox, (200,150) )
            self.drawBattleScreen()
    
    def commence(self, screen):
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
        
    def rollDie(self, target, range):
        d = random.randrange(range)
        if target >= d:
            return True
        else:
            return False
    
    # calls message
    def boxMessage(self, msg):
        self.myHud.boxMessage(msg)
        '''
        self.queueLock.acquire()
        self.hudQueue.put( (0, msg) )
        self.queueLock.release()
        '''
    
    # calls msgSystem
    def textMessage(self, msg):
        self.myHud.txtMessage(msg)
        '''
        self.queueLock.acquire()
        self.hudQueue.put( (1, msg) )
        self.queueLock.release()
        '''
    
    def fireball(self, itl):
        dmg = random.randrange(itl,2*itl)
        self.textMessage('The fireball hits the monster for '+str(dmg)+' points!')
        return dmg
    
    def iceball(self):
        pass
    
    def lightningball(self):
        pass
        
    # this controls all the logic of what goes on in an actual battle
    def fightBattle(self, hero, enemy):
        engagedEnemy = enemy
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) = hero.getPlayerStats()
        (armor, weapon) = ( hero.getArmorEquipped(), hero.getWeaponEquipped() )
        while engagedEnemy.getHP() > 0:
            #clock.tick(15)
            action = self.getAction()
            if action == 'Fight':
                #hero attacks
                if self.rollDie(0,2):
                    dmg = random.randrange(sth/2,sth)
                    self.textMessage("You hit the monster for "+str(dmg)+" points!")
                    #self.sounds[1].play()
                    engagedEnemy.takeDmg(dmg)
                else:
                    self.textMessage("You missed the monster!")
                    #self.sounds[2].play()
            elif action == 'Magic':
                attack = hero.castSpell( self.myMenu.invMenu(self.screen, hero.getSpells(), "Spells:" ), True )
                if attack == 0:
                    pass
                elif attack == 1:
                    engagedEnemy.takeDmg(self.fireball(itl))
            elif action == 'Item':
                hero.useItem(self.myMenu.invMenu(self.screen, hero.getItems(), "Items:" ) )
            elif action == 'Flee':
                if self.rollDie(1,3):
                    self.textMessage("You escaped safely.")
                    return True
                else:
                    self.textMessage("You can't escape!")                    
            #enemy attacks
            if engagedEnemy.getHP() > 0:
                if self.rollDie(0,2):
                    dmg = random.randrange(1,5)
                    self.textMessage("The monster hits you for "+str(dmg)+" points!")
                    #self.sounds[1].play()
                    if hero.takeDmg(dmg) < 1:
                        self.textMessage("You have died!")
                        return False
                else:
                    self.textMessage("The monster missed you!")
                    #self.sounds[2].play()
            self.myHud.update()
            self.drawBattleScreen()
        self.textMessage("The monster is dead!")
        if hero.increaseExp(5):
            self.textMessage("Congratulations! You have gained a level!")
        return True