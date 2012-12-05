import pygame, cPickle, gzip
from DISPLAY import menu, text
from IMG import images
import random, os
from OBJ import item
from SCRIPTS import shopScr

from UTIL import const, colors, load_image
from math import floor, ceil

class Townhall():
    
    def __init__(self, screen, interface, ticker, iH, menu):
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.screen = screen
        self.myInterface = interface
        self.ticker = ticker
        images.load()
        self.myMenu = menu
        self.images = range(2)
        self.images[0], r = load_image.load_image( os.path.join('MENU', "cursor.png" ), -1)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'inn.bmp'))
        self.storeScreen.fill( colors.black )
        self.storeScreen.blit( self.images[1], (0,0) )
        self.inputHandler = iH
        self.menuBox = pygame.Surface( ( int(ceil(124*2.4)), int(ceil(99*2.4)) ) )
    
    def drawStoreScreen(self):
        #self.myInterface.update()
        storeScreen_ = pygame.transform.scale(self.storeScreen, (720, 720) )
        storeScreen_.blit( self.menuBox, ( int(ceil(165*2.4)),
                                               int(ceil(190*2.4))) )
        self.screen.blit( storeScreen_, (0, 0) )
        pygame.display.flip()
    
    def getAction(self):
        options = ['Buy', 'Save', 'Return To Game', 'Exit Game']
        selection = 0
        while True:
            self.menuBox.fill( colors.gold )
            if pygame.font:
                for i in range(len(options)):
                    self.menuBox.blit( text.Text(options[i], os.getcwd()+"/FONTS/Squealer.ttf", const.shopTextFontSize), ( int(ceil(25*2.4)),
                                                                                                                      i*int(ceil(25*2.4)) ) )
            for event in pygame.event.get():
                event_ = self.inputHandler.getCmd(event)
                if event_ == pygame.K_UP:
                    selection -= 1
                    if selection == -1:
                        selection = len(options)-1
                if event_ == pygame.K_DOWN:
                    selection += 1
                    if selection == len(options):
                        selection = 0
                if event_ == pygame.K_RETURN:
                    return options[selection]
            self.menuBox.blit( self.images[0], (0, selection* int(ceil(25*2.4)) ) )
            self.drawStoreScreen()
    
    def getFile(self, FX):
        #FX.displayLoadingMessage(self.storeScreen, 'Loading saved game list...')
        saveFiles = range(3)
        desc = range(3)
        for i in range(3):
            if os.access("ransack"+str(i)+".sav", os.F_OK):
                peekFile = gzip.GzipFile("ransack"+str(i)+".sav", 'rb')
                ball = cPickle.load(peekFile)
                peekFile.close()
                desc[i] = 'Saved game '+str(i)+' Level '+str(ball[1][11])+' '+str(ball[0].getDays())+' Days '+ \
                                                                                str(ball[0].getHours())+':'+str(ball[0].getHours())+':'+ \
                                                                                str(ball[0].getMins())+'.'+ \
                                                                                str(ball[0].getSecs())
                saveFiles[i] = "ransack"+str(i)+".sav"
            else:
                saveFiles[i] = 'No file'
                desc[i] = 'No file'
        
        saveBox = pygame.Surface( (300,100) )
        selection = 0
        while True:
            saveBox.fill( colors.gold )
            if pygame.font:
                font = pygame.font.Font("./FONTS/gothic.ttf", 14)
                for i in range(3):
                    saveBox.blit( font.render(desc[i], 1, colors.white, colors.gold), (25,i*25) )
            for event in pygame.event.get():
                event_ = self.inputHandler.getCmd(event)
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
            saveBox.blit( self.images[0], (0, selection*25) )
            self.storeScreen.blit( saveBox, (50,200) )
            self.drawStoreScreen()
    
    def save(self, fileName, game, FX):
        if fileName == None:
            return False
        try:
            #FX.displayLoadingMessage(self.storeScreen, 'Saving game...')
            savFile = gzip.GzipFile(fileName, 'wb')
            cPickle.dump(game.getSaveBall(), savFile, 2)
            savFile.close()
            return True
        except IOError, e:
            print 'File I/O error', e
            return False
    
    def load(self, fileN):
        pass
    
    def enterStore(self, hero, game, FX):
        self.storeScreen.blit( self.images[1], (0,0) )
        FX.scrollFromCenter(game.gameBoard, self.storeScreen)
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Return To Game':
                FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                return
            elif action == 'Save':
                #game.gameOn = False
                if self.save( 'ransack0.sav', game, FX):
                    game.textMessage('Game Saved')
                else: game.textMessage('File Error o_O')
                FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                return
            elif action == 'Buy':
                pass
            elif action == 'Load':
                game.gameOn = False
                game.exitCode = 1
                filename = self.getFile()
                self.load( filename )
                game.loadFileName = filename
                FX.scrollFromCenter(self.storeScreen, game.gameBoard)
                return
            elif action == 'Exit Game':
                game.gameOn = False
                game.exitCode = 0
                game.loadFileName = None
                return
            self.drawStoreScreen()