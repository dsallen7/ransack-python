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
# using game sprites instead of full blown animations here

class battle():
    
    def __init__(self, screen, iH, menu):
        self.screen = screen
        
        self.battleField, r = load_image.load_image( os.path.join('ANIMATION', 'battlefield.bmp'), None)
        self.battleField.set_colorkey([255,0,0])
        self.background = pygame.Surface((300, 300))
        
        self.forestField, r = load_image.load_image( os.path.join('ANIMATION', 'forestField.bmp'), None)
        self.dungeonField, r = load_image.load_image( os.path.join('ANIMATION', 'dungeonField.bmp'), None)
        self.townField, r = load_image.load_image( os.path.join('ANIMATION', 'townField.bmp'), None)
        self.myMenu = menu
                
        self.enemyImgs = range(10)
        self.enemyImg = None
        self.heroImgs = range(10)
        self.heroImg = None

        self.heroImgIdx = 4
        self.enemyImgIdx = 6

        self.heroStepIdx = 0
        self.enemyStepIdx = 0
        
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
    def drawBattleScreen(self, game, enemy=None, enemyX = 50, enemyY = 100, heroX = 250, heroY = 100):
        if enemy is not None:
            self.battleField, r = load_image.load_image(os.path.join('ANIMATION', 'battlefield.bmp'), -1)
            if game.myMap.type == 'dungeon': self.background.blit(self.dungeonField, (0,0) )
            elif game.myMap.type == 'dungeon': self.background.blit(self.forestField, (0,0) )
            elif game.myMap.type == 'village': self.background.blit(self.townField, (0,0) )
            self.battleField.blit( self.enemyAvatar, (enemyX, enemyY) )
            self.battleField.blit( self.heroAvatar, (heroX, heroY) )
            self.battleField.blit( self.boxStat(enemy.getHP(), enemy.maxHP, colors.red, colors.black, (150, 30) ), (10, 85) )
            self.background.blit(self.battleField, (0,0) )
        #self.screen.blit( pygame.transform.scale(self.battleField, (720, 720) ), (0, 0) )
        game.Display.displayOneFrame(game.myInterface, game.FX, self.background, game, False, True)
        pygame.display.flip()

    def drawHeroAttack(self, game, enemy):
        for i in range(250, 240, -1):
            self.heroImgIdx = self.heroImgIdx + const.walkingList[self.heroStepIdx]
            self.heroStepIdx = ( self.heroStepIdx + 1 ) % 4
            self.heroAvatar = self.heroImgs[self.heroImgIdx]
            self.drawBattleScreen(game, enemy, 50, 100, i, 100)
        for i in range(240, 250):
            self.heroImgIdx = self.heroImgIdx + const.walkingList[self.heroStepIdx]
            self.heroStepIdx = ( self.heroStepIdx + 1 ) % 4
            self.heroAvatar = self.heroImgs[self.heroImgIdx]
            self.drawBattleScreen(game, enemy, 50, 100, i, 100)

    def drawEnemyAttack(self, game, enemy):
        for i in range(50, 60):
            self.enemyImgIdx = self.enemyImgIdx + const.walkingList[self.enemyStepIdx]
            self.enemyStepIdx = ( self.enemyStepIdx + 1 ) % 4
            self.enemyAvatar = self.enemyImgs[self.enemyImgIdx]
            self.drawBattleScreen(game, enemy, i, 100, 250, 100)
        for i in range(60, 50, -1):
            self.enemyImgIdx = self.enemyImgIdx + const.walkingList[self.enemyStepIdx]
            self.enemyStepIdx = ( self.enemyStepIdx + 1 ) % 4
            self.enemyAvatar = self.enemyImgs[self.enemyImgIdx]
            self.drawBattleScreen(game, enemy, i, 100, 250, 100)

    def drawHeroDamage(self, game, enemy):
        pass

    def drawEnemyDamage(self, game, enemy):
        pass

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
    
    def damageEnemy(self, game, enemy, dmg):
        for i in range(enemy.getHP(), enemy.getHP()-dmg, -1):
            enemy.takeDmg(1)
            self.drawBattleScreen(game, enemy)

    def heroTurn(self, game, enemy, board_):
        hero = game.myHero
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn) = hero.getPlayerStats()
        (armor, weapon) = ( hero.getArmorEquipped(), hero.getWeaponEquipped() )
        action = self.getAction(game)
        if action == 'Fight':
            #hero attacks
            #self.heroImg = self.heroImgs[1]
            self.drawHeroAttack(game, enemy)
            a = random.randrange(0, dex+5)
            if not (a > dex):
                dmg = random.randrange(sth/2,sth) + weapon.getLevel()**2
                game.textMessage('You hit the '+enemy.getName() +' for '+str(dmg)+' points!')
                game.SFX.play(1)
                self.damageEnemy(game, enemy, dmg)
            else:
                game.textMessage("You missed The "+enemy.getName()+"!")
                game.SFX.play(2)
            return True
        elif action == 'Magic':
            dmg = hero.castSpell( self.myMenu.invMenu(game, hero.getSpells(), "Spells:", ['Cast', 'Return'] ), game, True )
            if dmg in [True, False]: return dmg
            else:
                self.damageEnemy(game, enemy, dmg)
                return True
            
        elif action == 'Item':
            dmg = hero.useItem(self.myMenu.invMenu(game, hero.getItems(), "Items:", ['Use', 'Return'] ), game, True )
            if dmg in [True, False]: return dmg
            else:
                self.damageEnemy(game, enemy, dmg)
                return True
            
        elif action == 'Flee':
            if misc.rollDie(1,3):
                game.textMessage("You escaped safely.")
                game.FX.scrollFromCenter(self.battleField, board_)
                return 'escaped'
            else:
                game.textMessage("You can't escape!")
                return True
    # this controls all the logic of what goes on in an actual battle

    def fightBattle(self, game, enemy, board_, enemyImgs, heroImgs):
        self.heroImgs = heroImgs
        self.enemyImgs = enemyImgs
        self.enemyAvatar = enemyImgs[self.enemyImgIdx]
        self.heroAvatar = heroImgs[self.heroImgIdx]
        self.drawBattleScreen(game, enemy)
        game.FX.scrollFromCenter(board_, self.battleField)
        hero = game.myHero
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn) = hero.getPlayerStats()
        (armor, weapon) = (hero.getArmorEquipped(), hero.getWeaponEquipped())
        if enemy.getLevel() > 0:
            game.textMessage('You are facing a level {} {}!'.format(enemy.getLevel(), enemy.getName()))
        else:
            game.textMessage('You are facing the {}!'.format(enemy.getName()))
        time = 0
        while enemy.getHP() > 0:
            self.drawBattleScreen(game, enemy)
            if not hero.updateStatus(game):
                return False
            # hero turn
            while not self.heroTurn(game, enemy, board_):
                pass
            game.myInterface.update(game)
            self.drawBattleScreen(game, enemy)
            
            game.Ticker.tick(10)
            #enemy attacks
            self.drawEnemyAttack(game, enemy)
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
                        game.SFX.play(1)
                        self.enemyImg = self.enemyImgs[1]
                        if android:
                            android.vibrate(0.1)
                    else: game.textMessage("The {} attack is ineffective.".format(enemy.getName()))
                    if hero.takeDmg(dmg) < 1:
                        game.textMessage("You have died!")
                        #game.FX.scrollFromCenter(self.battleField, board_)
                        return 'died'
                else:
                    game.textMessage("The "+enemy.getName()+" missed you!")
                    game.SFX.play(2)
            game.Ticker.tick(10)
            game.myInterface.update(game)
            self.drawBattleScreen(game, enemy)
            pygame.time.wait(1000)
        game.textMessage("The "+enemy.getName()+" is dead!")
        if hero.increaseExp( enemyScr.expDict[enemy.getName()] + random.randrange(enemy.getLevel()*2, enemy.getLevel()*4)  ):
            game.textMessage("Congratulations! You have gained a level.")
        game.FX.scrollFromCenter(self.background, board_)
        return 'won'
