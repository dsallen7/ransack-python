import pygame, random, os
from UTIL import const, colors, load_image, button
from DISPLAY import text, menuBox
from OBJ import item, spell, weapon, armor
from SCRIPTS import armorScr
from IMG import images

from math import ceil, floor

from types import *

menuBoxPositions = [ ( int(ceil(80*const.scaleFactor)), int(ceil(80*const.scaleFactor)) ), 
                     ( int(ceil(115*const.scaleFactor)), int(ceil(80*const.scaleFactor)) ), 
                     ( int(ceil(150*const.scaleFactor)), int(ceil(80*const.scaleFactor)) ), 
                     ( int(ceil(185*const.scaleFactor)), int(ceil(80*const.scaleFactor)) ),
                     ( int(ceil(80*const.scaleFactor)), int(ceil(115*const.scaleFactor)) ), 
                     ( int(ceil(115*const.scaleFactor)), int(ceil(115*const.scaleFactor)) ), 
                     ( int(ceil(150*const.scaleFactor)), int(ceil(115*const.scaleFactor)) ), 
                     ( int(ceil(185*const.scaleFactor)), int(ceil(115*const.scaleFactor)) ) ]
'''
menuBoxPositions = [ ( 0, 0 ), ( 35, 0 ), ( 70, 0 ), ( 105, 0 ),
                     ( 0, 35 ), ( 35, 35), ( 70, 35 ), ( 105, 35 ) ]
menuBoxPositions = [ ( 150, 70 ), ( 185, 70 ), ( 220, 70 ), ( 255, 70 ),
                     ( 150, 105 ), ( 185, 105), ( 220, 105 ), ( 255, 105 ) ]
'''
boxPointsFn = lambda x: ( (x[0],x[1]), 
                          (x[0],x[1] + int(ceil(const.blocksize*const.scaleFactor)) ), 
                          (x[0] + int(ceil(const.blocksize*const.scaleFactor)), x[1]+int(ceil(const.blocksize*const.scaleFactor)) ), 
                          (x[0] + int(ceil(const.blocksize*const.scaleFactor)), x[1]) )

class menu():
    
    def __init__(self, screen, iH, Display, iFace, FX):
        self.images = images.mapImages
        self.statsBox, r = load_image.load_image( os.path.join('MENU', "statsBox.png") )
        self.iMenuBox, r = load_image.load_image( os.path.join('MENU', "invMenu.png" ) )
        self.helpBox, r  = load_image.load_image( os.path.join('MENU', "helpBox.png" ) )
        self.storyBox, r = load_image.load_image( os.path.join('MENU', "storyBox.png") )
        self.equipBox, r = load_image.load_image( os.path.join('MENU', "equipBox.png") )
        self.screen = screen
        self.title = ''
        self.cursorPos = (0,0)
        self.inputHandler = iH
        self.Display = Display
        self.interface = iFace
        self.FX = FX
    
    def openWindow(self, xDim, yDim):
        for i in range(10, (xDim/2), 5):
            borderBox = pygame.Surface( ( i*2, yDim) )
            borderBox.fill( colors.grey )
            msgBox = pygame.Surface( ( (i*2)-10, yDim-10 ) )
            msgBox.fill( colors.gold )
            borderBox.blit(msgBox, (5, 5) )
            borderBox = pygame.transform.scale(borderBox,
                                                (int( ceil(borderBox.get_width()*const.scaleFactor) ),
                                                 int( ceil(borderBox.get_height()*const.scaleFactor) ) ) )
            self.screen.blit(borderBox, 
                             ( (self.screen.get_width()/2)-(borderBox.get_width()/2), 41) )
            #(self.screen.get_width()/2)-(menuWin.get_width()/2)
            self.Display.displayOneFrame(self.interface, self.FX)

        return borderBox
    
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
        
    def itemsWin(self, items):
        #draw available items in window
        # takes: list of actual item class instances
        menu = []
        menuWin = pygame.Surface((120, 60 ))
        availableItems = []
        for i in range( len(items) ):
            item = items[i]
            
            if item in availableItems:
                pass
            else:
                (x, y) = menuBoxPositions[i]
                itemBox = menuBox.menuBox( x, y, item )
                #itemBox.fill( colors.black )
                if hasattr(item, "__iter__"):
                    itemBox.img = images.mapImages[item[0].getImg()].copy()
                else: itemBox.img =  images.mapImages[item.getImg()].copy()
                if pygame.font:
                    font = pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf", 10)
                    if hasattr(item, "__iter__"):
                        if item[0].name in ['item', 'spellbook', 'parchment']:
                            msgText = font.render( 'x'+str( len( item ) ), 1, colors.white, colors.black )
                            itemBox.img.blit(msgText, (17,17) )
                menu.append( itemBox )
                (x, y) = menuBoxPositions[i]
                menuWin.blit(itemBox.img, ( int(floor(x/const.scaleFactor))%150, int(floor(y/const.scaleFactor))%70) )
        return menuWin, menu
    
    def displayChest(self, chest, msg='Chest'):
        menuBox = self.openWindow(200, 120)
        
        menuBox = self.iMenuBox.copy()
        
        font = os.getcwd()+"/FONTS/gothic.ttf"
        size = 14
        
        menuWin = self.iMenuBox.copy()
        
        msgText = text.Text( msg, os.getcwd()+"/FONTS/Squealer.ttf", 18, colors.white, colors.gold )
        availableItems = []
        hPosList = [10]
        for i in chest:
            (type, num) = i         # num can be either an item level or quantity of gold
                                    # mods are the str, itl, dex modifiers of a weapon
            if type in range(const.FRUIT1, const.GOLD):
                availableItems += [ item.Item(type) ]
            elif type == const.GOLD:
                availableItems += [ item.Item(type, num) ]
            elif type in [const.PARCHMENT, const.SPELLBOOK]:
                availableItems += [ item.Item(type, num) ]
            elif type in range(const.WSWORD, const.RING):
                availableItems += [ weapon.Weapon(type, num ) ]
            elif type in range(const.HELMET, const.SSHIELD+1):
                availableItems += [ armor.Armor(type, num) ]
        itemsBox, menu = self.itemsWin(availableItems)
        #menuBox.blit(itemsBox, ( (menuBox.get_width()/2)-(itemsBox.get_width()/2), 60 ) )
        menuBox = pygame.transform.scale( menuBox, 
                                                 (int(ceil(menuBox.get_width() *const.scaleFactor)),
                                                  int(ceil(menuBox.get_height()*const.scaleFactor) ) ) )
        self.screen.blit(menuBox, ( ((self.screen.get_width()/2)-(menuBox.get_width()/2), 41) ) )
        for b in menu:
            self.screen.blit( pygame.transform.scale(b.img, (int(ceil(b.img.get_width()*const.scaleFactor)),
                                                                     int(ceil(b.img.get_height()*const.scaleFactor)) )), 
                                         (b.locX, b.locY) )
        self.screen.blit(msgText, ( (self.screen.get_width()/2)-(msgText.get_width()/2), 
                                     int(ceil(45*const.scaleFactor)) ) )
        self.Display.displayOneFrame(self.interface, self.FX)
        numItems = len(availableItems)
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass
        return availableItems
    
    # Input:  list of items to display in menu, text to display for menu heading
    # Output: player's selection from menu
    def mainMenu(self, hero, calledMenu):
        if calledMenu == 'items':
            pass
        elif calledMenu == 'spell':
            pass
        elif calledMenu == 'stats':
            pass
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
    
    def displayHelp(self):
        helpBox = self.openWindow(350, 300)
        helpBox = self.helpBox.copy()
                
        self.screen.blit(pygame.transform.scale(helpBox, 
                                                ( int(ceil(helpBox.get_width()*const.scaleFactor) ), 
                                                  int(ceil(helpBox.get_height()*const.scaleFactor) )) ), 
                                                ( 0, 41) )
        self.Display.displayOneFrame(self.interface, self.FX)
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass
    
    
    def displayStory(self, msg):
        storyBox = self.openWindow(350, 300)
        storyBox = pygame.transform.scale(self.storyBox.copy(), 
                                                ( int(ceil(self.storyBox.get_width()*const.scaleFactor) ), 
                                                  int(ceil(self.storyBox.get_height()*const.scaleFactor) )) )
        
        msg_ = text.Text(msg, os.getcwd()+"/FONTS/devinne.ttf", 16, colors.white, colors.gold, True, 22)
        storyBox.blit(msg_, ( (storyBox.get_width()/2)-(msg_.get_width()/2), 
                              (storyBox.get_height()/2)-(msg_.get_height()/2)) )
        self.screen.blit( storyBox, ( 0, 41) )
        self.Display.displayOneFrame(self.interface, self.FX)
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass
    
    def getStatsTextLine(self, line):
        graphicElements = []
        for element in line:
            if type(element) == IntType:
                rightmostElement = self.Display.images[element].copy()
                graphicElements.append(rightmostElement)
            elif type(element) == StringType:
                rightmostElement = text.Text(element, 
                                             os.getcwd()+"/FONTS/gothic.ttf", 
                                             10, 
                                             colors.white, 
                                             colors.black,
                                             True,
                                             36 )
                graphicElements.append(rightmostElement)
        w = 0
        h = 0
        for g in graphicElements:
            w += g.get_width()
            if g.get_height() > h:
                h = g.get_height()
        lineSurface = pygame.Surface((w, h))
        w = 0
        for g in graphicElements:
            lineSurface.blit( g, (w, 0) )
            w += g.get_width()
        return lineSurface
    
    def getStatsTextImg(self, hero):
        statsBox = pygame.Surface( ( int(ceil( self.screen.get_width()*0.65) ) ,
                                     int(ceil( self.screen.get_width()*0.5) ) ) )
        stats = hero.getPlayerStats()
        statsList = [ ['Name:'+hero.name],
                      ['HP: '+str(hero.currHP)+'/'+str(hero.maxHP)+' MP: '+str(hero.currMP)+'/'+str(hero.maxMP)],
                      ['Str: '+str(stats[4])+' Int: '+str(stats[6])+' Dex: '+str(stats[5])],
                      [const.ISHIELD,'Armor Class: '+str(hero.armorClass),const.LSWORD,' Weapon Class: '+str(hero.weaponClass)],
                      ['Level: '+str(hero.level)+' Monsters slain: '+str(hero.slain)],
                      ['Faith: ', 245+(hero.faith=='xtian')]
                     ]
        y = 0
        for s in statsList:
            tBox = self.getStatsTextLine(s)
            statsBox.blit( tBox, ( 0, y) )
            y += tBox.get_height()
        return statsBox
    
    def displayHeroStats(self, hero):
        
        statsBox = pygame.Surface((400,400))
        
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf", 14)
        
        for i in range( 0, 255, 8 ):
        
            statsBox = pygame.Surface(( int(ceil( self.screen.get_width()*0.75) ) ,
                                        int(ceil( self.screen.get_width()*0.75) ) ))
            statsBox.fill( colors.grey )
            statsBox.set_alpha( int(ceil(i*0.1)) )
            msgText = text.Text('Hero Stats', os.getcwd()+"/FONTS/Squealer.ttf", 18, colors.white, colors.grey)
            msgText.set_alpha(i)
            
            statsBox.blit(msgText, ( (statsBox.get_width()/2)-(msgText.get_width()/2) ,int(ceil(18*const.scaleFactor))) )
            statsBox.blit(self.getStatsTextImg(hero),  (int(ceil(10*const.scaleFactor)),
                                                        int(ceil(40*const.scaleFactor))) )
            statsBox.blit( pygame.transform.scale(hero.images[8], 
                                                  (int(ceil(const.scaleFactor*hero.images[8].get_width() ) ),
                                                   int(ceil(const.scaleFactor*hero.images[8].get_width() ) ) )), 
                          (25, 30)  )
    
            self.screen.blit( statsBox, ( (self.screen.get_width()/2)-(statsBox.get_width()/2), 41) )
            
            pygame.display.flip()
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass
    
    def drawEquipmentMenu(self, game):
        menu = []
        equipBox = self.equipBox.copy()
        
        font = os.getcwd()+"/FONTS/gothic.ttf"
        size = 8
        #show equipped armor and weapon
        (armor, weapon) = ( game.myHero.getArmorEquipped(), game.myHero.getWeaponEquipped() )
        weaponCopy = pygame.Surface( (30,30) )
        weaponCopy.blit( images.mapImages[ weapon.getImg() ], (0,0) )
        equipBox.blit(weaponCopy, (26, 30))
        menu.append( button.Button( ( int(ceil(26*const.scaleFactor)),
                                      int(ceil(30*const.scaleFactor)) ), 
                    'weapon', 
                    invisible=True ) )
        
        armorLocList = [( 242, 29 ), 
                        ( 31, 202 ), 
                        ( 169, 245 ),
                        ( 31, 112 ),
                        ( 240, 115),
                        (109, 51),
                        (219, 181),
                        (76, 243)]
        armorDescriptions = []
        for A in range( len(armor)-1 ):
            (x, y) = armorLocList[A]
            b = button.Button( ( int(ceil(x*const.scaleFactor)), int(ceil(y*const.scaleFactor)) ), 'armor', invisible=True )
            b.slot = A
            if armor[A] == None:
                menu.append( b )
            else:
                menu.append( b )
                armorCopy = images.mapImages[ armor[A].getImg() ]
                aBox = self.getDescText(armor[A], font, size, 'double')
                armorDescriptions.append( [ aBox,
                                           (int(ceil( (x*const.scaleFactor) - 0.1*aBox.get_width()  )), 
                                            int(ceil( (y+50) * const.scaleFactor)) ) ] )
                #self.writeText(armorCopy, (20,20), 'L'+str(armor[A].getLevel()), colors.white, colors.black,10)
                equipBox.blit(armorCopy, armorLocList[A])
        self.screen.blit(pygame.transform.scale(equipBox, 
                                            ( int(ceil(equipBox.get_width()*const.scaleFactor) ), 
                                              int(ceil(equipBox.get_height()*const.scaleFactor) )) ), 
                                            ( 0, 41) )
        for d in armorDescriptions:
            self.screen.blit( d[0], d[1] )
        self.screen.blit( self.getDescText(weapon, font, size, 'double'), 
                      ( int(ceil(20*const.scaleFactor )), 
                        int(ceil(104*const.scaleFactor)) ) )
        
        self.Display.displayOneFrame(self.interface, self.FX)
        return menu
    def equipmentMenu(self, game):
        equipBox = self.openWindow(350, 300)
        menu = self.drawEquipmentMenu(game)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for b in menu:
                        (x, y) = pygame.mouse.get_pos()
                        #x = int(ceil(const.scaleFactor*x))
                        #y = int(ceil(const.scaleFactor*y))
                        if b.hit(x, y):
                            if b.msg == 'weapon':
                                game.myHero.equipWeapon(self.invMenu(game.myHero.getWeapons(), "Weapons:", ['Equip', 'Return'] ))
                            elif b.msg == 'armor':
                                game.myHero.equipArmor(  self.invMenu( filter(lambda x:armorScr.categories[x.getType()]==armorScr.slotCategories[b.slot], 
                                                                              game.myHero.getArmor() ), 
                                                        "Armor:", ['Equip', 'Return']), b.slot )
                event_ = self.inputHandler.getCmd(event)
                if event_ == pygame.K_ESCAPE:
                    return
                if event_ == pygame.K_RETURN:
                    return
            menu = self.drawEquipmentMenu(game)
    
    def invMenu(self, items, msg, options, prices=None):
        menuWin = self.openWindow(self.iMenuBox.get_width(), 
                                  self.iMenuBox.get_height())
        
        font = os.getcwd()+"/FONTS/gothic.ttf"
        size = 10
        
        menuWin = self.iMenuBox.copy()
        
        msgText = text.Text( msg, os.getcwd()+"/FONTS/Squealer.ttf", 18, colors.white, colors.gold )
        
        #draw available items in window
        itemsBox, menu = self.itemsWin(items)
        menu = menu + [button.Button( (240, 350), options[0],os.getcwd()+"/FONTS/gothic.ttf", 14),
                       button.Button( (380, 350), options[1],os.getcwd()+"/FONTS/gothic.ttf", 14)
                       ]
        if menu is not []:
            selection = menu[0]
            for b in menu:
                self.screen.blit(b.img, (b.locX, b.locY) )
            boxPoints = boxPointsFn( (menu[0].locX-1, menu[0].locY-1) )
        copyWin = menuWin
        while True:
            menuWin = copyWin.copy()
            if selection.type == 'menuBox':
                descText = self.getDescText(selection.item, font, size)
                if prices is not None:
                    priceText = text.Text ( self.getPriceText( selection.item, prices ), font, size, colors.white, colors.gold )
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos()
                    if menu is not []:
                        for b in menu:
                            if b.hit(x, y):
                                if b.type == 'button':
                                    if b.msg == options[0]:
                                        try:
                                            return selection.item
                                        except AttributeError:
                                            return None
                                    elif b.msg == options[1]:
                                        return None
                                elif b.type == 'menuBox':
                                    selection = b
                                    boxPoints = boxPointsFn( (selection.locX-1, selection.locY-1) )
                event_ = self.inputHandler.getCmd(event)
                    
                event_ = self.inputHandler.getCmd(event)
                pygame.draw.lines( itemsBox, colors.black, True, boxPoints, 2 )
                if event_ == pygame.K_ESCAPE:
                    return None
                if event_ == pygame.K_RETURN:
                    if selection.type == 'button':
                        return None
                    else: return selection.item
            menuWin = pygame.transform.scale( menuWin, 
                                                 (int(ceil(menuWin.get_width() *const.scaleFactor)),
                                                  int(ceil(menuWin.get_height()*const.scaleFactor) ) ) )
            self.screen.blit( menuWin, ( (self.screen.get_width()/2)-(menuWin.get_width()/2), 41) )
            self.screen.blit(msgText, ( (self.screen.get_width()/2)-(msgText.get_width()/2), 
                                         int(ceil(45*const.scaleFactor)) ) )
            if selection.type == 'menuBox':
                pygame.draw.lines( self.screen, colors.white, True, boxPoints, 2 )
                self.screen.blit(descText, ( int(ceil(80*const.scaleFactor)), 
                                              int(ceil(165*const.scaleFactor)) ) )
                if prices is not None:
                    self.screen.blit(priceText, ( int(ceil(80*const.scaleFactor)), 
                                                  int(ceil(185*const.scaleFactor)) ) )
            
            if menu is not []:
                for b in menu:
                    if b.type == 'menuBox':
                        self.screen.blit( pygame.transform.scale(b.img, (int(ceil(b.img.get_width()*const.scaleFactor)),
                                                                     int(ceil(b.img.get_height()*const.scaleFactor)) )), 
                                         (b.locX, b.locY) )
            for b in menu:
                if b.type == 'button':
                    self.screen.blit(b.img, (b.locX, b.locY) )
            self.Display.displayOneFrame(self.interface, self.FX)
    
    def getPriceText(self, it, prices):
        if hasattr(it, "__iter__"):
            it = it[0]
        if it.getName() in ['armor', 'weapon']:
            return 'Price: $'+str( prices[it.priceID] )
        elif it.getName() == 'item':
            return 'Price: $'+str( prices[it.getType()] )
        elif it.getName() == 'spellbook' or it.getName() == 'parchment':
            return 'Price: $'+str( prices[(it.getType(), it.getSpellNum() )] )
    
    def getDescText(self, item, font, size, form = 'single'):
        if hasattr(item, "__iter__"):
            item = item[0]
        if item.getName() == 'item' or item.getName() == 'spell':
            return text.Text( item.getDesc(), font, size, colors.white, colors.gold, False, 36  )
        elif item.getName() == 'spellbook' or item.getName() == 'parchment':
            return text.Text( item.getDesc(), font, size, colors.white, colors.gold, False, 36  )
        elif item.getName() == 'armor' or item.getName() == 'weapon':
            dT = text.Text( item.getDesc(), font, size, colors.white, colors.gold, False, 36  )
            sT = text.Text( item.getStats(), font, int(ceil(size*0.75)), colors.white, colors.gold, False, 36  )
            if form == 'single':
                wT = pygame.Surface((int(ceil(dT.get_width()*1.1))+sT.get_width(), dT.get_height()))
                wT.fill(colors.gold)
                wT.blit(dT, (0,0))
                wT.blit(sT, ( int(ceil(dT.get_width()*1.1)), (wT.get_height()/2)-(sT.get_height()/2) ))
            elif form == 'double':
                wT = pygame.Surface(( max( dT.get_width(), sT.get_width()), dT.get_height()+sT.get_height() ))
                wT.fill(colors.gold)
                wT.blit(dT, (0,0) )
                wT.blit(sT, ( 0, dT.get_height() ) )
            return wT