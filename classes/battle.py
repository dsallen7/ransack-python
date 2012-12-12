import pygame, os
from DISPLAY import menu
import random
from UTIL import const, colors, load_image, button, misc
from math import floor, ceil
from SCRIPTS import enemyScr

try:
    import android
except:
    android = False
    print "No Android in battle"

# this class will be used to draw the animation occuring in the battle.

class battle():
    
    def __init__(self, screen, iH, menu):
        self.battleField, r = load_image.load_image( os.path.join('ANIMATION', 'battlefield.bmp'), None)
        self.battleField.set_colorkey([255,0,0])
        self.forestField, r = load_image.load_image( os.path.join('ANIMATION', 'forestField.bmp'), None)
        self.dungeonField, r = load_image.load_image( os.path.join('ANIMATION', 'dungeonField.bmp'), None)
        self.images = range(3)
        self.screen = screen
        
        self.background = pygame.Surface((300, 300))
        
        self.myMenu = menu
        
        #self.images[0], r = load_image.load_image('cursor.bmp', -1)
        
        self.enemyImgs = range(2)
        
        self.enemyImg = None
        
        self.heroImgs = range(2)
        
        self.heroImg = None
        
        self.inputHandler = iH
        
        self.buttons = [button.Button( (200, 150), 'Fight',os.getcwd()+"/FONTS/Squealer.ttf", 12),
                        button.Button( (200, 183), 'Magic',os.getcwd()+"/FONTS/Squealer.ttf", 12),
                        button.Button( (200, 216), 'Item',os.getcwd()+"/FONTS/Squealer.ttf", 12),
                        button.Button( (200, 249), 'Flee',os.getcwd()+"/FONTS/Squealer.ttf", 12)
                        
                        ]
        
    def writeText(self, surface, loc, text, fgc, bgc, size=18, font="SpinalTfanboy.ttf"):
        font = pygame.font.Font(os.getcwd()+"/FONTS/"+font, size)
        surface.blit( font.render(text, 1, fgc, bgc), loc )
    
    # can be called with or without enemy argument
    # if enemy is specified, battlefield will be drawn fresh
    def drawBattleScreen(self, game, enemy=None):
        if enemy is not None:
            self.battleField, r = load_image.load_image(os.path.join('ANIMATION', 'battlefield.bmp'), -1)
            if game.myMap.type == 'wilds':
                self.background.blit(self.forestField, (0,0) )
            else: self.background.blit(self.dungeonField, (0,0) )
            self.battleField.blit( self.boxStat(enemy.getHP(), enemy.maxHP, colors.red, colors.black, (150, 30) ), (204, 97) )
            self.battleField.blit( self.enemyImg, (125, 50)  )
            self.battleField.blit( self.heroImg, (0, 75)  )
            self.background.blit(self.battleField, (0,0) )
        #self.screen.blit( pygame.transform.scale(self.battleField, (720, 720) ), (0, 0) )
        game.Display.displayOneFrame(game.myInterface, game.FX, self.background, game, False, True)
        pygame.display.flip()
    
    # displays battle menu and waits for player to select choice,
    # returns choice to fightBattle()
    def getAction(self, game):
        options = ['FighT', 'Magic', 'ITem', 'Flee']
        selection = 0
        while True:
            menuBox = pygame.Surface( (60,100) )
            menuBox.set_colorkey(colors.gold)
            menuBox.fill( colors.gold )
            for b in self.buttons:
                self.background.blit(b.img, (b.locX, b.locY) )
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = pygame.mouse.get_pos()
                    for b in self.buttons:
                        if b.hit(int(ceil(x/const.scaleFactor)), 
                                 int(ceil(y/const.scaleFactor)) ):
                            return b.msg
                event_ = self.inputHandler.getCmd(event)
                if event_ == pygame.K_t:
                    game.screenShot()
                if event_ == pygame.QUIT:
                    os.sys.exit()
                elif event_ == pygame.K_ESCAPE:
                    pass
            #menuBox.blit( self.images[0], (0, selection*25) )            
            #self.background.blit( menuBox, (200,150) )
            self.drawBattleScreen(game)
    
    def commence(self, screen):
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
    
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
    
    def showEnemyDeath(self, game):
        for i in range(50, 300, 10):
            self.battleField, r = load_image.load_image(os.path.join('ANIMATION', 'battlefield.bmp'), -1)
            if game.myMap.type == 'wilds':
                self.background.blit(self.forestField, (0,0) )
            else: self.background.blit(self.dungeonField, (0,0) )
            self.battleField.blit( self.enemyImg, (125, i)  )
            self.battleField.blit( self.heroImg, (0, 75)  )
            self.background.blit(self.battleField, (0,0) )
            game.Display.displayOneFrame(game.myInterface, game.FX, self.background, game, False, True)
            pygame.display.flip()
        
    
    def loadEnemyImg(self, hero, enemy):
        if hero.gender == 'male':
            self.heroImgs[0], r = load_image.load_image( os.path.join('ANIMATION', 'hero_m1.bmp'), 2 )
            self.heroImgs[1], r = load_image.load_image( os.path.join('ANIMATION', 'hero_m2.bmp'), 2 )
        else:
            self.heroImgs[0], r = load_image.load_image( os.path.join('ANIMATION', 'hero_f1.bmp'), 2 )
            self.heroImgs[1], r = load_image.load_image( os.path.join('ANIMATION', 'hero_f2.bmp'), 2 )
        self.heroImg = self.heroImgs[0]
        enemyImgFilenames = enemyScr.imgFileDict[enemy.getName()]
        for i in range(len(enemyImgFilenames)):
             self.enemyImgs[i], r = load_image.load_image( os.path.join('ANIMATION', enemyImgFilenames[i]), 2 )
        self.enemyImg = self.enemyImgs[0]
    
    def damageEnemy(self, game, enemy, dmg):
        for i in range(enemy.getHP(), enemy.getHP()-dmg, -1):
            enemy.takeDmg(1)
            self.drawBattleScreen(game, enemy)
    
    # this controls all the logic of what goes on in an actual battle
    def fightBattle(self, game, enemy, board_):
        self.loadEnemyImg(game.myHero, enemy)
        self.drawBattleScreen(game, enemy)
        game.FX.scrollFromCenter(board_, self.battleField)
        #game.myInterface.update()
        hero = game.myHero
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn) = hero.getPlayerStats()
        (armor, weapon) = ( hero.getArmorEquipped(), hero.getWeaponEquipped() )
        if enemy.getLevel() > 0:
            game.textMessage( 'You are facing a level '+str(enemy.getLevel())+' '+enemy.getName()+'!' )
        else:
            game.textMessage( 'You are facing the '+enemy.getName()+'!' )
        time = 0
        while enemy.getHP() > 0:
            #clock.tick(15)
            self.enemyImg = self.enemyImgs[0]
            self.drawBattleScreen(game, enemy)
            if not hero.updateStatus(game):
                return False
                
            action = self.getAction(game)
            if action == 'Fight':
                #hero attacks
                self.heroImg = self.heroImgs[1]
                a = random.randrange(0, dex+5)
                if not (a > dex):
                    dmg = random.randrange(sth/2,sth) + weapon.getLevel()**2
                    game.textMessage('You hit the '+enemy.getName() +' for '+str(dmg)+' points!')
                    #game.SFX.play(1)
                    self.damageEnemy(game, enemy, dmg)
                else:
                    game.textMessage("You missed The "+enemy.getName()+"!")
                    #game.SFX.play(2)
            elif action == 'Magic':
                dmg = hero.castSpell( self.myMenu.invMenu(hero.getSpells(), "Spells:", ['Cast', 'Return'] ), game, True )
                if dmg in [True, False]: pass
                else: self.damageEnemy(game, enemy, dmg)
                
            elif action == 'Item':
                dmg = hero.useItem(self.myMenu.invMenu(hero.getItems(), "Items:", ['Use', 'Return'] ), game, True )
                if dmg in [True, False]: pass
                else: self.damageEnemy(game, enemy, dmg)
                
            elif action == 'Flee':
                if misc.rollDie(1,3):
                    game.textMessage("You escaped safely.")
                    game.FX.scrollFromCenter(self.battleField, board_)
                    return 'escaped'
                else:
                    game.textMessage("You can't escape!")
            self.heroImg = self.heroImgs[0]
            pygame.time.wait(1000)
            game.myInterface.update(game)
            self.drawBattleScreen(game, enemy)
            
            game.Ticker.tick(10)
            #enemy attacks
            if enemy.getHP() > 0:
                if not misc.rollDie(hero.dex, const.maxStats):
                    dmg = random.randrange(enemy.getBaseAttack()-5,enemy.getBaseAttack()+5) - ( hero.armorClass )
                    if dmg > 0:
                        game.textMessage("The "+enemy.getName()+" hits you for "+str(dmg)+" points!")
                        if enemy.poison:
                            if misc.rollDie(0,3):
                                if hero.isDamned:
                                    hero.isDamned = False
                                hero.isPoisoned = True
                                hero.poisonedAt = game.Ticker.getTicks()
                                game.textMessage("You are poisoned!")
                        elif enemy.damned:
                            if misc.rollDie(0,3):
                                if hero.isPoisoned:
                                    hero.isPoisoned = False
                                hero.isDamned = True
                                hero.damnedAt = game.Ticker.getTicks()
                                game.textMessage("You are damned!")
                        #game.SFX.play(1)
                        self.enemyImg = self.enemyImgs[1]
                        if android:
                            android.vibrate(0.1)
                    else: game.textMessage("The "+enemy.getName()+" attack is ineffective.")
                    if hero.takeDmg(dmg) < 1:
                        game.textMessage("You have died!")
                        game.FX.scrollFromCenter(self.battleField, board_)
                        return 'died'
                else:
                    game.textMessage("The "+enemy.getName()+" missed you!")
                    #game.SFX.play(2)
            game.Ticker.tick(10)
            game.myInterface.update(game)
            self.drawBattleScreen(game, enemy)
            pygame.time.wait(1000)
        game.textMessage("The "+enemy.getName()+" is dead!")
        self.showEnemyDeath(game)
        if hero.increaseExp( enemyScr.expDict[enemy.getName()] + random.randrange(enemy.getLevel()*2, enemy.getLevel()*4)  ):
            game.textMessage("Congratulations! You have gained a level.")
        game.FX.scrollFromCenter(self.background, board_)
        return 'won'