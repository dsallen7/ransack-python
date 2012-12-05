import pygame, os
from DISPLAY import menu, text
from IMG import images
import random
from OBJ import armor, weapon, item
from SCRIPTS import shopScr
from UTIL import const, colors, load_image

from math import floor, ceil

class Shop():
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.screen = screen
        self.myInterface = interface
        images.load()
        self.myMenu = menu
        self.images = range(2)
        self.images[0], r = load_image.load_image( os.path.join('MENU', "cursor.png" ), -1)
        self.type = type
        self.ticker = ticker
        self.storeScreen.fill( colors.black )
        self.inputHandler = iH
        self.menuBox = pygame.Surface( ( int(ceil(124*2.4)), int(ceil(99*2.4)) ) )
    
    def drawStoreScreen(self):
        #self.myInterface.update()
        storeScreen_ = pygame.transform.scale(self.storeScreen, (720, 720) )
        storeScreen_.blit( self.menuBox, ( int(ceil(165*2.4)),
                                               int(ceil(190*2.4))) )
        self.screen.blit( storeScreen_, (0, 0) )
        pygame.display.flip()
        
    def getAction(self):
        options = ['Buy', 'Sell', 'Exit Shop']
        selection = 0
        while True:
            self.menuBox.fill( colors.gold )
            if pygame.font:
                for i in range(3):
                    self.menuBox.blit( text.Text(options[i], os.getcwd()+"/FONTS/Squealer.ttf", const.shopTextFontSize), ( int(ceil(25*2.4)),
                                                                                                                      i*int(ceil(25*2.4)) ) )
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
            self.menuBox.blit( self.images[0], (0, selection* int(ceil(25*2.4)) ) )
            self.drawStoreScreen()
    
    def sell(self, items):
        return self.myMenu.invMenu(items, 'Select item to sell:', ['Sell', 'Return'], self.prices)
    
    def buy(self, items):
        return self.myMenu.invMenu( items, 'Select item to buy:', ['Buy', 'Return'], self.prices)
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
        from prices import weaponPrices as prices
        self.prices = prices
        
    def enterStore(self, hero, game, level):
        itemsList = shopScr.blacksmithShopsByLevel[ level ]
        items = []
        for i in itemsList:
            items.append( weapon.Weapon( i ) )
        
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit Shop':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy(items)
                if purchase == None: pass
                elif hero.takeGold( self.prices[ purchase.getType() ] ):
                    hero.gainWeapon( purchase.getType() )
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                sale = self.sell(hero.getWeapons())
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
        from prices import armorPrices as prices
        self.prices = prices
            
        
    def enterStore(self, hero, game, level):
        itemsList = shopScr.armoriesByLevel[ level ]
        items = []
        for i in itemsList:
            items.append( armor.Armor( i ) )
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit Shop':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy(items)
                if purchase == None: pass
                elif hero.takeGold( self.prices[purchase.getType()] ):
                    hero.gainArmor( purchase.getType() )
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                sale = self.sell(hero.getArmor())
                if sale == None: pass
                else:
                    hero.addGold( self.prices[ sale.getType() ]/2)
                    hero.loseArmor(sale)
            self.drawStoreScreen()
            
class itemShop(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'itemshop.bmp'))
        self.storeScreen.blit( self.images[1], (0,0) )
        from prices import itemPrices as prices
        self.prices = prices
        
        
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
                purchase = self.buy(items)
                if purchase == None: pass
                elif hero.takeGold( self.prices[purchase.getType()] ):
                    hero.getItem( purchase )
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                sale = self.sell(hero.getItems())
                if sale == None: pass
                else:
                    if hasattr(sale, "__iter__"):
                        sale = sale[0]
                    hero.addGold( self.prices[ sale.getType() ]/2 )
                    hero.takeItem( sale )
            self.drawStoreScreen()
            
class magicShop(Shop):
    
    def __init__(self, screen, interface, type, ticker, iH, menu):
        
        Shop.__init__(self, screen, interface, type, ticker, iH, menu)
        self.images[1], r = load_image.load_image( os.path.join('INT', 'magicshop.bmp'))
        self.storeScreen.blit( self.images[1], (0,0) )
        from prices import magicPrices as prices
        self.prices = prices
            
        
    def enterStore(self, hero, game, level):
        itemsList = shopScr.magicShopsByLevel[ level ]
        items = []
        for i in itemsList:
            items.append( item.Item( i[0], i[1], i[2] ) )
        
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit Shop':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy(items)
                if purchase == None: pass
                elif hero.takeGold( self.prices[(purchase.getType(), purchase.getLevel(), purchase.getSpellNum() )] ):
                    hero.getItem( purchase )
                else: game.textMessage("You don't have enough money!")
            elif action == 'Sell':
                self.ticker.tick(120)
                sale = self.sell(hero.getItems())
                if sale == None: pass
                else:
                    try:
                        if hasattr(sale, "__iter__"):
                            hero.addGold( self.prices[ ( sale[0].getType(), sale[0].getLevel(), sale[0].getSpellNum() ) ]/2 )
                            hero.takeItem(sale[0])
                        else:
                            hero.addGold( self.prices[ ( sale.getType(), sale.getLevel(), sale.getSpellNum() ) ]/2 )
                            hero.takeItem(sale)
                    except KeyError:
                        self.myInterface.txtMessage("We don't buy those...", None)
            self.drawStoreScreen()