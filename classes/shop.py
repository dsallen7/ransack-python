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
    
    def __init__(self, screen, hud, level, type):
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
        self.items = []
        if type == 'blacksmith':
            items = shopScr.blacksmithShopsByLevel[self.level]
            from OBJ import weapon
            from prices import weaponPrices as prices
            self.prices = prices
            for i in items:
                self.items.append( weapon.Weapon(i[0], i[1]) )
        elif type == 'itemshop':
            from OBJ import item
            from prices import itemPrices as prices
            self.prices = prices
            items = shopScr.itemShopsByLevel[self.level]
            for i in items:
                self.items.append( item.Item( i + 86 ) )

    
    def drawStoreScreen(self):
        self.myHud.update()
        self.screen.blit( self.storeScreen, (75,75) )
        pygame.display.flip()
        
    # displays battle menu and waits for player to select choice,
    # returns choice to fightBattle()
    def getAction(self):
        menuBox = pygame.Surface( (60,75) )
        options = ['Buy', 'Sell', 'Exit']
        selection = 0
        while True:
            menuBox.fill( yellow )
            if pygame.font:
                font = pygame.font.SysFont("URW Chancery L", 14)
                for i in range(3):
                    menuBox.blit( font.render(options[i], 1, white, yellow), (25,i*25) )
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
            self.storeScreen.blit( menuBox, (200,150) )
            self.drawStoreScreen()
    
    def sell(self, items):
        return self.myMenu.invMenu(items, 'Select item to sell:')
    
    def buy(self):
        return self.myMenu.storeMenu(self.items, 'Select item to buy:')
    
    def enterStore(self, hero):
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit':
                return
            elif action == 'Buy':
                purchase = self.buy()
                if purchase == None: pass
                elif hero.takeGold( self.prices[purchase] ):
                    if self.type == 'blacksmith':
                        hero.gainWeapon( purchase[0],purchase[1] )
                    elif self.type == 'itemshop':
                        hero.getItem( purchase-86 )
                else: self.myHud.txtMessage("You don't have enough money!")
            elif action == 'Sell':
                if self.type == 'blacksmith':
                    sale = self.sell(hero.getWeapons())
                elif self.type == 'itemshop':
                    sale = self.sell(hero.getItems())
                if sale == None: pass
                else: 
                    if self.type == 'blacksmith':
                        hero.addGold( self.prices[ (sale.getType(),sale.getLevel()) ]/2 )
                        hero.loseWeapon(sale)
                    elif self.type == 'itemshop':
                        hero.addGold( self.prices[ sale.getType() ]/2 )
                        hero.takeItem(sale.getType())
            self.drawStoreScreen()