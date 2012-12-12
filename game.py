import pygame, os, random, cPickle

from classes import battle, enemy, shop, tavern, townhall, director
import OBJ
from IMG import images
from HERO import hero
from DISPLAY import display, interface, menu
from SCRIPTS import mapScr, enemyScr

from NPC import npcspawner
#from SND import sfx

from MAP import world, map, mapgen#, mazegen
from UTIL import ticker, const, colors, load_image, misc

from math import ceil, floor

class game():
    
    def __init__(self, images, screen, clock, iFace, FX, iH, titleScreen, loadTicker=None, loadHero=None, loadWorld=None, loadDirector=None):
        self.Display = display.Display(screen, images)
        self.FX = FX
        if loadTicker == None:
            self.Ticker = ticker.Ticker()
        else: self.Ticker = loadTicker
        if loadDirector == None:
            self.Director = director.Director()
        else: self.Director = loadDirector
        self.myMenu = menu.menu(screen, iH, self.Display, iFace, FX)
        #self.levelDepth = levelDepth
        self.inputHandler = iH
        
        FX.displayLoadingMessage(titleScreen, 'Loading world...')
        self.myMap = None
        if loadWorld == None:
            self.myWorld = world.World('game')
            self.myMap = self.myWorld.initialMap
            self.myWorld.currentMap = self.myMap
            (x, y) = self.myMap.heroStart
            self.myHero = hero.hero(loadHero,
                                (x*const.blocksize,
                                y*const.blocksize)                               
                                )
        else:
            self.myWorld = world.World('game', loadWorld)
            self.myMap = self.myWorld.currentMap
            self.myHero = hero.hero(loadHero)
        
        FX.displayLoadingMessage(titleScreen, 'Loading game engine...')
        self.NPCs = []
        self.screen = screen
        self.gameBoard = pygame.Surface( [300,300] )
        
        #self.gameBoard = self.gameBoard.convert(32)
                
        #this is true while player is in a particular game
        self.gameOn = True
        self.DIM = const.DIM
                        
        self.myInterface = iFace
        self.addShops()
        self.addNPCs(self.myMap)
        
        self.myBattle = battle.battle(self.screen, iH, self.myMenu)
        self.clock = clock
        
        #self.SFX = sfx.sfx()
        
        self.inputHandler = iH
        self.state = 'overworld'
        self.won = False
    
    #toggles switch to continue running game
    def gameOver(self):
        self.gameOn = False
    
    def removeNPC(self, ID):
        for n in self.NPCs:
            if n.getID() == ID:
                self.NPCs.remove(n)
                try:
                    self.myMap.NPCs.remove( n.getID() )
                except ValueError as e:
                    print 'ValueError while removing NPC: ', e
                return
    
    def addNPCs(self, map, type='all'):
        if type=='all':
            self.NPCs = []
            self.myMap.newNPCs = []
            visibleNPCs = []
            for n in map.NPCs:
                self.NPCs.append( npcspawner.newNpc( n, self ) )
            self.allsprites = pygame.sprite.RenderPlain((self.myHero, self.NPCs))
            self.allsprites.clear(self.screen, self.gameBoard)
        elif type=='new':
            for n in map.newNPCs[:]:
                self.NPCs.append( npcspawner.newNpc( n, self ) )
                map.newNPCs.remove(n)
            self.allsprites = pygame.sprite.RenderPlain((self.myHero, self.NPCs))
            self.allsprites.clear(self.screen, self.gameBoard)
    
    def addShops(self):
        self.Tavern = tavern.Tavern(self.screen, self.myInterface, self.Ticker, 
                                    self.inputHandler, self.myMenu)
        self.Townhall = townhall.Townhall(self.screen, self.myInterface, self.Ticker, 
                                          self.inputHandler, self.myMenu)
        self.Itemshop = shop.itemShop(self.screen, self.myInterface, 'itemshop', self.Ticker,
                                      self.inputHandler, self.myMenu)
        self.Magicshop = shop.magicShop(self.screen, self.myInterface, 'magicshop', self.Ticker, 
                                        self.inputHandler, self.myMenu)
        self.Blacksmith = shop.Blacksmith(self.screen, self.myInterface, 'blacksmith', self.Ticker, 
                                          self.inputHandler, self.myMenu)
        self.Armory = shop.Armory(self.screen, self.myInterface, 'armory', self.Ticker, 
                                  self.inputHandler, self.myMenu)
        
    def transition(self, loc):
        gameBoard_old = self.gameBoard.copy()
        #transition
        oldType = self.myMap.type
        self.myMap = self.myWorld.currentMap
        
        if self.myMap.getType() == 'dungeon':
            self.boxMessage('Now entering dungeon level '+str( self.myWorld.currentMap.level ))
        elif oldType != self.myWorld.currentMap.type:
            self.boxMessage('Now entering '+self.myMap.getType())
        
        self.addNPCs(self.myMap)
        self.Display.redrawXMap(self.myMap)
        self.DIM = self.myMap.getDIM()
        (x,y) = loc
        self.myMap.setPlayerXY(x, y)
        self.myWorld.currentMap.setPlayerXY(x, y)
        self.myHero.setXY( x*const.blocksize,y*const.blocksize )
        self.Display.redrawMap(self.myMap, self.myHero, self.gameBoard)
        self.FX.scrollFromCenter( gameBoard_old, self.gameBoard  )
        self.myMenu.displayStory(self.Director.getNarrartionEventByMapName(self.myMap.getName() ) )
    
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
        #self.SFX.play(0)
    
    def event_handler(self, event):
        if event == None:
            return
        elif event == pygame.K_SPACE:
            return
        elif event == pygame.K_c:
            # cast spell
            self.myHero.castSpell( self.myMenu.invMenu(self.myHero.getSpells(), "Spells:", ['Cast', 'Return'] ), self )
        elif event == pygame.K_p:
            # print map
            print self.myMap.grid
        elif event == pygame.K_s:
            # show stats
            self.myMenu.displayHeroStats(self.myHero)
        elif event == pygame.K_i:
            # use item
            self.myHero.useItem( self.myMenu.invMenu(self.myHero.getItems(), "Items:", ['Use', 'Return'] ), self )
            '''
        elif event == pygame.K_w:
            # equip weapon - DEPRECATED
            self.myHero.equipWeapon(self.myMenu.invMenu(self.myHero.getWeapons(), "Weapons:", ['Equip', 'Return'] ))
        elif event == pygame.K_a:
            # equip armor - DEPRECATED
            self.myHero.equipArmor(self.myMenu.invMenu(self.myHero.getArmor(), "Armor:", ['Equip', 'Return'] ))
            '''
        elif event == pygame.K_t:
            # take screenshot
            self.screenShot()
        elif event == pygame.K_m:
            # show minimap
            self.myMap.callDrawMiniMap(self.screen, self.inputHandler)
            '''
            if self.myMap.type in ['dungeon', 'maze', 'fortress']:
                self.myMap.callDrawMiniMap(self.screen, self.inputHandler)
            else: self.myWorld.callDrawMiniMap(self.screen, self.inputHandler)
            '''
        elif event == pygame.K_RETURN:
            # action command
            self.actionCommand()
        elif event == pygame.K_h:
            # do nothing - advance clock by 1 min
            self.myMenu.displayHelp()
        elif event == pygame.K_e:
            #equipment menu
            self.myMenu.equipmentMenu(self)
        elif event == pygame.K_ESCAPE:
            os.sys.exit()
        else:
            if not self.myHero.moving:
                try:
                    return self.move(pygame.key.name(event))
                except TypeError as e:
                    print 'TypeError while trying to move: ', e
    
    def actionCommand(self):
        (dX, dY) = const.scrollingDict[self.myHero.dir]
        (x, y) = self.myHero.getXY()
        x = (x / const.blocksize) + dX
        y = (y / const.blocksize) + dY
        for n in self.NPCs:
            if ( x, y ) == n.getXY():
                r = n.interact(self.myInterface, self)
                if r == None: return
                elif r == 'battle':
                    if self.launchBattle(n.name, self.myWorld.currentMap.level):
                        self.removeNPC(n.getID())
                    else: n.confuse(30)
                    return
                elif r[0] == 'item':
                    if r[1] == const.GOLD:
                        self.myHero.getItem( OBJ.item.Item( r[1], r[2] ) )
                    else: self.myHero.getItem( OBJ.item.Item( r[1] ) )
                    return
                elif r == 'win':
                    self.won = True
                    self.gameOver()
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
        elif i == const.SIGN:
            self.boxMessage( self.myMap.grid[x][y].getMsgText() )
        elif i == const.COUNTER_EW or i == const.COUNTER_NS:
            shopID = self.myMap.grid[x][y].getShopID()
            if shopID[0] == 'blacksmith':
                self.Blacksmith.enterStore(self.myHero, self, shopID[1])
                pygame.time.wait(500)
                return
            elif shopID[0] == 'townhall':
                pygame.time.wait(500)
                return self.Townhall.enterStore(self.myHero, self, self.FX)
            elif shopID[0] == 'armory':
                self.Armory.enterStore(self.myHero, self, shopID[1])
                pygame.time.wait(500)
                return
            elif shopID[0] == 'itemshop':
                self.Itemshop.enterStore(self.myHero, self, shopID[1])
                pygame.time.wait(500)
                return
            elif shopID[0] == 'magicshop':
                self.Magicshop.enterStore(self.myHero, self, shopID[1])
                pygame.time.wait(500)
                return
            elif shopID[0] == 'tavern':
                self.Tavern.enterStore(self.myHero, self, self.FX)
                pygame.time.wait(500)
                return
        else:
            try:
                self.boxMessage( mapScr.descriptions[i] )
            except KeyError:
                self.boxMessage( 'Nothing here...')
    
    def move(self, direction):
        if direction not in ['up','down','left','right']: return
        x1,y1,x2,y2 = self.myHero.getRect()
        (X,Y) = self.myHero.getXY() # pixels
        (moveX,moveY) = self.myHero.changeDirection(direction)
        x = (X + moveX)/const.blocksize # tiles
        y = (Y + moveY)/const.blocksize
        # check for blocking NPCs
        for n in self.NPCs:
            if ( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize ) == n.getXY() and n.playerIsFacingMe( self.myHero ):
                #n.moveIT(self.myMap, self.myHero.getXY())
                return
        i = self.myMap.getEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize)
        # detect blocking tiles first, otherwise they will be ignored
        # portals
        if i in const.doorsList:
            try:
                newMap = self.myWorld.getMapByName( self.myMap.grid[x][y].portal[0] )
                self.myWorld.currentMap = newMap
                self.transition( ( self.myMap.grid[x][y].portal[1], 
                                   self.myMap.grid[x][y].portal[2] ) )
                self.Display.drawSprites(self.myHero,self.myMap,self.gameBoard,self,animated=False)
            except AttributeError as e:
                print 'AttributeError while trying to enter a door: ', e
                pass
            return
        elif i == const.EWDOOR:
            self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize,const.EWDOORO)
            self.Display.redrawXMap(self.myMap)
            return
        elif i == const.NSDOOR:
            self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize,const.NSDOORO)
            self.Display.redrawXMap(self.myMap)
            return
        elif i == -1 or i in range(const.BRICK1,86)+[const.CHEST]+[const.OCHEST]+range(128, 216):
            return
        # dungeon door
        elif i == const.DOOR:
            if self.myHero.getPlayerStats()[8] == 0:
                self.boxMessage( "The door is locked!" )
                return
            else:
                self.boxMessage( "The door creaks open..." )
                self.myHero.takeKey()
                self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize, self.myMap.defaultBkgd)
                return
        #item
        if i in range(const.FRUIT1, const.KEY + 1):
            self.myHero.getItem( OBJ.item.Item(i) )
            self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize, self.myMap.defaultBkgd)
            self.Display.redrawXMap(self.myMap)
            self.myInterface.boxMessage(const.itemMsgs[i])
            return
        # Stairs down
        if i == const.STAIRDN:
            loc = self.myWorld.downLevel()
            self.myMap = self.myWorld.currentMap
            self.transition( loc )
            #self.nextLevel()
            self.Display.drawSprites(self.myHero,self.myMap,self.gameBoard,self,animated=False)
            return
        # Stairs up
        if i == const.STAIRUP:
            loc = self.myWorld.upLevel()
            self.transition( loc )
            #self.prevLevel()
            self.Display.drawSprites(self.myHero,self.myMap,self.gameBoard,self,animated=False)
            return
        # edge of map
        if i == const.VOID:
            if (Y + moveY)/const.blocksize < 0:                     # north
                loc = self.myWorld.changeMap( 0, ( X/const.blocksize, Y/const.blocksize ) )
            elif (Y + moveY)/const.blocksize > self.myMap.getDIM()-1: # south
                loc = self.myWorld.changeMap( 1, ( X/const.blocksize, Y/const.blocksize ) )
            elif (X + moveX)/const.blocksize >= self.myMap.getDIM()-1:            # east
                loc = self.myWorld.changeMap( 2, ( X/const.blocksize, Y/const.blocksize ) )
            elif (X + moveX)/const.blocksize < 0:  # west
                loc = self.myWorld.changeMap( 3, ( X/const.blocksize, Y/const.blocksize ) )
            try:
                if loc is not False:
                    self.transition(loc)
                    self.Display.drawSprites(self.myHero,self.myMap,self.gameBoard,self,animated=False)
            except UnboundLocalError as e:
                print 'UnboundLocalError while leaving edge of map: ', e
            return
        # open space
        self.myHero.moving = True
        if ( (0 <= X+moveX < const.blocksize*self.myMap.getDIM() ) and (0 <= Y+moveY < const.blocksize*self.myMap.getDIM() ) and i in range(const.BRICK1) ):
            self.myHero.moving = True
            self.myMap.clearOccupied(X/const.blocksize,Y/const.blocksize)
            X += moveX
            Y += moveY
            self.myHero.setXY(X,Y)
            self.myMap.setOccupied(X/const.blocksize,Y/const.blocksize)
        
        if not self.myHero.updateStatus(self):
            self.gameOver()
        
        self.Ticker.tick(2)
        return True
    
    def getLoot(self, e):
        lootItems = []
        lootItems.append( (const.GOLD, random.randrange(enemyScr.lootDict[e]-3, 
                                             enemyScr.lootDict[e]+3) ) )
        if misc.rollDie(0, 4):
            lootItems.append( (const.PARCHMENT, random.choice( mapScr.parchByLevel[self.myWorld.currentMap.level] ) ) )
        return lootItems
    
    def launchBattle(self, mName, lD):
        self.boxMessage("The battle is joined!")
        result = self.myBattle.fightBattle(self, enemy.enemy(mName, lD), self.gameBoard )
        if result == 'escaped': # escaped from battle
            return False
        elif result == 'died': # died in battle
            self.gameOver()
        elif result == 'won': # won battle
            for item in self.myMenu.displayChest( self.getLoot(mName), 'Enemy Loot' ):
                msg = self.myHero.getItem(item)
                self.Ticker.tick(30)
                self.textMessage(msg)
            self.myHero.notchKill()
            # final boss
            if mName == 'Skeleton King':
                self.Director.setEvent(11)
            return True

    # calls interface.boxMessage
    def boxMessage(self, msg):
        self.myInterface.boxMessage(msg)
    
    # calls interface.txtMessage
    def textMessage(self, msg):
        self.myInterface.txtMessage(msg, self)
        pygame.display.flip()
    
    def getSaveBall(self):
        saveBall = (self.Ticker, self.myHero.getSaveBall(), self.myWorld.getWorldBall(), self.Director)
        
        return saveBall
    
    def updateSprites(self):
                
        if self.myMap.type in ['dungeon', 'maze', 'fortress']:
            self.allsprites = pygame.sprite.RenderPlain((self.myHero, self.visibleNPCs))
        else: self.allsprites = pygame.sprite.RenderPlain((self.myHero, self.NPCs))
        self.allsprites.clear(self.screen, self.gameBoard)
        rects = self.allsprites.draw(self.gameBoard)
        pygame.display.update(rects)
    
    def updateNPCs(self):
        #self.allsprites.update()
        self.visibleNPCs = []
        redraw = False
        for n in self.NPCs:
            (x, y) = n.getXY()
            self.myMap.grid[x][y].occupied = True
            if self.myMap.isVisible(x, y):
                self.visibleNPCs.append(n)
            r = n.update(self.myMap, self.myHero.getXY() )
            if r == True:# and n in self.visibleNPCs:
                redraw = True
            elif r == 'battle':
                if self.launchBattle(n.name, self.myWorld.currentMap.level):
                    self.removeNPC(n.getID())
                else: n.confuse(30)
                
        return redraw
    
    def displayOneFrame(self):
        self.Display.redrawMap(self.myMap, self.myHero, self.gameBoard)
        #self.updateSprites()
        self.Display.displayOneFrame(self.myInterface, self.FX, self.gameBoard, self, self.myMap.type in ['dungeon', 'maze', 'fortress'])

    def mainLoop(self):
        self.visibleNPCs = []
        if not self.Director.getEvent(0):
            self.myMenu.displayStory("So here you are in the same town, in front of the same house you've lived in forever. There's gotta be something else out there. It's time to go find it. Welcome to Ransack.")
            self.Director.setEvent(0)
        (pX, pY) = self.myHero.getXY()
        self.myMap.setPlayerXY( pX/const.blocksize, pY/const.blocksize )
        self.myMap.updateWindowCoordinates(self.myHero)
        self.Display.redrawXMap(self.myMap)
        self.updateSprites()
        self.Display.drawSprites(self.myHero, self.myMap, self.gameBoard, self, animated=False)
        while self.gameOn:
            #self.gameBoard.fill(colors.black)
            for event in pygame.event.get():
                event_ = self.inputHandler.getCmd(event)
                self.event_handler(event_)
            if pygame.mouse.get_pressed()[0]:
                event_ = self.inputHandler.getCmd(None)
                # don't want rapid repeats of action commands
                if event_ in [pygame.K_UP,
                              pygame.K_DOWN,
                              pygame.K_LEFT,
                              pygame.K_RIGHT,]:
                    self.event_handler(event_)
            if self.myMap.update( len(self.NPCs) ) == 'newNPCs':
                self.addNPCs(self.myMap, 'new')
            
            if self.updateNPCs() or self.myHero.moving:
                self.Display.drawSprites(self.myHero, self.myMap, self.gameBoard, self, self.myHero.dir, animated=True)
                    #self.Display.drawSprites(self.myHero, self.myMap, self.gameBoard, self, None, animated=True)
            self.displayOneFrame()
            
        self.myInterface.state = 'mainmenu'
        return self.won