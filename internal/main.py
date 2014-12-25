#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
ransack-python

Ransack - a Python based roguelike
'''
import pygame
import random
import gzip
import cPickle
import os

from classes import game
from UTIL import const, colors, load_image, inputHandler, button
from DISPLAY import interface, effects, menu, display, text
from HERO import creator
from OBJ import weapon

from UTIL import const, inputHandler

from math import ceil, floor
from SND import sfx
from IMG import images


try:
    import android
    import android.mixer as mixer
except ImportError as err:
    print ("in main: {}".format(err))
    android = False
    const.setScaleFactor(1)
    pygame.mixer.init()
    mixer = pygame.mixer

# Set the height and width of the screen
cfac = 1.0
screenSize = [720, 700]
screen = pygame.display.set_mode(screenSize)

if not pygame.font:
    print ('Warning, fonts disabled')

pygame.display.set_caption("Ransack")

pygame.init()
pygame.key.set_repeat(100, 100)
clock = pygame.time.Clock()
random.seed(os.urandom(1))

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

FX = effects.effects(clock, screen)
SFX = sfx.sfx(mixer)
C = creator.Creator()
iH = inputHandler.inputHandler(FX)
iFace = interface.Interface(screen, iH)
images.load()
D = display.Display(screen, images)

# this is the static game world i.e. non-generated world
# loaded once at startup and used thereafter
myWorldBall = None

selection = 0
options = ['Begin New Game', 'Load Saved Game', 'Credits', 'Exit']
buttons = []

if pygame.font:
    font = pygame.font.Font("./FONTS/chancery.ttf", 60)
y = 350
for o in options:
    line = font.render(o, 1, colors.white, colors.black)
    buttons.append(button.Button(((
        screen.get_width() / 2) - (line.get_width() / 2), y), o))
    y += 75

ifaceImg, r = load_image.load_image(os.path.join('MENU', 'interface_m.png'),
                                    None)
logo, r = load_image.load_image('logo.png', None)


def endScreen(game, msg):
    spi = os.getcwd()+"/FONTS/SpinalTfanboy.ttf"
    dev = os.getcwd()+"/FONTS/devinne.ttf"
    got = os.getcwd()+"/FONTS/gothic.ttf"
    dScreen = pygame.Surface((screen.get_width(), screen.get_width()))
    dScreen.fill(colors.black)
    msgText = text.Text(msg, os.getcwd()+"/FONTS/Squealer.ttf", 18,
                        colors.white, colors.gold)
    dScreen.blit(text.Text("Game Over", spi, 72, colors.red, colors.black),
                 (50, 0))
    font = pygame.font.Font("./FONTS/devinne.ttf", 18)
    if game.myHero.level < 4:
        dScreen.blit(text.Text("Nice Try, loser!", dev, 18,
                     colors.white, colors.black), (50, 200))
    elif game.myHero.level >= 4 and game.myHero.level < 10:
        dScreen.blit(text.Text("Not bad... for a beginner!", dev, 18,
                     colors.white, colors.black), (50, 350))
    dScreen.blit(text.Text("Level reached: {}".format(game.myHero.level),
                 got, 18, colors.white, colors.black), (50, 500))
    dScreen.blit(text.Text("{} days, {}:{}.{}".format(
                           game.Ticker.getDays(),
                           game.Ticker.getHours() % 24,
                           game.Ticker.getMins() % 60,
                           game.Ticker.getSecs()),
                           got, 14, colors.white,
                           colors.black), (50, 250))
    '''
    screen.blit(pygame.transform.scale(dScreen, (int(ceil(300 * 2.4)),
                                                 int(ceil(300 * 2.4)))),
                                                 (0, 0) )
                                                 '''
    screen.blit(dScreen, (0, 0))
    pygame.display.flip()
    while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN):
        pass


def launchNewGame(titleScreen):
    print('launchNewGame')
    newGame = game.game(images, screen, clock, iFace, FX, iH, titleScreen, SFX,
                        myWorldBall, loadHero=C.mainLoop(screen))
    FX.fadeOut(0)
    iFace.state = 'game'
    if newGame.mainLoop():
        endScreen(newGame, "You Win!")
    else:
        endScreen(newGame, "Game Over.")
    FX.fadeOut(0)


def loadWorld():
    try:
        if android:
            pass
        loadedWorld = gzip.GzipFile(os.getcwd() + '/MAP/WORLDS/MainWorld',
                                    'rb', 1)
        myWorldBall = cPickle.load(loadedWorld)
        loadedWorld.close()
        # self.installWorldBall(ball, context)
    except IOError as err:
        print('Cannot load world: {}'.format(err))
        return


def loadSavedGame(titleScreen):
    if android:
        android.hide_keyboard()
    try:
        FX.displayLoadingMessage(titleScreen, 'Loading game file...')
        savFile = gzip.GzipFile('ransack0.sav', 'rb', 1)
        FX.displayLoadingMessage(titleScreen, 'Loading saved game...')
        ball = cPickle.load(savFile)
        savFile.close()
        Game = game.game(images, screen, clock, iFace,
                         FX, iH, titleScreen, SFX, myWorldBall,
                         ball[0], ball[1], ball[2], ball[3])
        FX.fadeOut(0)
        iFace.state = 'game'
        if Game.mainLoop():
            endScreen(Game, "You Win!")
        else:
            endScreen(Game, "Game Over.")
        FX.fadeOut(0)
    except IOError as err:
        print ('loadSavedGame error: {}'.format(err))


def mouseHandler(m):
    (mx, my) = pygame.mouse.get_pos()
    if (230 <= mx < 480) and (375 <= my < 430):
        launchNewGame()
    elif (230 <= mx < 480) and (430 <= my < 485):
        loadSavedGame()
    elif (230 <= mx < 300) and (485 <= my < 540):
        os.sys.exit()


def updateDisplay():
    titleScreen = pygame.Surface((screenSize[0], screenSize[1]))
    menuBox = pygame.Surface((300, 300))
    menuBox.fill(colors.black)
    menuBox.set_colorkey(colors.black)
    clock.tick(20)
    screen.fill(colors.black)
    screen.blit(titleScreen, (0, 0))
    screen.blit(logo, ((screen.get_width()/2) - (logo.get_width() / 2), 100))
    if pygame.font:
        font = pygame.font.Font("./FONTS/SpinalTfanboy.ttf", 48)
        for b in buttons:
            screen.blit(b.img, (b.locX, b.locY))
            # line = font.render(options[i], 1, colors.white, colors.black)
            # menuBox.blit(line, (30, (i * line.get_height())))

    # menuBox = pygame.Surface( (450,450) )
    # menuBox.fill( colors.black )
    # menuBox.set_colorkey(colors.black)


def showCredits():
    creditsMenu = menu.menu(screen, iH, D, iFace, FX, SFX)
    creditsMenu.displayStory(
        "Ransack - An RPG Roguelike. All game code, story (if you can call it"
        " that!) and artwork, with the exclusion of fonts, created by"
        " D. Allen. dsallen7@gmail.com Powered by Python - www.python.org"
        " Game engine built with Pygame - pygame.org and ported to Android"
        " using PGS4a - pygame.renpy.org/")
    creditsMenu.displayStory(
        "Fonts used in game: Steelfish, Sqeualer by Ray"" Larabie,"
        " Typodermic Fonts - http://www.dafont.com/ typodermic.d1705 Gothic"
        " and Chancery by URW Software. urwpp.de/")
    creditsMenu.displayStory(
        "I'm a big fan of all the classic roguelikes, and"" cult favorites"
        " like Castle of the Winds and Moraff's World, as well as"
        " Japanese-style RPGs, from Final Fantasy to Suikoden to Pokemon."
        " So, you could call this a melting pot of all my gaming influences.")
    creditsMenu.displayStory(
        "This is a work in progress. I thank you for"" playing and if you"
        " notice any bugs or errors, have any ideas for improvments or"
        " enhancenments please drop me a line!")


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                selection = None
                (mX, mY) = pygame.mouse.get_pos()
                for b in buttons:
                    if b.hit(mX, mY):
                        selection = b.msg
                if selection == 'Begin New Game':
                    print('Begin New Game {}x{}'.format(screenSize[0],
                          screenSize[1]))
                    launchNewGame(pygame.Surface((screenSize[0],
                                  screenSize[1])))
                elif selection == 'Load Saved Game':
                    loadSavedGame(pygame.Surface((screenSize[0],
                                  screenSize[1])))
                elif selection == 'Credits':
                    showCredits()
                elif selection == 'Exit':
                    FX.fadeOut(0)
                    os.sys.exit()
                elif selection is None:
                    pass
        font = pygame.font.Font(os.getcwd()+"/FONTS/courier.ttf", 28)
        if android:
            screen.blit(font.render(str(android.get_dpi()), 1, colors.white,
                        colors.black), (0, 0))
        updateDisplay()
        pygame.display.flip()

if __name__ == '__main__':
    try:
        '''
        if android:
            MW = android.assets.open('WORLDS/MainWorld')
        else:
            MW = open('../assets/WORLDS/MainWorld', 'r')
            '''
        MW = open('../assets/WORLDS/MainWorld', 'r')
        loadedWorld = MW
        myWorldBall = cPickle.load(loadedWorld)
        # print myWorldBall
        loadedWorld.close()
    except cPickle.UnpicklingError as err:
        print('Cannot load MainWorld: {}'.format(err))
        os.sys.exit()
    except IOError as err:
        print('Cannot load MainWorld: {}'.format(err))
        os.sys.exit()
    main()
