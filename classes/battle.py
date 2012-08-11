import pygame
import menu
from load_image import *
from const import *
import random

# this class will be used to draw the animation occuring in the battle.

class battle():
    
    def __init__(self, screen, hud, ticker):
        self.battleField = pygame.Surface( (300,300) )
        self.battleField.fill( black )
        self.images = range(3)
        self.ticker = ticker
        self.screen = screen
        
        self.myMenu = menu.menu(screen)
        
        self.images[0], r = load_image('cursor.bmp')
        
        self.myHud = hud
    
    def writeText(self, surface, loc, text, fgc, bgc, size=18, font="SpinalTfanboy.ttf"):
        font = pygame.font.Font(os.getcwd()+"/FONTS/"+font, size)
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
        options = ['FighT', 'Magic', 'ITem', 'Flee']
        selection = 0
        while True:
            menuBox.fill( gold )
            if pygame.font:
                font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 14)
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
        self.textMessage('The fireball hits the monster for '+str(dmg)+' points!')
        return dmg
    
    def iceball(self, itl):
        dmg = random.randrange(itl,2*itl)
        self.textMessage('The iceball hits the monster for '+str(dmg)+' points!')
        return dmg
    
    def lightningball(self):
        pass
        
    # this controls all the logic of what goes on in an actual battle
    def fightBattle(self, hero, enemy):
        engagedEnemy = enemy
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn) = hero.getPlayerStats()
        (armor, weapon) = ( hero.getArmorEquipped(), hero.getWeaponEquipped() )
        self.textMessage( 'You are facing a level '+str(enemy.getLevel())+' '+enemy.getName()+'!' )
        time = 0
        while engagedEnemy.getHP() > 0:
            #clock.tick(15)
            if hero.isPoisoned:
                self.ticker.tick(5)
                if self.ticker.getTicks() - hero.poisonedAt >= 120:
                    self.textMessage('The poison has left your system.')
                    hero.isPoisoned = False
                else:
                    self.textMessage('The poison hurts you...')
                    if hero.takeDmg(1) < 1:
                        self.textMessage("You have died!")
                        return False
                
            action = self.getAction()
            if action == 'FighT':
                #hero attacks
                if self.rollDie(0,2):
                    dmg = random.randrange(sth/2,sth) + 10*weapon.getLevel()
                    self.textMessage('You hit the '+enemy.getName() +' for '+str(dmg)+' points!')
                    #self.sounds[1].play()
                    engagedEnemy.takeDmg(dmg)
                else:
                    self.textMessage("You missed The "+enemy.getName()+"!")
                    #self.sounds[2].play()
            elif action == 'Magic':
                result = hero.castSpell( self.myMenu.invMenu(hero.getSpells(), "Spells:" ),self.myHud, True )
                print result
                if result[0] == -2:
                    self.textMessage("That spell may not be cast in battle.")
                    continue
                if result[0] == -3:
                    self.textMessage("You don't have enough MP!")
                    continue
                elif result[0] == 1:
                    self.textMessage( result[1] )
                    engagedEnemy.takeDmg(self.fireball(itl))
                elif result[0] == 2:
                    self.textMessage( result[1] )
                    engagedEnemy.takeDmg(self.iceball(itl))
                else: self.textMessage( result[1] )
                    
            elif action == 'ITem':
                hero.useItem(self.myMenu.invMenu(hero.getItems(), "ITems:" ) )
            elif action == 'Flee':
                if self.rollDie(1,3):
                    self.textMessage("You escaped safely.")
                    return True
                else:
                    self.textMessage("You can't escape!")
            self.ticker.tick(15)
            #enemy attacks
            if engagedEnemy.getHP() > 0:
                if self.rollDie(0,2):
                    dmg = random.randrange(enemy.getLevel(),enemy.getLevel()+5) - random.randrange(dex/4)
                    self.textMessage("The "+enemy.getName()+" hits you for "+str(dmg)+" points!")
                    #self.sounds[1].play()
                    if enemy.poison:
                        if self.rollDie(1,7):
                            hero.isPoisoned = True
                            hero.poisonedAt = self.ticker.getTicks()
                            self.textMessage("You are poisoned!")
                    if hero.takeDmg(dmg) < 1:
                        self.textMessage("You have died!")
                        return False
                else:
                    self.textMessage("The "+enemy.getName()+" missed you!")
                    #self.sounds[2].play()
            self.ticker.tick(10)
            self.myHud.update()
            self.drawBattleScreen()
        self.textMessage("The "+enemy.getName()+" is dead!")
        if hero.increaseExp(5):
            self.textMessage("Congratulations! You have gained a level.")
        return random.randrange(enemy.getLevel()*2, enemy.getLevel()*4)