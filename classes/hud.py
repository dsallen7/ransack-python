import pygame, math
from pygame.locals import *
from load_image import *
import random

from IMG import images

from UTIL import const, colors

#import threading
import Queue

class hud( ):
    def __init__(self, screen, game):
        self.textBox1 = pygame.Surface((100, 250))
        self.textBox1.fill( colors.gold )
        self.textBox2 = pygame.Surface((300, 100))
        self.textBox2.fill( colors.gold )
        self.playerkeys = 0
        
        #for displaying messages or menus
        self.screen = screen
        
        self.invItems = []
        
        self.frameBox1, r = load_image("hudBox1.bmp",None)
        self.frameBox2, r = load_image("hudBox2.bmp",None)
        
        self.scrollText = ['']*5
        
        self.game = game
        self.gameBoard = game.gameBoard
        
        self.On = True
        
        self.popupWin = None
        self.popupLoc = None
        
        images.load()
    
    def writeText(self, surface, loc, text, fgc, bgc, size=14, font=os.getcwd()+"/FONTS/gothic.ttf"):
        font = pygame.font.Font(font, size)
        surface.blit( font.render(text, 1, fgc, bgc), loc )
    # Draw an arc that is a portion of a circle.
    # We pass in screen and color,
    # followed by a tuple (x,y) that is the center of the circle, and the radius.
    # Next comes the start and ending angle on the "unit circle" (0 to 360)
    #  of the circle we want to draw, and finally the thickness in pixels

    def boxStat(self, stat, mStat, fgc, bgc, loc):
        (x, y) = loc
        maxBoxWidth = 90
        maxBox = pygame.Surface( (90, 11) )
        maxBox.fill(bgc)
        maxBox.set_alpha(128)
        currBoxWidth = int(90 * float(stat)/float(mStat))
        if currBoxWidth > 0:
            currBox = pygame.Surface( (currBoxWidth, 11) )
            currBox.fill(fgc)
            currBox.set_alpha(128)
            #self.frameBox1.blit( maxBox, loc )
            self.frameBox1.blit( currBox, loc )
        else: pass
    
    def circleStat(self, stat, fgc, bgc, loc, radius, mStat=20):
        pygame.draw
        (cx,cy) = loc
        tx = cx
        ty = cy - radius
        deg = int(360 * float(stat)/float(mStat))
        rad = math.radians(deg)
        pygame.draw.circle(self.frameBox1, bgc, loc, radius)
        pygame.draw.line(self.frameBox1, fgc, (tx,ty), (cx,cy))
        pygame.draw.line(self.frameBox1, fgc, (cx,cy), (cx+ radius*math.sin( rad ), cy- radius*math.cos( rad ) ) )
        rect = (cx-radius,cy-radius,radius*2,radius*2)
        pygame.draw.arc(self.frameBox1,fgc,rect,0,rad,1)
    
    def drawClock(self, x, y):
        secs = self.game.Ticker.getSecs()
        mins = self.game.Ticker.getMins()
        hrs = self.game.Ticker.getHours()
        sRad = math.radians( 360* ( float(secs)/float(60) ) )
        mRad = math.radians( 360* ( float(mins)/float(60) ) )
        hRad = math.radians( 360* ( float(hrs)/float(12) ) )
        pygame.draw.line(self.frameBox1, colors.black, (x,y), (x+ 14*math.sin( sRad ), y- 14*math.cos( sRad ) ) )
        pygame.draw.line(self.frameBox1, colors.grey, (x,y), (x+ 12*math.sin( mRad ), y- 12*math.cos( mRad ) ), 2 )
        pygame.draw.line(self.frameBox1, colors.grey, (x,y), (x+ 9*math.sin( hRad ), y- 9*math.cos( hRad ) ), 2)
        
    def update( self ):
        stats = self.game.myHero.getPlayerStats()
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn) = stats
        (armor, weapon) = ( self.game.myHero.getArmorEquipped(), self.game.myHero.getWeaponEquipped() )
        self.textBox1 = pygame.Surface((100, 75))
        self.textBox1.fill( colors.gold )
        self.frameBox1, r = load_image("hudBox1.bmp",None)
        #draw stats
        self.boxStat(cHP, mHP, colors.dkred, colors.red, (29,53) )
        self.boxStat(cMP, mMP, colors.dkblue, colors.blue, (29,73) )
        #self.circleStat(sth, dkred, red, (41,107), 12)
        #self.circleStat(itl, grey, ltgrey, (74,107), 12)
        #self.circleStat(dex, purple, violet, (107,107), 12)
        self.boxStat(cEX, nEX, colors.green, colors.dkgreen, (29,93) )
        if self.game.myHero.isPoisoned:
            self.frameBox1.blit(images.mapImages[122], (30,111))
        # ticker
        self.drawClock(106, 159)
        #show equipped armor and weapon
        weaponCopy = pygame.Surface( (30,30) )
        weaponCopy.blit( images.mapImages[ weapon.getImg() ], (0,0) )
        self.writeText(weaponCopy, (17,17), 'L'+str(weapon.getLevel()), colors.white, colors.black, 10)
        self.frameBox1.blit(weaponCopy, (30, 180))
        
        armorLocList = [(90,180), (30,220), (90,220)]
        for A in range( len(armor) ):
            if armor[A] == None:
                pass
            else:
                armorCopy = images.mapImages[ armor[A].getImg() ]
                self.writeText(armorCopy, (20,20), 'L'+str(armor[A].getLevel()), colors.white, colors.black,10)
                self.frameBox1.blit(armorCopy, armorLocList[A])
        # gold
        goldBox = pygame.Surface( (30,30) )
        goldBox.blit( images.mapImages[const.GOLD], (0,0) )
        self.writeText(goldBox, (5,17), '$'+str(self.game.myHero.getGold()), colors.white, colors.black,10)
        self.frameBox1.blit( goldBox, (30, 260) )
        # keys
        keyBox = pygame.Surface( (30,30) )
        keyBox.blit( images.mapImages[const.KEY], (-5,0) )
        self.writeText(keyBox, (13,17), 'x'+str(kys), colors.white, colors.black,10)
        self.frameBox1.blit( keyBox, (90, 260) )
        
        if self.popupWin is not None:
            self.frameBox1.blit( self.popupWin, self.popupLoc )
        
        self.screen.blit(self.frameBox1, (const.blocksize*10+75, 75) )
        self.screen.blit(self.frameBox2, (75, const.blocksize*10+75) )
        self.screen.blit(self.gameBoard, (75,75) )

    
    def txtMessage(self, msg):
        self.textBox2 = pygame.Surface((400, 100))
        self.textBox2.fill( colors.gold )
        self.scrollText[0] = self.scrollText[1]
        self.scrollText[1] = self.scrollText[2]
        self.scrollText[2] = self.scrollText[3]
        self.scrollText[3] = self.scrollText[4]
        self.scrollText[4] = str(self.game.Ticker.getMins())+'.'+str(self.game.Ticker.getSecs())+' - '+msg
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/courier.ttf", 12)
            for i in range(5):
                Msg = font.render( self.scrollText[i], 1, colors.white, colors.gold)
                self.textBox2.blit(Msg, (0,20*i) )
        self.frameBox2.blit(self.textBox2, (25,25) )
        self.gameBoard.blit(self.frameBox2, (0, const.blocksize*10) )
        self.screen.blit(self.gameBoard, (75,75) )
        self.update()
    
    def getMsgText(self, message, font, fontsize):
        # returns a nicely formatted text box
        if pygame.font:
            font = pygame.font.Font(font, fontsize)
            if len(message) < const.maxLineWidth:
                msgText = pygame.Surface( (len(message)*(fontsize/2), fontsize*2 ) )
                msgText.fill(colors.gold)
                msgText.blit( font.render( message, 1, colors.white, colors.gold ), (0,0) )
            else:
                msgText = pygame.Surface( ( const.maxLineWidth*(fontsize/2), ((len(message)+1)/const.maxLineWidth)*fontsize*2 ))
                msgText.fill(colors.gold)
                hPos = 0
                words = message.split(' ')
                while words:
                    line = ''
                    while words and len(line+' '+words[0]) < const.maxLineWidth:
                        line = line + words[0] + ' '
                        words = words[1:]
                    lineText = font.render( line, 1, colors.white, colors.gold )
                    msgText.blit( lineText, ((msgText.get_width()/2)-(lineText.get_width()/2), hPos) )
                    hPos += fontsize
        return msgText
   
    def npcMessage(self, message, img):
        msgText = self.getMsgText(message, os.getcwd()+"/FONTS/devinne.ttf", 18)
        (px, py, px2, py2) = self.game.myHero.getRect()
        for i in range(msgText.get_width()/2):
            borderBox = pygame.Surface( ( ((i*2)+60 ), msgText.get_height()+20) )
            borderBox.fill( colors.grey )
            borderBox.blit(img, (10,10) )
            borderBox.blit(msgText, (40, 10) )
            self.screen.blit(borderBox, ( const.gameBoardOffset + px + const.blocksize + (msgText.get_width()/2) - i, const.gameBoardOffset + py + const.blocksize ) )
            #self.screen.blit(borderBox, ( (self.screen.get_width()/2)-i, (self.screen.get_height()/2)-(msgText.get_height()/2) ) )
            pygame.display.flip()
            
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
    def boxMessage(self, message):
        msgText = self.getMsgText(message, os.getcwd()+"/FONTS/devinne.ttf", 18)
        (px, py, px2, py2) = self.game.myHero.getRect()
        for i in range(msgText.get_width()/2):
            borderBox = pygame.Surface( ( ((i*2)+20 ), msgText.get_height()+20) )
            borderBox.fill( colors.grey )
            borderBox.blit(msgText, (10, 10) )
            self.screen.blit(borderBox, ( const.gameBoardOffset + px + const.blocksize + (msgText.get_width()/2) - i, const.gameBoardOffset + py + const.blocksize ) )
            #self.screen.blit(borderBox, ( (self.screen.get_width()/2)-i, (self.screen.get_height()/2)-(msgText.get_height()/2) ) )
            pygame.display.flip()
            
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
        
    def addPopup(self, text, loc):
        msgText = self.getMsgText(text, os.getcwd()+"/FONTS/gothic.ttf", 10)
        popupWin = pygame.Surface( (msgText.get_width()+5, msgText.get_height()+5) )
        popupWin.fill(colors.grey)
        popupWin.blit(msgText, (5,5) )
        self.popupWin = popupWin
        self.popupLoc = loc
    
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
                    self.addPopup(self.game.myHero.getWeaponEquipped().getStats(), (59,209)  )
                else: self.addPopup('None equipped', (59,209)  )
            # armor
            elif (90 < mx <= 119) and (180 < my <= 209):
                if self.game.myHero.getArmorEquipped()[0] is not None:
                    self.addPopup(self.game.myHero.getArmorEquipped()[0].getStats(), (119,209)  )
                else: self.addPopup('None equipped', (119,209)  )
            elif (30 < mx <= 59) and (220 < my <= 249):
                if self.game.myHero.getArmorEquipped()[1] is not None:
                    self.addPopup(self.game.myHero.getArmorEquipped()[1].getStats(), (59,249)  )
                else: self.addPopup('None equipped', (59,249)  )
            elif (90 < mx <= 119) and (220 < my <= 249):
                if self.game.myHero.getArmorEquipped()[2] is not None:
                    self.addPopup(self.game.myHero.getArmorEquipped()[2].getStats(), (119,249)  )
                else: self.addPopup('None equipped', (119,249)  )
                pass
            # gold
            elif (30 < mx <= 59) and (260 < my <= 289):
                pass
            # keys
            elif (90 < mx <= 119) and (260 < my <= 289):
                pass