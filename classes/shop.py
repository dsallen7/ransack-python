import pygame, os
from DISPLAY import menu, text
import random
from OBJ import armor, weapon, item
from SCRIPTS import shopScr, armorScr, weaponScr, prices
from UTIL import const, colors, load_image, misc

from math import floor, ceil

class Shop():
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.screen = screen
        self.myInterface = interface
        self.myMenu = menu
        self.images = range(2)
        self.images[0], r = load_image.load_image( os.path.join('MENU', "cursor.png" ), -1)
        self.type = type
        self.ticker = ticker
        self.storeScreen.fill( colors.black )
        self.inputHandler = iH
        self.menuBox = pygame.Surface( ( int(ceil(124*const.scaleFactor)), int(ceil(99*const.scaleFactor)) ) )
    
    def drawStoreScreen(self):
        #self.myInterface.update()
        storeScreen_ = pygame.transform.scale(self.storeScreen, (720, 720) )
        storeScreen_.blit( self.menuBox, ( int(ceil(165*const.scaleFactor)),
                                               int(ceil(190*const.scaleFactor))) )
        self.screen.blit( storeScreen_, (0, 0) )
        pygame.display.flip()
        
    def getAction(self):
        options = ['Buy', 'Sell', 'Exit Shop']
        selection = 0
        while True:
            self.menuBox.fill( colors.gold )
            if pygame.font:
                for i in range(3):
                    self.menuBox.blit( text.Text(options[i], os.getcwd()+"/FONTS/Squealer.ttf", const.shopTextFontSize), ( int(ceil(25*const.scaleFactor)),
                                                                                                                      i*int(ceil(25*const.scaleFactor)) ) )
                for event in pygame.event.get():
                    event_ = self.inputHandler.getCmd(event)
                    if event_ == pygame.K_UP:
                        selection -= 1
                        if selection == -1:
                            selection = len(options)-1
                    if event_ == pygame.K_DOWN:
                        selection += 1
                        if selection == len(options):
                            selection = 0
                    if event_ == pygame.K_RETURN:
                        return options[selection]
            self.menuBox.blit( self.images[0], (0, selection* int(ceil(25*const.scaleFactor)) ) )
            self.drawStoreScreen()
    
    def sell(self, items, pD ):
        return self.myMenu.invMenu(items, 'Select item to sell:', ['Sell', 'Return'], pD )
    
    def buy(self, items, pD):
        return self.myMenu.invMenu( items, 'Select item to buy:', ['Buy', 'Return'], pD )
        #return self.myMenu.storeMenu( items, 'Select item to buy:', self.prices)
    
    def enterStore(self, hero, game):
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit Shop':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy(items)
                if purchase == None: pass
                elif hero.takeGold( self.prices[purchase] ):
                    if self.type == 'blacksmith':
                        hero.gainWeapon( purchase[0],purchase[1] )
                    elif self.type == 'armory':
                        hero.gainArmor( purchase[0],purchase[1] )
                    elif self.type == 'itemshop':
                        hero.getItem( (purchase-const.FRUIT1,1) )
                    elif self.type == 'magicshop':
                        hero.getItem( (purchase[0],1), purchase[1], purchase[2] )
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                if self.type == 'blacksmith':
                    sale = self.sell(hero.getWeapons())
                elif self.type == 'itemshop':
                    sale = self.sell(hero.getItems())
                elif self.type == 'armory':
                    sale = self.sell(hero.getArmor())
                if sale == None: pass
                else: 
                    if self.type == 'blacksmith':
                        hero.addGold( self.prices[ (sale.getType(),sale.getLevel()) ]/2 )
                        hero.loseWeapon(sale)
                    elif self.type == 'itemshop':
                        hero.addGold( self.prices[ sale.getType() ]/2 )
                        hero.takeItem(sale.getType())
            self.drawStoreScreen()
            
class Blacksmith(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'blacksmith.bmp') )
        self.storeScreen.blit( self.images[1], (0,0) )
        self.stockedAt = None
    
    def stockStore(self, level):
        itemsList = shopScr.blacksmithShopsByLevel[ level ]
        items = []
        self.wPrices = {}
        for i in range(4):
            cItem = random.choice( itemsList )
            mods = [random.randrange(level, level+2),
                    random.randrange(level, level+2),
                    random.randrange(level, level+2) ]
            W = weapon.Weapon( cItem, mods )
            W.priceID = i
            items.append( W )
            self.wPrices[i] = prices.priceItem(W)
        return items
    
    def enterStore(self, hero, game, level):
        if self.stockedAt == None:
            self.items = self.stockStore( level )
            self.stockedAt = game.Ticker.getCount()
        else:
            count = game.Ticker.getCount()
            if ( self.stockedAt - count ) > 86400: # num. of secs in 1 day
                self.items = self.stockStore( level )
                self.stockedAt = count
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit Shop':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy(self.items, self.wPrices)
                if purchase == None: pass
                elif hero.takeGold( self.prices[ purchase.getType() ] ):
                    hero.gainWeapon( purchase.getType() )
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                sPrices = {}
                hWeapons = hero.getWeapons()
                for i in range( len( hWeapons ) ):
                    hWeapons[i].priceID = i
                    sPrices[i] = prices.priceItem( hWeapons[i] )
                sale = self.sell(hero.getWeapons(), sPrices)
                if sale == None: pass
                else: 
                    hero.addGold( self.prices[ (sale.getType(),sale.getLevel()) ]/2 )
                    hero.loseWeapon(sale)
            self.drawStoreScreen()
            
class Armory(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'armory.bmp'))
        self.storeScreen.blit( self.images[1], (0,0) )
        self.stockedAt = None
    
    def stockStore(self, level):
        itemsList = shopScr.armoriesByLevel[ level ]
        items = []
        self.aPrices = {}
        for i in range(8):
            cItem = random.choice( itemsList )
            if misc.rollDie(level, level+5):
                resist = random.choice( armorScr.resists )
            else: resist = None
            if cItem == const.RING:
                enh = random.choice( shopScr.enhancementsByLevel[level] )
                A = armor.Armor( cItem, resist, (enh, random.randrange(level, level+2)) )
                A.priceID = i
                items.append( A )
            else:
                #items.append( armor.Armor( cItem, resist ) )
                A = armor.Armor( cItem, resist )
                A.priceID = i
                items.append( A )
            self.aPrices[i] = prices.priceItem(A)
        return items
    
    def enterStore(self, hero, game, level):
        if self.stockedAt == None:
            self.items = self.stockStore( level )
            self.stockedAt = game.Ticker.getCount()
        else:
            count = game.Ticker.getCount()
            if ( self.stockedAt - count ) > 86400: # num. of secs in 1 day
                self.items = self.stockStore( level )
                self.stockedAt = count
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit Shop':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy(self.items, self.aPrices)
                if purchase == None: pass
                elif hero.takeGold( self.aPrices[purchase.priceID] ):
                    hero.gainArmor( purchase )
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                sPrices = {}
                hArmor = hero.getArmor()
                for i in range( len( hArmor ) ):
                    hArmor[i].priceID = i
                    sPrices[i] = prices.priceItem( hArmor[i] )/2
                sale = self.sell( hArmor, sPrices)
                if sale == None: pass
                else:
                    hero.addGold( sPrices[ sale.priceID ] )
                    hero.loseArmor(sale)
            self.drawStoreScreen()
            
class itemShop(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'itemshop.bmp'))
        self.storeScreen.blit( self.images[1], (0,0) )
        self.iPrices = prices.itemPrices
        
        
    def enterStore(self, hero, game, level):
        itemsList = shopScr.itemShopsByLevel[ level ]
        items = []
        for i in itemsList:
            items.append( item.Item( i + const.FRUIT1 ) )
        
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit Shop':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy(items, self.iPrices)
                if purchase == None: pass
                elif hero.takeGold( self.iPrices[purchase.getType()] ):
                    hero.getItem( purchase )
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                sPD = {}
                for p in self.iPrices:
                    sPD[p] = self.iPrices[p]/2
                sale = self.sell(hero.getItems(), sPD)
                if sale == None: pass
                else:
                    if hasattr(sale, "__iter__"):
                        sale = sale[0]
                    hero.addGold( self.iPrices[ sale.getType() ]/2 )
                    hero.takeItem( sale )
            self.drawStoreScreen()
            
class magicShop(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'magicshop.bmp'))
        self.storeScreen.blit( self.images[1], (0,0) )
        self.mPrices = prices.magicPrices
            
        
    def enterStore(self, hero, game, level):
        itemsList = shopScr.magicShopsByLevel[ level ]
        items = []
        for i in itemsList:
            items.append( item.Item( i[0], i[1] ) )
        
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit Shop':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy(items, self.mPrices)
                if purchase == None: pass
                elif hero.takeGold( self.mPrices[(purchase.getType(), purchase.getSpellNum() )] ):
                    hero.getItem( purchase )
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                sPD = {}
                for p in self.mPrices:
                    sPD[p] = self.mPrices[p]/2
                sale = self.sell(hero.getItems(), sPD)
                if sale == None: pass
                else:
                    try:
                        if hasattr(sale, "__iter__"):
                            hero.addGold( sPD[ ( sale[0].getType(), sale[0].getSpellNum() ) ] )
                            hero.takeItem(sale[0])
                        else:
                            hero.addGold( sPD[ ( sale.getType(), sale.getSpellNum() ) ] )
                            hero.takeItem(sale)
                    except KeyError:
                        self.myInterface.txtMessage("We don't buy those...", None)
            self.drawStoreScreen()