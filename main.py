import pygame, game, random, cPickle, gzip, os
from UTIL import const, colors, load_image, inputHandler, button
from DISPLAY import interface, effects
from HERO import creator
from OBJ import weapon

from math import ceil

try:
    import android
except:
    android = False
    print "No Android in main"

# Set the height and width of the screen
screenSize=[720,1280]
screen=pygame.display.set_mode(screenSize)
#pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

if not pygame.font: print 'Warning, fonts disabled'

pygame.display.set_caption("Ransack")

pygame.init()
pygame.key.set_repeat(100, 100)
clock = pygame.time.Clock()
random.seed( os.urandom(1) )

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

FX = effects.effects(clock, screen)

C = creator.Creator()

iH = inputHandler.inputHandler(FX)

iFace = interface.Interface(screen, iH)

images = range(3)

def getFile(titleScreen):
    FX.displayLoadingMessage(titleScreen, 'Loading saved game list...')
    saveFiles = range(3)
    desc = range(3)
    for i in range(3):
        if os.access("ransack"+str(i)+".sav", os.F_OK):
            peekFile = gzip.GzipFile("ransack"+str(i)+".sav", 'rb')
            ball = cPickle.load(peekFile)
            peekFile.close()
            desc[i] = 'Saved game '+str(i)+' Level '+str(ball[1][11])+' '+str(ball[0].getDays())+' Days '+ \
                                                                            str(ball[0].getHours()%24)+':'+ \
                                                                            str(ball[0].getMins()%60)+'.'+ \
                                                                            str(ball[0].getSecs())
            saveFiles[i] = "ransack"+str(i)+".sav"
        else:
            saveFiles[i] = 'No file'
            desc[i] = 'No file'
    
    saveBox = pygame.Surface( (600,200) )
    selection = 0
    while True:
        saveBox.fill( colors.gold )
        if pygame.font:
            font = pygame.font.Font("./FONTS/gothic.ttf", 32)
            for i in range(3):
                saveBox.blit( font.render(desc[i], 1, colors.white, colors.gold), (25, (33-16)+(i*66) ) )
        for event in pygame.event.get():
            event_ = iH.getCmd(event)
            if event_ == pygame.QUIT:
                os.sys.exit()
            if event_ == pygame.K_UP:
                selection -= 1
                if selection == -1:
                    selection = 2
            if event_ == pygame.K_DOWN:
                selection += 1
                if selection == 3:
                    selection = 0
            if event_ == pygame.K_RETURN:
                return "ransack"+str(selection)+".sav"
            if event_ == pygame.K_ESCAPE:
                return None
        saveBox.blit( images[0], (0, (33-12)+(selection*66)) )
        screen.blit( saveBox, (50,200) )
        pygame.display.flip()
        
def endScreen(game, msg):
    dScreen = pygame.Surface( (300, 300) )
    if pygame.font:
        font = pygame.font.Font("./FONTS/SpinalTfanboy.ttf", 72)
        dScreen.blit( font.render(msg, 1, colors.red, colors.black), (50,50) )
        font = pygame.font.Font("./FONTS/devinne.ttf", 18)
        if game.myHero.level < 4:
            dScreen.blit( font.render("Nice Try, loser!", 1, colors.white, colors.black), (50,125) )
        elif game.myHero.level >= 4 and game.myHero.level < 10:
            dScreen.blit( font.render("Not bad... for a beginner!", 1, colors.white, colors.black), (50,125) )
        font = pygame.font.Font("./FONTS/gothic.ttf", 18)
        dScreen.blit( font.render("Level reached: "+str(game.myHero.level), 1, colors.white, colors.black), (50,225) )
        font = pygame.font.Font("./FONTS/gothic.ttf", 14)
        dScreen.blit( font.render(str(game.Ticker.getDays())+"days, "+str(game.Ticker.getHours()%24)+":"+str(game.Ticker.getMins()%60)+"."+str(game.Ticker.getSecs()), 
                                  1, 
                                  colors.white, colors.black), 
                     (50,250) )
        screen.blit(pygame.transform.scale(dScreen, (int(ceil(300 * 2.4)), 
                                                     int(ceil(300 * 2.4)) ) ), 
                                                     (0, 0) )
        pygame.display.flip()
    while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass

def launchNewGame(titleScreen):
    newGame = game.game(screen, clock, iFace, FX, iH, titleScreen, loadHero=C.mainLoop(screen))
    FX.fadeOut(0)
    iFace.state = 'game'
    if newGame.mainLoop():
        endScreen(newGame, "You Win!")
    else:
        endScreen(newGame, "Game Over.")
    FX.fadeOut(0)

def loadSavedGame(titleScreen):
    if android:
         android.hide_keyboard()
    try:
        '''
        loadFile = getFile(titleScreen)
        if loadFile == None: pass
        else:
        '''
        FX.displayLoadingMessage(titleScreen, 'Loading game file...')
        savFile = gzip.GzipFile('ransack0.sav', 'rb')
        FX.displayLoadingMessage(titleScreen, 'Loading saved game...')
        ball = cPickle.load(savFile)
        savFile.close()
        Game = game.game(screen, clock, iFace, FX, iH, titleScreen, ball[0], ball[1], ball[2], ball[3])
        FX.fadeOut(0)
        iFace.state = 'game'
        if Game.mainLoop():
            endScreen(Game, "You Win!")
        else:
            endScreen(Game, "Game Over.")
        FX.fadeOut(0)
    except IOError, e:
        print 'File I/O error', e
    

def mouseHandler(m):
    (mx, my) = pygame.mouse.get_pos()
    if (230 <= mx < 480) and (375 <= my < 430):
        launchNewGame()
    elif (230 <= mx < 480) and (430 <= my < 485):
        loadSavedGame()
    elif (230 <= mx < 300) and (485 <= my < 540):
        os.sys.exit()
    

def main():
    titleScreen = pygame.Surface((screenSize[0],screenSize[0]))
    ifaceImg, r = load_image.load_image( os.path.join('MENU', 'interface_m.png'), None)
    screen.blit( pygame.transform.scale(ifaceImg, (int(ceil(300 * 2.4)), 
                                                   int(ceil(233 * 2.4)) ) ), (0, int(ceil(300 * 2.4))) )
    selection = 0
    options = ['Begin New Game', 'Load Saved Game', 'Exit']
    screen.blit(titleScreen, (0,0))
    buttons = []
    
    if pygame.font:
        font = pygame.font.Font("./FONTS/chancery.ttf", 60)
    y = 350
    for o in options:
        line = font.render(o, 1, colors.white, colors.black)
        buttons.append( button.Button( ( (screen.get_width()/2)-(line.get_width()/2), y), o ) )
        y = y + 75
    
    while True:
        menuBox = pygame.Surface( (450,450) )
        menuBox.fill( colors.black )
        menuBox.set_colorkey(colors.black)
            
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                selection = None
                (mX, mY) = pygame.mouse.get_pos()
                for b in buttons:
                    if b.hit(mX, mY):
                        selection = b.msg
                if selection == 'Begin New Game':
                    launchNewGame(titleScreen)
                elif selection == 'Load Saved Game':
                    loadSavedGame(titleScreen)
                elif selection == 'Exit':
                    FX.fadeOut(0)
                    os.sys.exit()
                elif selection == None:
                    pass
        '''
        menuBox.blit( images[0], (0, selection*line.get_height()+(line.get_height()/2) ) )
        titleScreen.blit(pygame.transform.scale(titleImg, (int(ceil(300 * 2.4)), 
                                                           int(ceil(300 * 2.4)) ) ), (0,0) )
        titleScreen.blit(menuBox, (200, 375) )
        '''
        screen.blit(titleScreen, (0,0))
        for b in buttons:
            #screen.blit(b.img, ( (b.locX + b.sizeX) - (b.sizeX) , b.locY ) )
            screen.blit(b.img, ( b.locX, b.locY ) )
        iFace.update()
        font = pygame.font.Font(os.getcwd()+"/FONTS/courier.ttf", 28)
        if android:
            screen.blit( font.render( str( android.get_dpi() ), 1, colors.white, colors.black ), (0,0) )
        pygame.display.flip()
main()