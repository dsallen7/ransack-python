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
                    self.menuBox.blit( text.Text(options[i], 
                                                 os.getcwd()+"/FONTS/Squealer.ttf", 
                                                 const.shopTextFontSize), 
                                      ( int(ceil(25*const.scaleFactor)),
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
    
    def getHeroSaleItems(self, hero):
        if self.name == 'blacksmith':
            return hero.getWeapons()
        elif self.name == 'armory' :
            return hero.getArmor()
        elif self.name == 'itemshop':
            #return hero.getItems()
            return filter( lambda x: x.getType() not in [const.SPELLBOOK, const.PARCHMENT], hero.getItems() )
        elif self.name == 'magicshop':
            return filter( lambda x: x.getType() in [const.SPELLBOOK, const.PARCHMENT], hero.getItems() )
    
    def enterStore(self, hero, game, level):
        if self.name in ['itemshop', 'magicshop']:
            self.stockStore(level)
        else:
            if self.stockedAt == None:
                self.items[level] = self.stockStore( level )
                self.stockedAt = game.Ticker.getCount()
            else:
                count = game.Ticker.getCount()
                if ( self.stockedAt - count ) > 86400: # num. of secs in 1 day
                    self.items[level] = self.stockStore( level )
                    self.stockedAt = count
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit Shop':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy(self.items[level], self.prices[level])
                if purchase == None: pass
                elif hero.takeGold( self.prices[level][purchase.priceID] ):
                    hero.getItem( purchase )
                    if self.name in ['blacksmith', 'armory']:
                        self.items[level].remove(purchase)
                    else:
                        self.stockStore(level)
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                sPrices = {}
                hSaleItems = self.getHeroSaleItems(hero)
                for i in range( len( hSaleItems ) ):
                    hSaleItems[i].priceID = i
                    sPrices[i] = prices.priceItem( hSaleItems[i] )/2
                sale = self.sell( hSaleItems, sPrices)
                if sale == None: pass
                else:
                    hero.addGold( sPrices[ sale.priceID ] )
                    hero.takeItem(sale)
                    if self.name in ['blacksmith', 'armory']:
                        self.items[level].append(sale)
                    else:
                        self.stockStore(level)
            self.drawStoreScreen()
            
class Blacksmith(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'blacksmith.bmp') )
        self.storeScreen.blit( self.images[1], (0,0) )
        self.stockedAt = None
        self.items = range(3)
        self.prices = range(3)
        self.name = 'blacksmith'
    
    def stockStore(self, level):
        itemsList = shopScr.blacksmithShopsByLevel[ level ]
        items = []
        self.prices[level] = {}
        for i in range(4):
            cItem = random.choice( itemsList )
            mods = [random.randrange(level, level+2),
                    random.randrange(level, level+2),
                    random.randrange(level, level+2) ]
            W = weapon.Weapon( cItem, mods )
            W.priceID = i
            items.append( W )
            self.prices[level][i] = prices.priceItem(W)
        return items

class Armory(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'armory.bmp'))
        self.storeScreen.blit( self.images[1], (0,0) )
        self.stockedAt = None
        self.items = range(3)
        self.prices = range(3)
        self.name = 'armory'
    
    def stockStore(self, level):
        itemsList = shopScr.armoriesByLevel[ level ]
        items = []
        self.prices[level] = {}
        for i in range(4):
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
            self.prices[level][i] = prices.priceItem(A)
        return items
            
class itemShop(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'itemshop.bmp'))
        self.storeScreen.blit( self.images[1], (0,0) )
        self.iPrices = prices.itemPrices
        self.name = 'itemshop'
        self.items = range(3)
        self.prices = range(3)
    def stockStore(self, level):
        itemsList = shopScr.itemShopsByLevel[ level ]
        self.items[level] = []
        self.prices[level] = {}
        for i in itemsList:
            iT = item.Item( i )
            iT.priceID = i
            self.items[level].append( iT )
            self.prices[level][i] = prices.priceItem(iT)
            
class magicShop(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'magicshop.bmp'))
        self.storeScreen.blit( self.images[1], (0,0) )
        self.mPrices = prices.magicPrices
        self.name = 'magicshop'
        self.items = range(3)
        self.prices = range(3)
        
    def stockStore(self, level):
        itemsList = shopScr.magicShopsByLevel[ level ]
        self.prices[level] = {}
        self.items[level] = []
        for i in itemsList:
            iT = item.Item( i[0], i[1] )
            iT.priceID = i
            self.items[level].append( iT )
            self.prices[level][i] = prices.priceItem(iT)