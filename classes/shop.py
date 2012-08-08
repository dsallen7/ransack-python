import pygame
import menu
from load_image import *
from const import *
from classes import menu
from IMG import images
import random
from OBJ import item
from SCRIPTS import shopScr


class Shop():
    
    def __init__(self, screen, hud, level, type, ticker):
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.screen = screen
        self.myHud = hud
        images.load()
        self.myMenu = menu.menu(screen)
        self.images = range(2)
        self.images[0], r = load_image('cursor.bmp')
        self.type = type
        self.level = level
        self.ticker = ticker
        self.items = []
        if type == 'blacksmith':
            items = shopScr.blacksmithShopsByLevel[self.level]
            self.images[1], r = load_image('blacksmith.bmp')
            from OBJ import weapon
            from prices import weaponPrices as prices
            self.prices = prices
            for i in items:
                self.items.append( weapon.Weapon(i[0], i[1]) )
        elif type == 'armory':
            items = shopScr.armoriesByLevel[self.level]
            self.images[1], r = load_image('armory.bmp')
            from OBJ import armor
            from prices import armorPrices as prices
            self.prices = prices
            for i in items:
                self.items.append( armor.Armor(i[0], i[1]) )
        elif type == 'itemshop':
            from OBJ import item
            self.images[1], r = load_image('itemshop.bmp')
            from prices import itemPrices as prices
            self.prices = prices
            items = shopScr.itemShopsByLevel[self.level]
            for i in items:
                self.items.append( item.Item( i + 86 ) )
        elif type == 'magicshop':
            from OBJ import item
            self.images[1], r = load_image('magicshop.bmp')
            from prices import magicPrices as prices
            self.prices = prices
            items = shopScr.magicShopsByLevel[self.level]
            for i in items:
                self.items.append( item.Item( i[0], i[1], i[2] ) )
        self.storeScreen.fill( black )
        self.storeScreen.blit( self.images[1], (0,0) )

    
    def drawStoreScreen(self):
        self.myHud.update()
        self.screen.blit( self.storeScreen, (75,75) )
        pygame.display.flip()
        
    # displays battle menu and waits for player to select choice,
    # returns choice to fightBattle()
    def getAction(self):
        menuBox = pygame.Surface( (124,99) )
        options = ['Buy', 'Sell', 'ExiT']
        selection = 0
        while True:
            menuBox.fill( gold )
            if pygame.font:
                font = pygame.font.Font(os.getcwd()+"/FONTS/SpinalTfanboy.ttf", 18)
                for i in range(3):
                    menuBox.blit( font.render(options[i], 1, white, gold), (25,i*25) )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection -= 1
                        if selection == -1:
                            selection = 2
                    if event.key == pygame.K_DOWN:
                        selection += 1
                        if selection == 3:
                            selection = 0
                    if event.key == pygame.K_RETURN:
                        return options[selection]
            menuBox.blit( self.images[0], (0, selection*25) )            
            self.storeScreen.blit( menuBox, (165,190) )
            self.drawStoreScreen()
    
    def sell(self, items):
        return self.myMenu.invMenu(items, 'SelecT iTem to sell:')
    
    def buy(self):
        return self.myMenu.storeMenu(self.items, 'SelecT iTem to buy:', self.prices)
    
    def enterStore(self, hero):
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'ExiT':
                return
            elif action == 'Buy':
                self.ticker.tick(60)
                purchase = self.buy()
                if purchase == None: pass
                elif hero.takeGold( self.prices[purchase] ):
                    if self.type == 'blacksmith':
                        hero.gainWeapon( purchase[0],purchase[1] )
                    elif self.type == 'armory':
                        hero.gainArmor( purchase[0],purchase[1] )
                    elif self.type == 'itemshop':
                        hero.getItem( (purchase-86,1) )
                    elif self.type == 'magicshop':
                        hero.getItem( (purchase[0],1), purchase[1], purchase[2] )
                else: self.myHud.txtMessage("You don'T have enough money!")
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