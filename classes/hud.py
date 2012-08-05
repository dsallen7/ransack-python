import pygame, math
from pygame.locals import *
from load_image import *
from const import *
import random

from IMG import images

#import threading
import Queue

class hud( ):
    def __init__(self, screen, game):
        self.textBox1 = pygame.Surface((100, 250))
        self.textBox1.fill( gold )
        self.textBox2 = pygame.Surface((300, 100))
        self.textBox2.fill( gold )
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
        
    def update( self ):
        stats = self.game.myHero.getPlayerStats()
        (cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX) = stats
        (armor, weapon) = ( self.game.myHero.getArmorEquipped(), self.game.myHero.getWeaponEquipped() )
        self.textBox1 = pygame.Surface((100, 75))
        self.textBox1.fill( gold )
        self.frameBox1, r = load_image("hudBox1.bmp",None)
        #draw stats
        self.boxStat(cHP, mHP, dkred, red, (29,53) )
        self.boxStat(cMP, mMP, dkblue, blue, (29,79) )
        self.circleStat(sth, dkred, red, (41,107), 12)
        self.circleStat(itl, grey, ltgrey, (74,107), 12)
        self.circleStat(dex, purple, violet, (107,107), 12)
        self.boxStat(cEX, nEX, green, dkgreen, (29,129) )
        # ticker
        secs = self.game.Ticker.getSecs()
        mins = self.game.Ticker.getMins()
        hrs = self.game.Ticker.getHours()
        sRad = math.radians( 360* ( float(secs)/float(60) ) )
        mRad = math.radians( 360* ( float(mins)/float(60) ) )
        hRad = math.radians( 360* ( float(hrs)/float(60) ) )
        pygame.draw.line(self.frameBox1, black, (106,159), (106+ 14*math.sin( sRad ), 159- 14*math.cos( sRad ) ) )
        pygame.draw.line(self.frameBox1, grey, (106,159), (106+ 12*math.sin( mRad ), 159- 12*math.cos( mRad ) ), 2 )
        pygame.draw.line(self.frameBox1, grey, (106,159), (106+ 9*math.sin( hRad ), 159- 9*math.cos( hRad ) ), 2)
        #show equipped armor and weapon
        weaponCopy = pygame.Surface( (30,30) )
        weaponCopy.blit( images.mapImages[ weapon.getImg() ], (0,0) )
        self.writeText(weaponCopy, (17,17), 'L'+str(weapon.getLevel()), white, black, 10)
        self.frameBox1.blit(weaponCopy, (30, 180))
        
        armorLocList = [(90,180), (30,220), (90,220)]
        for A in range( len(armor) ):
            if armor[A] == None:
                pass
            else:
                armorCopy = images.mapImages[ armor[A].getImg() ]
                self.writeText(armorCopy, (20,20), 'L'+str(armor[A].getLevel()), white, black,10)
                self.frameBox1.blit(armorCopy, armorLocList[A])
        # gold
        goldBox = pygame.Surface( (30,30) )
        goldBox.blit( images.mapImages[GOLD], (0,0) )
        self.writeText(goldBox, (5,17), '$'+str(self.game.myHero.getGold()), white, black,10)
        self.frameBox1.blit( goldBox, (30, 260) )
        # keys
        keyBox = pygame.Surface( (30,30) )
        keyBox.blit( images.mapImages[KEY], (-5,0) )
        self.writeText(keyBox, (13,17), 'x'+str(kys), white, black,10)
        self.frameBox1.blit( keyBox, (90, 260) )
        
        self.screen.blit(self.frameBox1, (blocksize*10+75, 75) )
        self.screen.blit(self.frameBox2, (75, blocksize*10+75) )
        self.screen.blit(self.gameBoard, (75,75) )

    
    def txtMessage(self, msg):
        self.textBox2 = pygame.Surface((400, 100))
        self.textBox2.fill( gold )
        self.scrollText[0] = self.scrollText[1]
        self.scrollText[1] = self.scrollText[2]
        self.scrollText[2] = self.scrollText[3]
        self.scrollText[3] = self.scrollText[4]
        self.scrollText[4] = msg
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf", 18)
            for i in range(5):
                Msg = font.render( self.scrollText[i], 1, white, gold)
                self.textBox2.blit(Msg, (0,20*i) )
        self.frameBox2.blit(self.textBox2, (25,25) )
        self.gameBoard.blit(self.frameBox2, (0, blocksize*10) )
        self.screen.blit(self.gameBoard, (75,75) )
    
   
    def boxMessage(self, text):
        for i in range(88):
            borderBox = pygame.Surface( ( ((i*2)+5 ), 60) )
            borderBox.fill( grey )
            msgBox = pygame.Surface( (i*2, 50 ) )
            msgBox.fill( gold )
            borderBox.blit(msgBox, (5, 5) )
            self.screen.blit(borderBox, (188-i, 200) )
            pygame.display.flip()
            
        borderBox = pygame.Surface( ( 186, 60 ) )
        borderBox.fill( grey )
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 18)
            msgText = font.render( text, 1, white, gold )
            msgBox.blit(msgText, (10,10) )
        borderBox.blit( msgBox, (5, 5) )
        self.screen.blit(borderBox, (100, 200) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass