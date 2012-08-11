import pygame, game, random, pickle
from const import *
from load_image import *

# Set the height and width of the screen
screenSize=[600,600]
screen=pygame.display.set_mode(screenSize)
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

if not pygame.font: print 'Warning, fonts disabled'

pygame.display.set_caption("Ransack")

pygame.init()
pygame.key.set_repeat(100, 100)
clock = pygame.time.Clock()
random.seed()


images = range(3)
images[0], r = load_image('cursor.bmp', -1)

def getFile():
    saveFiles = range(3)
    desc = range(3)
    for i in range(3):
        if os.access("ransack"+str(i)+".sav", os.F_OK):
            peekFile = open("ransack"+str(i)+".sav", 'r')
            ball = pickle.load(peekFile)
            peekFile.close()
            desc[i] = 'Saved game '+str(i)+' Level '+str(ball[0][11])+' '+str(ball[2].getDays())+' Days '+ \
                                                                            str(ball[2].getHours()%24)+':'+ \
                                                                            str(ball[2].getMins()%60)+'.'+ \
                                                                            str(ball[2].getSecs())
            saveFiles[i] = "ransack"+str(i)+".sav"
        else:
            saveFiles[i] = 'No file'
            desc[i] = 'No file'
    
    saveBox = pygame.Surface( (300,100) )
    selection = 0
    while True:
        saveBox.fill( gold )
        if pygame.font:
            font = pygame.font.Font("./FONTS/gothic.ttf", 14)
            for i in range(3):
                saveBox.blit( font.render(desc[i], 1, white, gold), (25,i*25) )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection -= 1
                    if selection == -1:
                        selection = 2
                if event.key == pygame.K_DOWN:
                    selection += 1
                    if selection == 3:
                        selection = 0
                if event.key == pygame.K_RETURN:
                    return "ransack"+str(selection)+".sav"
                if event.key == pygame.K_ESCAPE:
                    return None
        saveBox.blit( images[0], (0, selection*25) )
        screen.blit( saveBox, (100,200) )
        pygame.display.flip()

def main():    
    titleScreen = pygame.Surface(screenSize)
    titleScreen.fill(black)
    titleImg, titleRect = load_image('titlescreen.bmp', -1)
    titleScreen.blit(titleImg, (50,50) )
    selection = 0
    options = ['Begin New Game', 'Load Saved Game', 'Level EdiTor']
    screen.blit(titleScreen, (0,0))
    menuBox = pygame.Surface( (200,80) )
    while True:
        menuBox.fill( brown )
        screen.blit(titleScreen, (0,0))
        clock.tick(20)
        
        if pygame.font:
            font = pygame.font.Font("./FONTS/SpinalTfanboy.ttf", 28)
            for i in range(len(options)):
                menuBox.blit( font.render(options[i], 1, gold, brown), (30,(i*25)) )
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    os.sys.exit()
                if event.key == pygame.K_UP:
                    selection -= 1
                    if selection == -1:
                        selection = len(options)-1
                if event.key == pygame.K_DOWN:
                    selection += 1
                    if selection == len(options):
                        selection = 0
                if event.key == pygame.K_RETURN:
                    if options[selection] == 'Begin New Game':
                        newGame = game.game(screen, clock)
                        newGame.mainLoop()
                    elif options[selection] == 'Load Saved Game':
                        try:
                            loadFile = getFile()
                            if loadFile == None: pass
                            else:
                                savFile = open(loadFile, 'r')
                                ball = pickle.load(savFile)
                                savFile.close()
                                Game = game.game(screen, clock, loadHero=ball[0], loadDungeon=ball[1], loadTicker = ball[2], currentMap = ball[3])
                                Game.mainLoop()
                        except IOError, e:
                            print 'File I/O error', e
        
        menuBox.blit( images[0], (0, selection*25) )
        titleScreen.blit(menuBox, (200, 375) )
        pygame.display.flip()
    
main()