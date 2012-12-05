import pygame, random, os
from UTIL import const, colors, load_image, button
from DISPLAY import text, menuBox
from OBJ import item, spell, weapon, armor

from IMG import images

from math import ceil, floor

menuBoxPositions = [ ( int(ceil(80*2.4)), int(ceil(80*2.4)) ), 
                     ( int(ceil(115*2.4)), int(ceil(80*2.4)) ), 
                     ( int(ceil(150*2.4)), int(ceil(80*2.4)) ), 
                     ( int(ceil(185*2.4)), int(ceil(80*2.4)) ),
                     ( int(ceil(80*2.4)), int(ceil(115*2.4)) ), 
                     ( int(ceil(115*2.4)), int(ceil(115*2.4)) ), 
                     ( int(ceil(150*2.4)), int(ceil(115*2.4)) ), 
                     ( int(ceil(185*2.4)), int(ceil(115*2.4)) ) ]
'''
menuBoxPositions = [ ( 0, 0 ), ( 35, 0 ), ( 70, 0 ), ( 105, 0 ),
                     ( 0, 35 ), ( 35, 35), ( 70, 35 ), ( 105, 35 ) ]
menuBoxPositions = [ ( 150, 70 ), ( 185, 70 ), ( 220, 70 ), ( 255, 70 ),
                     ( 150, 105 ), ( 185, 105), ( 220, 105 ), ( 255, 105 ) ]
'''
boxPointsFn = lambda x: ( (x[0],x[1]), 
                          (x[0],x[1] + int(ceil(const.blocksize*2.4)) ), 
                          (x[0] + int(ceil(const.blocksize*2.4)), x[1]+int(ceil(const.blocksize*2.4)) ), 
                          (x[0] + int(ceil(const.blocksize*2.4)), x[1]) )

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
        for i in range(10, (xDim/2)+1, 5):
            borderBox = pygame.Surface( ( i*2, yDim) )
            borderBox.fill( colors.grey )
            msgBox = pygame.Surface( ( (i*2)-10, yDim-10 ) )
            msgBox.fill( colors.gold )
            borderBox.blit(msgBox, (5, 5) )
            borderBox = pygame.transform.scale(borderBox,
                                                (int( ceil(borderBox.get_width()*2.4) ),
                                                 int( ceil(borderBox.get_height()*2.4) ) ) )
            self.screen.blit(borderBox, 
                             ( (self.screen.get_width()/2)-(2*i)-20, 41) )
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
                            pass 
                            #msgText = font.render( 'x'+str(item[0].qty), 1, colors.white, colors.black )
                            #itemBox.blit(msgText, (17,17) )
                        else:
                            msgText = font.render( 'L'+str(item[0].getLevel()), 1, colors.white, colors.black )
                            itemBox.img.blit(msgText, (17,17) )
                    else:
                        if item.name in ['item', 'spellbook', 'parchment']:
                            pass
                            #msgText = font.render( 'x'+str(item.qty), 1, colors.white, colors.black )
                            #itemBox.blit(msgText, (17,17) )
                        else: 
                            msgText = font.render( 'L'+str(item.getLevel()), 1, colors.white, colors.black )
                            itemBox.img.blit(msgText, (17,17) )
                menu.append( itemBox )
                (x, y) = menuBoxPositions[i]
                menuWin.blit(itemBox.img, ( int(floor(x/2.4))%150, int(floor(y/2.4))%70) )
        return menuWin, menu
    
    def displayChest(self, chest):
        menuBox = self.openWindow(200, 120)
        
        menuBox = self.iMenuBox.copy()
        
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/Squealer.ttf", 18)
            msgText = font.render( 'Chest', 1, colors.white, colors.gold )
            menuBox.blit(msgText, ( (menuBox.get_width()/2)-(msgText.get_width()/2) ,20) )
        availableItems = []
        hPosList = [10]
        for i in chest:
            if len(i) == 2:
                (type, num) = i         # num can be either an item level or quantity of gold
            else: (type, num, mods) = i # mods are the str, itl, dex modifiers of a weapon
            if type in range(13):
                availableItems += [ item.Item(type+const.FRUIT1) ]
            elif type == 13:
                availableItems += [ item.Item(type+const.FRUIT1, num) ]
            elif type in [14, 15]:
                availableItems += [ item.Item(type+const.FRUIT1, None, num) ]
            elif type in range(26,29):
                availableItems += [ weapon.Weapon(type, num, mods ) ]
            elif type in range(31,34):
                availableItems += [ armor.Armor(type, num) ]
        itemsBox, menu = self.itemsWin(availableItems)
        #menuBox.blit(itemsBox, ( (menuBox.get_width()/2)-(itemsBox.get_width()/2), 60 ) )
        menuBox = pygame.transform.scale( menuBox, 
                                                 (int(ceil(menuBox.get_width() *2.4)),
                                                  int(ceil(menuBox.get_height()*2.4) ) ) )
        self.screen.blit(menuBox, ( ((self.screen.get_width()/2)-(menuBox.get_width()/2), 41) ) )
        for b in menu:
            self.screen.blit( pygame.transform.scale(b.img, (int(ceil(b.img.get_width()*2.4)),
                                                                     int(ceil(b.img.get_height()*2.4)) )), 
                                         (b.locX, b.locY) )
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
                                                ( int(ceil(helpBox.get_width()*2.4) ), 
                                                  int(ceil(helpBox.get_height()*2.4) )) ), 
                                                ( 0, 41) )
        self.Display.displayOneFrame(self.interface, self.FX)
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass
    
    
    def displayStory(self, msg):
        storyBox = self.openWindow(350, 300)
        storyBox = pygame.transform.scale(self.storyBox.copy(), 
                                                ( int(ceil(self.storyBox.get_width()*2.4) ), 
                                                  int(ceil(self.storyBox.get_height()*2.4) )) )
        
        msg_ = text.Text(msg, os.getcwd()+"/FONTS/devinne.ttf", 16, colors.white, colors.gold, True, 22)
        storyBox.blit(msg_, ( (storyBox.get_width()/2)-(msg_.get_width()/2), 
                              (storyBox.get_height()/2)-(msg_.get_height()/2)) )
        self.screen.blit( storyBox, ( 0, 41) )
        self.Display.displayOneFrame(self.interface, self.FX)
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass
    
    def getStatsTextImg(self, hero):
        statsBox = pygame.Surface( ( int(ceil( self.screen.get_width()*0.65) ) ,
                                     int(ceil( self.screen.get_width()*0.5) ) ) )
        stats = hero.getPlayerStats()
        statsList = ['Name:'+hero.name,
                     'HP: '+str(hero.currHP)+'/'+str(hero.maxHP),
                     'MP: '+str(hero.currMP)+'/'+str(hero.maxMP),
                     'Str: '+str(stats[4])+' Int: '+str(stats[6])+' Dex: '+str(stats[5]),
                     'Armor: '+str(hero.armorClass),
                     'Level: '+str(hero.level),
                     'Monsters slain: '+str(hero.slain)
                     ]
        y = 0
        for s in statsList:
            tBox = text.Text(s, 
                             os.getcwd()+"/FONTS/gothic.ttf", 
                             14, 
                             colors.white, 
                             colors.black )
            statsBox.blit( tBox, 
                          ( (statsBox.get_width()/4), 
                             y) )
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
            
#            statsBox = pygame.transform.scale(statsBox, 
#                                                    ( int(ceil(statsBox.get_width()*2.4) ), 
#                                                      int(ceil(statsBox.get_height()*2.4) )) )
            
            statsBox.blit(msgText, ( (statsBox.get_width()/2)-(msgText.get_width()/2) ,int(ceil(20*2.4))) )
            statsBox.blit(self.getStatsTextImg(hero),  (int(ceil(10*2.4)),
                                                        int(ceil(40*2.4))) )
            statsBox.blit( hero.images[8], (25, 30)  )
    
            self.screen.blit( statsBox, ( (self.screen.get_width()/2)-(statsBox.get_width()/2), 41) )
            
            pygame.display.flip()#self.Display.displayOneFrame(self.interface, self.FX)
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass
    
    def drawEquipmentMenu(self, game):
        menu = []
        equipBox = self.equipBox.copy()
        #show equipped armor and weapon
        (armor, weapon) = ( game.myHero.getArmorEquipped(), game.myHero.getWeaponEquipped() )
        weaponCopy = pygame.Surface( (30,30) )
        weaponCopy.blit( images.mapImages[ weapon.getImg() ], (0,0) )
        weaponCopy.blit( text.Text( 'L'+str(weapon.getLevel() ), 
                                    os.getcwd()+"/FONTS/gothic.ttf", 
                                    4, 
                                    colors.white, 
                                    colors.black, 
                                    True ), 
                        (17,17) )
        equipBox.blit(weaponCopy, (26, 30))
        menu.append( button.Button( ( int(ceil(26*2.4)),
                                      int(ceil(30*2.4)) ), 
                    'weapon', 
                    invisible=True ) )
        
        armorLocList = [( 202, 30 ), 
                        ( 31, 202 ), 
                        ( 203, 202 )]
        armorDescriptions = []
        for A in range( len(armor) ):
            (x, y) = armorLocList[A]
            if armor[A] == None:
                menu.append( button.Button( ( int(ceil(x*2.4)), int(ceil(y*2.4)) ), 'armor', invisible=True ) )
            else:
                menu.append( button.Button( (int(ceil(x*2.4)), int(ceil(y*2.4))), 'armor', invisible=True ) )
                armorCopy = images.mapImages[ armor[A].getImg() ]
                armorCopy.blit( text.Text( 'L'+str(armor[A].getLevel() ), 
                                           os.getcwd()+"/FONTS/gothic.ttf", 
                                           4, 
                                           colors.white, 
                                           colors.black, 
                                           True ), 
                               (17,17) )
                aBox = text.Text( armor[A].getStats(), 
                                                       os.getcwd()+"/FONTS/gothic.ttf", 
                                                       8, 
                                                       colors.white, 
                                                       colors.gold, 
                                                       True,
                                                       20  )
                armorDescriptions.append( [ aBox,
                                           (int(ceil( (x*2.4) - 0.1*aBox.get_width()  )), 
                                            int(ceil( (y+50) * 2.4)) ) ] )
                #self.writeText(armorCopy, (20,20), 'L'+str(armor[A].getLevel()), colors.white, colors.black,10)
                equipBox.blit(armorCopy, armorLocList[A])
        self.screen.blit(pygame.transform.scale(equipBox, 
                                            ( int(ceil(equipBox.get_width()*2.4) ), 
                                              int(ceil(equipBox.get_height()*2.4) )) ), 
                                            ( 0, 41) )
        for d in armorDescriptions:
            self.screen.blit( d[0], d[1] )
        self.screen.blit( text.Text( weapon.getStats(), 
                                  os.getcwd()+"/FONTS/gothic.ttf", 
                                  8, 
                                  colors.white, 
                                  colors.gold, 
                                  True,
                                  20  ), 
                      ( int(ceil(16*2.4 )), 
                        int(ceil(108*2.4)) ) )
        
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
                        #x = int(ceil(2.4*x))
                        #y = int(ceil(2.4*y))
                        if b.hit(x, y):
                            if b.msg == 'weapon':
                                game.myHero.equipWeapon(self.invMenu(game.myHero.getWeapons(), "Weapons:", ['Equip', 'Return'] ))
                            elif b.msg == 'armor':
                                game.myHero.equipArmor(self.invMenu(game.myHero.getArmor(), "Armor:", ['Equip', 'Return'] ))
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
        size = 14
        
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
            boxPoints = boxPointsFn( (menu[0].locX, menu[0].locY) )
        copyWin = menuWin
        while True:
            menuWin = copyWin.copy()
            if selection.type == 'menuBox':
                descText = text.Text( self.getDescText(selection.item), font, size, colors.white, colors.gold, False, 28  )
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
                pygame.draw.lines( itemsBox, colors.black, True, boxPoints, 1 )
                if event_ == pygame.K_ESCAPE:
                    return None
                if event_ == pygame.K_RETURN:
                    if selection.type == 'button':
                        return None
                    else: return selection.item
            menuWin = pygame.transform.scale( menuWin, 
                                                 (int(ceil(menuWin.get_width() *2.4)),
                                                  int(ceil(menuWin.get_height()*2.4) ) ) )
            self.screen.blit( menuWin, ( (self.screen.get_width()/2)-(menuWin.get_width()/2), 41) )
            self.screen.blit(msgText, ( (self.screen.get_width()/2)-(msgText.get_width()/2), 
                                         int(ceil(50*2.4)) ) )
            if selection.type == 'menuBox':
                pygame.draw.lines( self.screen, colors.white, True, boxPoints, 1 )
                self.screen.blit(descText, ( int(ceil(80*2.4)), 
                                              int(ceil(165*2.4)) ) )
                if prices is not None:
                    self.screen.blit(priceText, ( int(ceil(80*2.4)), 
                                                  int(ceil(185*2.4)) ) )
            
            if menu is not []:
                for b in menu:
                    if b.type == 'menuBox':
                        self.screen.blit( pygame.transform.scale(b.img, (int(ceil(b.img.get_width()*2.4)),
                                                                     int(ceil(b.img.get_height()*2.4)) )), 
                                         (b.locX, b.locY) )
            for b in menu:
                if b.type == 'button':
                    self.screen.blit(b.img, (b.locX, b.locY) )
            self.Display.displayOneFrame(self.interface, self.FX)
    
    def getPriceText(self, item, prices):
        if item.getName() in ['item', 'armor', 'weapon']:
            return 'Price: $'+str( prices[item.getType()] )
        elif item.getName() == 'spellbook' or item.getName() == 'parchment':
            return 'Price: $'+str( prices[(item.getType(), item.getLevel(), item.getSpellNum() )] )
    
    def getDescText(self, item):
        if item.getName() == 'item' or item.getName() == 'spell':
            return item.getDesc()
        elif item.getName() == 'spellbook' or item.getName() == 'parchment':
            return item.getDesc()
        elif item.getName() == 'armor' or item.getName() == 'weapon':
            return item.getStats()