import pygame, os, random, cPickle, gzip
import battle, enemy, shop, tavern, townhall, director
import OBJ
from IMG import images
from HERO import hero
from DISPLAY import display, interface, menu
from SCRIPTS import mapScr, enemyScr
from NPC import npcspawner
from SND import sfx
from MAP import world, generalmap, mapgen
from UTIL import ticker, const, colors, load_image, misc, astar
from math import ceil, floor
from types import TupleType


class game():

    def __init__(self, images, screen, clock, iFace, FX, iH, titleScreen, SFX, myWorldBall,
                 loadTicker=None, loadHero=None, loadWorld=None, loadDirector=None):
        self.Display = display.Display(screen, images)
        self.FX = FX
        self.SFX = SFX
        if loadTicker is None:
            self.Ticker = ticker.Ticker()
        else: self.Ticker = loadTicker
        if loadDirector is None:
            self.Director = director.Director()
        else: self.Director = loadDirector
        self.myMenu = menu.menu(screen, iH, self.Display, iFace, FX, SFX)
        #self.levelDepth = levelDepth
        self.inputHandler = iH
        
        FX.displayLoadingMessage(titleScreen, 'Loading world...')
        # myWorldBall is the game world which always is loaded
        # loadWorld is the levels which have been generated ingame and saved
        self.myMap = None
        if loadWorld is None:
            self.myWorld = world.World('game', myWorldBall)
            self.myMap = self.myWorld.initialMap
            self.myWorld.currentMap = self.myMap
            (x, y) = self.myMap.heroStart
            self.myHero = hero.hero(loadHero,
                                (x*const.blocksize,
                                y*const.blocksize)                               
                                )
        else:
            self.myWorld = world.World('game', myWorldBall, loadWorld)
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
    
    def getNPCByName(self, name):
        for n in self.NPCs:
            if n.name == name:
                return n

    def addNPCs(self, map, type='all'):
        if type=='all':
            self.NPCs = []
            self.myMap.newNPCs = []
            visibleNPCs = []
            for n in map.NPCs:
                try:
                    self.NPCs.append( npcspawner.newNpc( n, self ) )
                except TypeError as e:
                    print 'TypeError while adding NPC: ',n , e

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
        l = 2 + self.myHero.hasItem(const.LANTERN)
        oldType = self.myMap.type
        self.myMap = self.myWorld.currentMap
        
        if self.myMap.getType() == 'dungeon':
            self.boxMessage('Now entering dungeon level '+str( self.myWorld.currentMap.level ))
        elif oldType != self.myWorld.currentMap.type:
            self.boxMessage('Now entering '+self.myMap.getType())
        self.addNPCs(self.myMap)
        self.Display.redrawXMap(self.myMap, l)
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
        if type(event) == TupleType:
            if event == (0,0): return
            (topX, topY) = self.myMap.topMapCorner
            event = (event[0]+topX, event[1]+topY)
            for m in astar.ransackPathfinder(self.myMap.getBinaryMap(), self.myMap.getPlayerXY(), event ):
                self.myHero.moveQueue.push(int(m))
            return
        if event == None:
            return
        elif event == pygame.K_SPACE:
            return
        elif event == pygame.K_c:
            # cast spell
            self.myHero.castSpell( self.myMenu.mainMenu(self, 'spell'), self )
        elif event == pygame.K_p:
            # print map
            print self.myMap.grid
        elif event == pygame.K_s:
            # show stats
            self.myMenu.displayHeroStats(self.myHero)
        elif event == pygame.K_i:
            # use item
            self.myHero.useItem( self.myMenu.mainMenu(self, 'items'), self  )
        elif event == pygame.K_t:
            # take screenshot
            self.screenShot()
        elif event == pygame.K_m:
            # show minimap
            self.myMap.callDrawMiniMap(self.screen, self.inputHandler)
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
            if self.myInterface.npcDialog('Are you sure you want to quit?', self.myHero.images[2]) == 'Yes':
                os.sys.exit()
            else:
                pass
        else:
            if not self.myHero.moving:
                try:
                    return self.move(pygame.key.name(event))
                except TypeError as e:
                    print 'TypeError while trying to move: ', e
    
    def saveGame(self, fileName):
        if fileName == None:
            return False
        try:
            #FX.displayLoadingMessage(self.storeScreen, 'Saving game...')
            savFile = gzip.GzipFile(fileName, 'wb', 1)
            cPickle.dump(self.getSaveBall(), savFile, 2)
            savFile.close()
            return True
        except IOError, e:
            print 'File I/O error', e
            return False
    
    def actionCommand(self):
        (dX, dY) = const.scrollingDict[self.myHero.dir]
        (x, y) = self.myHero.getXY()
        x = (x / const.blocksize) + dX
        y = (y / const.blocksize) + dY
        l = 2 + self.myHero.hasItem(const.LANTERN)
        for n in self.NPCs:
            if ( x, y ) == n.getXY():
                r = n.interact(self.myInterface, self)
                if r == None: return
                elif r == 'battle':
                    if self.launchBattle(n, self.myWorld.currentMap.level):
                        self.removeNPC(n.getID())
                    else: n.confuse(30)
                    return
                elif r[0] == 'item':
                    if r[1] == const.GOLD:
                        self.myHero.getItem( OBJ.item.Item( r[1], r[2] ) )
                    else:
                        for i in range( r[2] ):
                            self.myHero.getItem( OBJ.item.Item( r[1] ) )
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
            self.Display.redrawXMap(self.myMap, l)
            return
        elif i == const.EWFAKE:
            self.Ticker.tick(60)
            self.textMessage( 'You find a secret door!')
            self.myMap.setEntry( x, y, const.EWDOOR )
            self.Display.redrawXMap(self.myMap, l)
            return
        elif i == const.NSFAKE:
            self.Ticker.tick(60)
            self.textMessage( 'You find a secret door!')
            self.myMap.setEntry( x, y, const.NSDOOR )
            self.Display.redrawXMap(self.myMap, l)
            return
        elif i == const.SIGN:
            self.boxMessage( self.myMap.grid[x][y].getMsgText() )
        elif i == const.WELLSP:
            if self.myHero.drinkWater():
                self.boxMessage( 'Your thirst is quenched!')
            else:
                self.boxMessage("You don't need a drink now!")
                
        elif i == const.COUNTER_EW or i == const.COUNTER_NS:
            shopID = self.myMap.grid[x][y].getShopID()
            if shopID[0] == 'blacksmith':
                self.Blacksmith.enterStore(self.myHero, self, shopID[1])
                pygame.time.wait(500)
                return
            elif shopID[0] == 'townhall':
                pygame.time.wait(500)
                return self.Townhall.enterStore(self.myHero, self, self.FX, shopID[1],
                                                (self.myMap.getName(), self.myMap.getPlayerXY() ) )
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
    # takes string name of new map along with new coordinates
    def portalMove(self, newMap, newX, newY):
        try:
            self.myWorld.currentMap = self.myWorld.getMapByName( newMap )
            self.transition( (newX, newY) )
            self.Display.drawSprites(self.myHero,self.myMap,self.gameBoard,self,animated=False)
        except AttributeError as e:
            #print 'AttributeError while trying to enter a door: ', e
            pass
        
    def move(self, direction):
        if direction not in ['up','down','left','right']: return
        x1,y1,x2,y2 = self.myHero.getRect()
        (X,Y) = self.myHero.getXY() # pixels
        (moveX,moveY) = self.myHero.changeDirection(direction)
        l = 2 + self.myHero.hasItem(const.LANTERN)
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
                newMap = self.myMap.grid[x][y].portal[0]
                (newX, newY) = ( self.myMap.grid[x][y].portal[1],
                                 self.myMap.grid[x][y].portal[2] )
                self.portalMove(newMap, newX, newY)
            except AttributeError as e:
                if i in const.doorsList[:7]:
                    self.boxMessage( "The door is locked." )
                print 'AttributeError while trying to enter a door: ', e
                pass
            return
        elif i == const.EWDOOR:
            self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize,const.EWDOORO)
            self.Display.redrawXMap(self.myMap, l)
            return
        elif i == const.NSDOOR:
            self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize,const.NSDOORO)
            self.Display.redrawXMap(self.myMap, l)
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
                self.Display.redrawXMap(self.myMap, l)
                return
        #item
        if i in range(const.FRUIT1, const.KEY + 1):
            self.myHero.getItem( OBJ.item.Item(i) )
            self.myMap.setEntry( (X + moveX)/const.blocksize, (Y + moveY)/const.blocksize, self.myMap.defaultBkgd)
            self.Display.redrawXMap(self.myMap, l)
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
    
    # takes enemy NPC object, dungeon level
    def launchBattle(self, enemyNpc, lD):
        #self.boxMessage("The battle is joined!")
        result = self.myBattle.fightBattle(self, enemy.enemy(enemyNpc.name, lD), self.gameBoard, enemyNpc.images, self.myHero.images)
        #result = self.myBattle.fightBattle(self, enemy.enemy(enemyNpc.name, lD), self.gameBoard )
        if result == 'escaped': # escaped from battle
            return False
        elif result == 'died': # died in battle
            self.gameOver()
        elif result == 'won': # won battle
            for item in self.myMenu.displayChest( self.getLoot(enemyNpc.name), 'Enemy Loot' ):
                msg = self.myHero.getItem(item)
                self.Ticker.tick(30)
                self.textMessage(msg)
            self.myHero.notchKill()
            # final boss
            if enemyNpc.name == 'Garden Badger':
                self.Director.advanceQuest(0)
                if self.Director.getQuestStatus(0) == 3:
                    self.boxMessage("Finished off those garden badgers, did ya? Garden Variety is more like it!")
            elif enemyNpc.name == 'Skeleton King':
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
        saveBall = (self.Ticker, self.myHero.getSaveBall(), self.myWorld.getWorldBall('game'), self.Director)
        return saveBall
    
    def updateSprites(self):
        if self.myMap.type in const.darkMaps:
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
            if not n.moveQueue.isEmpty():
                n.move( n.moveFromQueue(), self.myMap, self.myMap.getPlayerXY() )
                redraw = True
            else:
                r = n.update(self.myMap, self.myHero.getXY() )
                if r == True:  # and n in self.visibleNPCs:
                    redraw = True
                elif r == 'battle':
                    self.myInterface.npcMessage( n.message, n.images[2] )
                    self.displayOneFrame()
                    if self.launchBattle(n, self.myWorld.currentMap.level):
                        self.removeNPC(n.getID())
                    else: n.confuse(30)
                
        return redraw
    
    def displayOneFrame(self):
        self.Display.redrawMap(self.myMap, self.myHero, self.gameBoard)
        #self.updateSprites()
        self.Display.displayOneFrame(self.myInterface, self.FX, self.gameBoard, self, self.myMap.type in const.darkMaps)

    def mainLoop(self):
        self.visibleNPCs = []
        if not self.Director.getEvent(0):
            self.myMenu.displayStory("So here you are in the same town, in front of the same house you've lived in forever. There's gotta be something else out there. It's time to go find it. Welcome to Ransack.")
            self.Director.setEvent(0)
        (pX, pY) = self.myHero.getXY()
        self.myMap.setPlayerXY( pX/const.blocksize, pY/const.blocksize )
        self.myMap.updateWindowCoordinates(self.myHero)
        self.Display.redrawXMap(self.myMap, 2)
        self.updateSprites()
        self.Display.drawSprites(self.myHero, self.myMap, self.gameBoard, self, animated=False)
        while self.gameOn:
            if not self.myHero.moveQueue.isEmpty():
                self.move( self.myHero.moveFromQueue() )
            else:
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
            pygame.time.wait(10)
            
        self.myInterface.state = 'mainmenu'
        return self.won
