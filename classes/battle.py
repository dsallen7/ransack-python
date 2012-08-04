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
        
        self.myMenu = menu.menu(screen)
        
        self.images[0], r = load_image('cursor.bmp')
        
        self.myHud = hud
    
    def writeText(self, surface, loc, text, fgc, bgc, size=18, font="SpinalTfanboy.ttf"):
        font = pygame.font.Font("../FONTS/"+font, size)
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
        options = ['FighT', 'Magic', 'Item', 'Flee']
        selection = 0
        while True:
            menuBox.fill( gold )
            if pygame.font:
                font = pygame.font.Font("../FONTS/SpinalTfanboy.ttf", 14)
                for i in range(4):
                    menuBox.blit( font.render(options[i], 1, white, gold), (25,i*25) )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection -= 1
                        if selection == -1:
                            selection = 3
                    elif event.key == pygame.K_DOWN:
                        selection += 1
                        if selection == 4:
                            selection = 0
                    elif event.key == pygame.K_RETURN:
                        return options[selection]
                    elif event.key == pygame.K_ESCAPE:
                        pass
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
        self.myHud.update()
    
    # calls msgSystem
    def textMessage(self, msg):
        self.myHud.txtMessage(msg)
        self.myHud.update()
    
    def fireball(self, itl):
        dmg = random.randrange(itl,2*itl)
        self.textMessage('The fireball hiTs The monsTer for '+str(dmg)+' poinTs!')
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
        self.textMessage( 'You are facing a level '+str(enemy.getLevel())+' '+enemy.getName()+'!' )
        while engagedEnemy.getHP() > 0:
            #clock.tick(15)
            action = self.getAction()
            if action == 'FighT':
                #hero attacks
                if self.rollDie(0,2):
                    dmg = random.randrange(sth/2,sth) + 10*weapon.getLevel()
                    self.textMessage('You hiT The '+enemy.getName() +' for '+str(dmg)+' poinTs!')
                    #self.sounds[1].play()
                    engagedEnemy.takeDmg(dmg)
                else:
                    self.textMessage("You missed The "+enemy.getName()+"!")
                    #self.sounds[2].play()
            elif action == 'Magic':
                attack = hero.castSpell( self.myMenu.invMenu(hero.getSpells(), "Spells:" ), True )
                if attack == 0:
                    pass
                elif attack == 1:
                    engagedEnemy.takeDmg(self.fireball(itl))
            elif action == 'Item':
                hero.useItem(self.myMenu.invMenu(hero.getItems(), "ITems:" ) )
            elif action == 'Flee':
                if self.rollDie(1,3):
                    self.textMessage("You escaped safely.")
                    return True
                else:
                    self.textMessage("You can'T escape!")       
            #enemy attacks
            if engagedEnemy.getHP() > 0:
                if self.rollDie(0,2):
                    dmg = random.randrange(enemy.getLevel(),enemy.getLevel()+5) - random.randrange(dex/2)
                    self.textMessage("The "+enemy.getName()+" hiTs you for "+str(dmg)+" poinTs!")
                    #self.sounds[1].play()
                    if enemy.poison:
                        if self.rollDie(1,5):
                            hero.isPoisoned = True
                            self.textMessage("You are poisoned!")
                    if hero.takeDmg(dmg) < 1:
                        self.textMessage("You have died!")
                        return False
                else:
                    self.textMessage("The "+enemy.getName()+" missed you!")
                    #self.sounds[2].play()
            self.myHud.update()
            self.drawBattleScreen()
        self.textMessage("The "+enemy.getName()+" is dead!")
        if hero.increaseExp(5):
            self.textMessage("CongraTulaTions! You have gained a level!")
        return random.randrange(enemy.getLevel()*2, enemy.getLevel()*4)