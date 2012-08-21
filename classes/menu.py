import pygame, random, os
from load_image import *
from UTIL import const, colors

from IMG import images

positions = [ (0,0), (35,0), (70,0), (105,0),
               (0,35), (35,35), (70,35), (105,35) ]

boxPointsFn = lambda x: ( (x[0],x[1]), (x[0],x[1]+const.blocksize), (x[0]+const.blocksize, x[1]+const.blocksize), (x[0]+const.blocksize, x[1]) )

class menu():
    
    def __init__(self, screen):
        self.images = images.mapImages
        self.screen = screen
        self.title = ''
        self.cursorPos = (0,0)
    
    def openWindow(self, xDim, yDim):
        for i in range(xDim/2):
            borderBox = pygame.Surface( ( ((i*2)+10 ), yDim) )
            borderBox.fill( colors.grey )
            msgBox = pygame.Surface( ( i*2, yDim-10 ) )
            msgBox.fill( colors.gold )
            borderBox.blit(msgBox, (5, 5) )
            self.screen.blit(borderBox, ( (self.screen.get_size()[0]/2)-i, 100) )
            pygame.display.flip()

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
        
    def menuWin(self, items):
        #draw available items in window
        menuBox = pygame.Surface( (150,70) )
        availableItems = []
        for i in range( len(items) ):
            item = items[i]
            
            if item in availableItems:
                pass
            else:
                itemBox = pygame.Surface( (const.blocksize, const.blocksize) )
                itemBox.fill( colors.black )
                itemBox.blit( images.mapImages[item.getImg()], (0, 0) )
                if pygame.font:
                    font = pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf", 10)
                    if item.name == 'item': 
                        msgText = font.render( 'x'+str(item.qty), 1, colors.white, colors.black )
                        itemBox.blit(msgText, (17,17) )
                    elif item.name == 'magicitem': pass
                    elif item.name == 'spellbook': pass
                    elif item.name == 'parchment': pass
                    else: 
                        msgText = font.render( 'L'+str(item.getLevel()), 1, colors.white, colors.black )
                        itemBox.blit(msgText, (17,17) )
                menuBox.blit( itemBox, positions[i] )
                availableItems.append(item)
        return menuBox, availableItems
    
    def displayChest(self, chest):
        menuBox = self.openWindow(188, 120)
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 14)
            msgText = font.render( 'ChesT', 1, colors.white, colors.gold )
            menuBox.blit(msgText, (10,10) )
        #draw available items in window
        w = 10 #var to draw items across screen
        availableItems = []
        hPosList = [10]
        for item in chest:
            (type, num) = item
            itemBox = pygame.Surface( (const.blocksize, const.blocksize) )
            itemBox.fill( colors.black )
            itemBox.blit( images.mapImages[type+86], (0, 0) )
            if pygame.font:
                font = pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf", 10)
                msgText = font.render( 'x'+str(num), 1, colors.white, colors.black )
                itemBox.blit(msgText, (17,17) )
            menuBox.blit( itemBox, (w, 30) )
            if w not in hPosList:
                hPosList += [w]
            availableItems += [(type, num)]
            w += const.blocksize
        hPos = 10 #horizontal position of selection box
        boxPointsFn = lambda x: ( (x,const.blocksize), (x,2*const.blocksize), (x+const.blocksize, 2*const.blocksize), (x+const.blocksize, const.blocksize) )
        boxPoints = boxPointsFn(hPos)
        pygame.draw.lines( menuBox, colors.white, True, boxPoints, 1 )
        
        self.screen.blit(menuBox, ( (self.screen.get_size()[0]/2)-(188/2), 100) )        
        pygame.display.flip()
        numItems = len(availableItems)
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
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
    
    def displayHeroStats(self, hero):
        stats = hero.getPlayerStats()
        
        statsBox = self.openWindow(200, 130)
        
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 18)
            msgText = font.render( 'Hero STaTs', 1, colors.white, colors.gold )
            statsBox.blit(msgText, ( (statsBox.get_width()/2)-(msgText.get_width()/2) ,10) )
        
        statsBox.blit( hero.images[2], (25, 30)  )
        textBox = pygame.Surface( (125, 75) )
        textBox.fill(colors.black)
        statsBox.blit(textBox, ( statsBox.get_width()/4 ,30) )
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/gothic.ttf", 14)
        statsBox.blit( font.render('Level: '+str(hero.level), 1, colors.white, colors.black ), ( statsBox.get_width()/4 ,30) )
        statsBox.blit( font.render('Str: '+str(stats[4])+' Int: '+str(stats[6])+' Dex: '+str(stats[5]), 1, colors.white, colors.black ), ( statsBox.get_width()/4 ,60) )
        self.screen.blit(statsBox, ( (self.screen.get_width()/2)-(statsBox.get_width()/2), 100) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
    
    def invMenu(self, items, text):
        menuBox = self.openWindow(200, 130)
        
        if pygame.font:
            #print os.getcwd()
            font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 18)
            msgText = font.render( text, 1, colors.white, colors.gold )
            menuBox.blit(msgText, ( (menuBox.get_width()/2)-(msgText.get_width()/2) ,10) )
        
        #draw available items in window
        itemsBox, availableItems = self.menuWin(items)
        menuBox.blit( itemsBox, ((menuBox.get_width()/2)-(itemsBox.get_width()/2), 40) )
        selection = 0
        cursorPos = positions[0]
        boxPoints = boxPointsFn(cursorPos)
        pygame.draw.lines( itemsBox, colors.white, True, boxPoints, 1 )
        
        numItems = len(availableItems)
        font = pygame.font.Font(os.getcwd()+"/FONTS/courier.ttf", 14)
        copyBox = menuBox
        # wait for selection
        while True:
            menuBox = copyBox.copy()
            if numItems >= 1:
                descBox = font.render( availableItems[selection].getDesc(), 1, colors.white, colors.gold )
                menuBox.blit( descBox, ((menuBox.get_width()/2)-(descBox.get_width()/2),30) )
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.draw.lines( itemsBox, colors.black, True, boxPoints, 1 )
                    if event.key == pygame.K_RIGHT:
                        if numItems <= 1:
                            pass
                        elif selection < numItems - 1:
                            selection += 1
                        else:
                            selection = 0
                    if event.key == pygame.K_LEFT:
                        if numItems <= 1:
                            pass
                        elif selection  == 0:
                            selection = numItems - 1
                        else:
                            selection -= 1
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key == pygame.K_RETURN:
                        if availableItems == []: return None
                        else: return availableItems[selection]
            cursorPos = positions[selection]
            boxPoints = boxPointsFn(cursorPos)
            pygame.draw.lines( itemsBox, colors.white, True, boxPoints, 1 )
            menuBox.blit( itemsBox, ((menuBox.get_width()/2)-(itemsBox.get_width()/2), 40) )
            self.screen.blit(menuBox, ( (self.screen.get_size()[0]/2)-(200/2), 100) )  
            pygame.display.flip()
        #while (pygame.event.wait().type != pygame.KEYDOWN): pass

    def storeMenu(self, items, text, prices):
        menuBox = self.openWindow(200, 130)
        
        if pygame.font:
            font = pygame.font.Font(os.getcwd()+"/FONTS/courier.ttf", 14)
            msgText = font.render( text, 1, colors.white, colors.gold )
            menuBox.blit(msgText, ( (menuBox.get_width()/2)-(msgText.get_width()/2) ,10) )
        
        #draw available items in window
        itemsBox, availableItems = self.menuWin(items)
        #menuBox.blit( itemsBox, ((menuBox.get_width()/2)-(menuBox.get_width()/2), 50) )
        selection = 0
        cursorPos = positions[0]
        boxPoints = boxPointsFn(cursorPos)
        pygame.draw.lines( itemsBox, colors.white, True, boxPoints, 1 )
        
        self.screen.blit(menuBox, ( (self.screen.get_size()[0]/2)-(200/2), 100) )    
        pygame.display.flip()
        numItems = len(availableItems)
        copyBox = menuBox
        # wait for selection
        while True:
            menuBox = copyBox.copy()
            if availableItems[selection].getName() == 'item':
                priceText = font.render( availableItems[selection].getDesc()+' $'+str( prices[availableItems[selection].getType()] ), 1, colors.white, colors.gold )
            elif availableItems[selection].getName() == 'spellbook' or availableItems[selection].getName() == 'parchment':
                priceText = font.render( availableItems[selection].getDesc()+' $'+str( prices[(availableItems[selection].getType(), availableItems[selection].getLevel(), availableItems[selection].getSpellNum() )] ), 1, colors.white, colors.gold )
            elif availableItems[selection].getName() == 'armor' or availableItems[selection].getName() == 'weapon':
                priceText = font.render( availableItems[selection].getDesc()+' $'+str( prices[(availableItems[selection].getType(), availableItems[selection].getLevel() )] ), 1, colors.white, colors.gold )
            menuBox.blit(priceText, ( (menuBox.get_width()/2)-(priceText.get_width()/2) , 20) )
            #menuBox.blit( font.render( availableItems[selection].getDesc(), 1, colors.white, colors.gold ), (35,20) )
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.draw.lines( itemsBox, colors.black, True, boxPoints, 1 )
                    if event.key == pygame.K_RIGHT:
                        if numItems == 0 or numItems == 1:
                            pass
                        elif selection < numItems - 1:
                            selection += 1
                        else:
                            selection = 0
                    if event.key == pygame.K_LEFT:
                        if numItems == 0 or numItems == 1:
                            pass
                        elif selection  == 0:
                            selection = numItems - 1
                        else:
                            selection -= 1
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key == pygame.K_RETURN:
                        if availableItems == []: return None
                        elif availableItems[selection].getName() == 'item': return availableItems[selection].getType()
                        elif availableItems[selection].getName() == 'spellbook': return ( availableItems[selection].getType(), availableItems[selection].getLevel(),availableItems[selection].getSpellNum() )
                        else: return (availableItems[selection].getType(), availableItems[selection].getLevel() )
            cursorPos = positions[selection]
            boxPoints = boxPointsFn(cursorPos)
            pygame.draw.lines( itemsBox, colors.white, True, boxPoints, 1 )
            menuBox.blit( itemsBox, ((menuBox.get_width()/2)-(itemsBox.get_width()/2), 50) )
            self.screen.blit(menuBox, ( (self.screen.get_size()[0]/2)-(200/2), 100) )  
            pygame.display.flip()
        #while (pygame.event.wait().type != pygame.KEYDOWN): pass
