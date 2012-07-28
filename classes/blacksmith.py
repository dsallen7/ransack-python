import pygame
import menu
from load_image import *
from const import *
from classes import menu
from IMG import images
import random

weaponPrices = { (0,0): 100,
                  (1,0): 100,
                  (2,0): 100,
                  (3,0): 100,
                  (0,1): 500,
                  (1,1): 500,
                  (2,1): 500,
                  (3,1): 500,
                  (0,2): 1000,
                  (1,2): 1000,
                  (2,2): 1000,
                  (3,2): 1000,
                }

class Blacksmith():
    
    def __init__(self, screen, hud, items, type):
        self.storeScreen = pygame.Surface( (300,300) )
        self.inventory = []
        self.screen = screen
        self.myHud = hud
        images.load()
        self.myMenu = menu.menu(screen)
        self.images = range(2)
        self.images[0], r = load_image('cursor.bmp')
        self.items = []
        self.type = type
        
        if type == 'blacksmith':
            from OBJ import weapon
            for i in items:
                self.items.append( weapon.Weapon(i[0], i[1]) )
        elif type == 'armory':
            from OBJ import armor
            for i in items:
                self.items.append( armor.Armor(i[0], i[1]) )
        elif type == 'itemshop':
            from OBJ import item
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
        return self.myMenu.invMenu(items, 'Select item to buy:')
    
    def buy(self):
        return self.myMenu.storeMenu(self.items, 'Select item to sell:')
    
    def enterStore(self, hero):
        self.drawStoreScreen()
        while True:
            action = self.getAction()
            if action == 'Exit':
                return
            elif action == 'Buy':
                purchase = self.buy()
                if purchase == None: pass
                elif hero.takeGold( weaponPrices[purchase] ):
                    hero.gainWeapon( purchase[0],purchase[1] )
                else: self.myHud.txtMessage("You don't have enough money!")
            elif action == 'Sell':
                sale = self.sell(hero.getWeapons())
                if sale == None: pass
                else: 
                    hero.addGold( weaponPrices[ (sale.getType(),sale.getLevel()) ]/2 )
                    hero.loseWeapon(sale)
            self.drawStoreScreen()