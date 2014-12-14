import pygame
import math
import os
from pygame.locals import *

import random

from IMG import images
from UTIL import const, colors, load_image, button
from DISPLAY import text
from math import ceil

#import threading
import Queue


class Interface():
    def __init__(self, screen, iH):
        self.textBox1 = pygame.Surface((100, 250))
        self.textBox1.fill(colors.gold)
        self.textBox2 = pygame.Surface((300, 100))
        self.textBox2.fill(colors.gold)
        self.playerkeys = 0

        #for displaying messages or menus
        self.screen = screen
        self.inputHandler = iH
        self.invItems = []

        self.frameBox1, r = load_image.load_image("hudBox1.bmp", None)
        self.frameBox2, r = load_image.load_image("hudBox2.bmp", None)
        self.outerframe, r = load_image.load_image("gamescreen600.bmp", None)

        self.scrollText = [''] * 5

        #self.game = game
        #self.gameBoard = game.gameBoard

        self.On = True

        self.popupWin = None
        self.popupLoc = None
        images.load()

    def writeText(self, surface, loc, text, fgc, bgc, size=14,
            font=os.getcwd() + "/FONTS/gothic.ttf"):
        font = pygame.font.Font(font, size)
        surface.blit(font.render(text, 1, fgc, bgc), loc)

    def boxStat(self, stat, mStat, fgc, bgc, loc):
        (x, y) = loc
        maxBoxWidth = 90
        maxBox = pygame.Surface((90, 11))
        maxBox.fill(bgc)
        #maxBox.set_alpha(192)
        currBoxWidth = int(90 * float(stat) / float(mStat))
        if currBoxWidth > 0:
            currBox = pygame.Surface((currBoxWidth, 11))
            currBox.fill(fgc)
            #currBox.set_alpha(192)
            #self.frameBox1.blit( maxBox, loc )
            self.frameBox1.blit(currBox, loc)
        else:
            pass

    def circleStat(self, stat, fgc, bgc, loc, radius, mStat=20):
        pygame.draw
        (cx, cy) = loc
        tx = cx
        ty = cy - radius
        deg = int(360 * float(stat) / float(mStat))
        rad = math.radians(deg)
        pygame.draw.circle(self.frameBox1, bgc, loc, radius)
        pygame.draw.line(self.frameBox1, fgc, (tx, ty), (cx, cy))
        pygame.draw.line(self.frameBox1, fgc, (cx, cy),
            (cx + radius * math.sin(rad), cy - radius * math.cos(rad)))
        rect = (cx - radius, cy - radius, radius * 2, radius * 2)
        pygame.draw.arc(self.frameBox1, fgc, rect, 0, rad, 1)

    def drawClock(self, x, y, Ticker):
        secs = Ticker.getSecs()
        mins = Ticker.getMins()
        hrs = Ticker.getHours()
        sRad = math.radians(360 * (float(secs) / float(60)))
        mRad = math.radians(360 * (float(mins) / float(60)))
        hRad = math.radians(360 * (float(hrs) / float(12)))
        pygame.draw.line(self.frameBox1, colors.black, (x, y),
            (x + 14 * math.sin(sRad), y - 14 * math.cos(sRad)))
        pygame.draw.line(self.frameBox1, colors.grey, (x, y),
            (x + 12 * math.sin(mRad), y - 12 * math.cos(mRad)), 2)
        pygame.draw.line(self.frameBox1, colors.grey, (x, y),
            (x + 9 * math.sin(hRad), y - 9 * math.cos(hRad)), 2)

    def update( self, game=None ):
        stats = game.myHero.getPlayerStats()
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn) = stats
        (armor, weapon) = (game.myHero.getArmorEquipped(),
                           game.myHero.getWeaponEquipped())
        self.textBox1 = pygame.Surface((100, 75))
        self.textBox1.fill(colors.gold)
        self.frameBox1, r = load_image.load_image("hudBox1.bmp", None)
        #draw stats
        self.boxStat(cHP, mHP, colors.dkred, colors.red, (29, 53))
        self.boxStat(cMP, mMP, colors.dkblue, colors.blue, (29, 73))
        self.boxStat(cEX, nEX, colors.green, colors.dkgreen, (29, 93))
        if game.myHero.isPoisoned:
            self.frameBox1.blit(images.mapImages[122], (30, 111))
        elif game.myHero.isDamned:
            self.frameBox1.blit(images.mapImages[123], (30, 111))
        # ticker
        self.drawClock(106, 159, game.Ticker)
        #show equipped armor and weapon
        weaponCopy = pygame.Surface((30, 30))
        #weaponCopy.blit(images.mapImages[weapon.getImg()], (0, 0))
        self.writeText(weaponCopy, (17, 17), 'L' + str(weapon.getLevel()),
            colors.white, colors.black, 10)
        self.frameBox1.blit(weaponCopy, (30, 180))

        armorLocList = [(90, 180), (30, 220), (90, 220)]
        for A in range(len(armor)):
            if armor[A] is None:
                pass
            else:
                armorCopy = images.mapImages[armor[A].getImg()]
                self.writeText(armorCopy, (20, 20), 'L' + str(
                    armor[A].getLevel()), colors.white, colors.black, 10)
                self.frameBox1.blit(armorCopy, armorLocList[A])
        # gold
        goldBox = pygame.Surface((30, 30))
        goldBox.blit(images.mapImages[const.GOLD], (0, 0))
        self.writeText(goldBox, (5, 17), '$' + str(
            game.myHero.getGold()), colors.white, colors.black, 10)
        self.frameBox1.blit(goldBox, (30, 260))
        # keys
        keyBox = pygame.Surface((30, 30))
        keyBox.blit(images.mapImages[const.KEY], (-5, 0))
        self.writeText(keyBox, (13, 17), 'x' + str(kys),
            colors.white, colors.black, 10)
        self.frameBox1.blit(keyBox, (90, 260))

        if self.popupWin is not None:
            self.frameBox1.blit(self.popupWin, self.popupLoc)
        self.screen.blit(self.outerframe, (0,0) )
        self.screen.blit(self.frameBox1, (const.blocksize * 10 + 75, 75))
        self.screen.blit(self.frameBox2, (75, const.blocksize * 10 + 75))
        self.screen.blit(game.gameBoard, (75, 75))

    def txtMessage(self, msg, game):
        self.textBox2 = pygame.Surface((400, 100))
        self.textBox2.fill(colors.gold)
        self.scrollText[0] = self.scrollText[1]
        self.scrollText[1] = self.scrollText[2]
        self.scrollText[2] = self.scrollText[3]
        self.scrollText[3] = self.scrollText[4]
        self.scrollText[4] = '{}:{}.{} - {}'.format(
            game.Ticker.getHours() % 24,
            game.Ticker.getMins() % 60,
            game.Ticker.getSecs(), msg)
        if pygame.font:
            font = pygame.font.Font(os.getcwd() + "/FONTS/courier.ttf", 12)
            for i in range(5):
                Msg = font.render(self.scrollText[i], 1,
                    colors.white, colors.gold)
                self.textBox2.blit(Msg, (0, 20 * i))
        self.frameBox2.blit(self.textBox2, (25, 25))
        game.gameBoard.blit(self.frameBox2, (0, const.blocksize * 10))
        self.screen.blit(game.gameBoard, (75, 75))
        self.update(game)

    # displays message along with image of face
    def npcMessage(self, message, img):
        #self.SFX.play(3)
        msgText = text.Text(message, os.getcwd()+"/FONTS/devinne.ttf", 18, colors.white, colors.gold, True, 18)
        for i in range( 0, 255, 8 ):
            borderBox = pygame.Surface( ( msgText.get_width()+ int(ceil(img.get_width()*const.scaleFactor))+ int(ceil(20*const.scaleFactor)),
                                          msgText.get_height()+ int(ceil(img.get_width()*const.scaleFactor)) ) )
            borderBox.fill( colors.grey )
            #borderBox.blit(msgText, (int(ceil(50*const.scaleFactor)), int(ceil(10*const.scaleFactor))) )
            borderBox.set_alpha( int(ceil(i*0.1)) )
            msgText.set_alpha(i)
            self.screen.blit( borderBox,
                            ( self.screen.get_width()/2-borderBox.get_width()/2 , 150 ) )
            self.screen.blit( pygame.transform.scale(img,
                                                   (int(ceil(img.get_width()*const.scaleFactor)),
                                                    int(ceil(img.get_width()*const.scaleFactor)) ) ),
                            ( self.screen.get_width()/2-borderBox.get_width()/2 + int(ceil(10*const.scaleFactor)),
                              150 + int(ceil(10*const.scaleFactor))  ) )
            self.screen.blit( msgText,
                            ( (self.screen.get_width()/2-borderBox.get_width()/2)+int(ceil(50*const.scaleFactor)) , 150 ) )
            pygame.display.flip()
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass

    # same as npcMessage but returns yes/no input
    def npcDialog(self, message, img=None):
        #self.SFX.play(3)
        msgText = text.Text(message, os.getcwd()+"/FONTS/devinne.ttf", 18, colors.white, colors.gold, True)
        if img == None:
            borderBox = pygame.Surface( ( msgText.get_width(), msgText.get_height()  ) )
        else:
            borderBox = pygame.Surface( ( msgText.get_width()+ int(ceil(img.get_width()*const.scaleFactor))+ int(ceil(20*const.scaleFactor)),
                                      msgText.get_height()+ int(ceil(img.get_width()*const.scaleFactor)) ) )
        borderBox.fill( colors.grey )
        buttons = [ button.Button( ( (self.screen.get_width()/2-borderBox.get_width()/2)+int(ceil(50*const.scaleFactor)),
                                 150 + msgText.get_height() ),
                                 'Yes' ),
                    button.Button( ( (self.screen.get_width()/2-borderBox.get_width()/2)+int(ceil(50*const.scaleFactor))+(borderBox.get_width()-200),
                                 150 + msgText.get_height() ),
                                 'No' )
                   ]
        for i in range( 0, 255, 8 ):
            #borderBox.blit(msgText, (int(ceil(50*const.scaleFactor)), int(ceil(10*const.scaleFactor))) )
            borderBox.set_alpha( int(ceil(i*0.1)) )
            msgText.set_alpha(i)
            self.screen.blit( borderBox,
                            ( self.screen.get_width()/2-borderBox.get_width()/2 , 150 ) )
            if img is not None:
                self.screen.blit( pygame.transform.scale(img,
                                                       (int(ceil(img.get_width()*const.scaleFactor)),
                                                        int(ceil(img.get_width()*const.scaleFactor)) ) ),
                                ( self.screen.get_width()/2-borderBox.get_width()/2 + int(ceil(10*const.scaleFactor)),
                                  150 + int(ceil(10*const.scaleFactor))  ) )
                self.screen.blit( msgText,
                                ( (self.screen.get_width()/2-borderBox.get_width()/2)+int(ceil(50*const.scaleFactor)) , 150 ) )
            else:
                self.screen.blit( msgText,
                                ( (self.screen.get_width()/2-borderBox.get_width()/2), 150 ) )
            for b in buttons:
                self.screen.blit(b.img, (b.locX, b.locY ) )
            pygame.display.flip()

        while True:
            for e in pygame.event.get():
                e_ = self.inputHandler.getCmd(e)
                if e_ == pygame.K_RETURN:
                    return
                else:
                    (x, y) = pygame.mouse.get_pos()
                    for b in buttons:
                        if b.hit( x, y ):
                            return b.msg

    def boxMessage(self, message):

        msgText = text.Text(message, os.getcwd()+"/FONTS/devinne.ttf", 18, colors.white, colors.gold, True)
        for i in range( 0, 255, 8 ):
            borderBox = pygame.Surface( ( msgText.get_width(), msgText.get_height() ) )
            borderBox.fill( colors.grey )
            borderBox.set_alpha( int(ceil(i*0.1)) )
            msgText.set_alpha(i)
            self.screen.blit( borderBox,
                            ( self.screen.get_width()/2-borderBox.get_width()/2, 150 ) )
            self.screen.blit( msgText,
                            ( self.screen.get_width()/2-borderBox.get_width()/2, 150 ) )
            pygame.display.flip()

        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass

    def addPopup(self, text_display, loc):
        msgText = text.Text(text_display,
            os.getcwd() + "/FONTS/gothic.ttf", 10)
        popupWin = pygame.Surface((msgText.get_width() + 10,
                                   msgText.get_height() + 10))
        popupWin.fill(colors.grey)
        popupWin.blit(msgText, (5, 5))
        self.popupWin = popupWin
        (lx, ly) = loc
        lx = lx - popupWin.get_width()
        ly = ly - popupWin.get_height()
        self.popupLoc = (lx, ly)
        pygame.display.flip()

    def mouseHandler(self, event, mx, my):
        if event.type == pygame.MOUSEBUTTONUP:
            self.popupWin = None
            self.popupLoc = None
        else:
            if (30 < mx <= 59) and (111 < my <= 140):
                pass
            elif (90 < mx <= 119) and (111 < my <= 140):
                pass
            # weapon
            elif (30 < mx <= 59) and (180 < my <= 209):
                if self.game.myHero.getWeaponEquipped() is not None:
                    self.addPopup(
                        self.game.myHero.getWeaponEquipped().getStats(),
                        (59, 209))
                else:
                    self.addPopup('None equipped', (mx, my))
            # armor
            elif (90 < mx <= 119) and (180 < my <= 209):
                if self.game.myHero.getArmorEquipped()[0] is not None:
                    self.addPopup(
                        self.game.myHero.getArmorEquipped()[0].getStats(),
                        (119, 209))
                else:
                    self.addPopup('None equipped', (119, 209))
            elif (30 < mx <= 59) and (220 < my <= 249):
                if self.game.myHero.getArmorEquipped()[1] is not None:
                    self.addPopup(
                        self.game.myHero.getArmorEquipped()[1].getStats(),
                        (59, 249))
                else:
                    self.addPopup('None equipped', (59, 249))
            elif (90 < mx <= 119) and (220 < my <= 249):
                if self.game.myHero.getArmorEquipped()[2] is not None:
                    self.addPopup(
                        self.game.myHero.getArmorEquipped()[2].getStats(),
                        (119, 249))
                else:
                    self.addPopup('None equipped', (119, 249))
                pass
            # gold
            elif (30 < mx <= 59) and (260 < my <= 289):
                pass
            # keys
            elif (90 < mx <= 119) and (260 < my <= 289):
                pass
