import pygame, pickle
from load_image import *
from const import *
from classes import menu
from IMG import images
import random, os
from OBJ import item
from SCRIPTS import shopScr


class Tavern():
    
    def __init__(self, screen, hud, ticker):
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.screen = screen
        self.myHud = hud
        self.ticker = ticker
        images.load()
        self.myMenu = menu.menu(screen)
        self.images = range(2)
        self.images[0], r = load_image('cursor.bmp')
        self.images[1], r = load_image('inn.bmp')
        self.storeScreen.fill( black )
        self.storeScreen.blit( self.images[1], (0,0) )
    
    def drawStoreScreen(self):
        self.myHud.update()
        self.screen.blit( self.storeScreen, (75,75) )
        pygame.display.flip()
    
    def getAction(self):
        menuBox = pygame.Surface( (124,99) )
        options = ['Save', 'Load', 'ReTurn To Game', 'ExiT To Main Menu']
        selection = 0
        while True:
            menuBox.fill( gold )
            if pygame.font:
                font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 18)
                for i in range(len(options)):
                    menuBox.blit( font.render(options[i], 1, white, gold), (25,i*25) )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection -= 1
                        if selection == -1:
                            selection = len(options)-1
                    if event.key == pygame.K_DOWN:
                        selection += 1
                        if selection == len(options):
                            selection = 0
                    if event.key == pygame.K_RETURN:
                        return options[selection]
            menuBox.blit( self.images[0], (0, selection*25) )            
            self.storeScreen.blit( menuBox, (165,190) )
            self.drawStoreScreen()
    '''
    def getFile(self):
        saveFiles = range(3)
        for i in range(3):
            if os.access("ransack"+str(i)+".sav", os.F_OK):
                saveFiles[i] = "ransack"+str(i)+".sav"
            else: saveFiles[i] = 'No file'
        
        saveBox = pygame.Surface( (150,100) )
        selection = 0
        while True:
            saveBox.fill( gold )
            if pygame.font:
                font = pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf", 18)
                for i in range(3):
                    saveBox.blit( font.render(saveFiles[i], 1, white, gold), (25,i*25) )
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
            saveBox.blit( self.images[0], (0, selection*25) )
            self.storeScreen.blit( saveBox, (50,50) )
            self.drawStoreScreen()'''
    def getFile(self):
        saveFiles = range(3)
        desc = range(3)
        for i in range(3):
            if os.access("ransack"+str(i)+".sav", os.F_OK):
                peekFile = open("ransack"+str(i)+".sav", 'r')
                ball = pickle.load(peekFile)
                peekFile.close()
                desc[i] = 'Saved game '+str(i)+' Level '+str(ball[0][11])+' '+str(ball[2].getDays())+' Days '+ \
                                                                                str(ball[2].getHours())+':'+str(ball[2].getHours())+':'+ \
                                                                                str(ball[2].getMins())+'.'+ \
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
            saveBox.blit( self.images[0], (0, selection*25) )
            self.storeScreen.blit( saveBox, (100,200) )
            self.drawStoreScreen()
    
    def save(self, fileName, game):
        try:
            savFile = open(fileName, 'w')
            pickle.dump(game.getSaveBall(), savFile)
            savFile.close()
        except IOError, e:
            print 'File I/O error', e
    
    def load(self, fileN):
        pass
    
    def enterStore(self, hero, game):
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'ReTurn To Game':
                return
            elif action == 'Save':
                #game.gameOn = False
                self.save( self.getFile(), game )
                return
            elif action == 'Load':
                game.gameOn = False
                game.exitCode = 1
                filename = self.getFile()
                self.load( filename )
                game.loadFileName = filename
                return
            elif action == 'ExiT To Main Menu':
                game.gameOn = False
                game.exitCode = 0
                game.loadFileName = None
                return
            self.drawStoreScreen()