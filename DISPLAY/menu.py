import pygame, random, os
from UTIL import const, colors, load_image, button
from DISPLAY import text, menuBox
from OBJ import item, spell, weapon, armor

from IMG import images

from math import ceil
'''
menuBoxPositions = [ ( int(ceil(150*2.4)), int(ceil(70*2.4)) ), ( int(ceil(185*2.4)), int(ceil(70*2.4)) ), ( int(ceil(220*2.4)), int(ceil(70*2.4)) ), ( int(ceil(255*2.4)), int(ceil(70*2.4)) ),
                     ( int(ceil(150*2.4)), int(ceil(105*2.4)) ), ( int(ceil(185*2.4)), int(ceil(105*2.4)) ), ( int(ceil(220*2.4)), int(ceil(105*2.4)) ), ( int(ceil(255*2.4)), int(ceil(105*2.4)) ) ]
menuBoxPositions = [ ( 0, 0 ), ( 35, 0 ), ( 70, 0 ), ( 105, 0 ),
                     ( 0, 35 ), ( 35, 35), ( 70, 35 ), ( 105, 35 ) ]
'''
menuBoxPositions = [ ( 150, 70 ), ( 185, 70 ), ( 220, 70 ), ( 255, 70 ),
                     ( 150, 105 ), ( 185, 105), ( 220, 105 ), ( 255, 105 ) ]

boxPointsFn = lambda x: ( (x[0],x[1]), 
                          (x[0],x[1] + int(ceil(const.blocksize*2.4)) ), 
                          (x[0] + int(ceil(const.blocksize*2.4)), x[1]+int(ceil(const.blocksize*2.4)) ), 
                          (x[0] + int(ceil(const.blocksize*2.4)), x[1]) )

class menu():
    
    def __init__(self, screen, iH, Display, iFace, FX):
        self.images = images.mapImages
        self.statsBox, r = load_image.load_image("statsBox.bmp")
        self.iMenuBox, r = load_image.load_image("invMenu.bmp")
        self.helpBox, r = load_image.load_image("helpBox.bmp")
        self.storyBox, r = load_image.load_image("storyBox.bmp")
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
                menuWin.blit(itemBox.img, (x%150, y%70) )
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
        itemsBox, availableItems = self.itemsWin(availableItems)
        menuBox.blit(itemsBox, ( (menuBox.get_width()/2)-(itemsBox.get_width()/2), 60 ) )
        menuBox = pygame.transform.scale( menuBox, 
                                                 (int(ceil(menuBox.get_width() *2.4)),
                                                  int(ceil(menuBox.get_height()*2.4) ) ) )
        self.screen.blit(menuBox, ( ((self.screen.get_width()/2)-(menuBox.get_width()/2), 41) ) )
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
        storyBox = self.storyBox.copy()
        
        msg_ = text.Text(msg, os.getcwd()+"/FONTS/devinne.ttf", 8, colors.white, colors.gold, True, 22)
        storyBox.blit(msg_, (25, 25) )
        self.screen.blit(pygame.transform.scale(storyBox, 
                                                ( int(ceil(storyBox.get_width()*2.4) ), 
                                                  int(ceil(storyBox.get_height()*2.4) )) ), 
                                                ( 0, 41) )
        self.Display.displayOneFrame(self.interface, self.FX)
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass
        
    def displayHeroStats(self, hero):
        stats = hero.getPlayerStats()
        
        statsBox = self.openWindow(350, 300)
        statsBox = self.statsBox.copy()
        
        statsBox.blit( hero.images[8], (25, 30)  )
        textBox = pygame.Surface( (200, 200) )
        textBox.fill(colors.black)
        statsBox.blit(textBox, ( statsBox.get_width()/4 ,40) )
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf", 14)
        
        statsBox = pygame.transform.scale(statsBox, 
                                                ( int(ceil(statsBox.get_width()*2.4) ), 
                                                  int(ceil(statsBox.get_height()*2.4) )) )
        
        msgText = text.Text('Hero Stats', os.getcwd()+"/FONTS/Squealer.ttf", 18)
        statsBox.blit(msgText, ( (statsBox.get_width()/2)-(msgText.get_width()/2) ,int(ceil(20*2.4))) )
        statsList = ['Name:'+hero.name,
                     'HP: '+str(hero.currHP)+'/'+str(hero.maxHP),
                     'MP: '+str(hero.currMP)+'/'+str(hero.maxMP),
                     'Str: '+str(stats[4])+' Int: '+str(stats[6])+' Dex: '+str(stats[5]),
                     'Armor: '+str(hero.armorClass),
                     'Level: '+str(hero.level),
                     'Monsters slain: '+str(hero.slain)
                     ]
        y = int(ceil(40*2.4))
        for s in statsList:
            print s
            tBox = text.Text(s, 
                                     os.getcwd()+"/FONTS/gothic.ttf", 
                                     14, 
                                     colors.white, 
                                     colors.black )
            statsBox.blit( tBox, 
                          ( (statsBox.get_width()/4), 
                             y) )
            y += tBox.get_height()
        self.screen.blit( statsBox, ( 0, 41) )
        
        self.Display.displayOneFrame(self.interface, self.FX)
        while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass
    
    def invMenu(self, items, text):
        menuWin = self.openWindow(200, 200)
        
        menuWin = self.iMenuBox.copy()
        
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/Squealer.ttf", 18)
            msgText = font.render( text, 1, colors.white, colors.gold )
            menuWin.blit(msgText, ( (menuWin.get_width()/2)-(msgText.get_width()/2) ,20) )
        
        #draw available items in window
        itemsBox, menu = self.itemsWin(items)
        #menuWin.blit( itemsBox, ((menuWin.get_width()/2)-(itemsBox.get_width()/2), 60) )
        menu = menu + [button.Button( (240, 330), 'Use',os.getcwd()+"/FONTS/gothic.ttf", 14),
                       button.Button( (300, 330), 'Return',os.getcwd()+"/FONTS/gothic.ttf", 14)
                       ]
        if menu is not []:
            selection = menu[0]
            for b in menu:
                self.screen.blit(b.img, (b.locX, b.locY) )
            boxPoints = boxPointsFn( (menu[0].locX, menu[0].locY) )
        copyWin = menuWin
        while True:
            menuWin = copyWin.copy()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos()
                    if menu is not []:
                        for b in menu:
                            if b.hit(x, y):
                                if b.type == 'button':
                                    if b.msg == 'Use':
                                        try:
                                            return selection.item
                                        except AttributeError:
                                            return None
                                    elif b.msg == 'Return':
                                        return None
                                elif b.type == 'menuBox':
                                    print 'MenuBox'
                                    boxPoints = boxPointsFn( (b.locX, b.locY) )
                                    selection = b.item
                event_ = self.inputHandler.getCmd(event)
                pygame.draw.lines( itemsBox, colors.black, True, boxPoints, 1 )
                if event_ == pygame.K_ESCAPE:
                    return None
                if event_ == pygame.K_RETURN:
                    if selection.type == 'button':
                        return None
                    else: return selection.item
            #cursorPos = positions[selection]  
            if menu is not []:
                selection = menu[0]
                for b in menu:
                    self.screen.blit(b.img, (b.locX, b.locY) )
            pygame.draw.lines( itemsBox, colors.white, True, boxPoints, 1 )
            menuWin.blit( itemsBox, ((menuWin.get_width()/2)-(itemsBox.get_width()/2), 60) )
            menuWin = pygame.transform.scale( menuWin, 
                                            ( int(ceil(menuWin.get_width()*2.4) ), 
                                              int(ceil(menuWin.get_height()*2.4) )) )
            self.screen.blit(menuWin, ( self.screen.get_width()/2-menuWin.get_width()/2 , 41) )
            self.Display.displayOneFrame(self.interface, self.FX)
    
    def storeMenu(self, items, text, prices):
        menuWin = self.openWindow(200, 200)
        
        menuWin = self.iMenuBox.copy()
        
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf", 14)
            msgText = font.render( text, 1, colors.white, colors.gold )
            menuWin.blit(msgText, ( (menuWin.get_width()/2)-(msgText.get_width()/2) , 20) )
        
        # wait for selection
        
        itemsBox, menu = self.itemsWin(items)
        menuWin.blit( itemsBox, ((menuWin.get_width()/2)-(itemsBox.get_width()/2), 60) )
        menu = menu + [button.Button( (240, 330), 'Buy',os.getcwd()+"/FONTS/gothic.ttf", 14),
                       button.Button( (300, 330), 'Return',os.getcwd()+"/FONTS/gothic.ttf", 14)
                       ]
        if menu is not []:
            selection = menu[0]
            for b in menu:
                self.screen.blit(b.img, (b.locX, b.locY) )
            boxPoints = boxPointsFn( (menu[0].locX, menu[0].locY) )
        copyBox = menuWin
        
        
        while True:
            menuWin = copyBox.copy()
            descText = font.render( selection.item.getDesc(), 1, colors.white, colors.gold  )
            menuWin.blit(descText, ( (menuWin.get_width()/2)-(descText.get_width()/2) , 135) )
            
            if selection.item.getName() == 'item':
                priceText = font.render( 'Cost: $'+str( prices[selection.item.getType()] ), 1, colors.white, colors.gold )
            elif selection.item.getName() == 'spellbook' or selection.item.getName() == 'parchment':
                priceText = font.render( 'Cost: $'+str( prices[(selection.item.getType(), selection.item.getLevel(), selection.item.getSpellNum() )] ), 1, colors.white, colors.gold )
            elif selection.item.getName() == 'armor':
                priceText = font.render( 'Cost $'+str( prices[(selection.item.getType(), selection.item.getLevel() )] ), 1, colors.white, colors.gold )
            elif selection.item.getName() == 'weapon':
                priceText = font.render( 'Cost $'+str( prices[(selection.item.getType(), selection.item.getLevel() )] ), 1, colors.white, colors.gold )
            menuWin.blit(priceText, ( (menuWin.get_width()/2)-(priceText.get_width()/2) , 155) )
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos()
                    if menu is not []:
                        for b in menu:
                            if b.hit(x, y):
                                if b.type == 'button':
                                    if b.msg == 'Buy':
                                        return selection.item
                                    elif b.msg == 'Return':
                                        return None
                                elif b.type == 'menuBox':
                                    selection = b
                                    boxPoints = boxPointsFn( (selection.locX, selection.locY) )
                event_ = self.inputHandler.getCmd(event)
                #pygame.draw.lines( itemsBox, colors.black, True, boxPoints, 1 )
                if event_ == pygame.K_ESCAPE:
                    return None
                if event_ == pygame.K_RETURN:
                    return selection.item
            #boxPoints = boxPointsFn(cursorPos)
            menuWin.blit( itemsBox, ((menuWin.get_width()/2)-(itemsBox.get_width()/2), 60) )
            menuWin = pygame.transform.scale( menuWin, 
                                                 (int(ceil(menuWin.get_width() *2.4)),
                                                  int(ceil(menuWin.get_height()*2.4) ) ) )
            
            pygame.draw.lines( menuWin, colors.white, True, boxPoints, 1 )
            self.screen.blit( menuWin, ( (self.screen.get_width()/2)-(menuWin.get_width()/2), 41) )
            for b in menu:
                if b.type == 'button':
                    self.screen.blit(b.img, (b.locX, b.locY) )
            self.Display.displayOneFrame(self.interface, self.FX)
