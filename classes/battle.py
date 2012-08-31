import pygame
import menu
from load_image import *
import random
from UTIL import const, colors

# this class will be used to draw the animation occuring in the battle.

class battle():
    
    def __init__(self, screen):
        self.battleField = pygame.Surface( (300,300) )
        self.battleField.fill( colors.black )
        self.images = range(3)
        self.screen = screen
        
        self.myMenu = menu.menu(screen)
        
        self.images[0], r = load_image('cursor.bmp')
        
    def writeText(self, surface, loc, text, fgc, bgc, size=18, font="SpinalTfanboy.ttf"):
        font = pygame.font.Font(os.getcwd()+"/FONTS/"+font, size)
        surface.blit( font.render(text, 1, fgc, bgc), loc )
        
    def drawBattleScreen(self, enemy=None):
        if enemy is not None:
            self.battleField.blit( self.boxStat(enemy.getHP(), enemy.maxHP, colors.red, colors.green, (150,30) ), (150,30) )
        self.screen.blit( self.battleField, (const.gameBoardOffset, const.gameBoardOffset) )
        pygame.display.flip()
    
    # displays battle menu and waits for player to select choice,
    # returns choice to fightBattle()
    def getAction(self):
        menuBox = pygame.Surface( (60,100) )
        options = ['FighT', 'Magic', 'ITem', 'Flee']
        selection = 0
        while True:
            menuBox.fill( colors.gold )
            if pygame.font:
                font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 14)
                for i in range(4):
                    menuBox.blit( font.render(options[i], 1, colors.white, colors.gold), (25,i*25) )
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
    
    def boxStat(self, stat, mStat, fgc, bgc, loc):
        (x, y) = loc
        maxBoxWidth = 90
        maxBox = pygame.Surface( (90, 11) )
        maxBox.fill(bgc)
        currBoxWidth = int(90 * float(stat)/float(mStat))
        if currBoxWidth > 0:
            currBox = pygame.Surface( (currBoxWidth, 11) )
            currBox.fill(fgc)
            maxBox.blit(currBox, (0,0) )
        return maxBox
    
    # this controls all the logic of what goes on in an actual battle
    def fightBattle(self, game, enemy):
        hero = game.myHero
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn) = hero.getPlayerStats()
        (armor, weapon) = ( hero.getArmorEquipped(), hero.getWeaponEquipped() )
        game.textMessage( 'You are facing a level '+str(enemy.getLevel())+' '+enemy.getName()+'!' )
        time = 0
        while enemy.getHP() > 0:
            #clock.tick(15)
            if hero.isPoisoned:
                game.Ticker.tick(5)
                if game.Ticker.getTicks() - hero.poisonedAt >= 120:
                    game.textMessage('The poison has left your system.')
                    hero.isPoisoned = False
                else:
                    game.textMessage('The poison hurts you...')
                    if hero.takeDmg(1) < 1:
                        game.textMessage("You have died!")
                        return False
                
            action = self.getAction()
            if action == 'FighT':
                #hero attacks
                if self.rollDie(0,2):
                    dmg = random.randrange(sth/2,sth) + 10*weapon.getLevel()
                    game.textMessage('You hit the '+enemy.getName() +' for '+str(dmg)+' points!')
                    #self.sounds[1].play()
                    enemy.takeDmg(dmg)
                else:
                    game.textMessage("You missed The "+enemy.getName()+"!")
                    #self.sounds[2].play()
            elif action == 'Magic':
                enemy.takeDmg( hero.castSpell( self.myMenu.invMenu(hero.getSpells(), "Spells:" ), game, True ) )
                    
            elif action == 'ITem':
                hero.useItem(self.myMenu.invMenu(hero.getItems(), "ITems:" ), game, True )
            elif action == 'Flee':
                if self.rollDie(1,3):
                    game.textMessage("You escaped safely.")
                    return True
                else:
                    game.textMessage("You can't escape!")
            game.Ticker.tick(15)
            #enemy attacks
            if enemy.getHP() > 0:
                if self.rollDie(0,2):
                    dmg = random.randrange(enemy.getBaseAttack()-5,enemy.getBaseAttack()+5) - random.randrange(dex/4)
                    game.textMessage("The "+enemy.getName()+" hits you for "+str(dmg)+" points!")
                    #self.sounds[1].play()
                    if enemy.poison:
                        if self.rollDie(1,7):
                            hero.isPoisoned = True
                            hero.poisonedAt = self.ticker.getTicks()
                            game.textMessage("You are poisoned!")
                    if hero.takeDmg(dmg) < 1:
                        game.textMessage("You have died!")
                        return False
                else:
                    game.textMessage("The "+enemy.getName()+" missed you!")
                    #self.sounds[2].play()
            game.Ticker.tick(10)
            game.myHud.update()
            self.drawBattleScreen(enemy)
        game.textMessage("The "+enemy.getName()+" is dead!")
        if hero.increaseExp(5):
            game.textMessage("Congratulations! You have gained a level.")
        return random.randrange(enemy.getLevel()*2, enemy.getLevel()*4)