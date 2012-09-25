import pygame, os, random, pickle

from classes import battle, menu, enemy, shop, tavern, director
import OBJ
from IMG import images
from HERO import hero
from NPC import npc
from DISPLAY import display, hud

from MAP import map, mapgen, mazegen
from UTIL import ticker, const, colors, load_image

class game():
    
    def __init__(self, screen, clock, FX, loadTicker=None, loadHero=None, loadDungeon=None, loadDirector=None, currentMap=2, levelDepth=0):
        self.Display = display.Display(screen)
        self.FX = FX
        if loadTicker == None:
            self.Ticker = ticker.Ticker()
        else: self.Ticker = loadTicker
        if loadHero == None:
            self.myHero = hero.hero()
        else: self.myHero = hero.hero(load=loadHero)
        if loadDirector == None:
            self.Director = director.Director()
        else: self.Director = loadDirector
        self.myMenu = menu.menu(screen)
        self.levelDepth = levelDepth
        self.currentMap = currentMap
        
        # a dungeon is just an array of maps
        self.myMap = None
        if loadDungeon == None:
            self.myDungeon = []
            for mapFileName in const.mapList:
                self.myDungeon += [map.gameMap(mapFileName, type='village')]
        else: self.myDungeon = loadDungeon
        
        self.fortressMaps = []
        for mapFileName in const.fMapList:
            self.fortressMaps += [map.gameMap(mapFileName, type='fortress')]
        
        self.myMap = self.myDungeon[self.currentMap]
        self.NPCs = []
        self.screen = screen
        self.gameBoard = pygame.Surface( [300,300] )
                
        #this is true while player is in a particular game
        self.gameOn = True
        self.DIM = const.DIM

        images.load()
        
        # 0 : camera
        # 1 : sword
        # 2 : miss
        self.sounds = range(3)
        self.sounds[0] = pygame.mixer.Sound(os.path.join('SND', 'camera.wav' ))
        self.sounds[1] = pygame.mixer.Sound(os.path.join('SND', 'sword1.wav' ))
        self.sounds[2] = pygame.mixer.Sound(os.path.join('SND', 'miss.wav' ))
        
        self.myHud = hud.hud(self.screen, self)
        self.addShops(self.myMap)
        self.addNPCs(self.myMap)
        
        self.myBattle = battle.battle(self.screen)
        self.clock = clock
        
        self.won = False
    
    #toggles switch to continue running game
    def gameOver(self):
        self.gameOn = False
    
    def removeNPC(self, ID):
        for n in self.NPCs:
            if n.getID() == ID:
                self.NPCs.remove(n)
                self.myMap.NPCs.remove( n.getID() )
                return
    
    def addNPCs(self, map):
        self.NPCs = []
        visibleNPCs = []
        for n in map.NPCs:
            self.NPCs.append( npc.newNpc( n, self ) )
        self.allsprites = pygame.sprite.RenderPlain((self.myHero, self.NPCs))
        self.allsprites.clear(self.screen, self.gameBoard)
    
    def addShops(self, map):        
        self.Blacksmiths = range(4)
        self.Armories = range(4)
        self.Itemshops = range(4)
        self.Magicshops = range(4)
        self.Taverns = range(4)
        if map.shops is not None:
            for s in map.shops:                
                if map.shops[s][0] == 'tavern':
                    self.Tavern = tavern.Tavern(self.screen, self.myHud, self.Ticker) 
                if map.shops[s][0] == 'itemshop':
                    self.Itemshops[map.shops[s][1]] = shop.itemShop(self.screen, self.myHud, map.shops[s][1], 'itemshop', self.Ticker)
                if map.shops[s][0] == 'magicshop':
                    self.Magicshops[map.shops[s][1]] = shop.magicShop(self.screen, self.myHud, map.shops[s][1], 'magicshop', self.Ticker)
                if map.shops[s][0] == 'blacksmith':
                    self.Blacksmiths[map.shops[s][1]] = shop.Blacksmith(self.screen, self.myHud, map.shops[s][1], 'blacksmith', self.Ticker)
                if map.shops[s][0] == 'armory':
                    self.Armories[map.shops[s][1]] = shop.Armory(self.screen, self.myHud, map.shops[s][1], 'armory', self.Ticker)

    
    def generateMap(self, dimension, level, type):
        if type == 'dungeon':
            MG = mapgen.Generator(dimension, level)
            MG.generateMap(20)
            newMap = map.gameMap(None, MG.getMapBall(), level=self.levelDepth)
        elif type == 'maze':
            MG = mazegen.Generator(dimension, level)
            MG.generateMap()
            newMap = map.gameMap(None, MG.getMapBall(), level=self.levelDepth, type='maze')
        return newMap
        
    def nextLevel(self):
        self.currentMap += 1
        if self.currentMap == len(self.myDungeon):
            self.levelDepth += 1
            if self.levelDepth == 10:
                self.myDungeon = self.myDungeon + self.fortressMaps
                self.boxMessage('Now entering fortress')
            else:
                if ( self.levelDepth % 5 ) == 0:
                    self.myDungeon.append(self.generateMap(40, self.levelDepth, type = 'maze') )
                else:
                    self.myDungeon.append(self.generateMap(40, self.levelDepth, type = 'dungeon') )
                self.boxMessage('Now entering dungeon level '+str(self.levelDepth))
            self.myMap = self.myDungeon[self.currentMap]
            self.Display.redrawXMap(self.myMap)
        else:
            self.myMap = self.myDungeon[self.currentMap]
            self.addShops(self.myMap)
            self.Display.redrawXMap(self.myMap)
            if self.myMap.getType() == 'dungeon':
                self.levelDepth += 1
                self.boxMessage('Now entering dungeon level '+str(self.levelDepth))
            else: self.boxMessage('Now entering '+self.myMap.getType())
        self.DIM = self.myMap.getDIM()
        self.addNPCs(self.myMap)
        (x,y) = self.myMap.getPOE()
        self.myHero.setXY( x*const.blocksize,y*const.blocksize )
    
    def prevLevel(self):
        self.currentMap -= 1
        if self.levelDepth > 0:
            self.levelDepth -= 1
        self.myMap = self.myDungeon[self.currentMap]
        if self.myMap.getType() == 'dungeon':
            self.boxMessage('Now entering dungeon level '+str(self.levelDepth))
        else:
            self.addShops(self.myMap)
            self.boxMessage('Now entering '+self.myMap.getType())
        self.addNPCs(self.myMap)
        self.Display.redrawXMap(self.myMap)
        self.DIM = self.myMap.getDIM()
        (x,y) = self.myMap.getPOEx()
        self.myHero.setXY( x*const.blocksize,y*const.blocksize )
    
    #takes screen shot and saves as bmp in serial fashion, beginning with 1
    def screenShot(self):
        serial = 1
        while os.access("ransack"+str(serial)+".bmp", os.F_OK):
            serial += 1
        pygame.image.save(self.screen, "ransack"+str(serial)+".bmp")
        flash = pygame.Surface([450,450])
        flash.fill(colors.white)
        self.screen.blit(flash,(75,75))
        self.clock.tick(100)
        self.sounds[0].play()
    
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            elif event.key == pygame.K_c:
                # cast spell
                self.myHero.castSpell( self.myMenu.invMenu(self.myHero.getSpells(), "Spells:" ), self )
            elif event.key == pygame.K_s:
                # show stats
                self.myMenu.displayHeroStats(self.myHero)
            elif event.key == pygame.K_i:
                # use item
                self.Ticker.tick( self.myHero.useItem( self.myMenu.invMenu(self.myHero.getItems(), "ITems:" ), self ) )
            elif event.key == pygame.K_w:
                # equip weapon
                self.myHero.equipWeapon(self.myMenu.invMenu(self.myHero.getWeapons(), "Weapons:" ))
            elif event.key == pygame.K_a:
                # equip armor
                self.myHero.equipArmor(self.myMenu.invMenu(self.myHero.getArmor(), "Armor:" ))
            elif event.key == pygame.K_t:
                # take screenshot
                self.screenShot()
            elif event.key == pygame.K_m:
                # show minimap
                self.myMap.callDrawMiniMap(self.screen)
            elif event.key == pygame.K_RETURN:
                # action command
                self.actionCommand()
            elif event.key == pygame.K_r:
                # do nothing - advance clock by 1 min
                self.Ticker.tick(60)
            else:
                return self.move(pygame.key.name(event.key))
    
    def mouseHandler(self, event):
        (mx, my) = pygame.mouse.get_pos()
        if (const.gameBoardOffset <= mx < const.gameBoardOffset+self.gameBoard.get_width() ) and (const.gameBoardOffset <= my < const.gameBoardOffset+self.gameBoard.get_height() ):
            # map handler
            pass
        elif (const.gameBoardOffset+self.gameBoard.get_width()  < mx <= const.gameBoardOffset+self.gameBoard.get_width()+150) and (const.gameBoardOffset < my <= const.gameBoardOffset+300):
            # hud handler
            self.myHud.mouseHandler(event, mx-(const.gameBoardOffset+self.gameBoard.get_width()), my-const.gameBoardOffset)
    
    def actionCommand(self):
        (dX, dY) = const.scrollingDict[self.myHero.dir]
        (x, y) = self.myHero.getXY()
        x = (x / const.blocksize) + dX
        y = (y / const.blocksize) + dY
        for n in self.NPCs:
            if ( x, y ) == n.getXY():
                r = n.interact(self.myHud)
                if r == None: return
                elif r == 'battle':
                    if self.launchBattle(n.name, self.levelDepth):
                        self.removeNPC(n.getID())
                    else: n.confuse(30)
                    return
                elif r[0] == 'item':
                    self.myHero.getItem( OBJ.item.Item( r[1] ) )
                    return
        i = self.myMap.getEntry(x, y)
        # Chest
        if i == const.CHEST:
            self.textMessage( 'The chest contains:')
            chestlist = self.myMap.chests[(x, y)]
            for item in self.myMenu.displayChest( chestlist ):
                msg = self.myHero.getItem(item)
                self.Ticker.tick(30)
                self.textMessage(msg)
            self.myMap.setEntry( x, y, const.OCHEST )
            self.Display.redrawXMap(self.myMap)
            return
        elif i == const.EWFAKE:
            self.Ticker.tick(60)
            self.textMessage( 'You find a secret door!')
            self.myMap.setEntry( x, y, const.EWDOOR )
            self.Display.redrawXMap(self.myMap)
            return
        elif i == const.NSFAKE:
            self.Ticker.tick(60)
            self.textMessage( 'You find a secret door!')
            self.myMap.setEntry( x, y, const.NSDOOR )
            self.Display.redrawXMap(self.myMap)
            return
        self.boxMessage( 'Nothing here...')
    
    def move(self, direction):
        if direction not in ['up','down','left','right']: return
        x1,y1,x2,y2 = self.myHero.getRect()
        (X,Y) = self.myHero.getXY()
        (moveX,moveY) = self.myHero.changeDirection(direction)
        for n in self.NPCs:
            if ( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize ) == n.getXY():
                return
        i = self.myMap.getEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize)
        # detect blocking tiles first, otherwise they will be ignored
        # stores
        if i == const.BLKSMDOOR:
            self.Blacksmiths[self.myMap.shops[( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize)][1]].enterStore(self.myHero)
            return
        if i == const.ARMRYDOOR:
            self.Armories[self.myMap.shops[( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize)][1]].enterStore(self.myHero)
            return
        if i == const.ITEMSDOOR:
            self.Itemshops[self.myMap.shops[( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize)][1]].enterStore(self.myHero)
            return
        if i == const.MAGICDOOR:
            self.Magicshops[self.myMap.shops[( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize)][1]].enterStore(self.myHero)
        if i == const.TAVRNDOOR:
            return self.Tavern.enterStore(self.myHero, self)
        if i == const.EWDOOR:
            self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize,const.EWDOORO)
            self.Display.redrawXMap(self.myMap)
        if i == const.NSDOOR:
            self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize,const.NSDOORO)
            self.Display.redrawXMap(self.myMap)
        if i == -1 or i in range(24,86):
            return
        # dungeon door
        if i == const.DOOR:
            if self.myHero.getPlayerStats()[8] == 0:
                self.boxMessage( "The door is locked!" )
                return
            else:
                self.boxMessage( "The door creaks open..." )
                self.myHero.takeKey()
                self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize, self.myMap.defaultBkgd)
        #item
        if i in range(86,109):
            self.myHero.getItem( OBJ.item.Item(i) )
            self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize, self.myMap.defaultBkgd)
            self.myHud.boxMessage(const.itemMsgs[i])
        # Stairs down
        if i == const.STAIRDN:
            self.nextLevel()
            self.Display.drawSprites(self.myHero,self.myMap,self.gameBoard,self,animated=False)
            return
        # Stairs up
        if i == const.STAIRUP:
            self.prevLevel()
            self.Display.drawSprites(self.myHero,self.myMap,self.gameBoard,self,animated=False)
            return
        # open space
        if ( (0 <= X+moveX < const.blocksize*self.myMap.getDIM() ) and (0 <= Y+moveY < const.blocksize*self.myMap.getDIM() ) and i in range(24) ):
            self.myHero.moving = True
            X += moveX
            Y += moveY
            self.myHero.setXY(X,Y)
        self.Display.redrawXMap(self.myMap)
        
        if not self.myHero.updateStatus(self.Ticker, self.myHud):
            self.gameOver()
        
        self.Ticker.tick(2)
        return True
    
    def launchBattle(self, mName, lD):
        self.boxMessage("The baTTle is joined!")
        #self.FX.fadeOut(const.gameBoardOffset)
        g = self.myBattle.fightBattle(self, enemy.enemy(mName, lD) )
        if g == True: # escaped from battle
            return False
        elif g == False: # died in battle
            self.gameOver()
        else: # won battle
            self.textMessage('You find '+str(g)+' gold pieces!')
            self.myHero.addGold(g)
            # final boss
            if mName == 'Skeleton King':
                self.won = True
            return True
    
    def rollDie(self, target, range):
        d = random.randrange(range)
        if target >= d:
            return True
        else:
            return False

    # calls hud.boxMessage
    def boxMessage(self, msg):
        self.myHud.boxMessage(msg)
    
    # calls hud.txtMessage
    def textMessage(self, msg):
        self.myHud.txtMessage(msg)
    
    def getSaveBall(self):
        saveBall = (self.Ticker, self.myHero.getSaveBall(), self.myDungeon, self.Director, self.currentMap, self.levelDepth)
        
        return saveBall
    
    def updateSprites(self):
        #self.allsprites.update()
        visibleNPCs = []
        for n in self.NPCs:
            (x, y) = n.getXY()
            self.myMap.grid[x][y].occupied = True
            if self.myMap.isVisible(x, y):
                visibleNPCs.append(n)
                
        if self.myMap.type in ['dungeon', 'maze', 'fortress']:
            self.allsprites = pygame.sprite.RenderPlain((self.myHero, visibleNPCs))
        else: self.allsprites = pygame.sprite.RenderPlain((self.myHero, self.NPCs))
        self.allsprites.clear(self.screen, self.gameBoard)
        rects = self.allsprites.draw(self.gameBoard)
        pygame.display.update(rects)
    
    def displayGameBoard(self):
        self.updateSprites()
        if self.myMap.type == 'dungeon':
            pass#self.Display.drawShade(self.myMap, self.gameBoard)
        self.screen.blit( self.gameBoard, (const.gameBoardOffset, const.gameBoardOffset) )
        pygame.display.flip()
    
    def updateNPCs(self):
        redraw = False
        for n in self.NPCs:
            r = n.update(self.myMap, self.myHero.getXY() )
            if r == True:
                redraw = True
            elif r == 'battle':
                if self.launchBattle(n.name, self.levelDepth):
                    self.removeNPC(n.getID())
                else: n.confuse(30)
                
        return redraw
        

    def mainLoop(self):
        gameFrame, gameFrameRect = load_image.load_image('gamescreen600.bmp', None)
        self.screen.blit(gameFrame,(0,0))
        
        (pX, pY) = self.myMap.getPlayerXY()
        self.myHero.setXY(pX*const.blocksize, pY*const.blocksize)
        
        self.myMap.updateWindowCoordinates(self.myHero)
        self.Display.drawSprites(self.myHero, self.myMap, self.gameBoard, self, animated=False)
        self.updateSprites()
        self.Display.redrawXMap(self.myMap)
        font = pygame.font.SysFont("arial", 14)
        while self.gameOn:
            #self.clock.tick(30)
            self.gameBoard.fill(colors.black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    os.sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if not self.myHero.moving: 
                        heroMove = self.event_handler(event)
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    self.mouseHandler(event)
            self.myHud.update()
                #self.Display.drawNPC(npc, self.myMap, self, animated=True)
            self.screen.blit( self.myHero.showLocation(), (0, 0) )
            font = pygame.font.SysFont("arial", 14)
            self.screen.blit( font.render( str(self.myMap.getDIM()) , 1, colors.red, colors.yellow ), (300,0) )
            if self.updateNPCs() or self.myHero.moving:
                self.Display.drawSprites(self.myHero, self.myMap, self.gameBoard, self, self.myHero.dir, animated=True)
            else: 
                self.Display.drawSprites(self.myHero, self.myMap, self.gameBoard, self, None, animated=True)
            self.Display.redrawMap(self.myMap, self.myHero, self.gameBoard)
            self.displayGameBoard()
        return self.won