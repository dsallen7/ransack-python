import random
import os
import pygame
import cPickle
import gzip
from load_image import *
from DISPLAY import menu
from IMG import images
from OBJ import item
from SCRIPTS import shopScr

from UTIL import const, colors


class Tavern():

    def __init__(self, screen, interface, ticker, iH, menu):
        self.storeScreen = pygame.Surface((300, 300))
        self.inventory = []
        self.screen = screen
        self.myHud = interface
        self.ticker = ticker
        images.load()
        self.myMenu = menu
        self.images = range(2)
        #self.images[0], r = load_image('cursor.bmp', -1)
        #self.images[1], r = load_image(os.path.join('INT', 'inn.bmp'))
        self.storeScreen.fill(colors.black)
        #self.storeScreen.blit(self.images[1], (0, 0))

    def drawStoreScreen(self):
        self.myHud.update()
        self.screen.blit(self.storeScreen, (75, 75))
        pygame.display.flip()

    def getAction(self):
        menuBox = pygame.Surface((124, 99))
        options = ['Save', 'Sleep', 'ReTurn To Game', 'ExiT To Main Menu']
        selection = 0
        while True:
            menuBox.fill(colors.gold)
            if pygame.font:
                font = pygame.font.Font(
                    os.getcwd() + "/FONTS/SpinalTfanboy.ttf", 18)
                for i in range(len(options)):
                    menuBox.blit(font.render(options[i], 1,
                        colors.white, colors.gold), (25, i * 25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection -= 1
                        if selection == -1:
                            selection = len(options) - 1
                    if event.key == pygame.K_DOWN:
                        selection += 1
                        if selection == len(options):
                            selection = 0
                    if event.key == pygame.K_RETURN:
                        return options[selection]
            menuBox.blit(self.images[0], (0, selection * 25))
            self.storeScreen.blit(menuBox, (165, 190))
            self.drawStoreScreen()

    def getFile(self):
        saveFiles = range(3)
        desc = range(3)
        for i in range(3):
            if os.access("ransack" + str(i) + ".sav", os.F_OK):
                peekFile = gzip.GzipFile("ransack" + str(i) + ".sav", 'rb')
                ball = cPickle.load(peekFile)
                peekFile.close()
                desc[i] = 'Saved game ' + str(i) + ' Level ' + \
                    str(ball[1][11]) + ' ' + str(ball[0].getDays()) + \
                    ' Days ' + \
                    str(ball[0].getHours()) + ':' + \
                    str(ball[0].getHours()) + ':' + \
                    str(ball[0].getMins()) + '.' + \
                    str(ball[0].getSecs())
                saveFiles[i] = "ransack" + str(i) + ".sav"
            else:
                saveFiles[i] = 'No file'
                desc[i] = 'No file'

        saveBox = pygame.Surface((300, 100))
        selection = 0
        while True:
            saveBox.fill(colors.gold)
            if pygame.font:
                font = pygame.font.Font("./FONTS/gothic.ttf", 14)
                for i in range(3):
                    saveBox.blit(font.render(desc[i], 1,
                        colors.white, colors.gold), (25, i * 25))
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
                        return "ransack" + str(selection) + ".sav"
                    if event.key == pygame.K_ESCAPE:
                        return None
            saveBox.blit(self.images[0], (0, selection * 25))
            self.storeScreen.blit(saveBox, (100, 200))
            self.drawStoreScreen()

    def save(self, fileName, game):
        if fileName is None:
            return
        try:
            savFile = gzip.GzipFile(fileName, 'wb')
            cPickle.dump(game.getSaveBall(), savFile, 2)
            savFile.close()
        except IOError, e:
            print 'File I/O error', e

    def load(self, fileN):
        pass

    def enterStore(self, hero, game):
        self.storeScreen.blit(self.images[1], (0, 0))
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'ReTurn To Game':
                return
            elif action == 'Save':
                #game.gameOn = False
                self.save(self.getFile(), game)
                return
            elif action == 'Sleep':
                if hero.takeGold((hero.getMaxHP() - hero.getCurrHP()) / 2):
                    self.myHud.txtMessage('Your HP and MP are now full')
                    self.myHud.txtMessage('Thank you for staying with us!')
                    hero.refillPts()
            elif action == 'Load':
                game.gameOn = False
                game.exitCode = 1
                filename = self.getFile()
                self.load(filename)
                game.loadFileName = filename
                return
            elif action == 'ExiT To Main Menu':
                game.gameOn = False
                game.exitCode = 0
                game.loadFileName = None
                return
            self.drawStoreScreen()
