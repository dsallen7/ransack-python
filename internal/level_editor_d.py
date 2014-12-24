from types import *
import pygame, os, cPickle, random, gzip

from MAP import world, mapgen, mazegen, wilds, cavegen, tile
from DISPLAY import text
from UTIL import queue, const, colors, eztext, load_image, misc, button
from IMG import images, spritesheet
from math import floor, ceil
from SCRIPTS import npcScr, mapScr

from random import choice

# Eztext courtesy of http://www.pygame.org/project-EzText-920-.html
class Handler():
    
    def __init__(self, cPos):
        self.cursorPos = cPos
        self.currentTile = 0
        self.sideImg, sideRect = load_image.load_image('sidebar.bmp')
        self.npcImg = {}
        npcAvatar = pygame.Surface((const.blocksize, const.blocksize))
        for n in npcScr.npcList:
            npcImgFilename = n+'.bmp'
            npcImgs = images.loadNPC(npcImgFilename)
            self.npcImg[ n ] = npcImgs[2]
        #self.npcImg, npcR = load_image('npc.bmp')
        self.drawMode = False
        self.cursorColor = colors.white
        self.offset = 0
        self.numImages = len(mapImages)
        self.topX = 0
        self.topY = 0
        self.visited = []
        
        self.BFSQueue = queue.Queue()
        
        self.mouseAction = 'draw'
        self.drawLayers = ['fore', 'back']
        self.drawLayer = self.drawLayers[0]
        self.selecting = False
        
        self.selectBoxPoints = None
        
        self.placeNPC = False
        
        self.myMap = myWorld.currentMap
        
        self.editorImages = range(7)
        editorSpriteSheet = spritesheet.spritesheet('editorsheet.bmp')
        for i in range(7):
            self.editorImages[i] = editorSpriteSheet.image_at((i*const.blocksize, 0, const.blocksize, const.blocksize), -1 )
    
    def drawBox(self, pos, color):
        (x,y) = pos
        boxPoints = ( (x,y), (x,y+blocksize), (x+blocksize,y+blocksize), (x+blocksize,y) )
        pygame.draw.lines( gridField, color, True, boxPoints, 1 )

    def switchTile(self):
        self.currentTile += 1
        self.currentTile = self.currentTile % self.numImages
        
#    def drawTile(self, x, y):
    
    def addMap(self, name):
        myWorld.addMap(name, None)
    
    def addNPC(self, loc):
        npcWin = pygame.Surface((300,300))
        npcWin.fill(colors.black)
        for i in range( len( npcScr.npcList ) ):
            npcWin.blit( self.npcImg[ npcScr.npcList[i] ], ( (i%4)*blocksize, (i/4)*blocksize))
        screen.blit(npcWin, (100,100) )
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mx, my) = event.pos
                    if 100 <= mx < 400 and 100 <= my < 400:
                        self.myMap.NPCs.append( ( loc, 
                                                  npcScr.npcList[(mx-100)/blocksize + (my-100)/blocksize * 4], 
                                                  self.getInput('Enter message (optional): '),
                                                  self.getInput('Enter name (optional): ') ) )
                        return 
    
    def selectAccessory(self):
        accWin = pygame.Surface((100,100))
        accWin.fill(colors.black)
        for i in range( len( accImages ) ):
            accWin.blit( accImages[ i ], ( (i%4)*15, (i/4)*10))
        screen.blit(accWin, (100,100) )
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mx, my) = event.pos
                    if 100 <= mx < 400 and 100 <= my < 400:
                        return (mx-100)/15 + (my-100)/10 * 4
    
    def tileProperties(self, tile):
        (x, y) = tile
        
        while True:
            if self.myMap.getEntry(x,y) in range(const.TABLE1, const.TABLE3+1):
                infoWin = pygame.Surface((300,300))
            else: 
                infoWin = pygame.Surface((300,270))
            infoWin.fill(colors.black)
            if pygame.font:
                font = pygame.font.SysFont("arial",20)
                infoWin.blit( font.render('Foreground: '+str(self.myMap.getEntry(x, y) ), 1, colors.white, colors.black), (0, 0) )
                infoWin.blit( font.render('Background: '+str(self.myMap.getEntry(x, y) ), 1, colors.white, colors.black), (0, 30) )
                try:
                    p = self.myMap.grid[x][y].portal
                    if p == None:
                        p = '-'
                    else: p = p[0]+' at '+str(p[1])+', '+str(p[2])
                except AttributeError:
                    p = '-'
                infoWin.blit( font.render('Portal at: '+p, 1, colors.white, colors.black), (0, 60) )
                try:
                    s = self.myMap.grid[x][y].shopID
                    if s == None:
                        s = '-'
                    else: s = s[0]+' level '+str(s[1])
                except AttributeError:
                    s = '-'
                infoWin.blit( font.render('Shop: '+s, 1, colors.white, colors.black), (0, 90) )
                infoWin.blit( font.render('Reset Tile', 1, colors.white, colors.black), (0, 120) )
                if self.myMap.getEntry(x,y) in range(const.TABLE1, const.TABLE3+1):
                    try:
                        a = mapScr.accessoryList[ self.myMap.grid[x][y].accessory ]+'('+str(self.myMap.grid[x][y].accessory)+')'
                        if a == None:
                            a = '-'
                    except AttributeError:
                        a = '-'
                    except TypeError:
                        a = '-'
                    infoWin.blit( font.render('Accessory: '+a, 1, colors.white, colors.black), (0, 150) )
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mX, mY) = pygame.mouse.get_pos()
                    if 200 <= mX < 500 and 200 <= mY < 200 + infoWin.get_height():
                        Index = (mY-200)/30
                        if Index == 0:
                            self.myMap.setEntry( x, y, int( self.getInput('Enter tile FG: ') ) )
                        elif Index == 1:
                            self.myMap.setEntry( x, y, int( self.getInput('Enter tile BG: ') ) )
                        elif Index == 2:
                            self.myMap.grid[x][y].portal = ( self.getInput('Enter target map: '), 
                                                             int( self.getInput('Enter portal x: ') ), 
                                                             int( self.getInput('Enter portal y: ') ) )
                        elif Index == 3:
                            self.myMap.grid[x][y].shopID = ( self.getInput('Enter shop type: '), 
                                                             int( self.getInput('Enter level: ') ) )
                        elif Index == 4:
                            self.myMap.setEntry( x, y, const.DFLOOR1 )
                            self.myMap.grid[x][y].portal = None
                            self.myMap.grid[x][y].shopID = None
                            self.myMap.grid[x][y].accessory = None
                        elif Index == 5:
                            self.myMap.grid[x][y].accessory = ( self.selectAccessory() )
                    return
                if event.type == pygame.QUIT:
                    os.sys.exit()
                        
            screen.blit(infoWin, (200, 200) )
            pygame.display.flip()
    
    def removeMap(self):
        mapWin = pygame.Surface((200,420))
        mapWin.fill(colors.black)
        mapList = myWorld.getMapList()
        mapList.sort()
        if pygame.font:
            font = pygame.font.SysFont("arial",20)
            y_ = 0
            for map in mapList:
                mapWin.blit( font.render(map, 1, colors.white, colors.black), (0,y_) )
                y_ += 30
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mX, mY) = pygame.mouse.get_pos()
                    if 200 <= mX < 300 and 200 <= mY < 620:
                        mapIndex = (mY-200)/30
                        if mapIndex+1 <= len(mapList):
                            myWorld.removeMapByName( mapList[mapIndex] )
                    return
                if event.type == pygame.QUIT:
                    os.sys.exit()
                        
            screen.blit(mapWin, (200, 200) )
            pygame.display.flip()
    
    def switchMap(self):
        mapList = myWorld.getMapList()
        mapWin = pygame.Surface(( 200*(( len(mapList)/10) + 1 ), 900 ))
        mapWin.fill(colors.black)
        mapList.sort()
        mapB = []
        numRows = 20
        if pygame.font:
            font = pygame.font.SysFont("arial",20)
            y_ = 0
            x_ = 0
            for map in mapList:
                b = button.Button( ( 200+(((x_/numRows))*200), (y_*30)), map, os.getcwd()+"/FONTS/gothic.ttf", 14)
                mapB.append( b )
                mapWin.blit( b.img, ( ((x_/numRows))*200, (y_*30)) )
                y_ += 1
                x_ += 1
                y_ = y_ % numRows
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mX, mY) = pygame.mouse.get_pos()
                    for b in mapB:
                        (x, y) = pygame.mouse.get_pos()
                        if b.hit(x, y):
                            return myWorld.getMapByName( b.msg )
                if event.type == pygame.QUIT:
                    os.sys.exit()
            screen.blit(mapWin, (200, 0) )
            pygame.display.flip()
    
    def getMapInfo(self):
        
        while True:
            infoWin = pygame.Surface((300,330))
            infoWin.fill(colors.black)
            if pygame.font:
                font = pygame.font.SysFont("arial",20)
                infoWin.blit( font.render('Name: '+self.myMap.getName(), 1, colors.white, colors.black), (0,0) )
                infoWin.blit( font.render('Up: '+self.myMap.up[0], 1, colors.white, colors.black), (0,30) )
                if self.myMap.down[0] == 'dungeon':
                    infoWin.blit( font.render('Down: '+self.myMap.down[0]+' '+str(self.myMap.down[1]), 1, colors.white, colors.black), (0,60) )
                else: infoWin.blit( font.render('North: '+self.myMap.neighbors[0], 1, colors.white, colors.black), (0,90) )
                infoWin.blit( font.render('South: '+self.myMap.neighbors[1], 1, colors.white, colors.black), (0,120) )
                infoWin.blit( font.render('East: '+self.myMap.neighbors[2], 1, colors.white, colors.black), (0,150) )
                infoWin.blit( font.render('West: '+self.myMap.neighbors[3], 1, colors.white, colors.black), (0,180) )
                infoWin.blit( font.render('Type: '+self.myMap.type, 1, colors.white, colors.black), (0,210) )
                try:
                    if myWorld.initialMap.getName() == self.myMap.getName():
                        infoWin.blit( font.render('Initial: Yes', 1, colors.white, colors.black), (0,240) )
                    else: infoWin.blit( font.render('Initial: No', 1, colors.white, colors.black), (0,240) )
                except AttributeError:
                    infoWin.blit( font.render('Initial: No', 1, colors.white, colors.black), (0,240) )
                try:
                    infoWin.blit( font.render('Level: '+str(self.myMap.level), 1, colors.white, colors.black), (0,270) )
                except AttributeError:
                    infoWin.blit( font.render('Level: -', 1, colors.white, colors.black), (0,270) )
                infoWin.blit( font.render('Size: '+str(self.myMap.getDIM() ), 1, colors.white, colors.black), (0,300) )
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mX, mY) = pygame.mouse.get_pos()
                    if 200 <= mX < 400 and 200 <= mY < 530:
                        Index = (mY-200)/30
                        if Index == 0:
                            self.myMap.setName( self.getInput('Enter map name: ') )
                        elif Index == 1:
                            self.myMap.up = ( self.getInput('Enter name of map up: '), )
                        elif Index == 2:
                            mName = self.getInput('Enter name of map down: ')
                            if mName == 'dungeon':
                                self.myMap.down = ( mName, 
                                                int(self.getInput('Enter number of levels: ')),
                                                self.getInput('Enter name of map final map: ') )
                            else: self.myMap.down = (mName,)
                        elif Index == 3:
                            self.myMap.neighbors[0] = self.switchMap().getName()#self.getInput('Enter name of map north: ')
                        elif Index == 4:
                            self.myMap.neighbors[1] = self.switchMap().getName()#self.getInput('Enter name of map south: ')
                        elif Index == 5:
                            self.myMap.neighbors[2] = self.switchMap().getName()#self.getInput('Enter name of map east: ')
                        elif Index == 6:
                            self.myMap.neighbors[3] = self.switchMap().getName()#self.getInput('Enter name of map west: ')
                        elif Index == 7:
                            self.myMap.type = self.getInput('Enter map type: ')
                        elif Index == 8:
                            myWorld.initialMap = myWorld.getMapByName( self.myMap.getName() )
                        elif Index == 9:
                            self.myMap.level = int( self.getInput('Enter map level: ') )
                        elif Index == 10:
                            self.myMap.changeDimensions( int ( self.getInput('Enter new size: ') ))
                    return
                if event.type == pygame.QUIT:
                    os.sys.exit()
                        
            screen.blit(infoWin, (200, 200) )
            pygame.display.flip()
    
    def importMap(self):
        filename = self.getFilename()
        
        
    #@tail_call_optimized
    def floodFillBFS(self,pieceLocation):
        if (pieceLocation == None):
            return
        (x,y) = pieceLocation
        entryList = []
        for (Cx,Cy) in const.CARDINALS:
            if (self.myMap.getEntry(x,y) == self.myMap.getEntry(x+Cx,y+Cy) and (x+Cx,y+Cy) not in self.visited and ~self.BFSQueue.has( (x+Cy, y+Cy) ) ):
                self.BFSQueue.push( (x+Cx, y+Cy) )
                entryList += [ (x+Cx,y+Cy) ]
                self.visited += [ (x+Cx,y+Cy) ]
            else:
                entryList += [ None ]
        if ( entryList == [None,None,None,None] ):
            return (x,y)
        else:
            return [ (x, y) ] + [ self.floodFillBFS(self.BFSQueue.pop()) ] + [self.floodFillBFS(self.BFSQueue.pop()) ] + [self.floodFillBFS(self.BFSQueue.pop()) ] + [self.floodFillBFS(self.BFSQueue.pop()) ]

    def floodFill(self, tile, start):
        (x,y) = start
        x = x / blocksize
        y = y / blocksize
        self.visited = [ (x,y) ]
        self.BFSQueue.reset()
        floodArea = misc.flatten( self.floodFillBFS( (x,y) ) )
        floodArea = list( set(floodArea) )
        for entry in floodArea:
            (x,y) = entry
            self.place(x, y, tile)
            #self.myMap.setEntry(x,y,tile)
    
    def getInput(self, msg):
        #get file name
        input = None
        txtbx = eztext.Input(maxlength=300, color=(255,0,0), prompt=msg)
        inputWindow = pygame.Surface( (1200,100) )
        while input == None:
            # make sure the program is running at 30 fps
            clock.tick(30)

            # events for txtbx
            events = pygame.event.get()
            # process other events
            for event in events:
                # close it x button si pressed
                if event.type == pygame.QUIT:
                        os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input = txtbx.getValue()

            # clear the screen
            inputWindow.fill((25,25,25))
            # update txtbx
            txtbx.update(events)
            # blit txtbx on the sceen
            txtbx.draw(inputWindow)
            gridField.blit(inputWindow, (100,100) )
            screen.blit(gridField,(0,0))
            # refresh the display
            pygame.display.flip()
        return input
    
    def fillChest(self, chestItems):
        menuBox = pygame.Surface( (150, 350) )
        itemsList = range(const.FRUIT1, const.CERTIFICATE+1)+range(const.WSWORD, const.SSHIELD+1)
        print itemsList
        for i in range( len( itemsList ) ):
            menuBox.blit(mapImages[itemsList[i]], (15+((i)%4)*blocksize, 50+((i)/4)*blocksize))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return chestItems
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mx, my) = event.pos
                    if 115 <= mx < 235 and 150 <= my < 330:
                        itemNum = itemsList[(mx-115)/blocksize + (my-150)/blocksize * 4]
                        if itemNum in range(const.FRUIT1, const.GOLD):
                            chestItems.append( (itemNum, 1) )
                        elif itemNum == const.GOLD:
                            chestItems.append( (itemNum, int(self.getInput('Enter amount of gold: ')) ) )
                        elif itemNum == const.SPELLBOOK or itemNum == const.PARCHMENT:
                            chestItems.append( (itemNum, int(self.getInput('Enter spell number: ') ) ) )
                        elif itemNum == const.CERTIFICATE:
                            chestItems.append( (itemNum, int(self.getInput('Enter type save(0) or return(1): ') ) ) )
                        elif itemNum in range(const.WSWORD, const.RING): #weapon
                            chestItems.append( (itemNum,
                                                [ int(self.getInput("Enter plus Str: ")),
                                                  int(self.getInput("Enter plus Int: ")),
                                                  int(self.getInput("Enter plus Dex "))   ] ) )
                        elif itemNum == const.RING:
                            chestItems.append( (itemNum, 
                                                (self.getInput("Enter enhancement type (plusHP, plusMP, plusWP): "),
                                                int(self.getInput("Enter enhancement level: ")) ) ) )
                        elif itemNum in range(const.HELMET, const.SSHIELD+1): #armor
                            chestItems.append( (itemNum, self.getInput("Enter resist: ") ) )
            for item in chestItems:
                menuBox.blit(mapImages[ item[0] ], (len(chestItems)*blocksize, 15) )
            screen.blit(menuBox, (100,100) )
            pygame.display.flip()
    
    def getFilename(self):
        return self.getInput('Enter filename: ')
    
    def saveMap(self):
        filename = self.getFilename()
        ball = self.myMap.getMapBall()
        try:
            save = gzip.GzipFile(os.getcwd()+'/MAP/LEVELS/'+filename, 'wb')
            cPickle.dump(ball, save)
            save.close()
        except IOError, message:
            print 'Cannot load map:', filename
            return
    
    def loadMap(self, filename=None):
        if filename == None:
            filename = self.getFilename()
        try:
            save = gzip.GzipFile(os.getcwd()+'/MAP/LEVELS/'+filename, 'rb')
            ball = cPickle.load(save)
            save.close()
            self.myMap.installBall(ball)
        except IOError, message:
            print 'Cannot load map:', filename
            return
    
    def saveWorld(self):
        filename = self.getFilename()
        self.boxMessage('Saving'+filename+' ...')
        ball = myWorld.getWorldBall('editor')
        try:
            self.boxMessage('Opening zipfile '+filename+' ...')
            #save = gzip.GzipFile(os.getcwd()+'../assets/WORLDS/'+filename, 'wb', 1)
            save = open('../assets/WORLDS/'+filename, "w")
            self.boxMessage('Dumping saveball '+filename+' ...')
            cPickle.dump(ball, save)
            self.boxMessage('Closing zipfile '+filename+' ...')
            save.close()
        except IOError, message:
            print 'Cannot load world:', filename
            return
    def loadWorld(self):
        filename = self.getFilename()
        self.boxMessage('Loading'+filename+' ...')
        try:
            self.boxMessage('Opening zipfile of '+filename+' ...')
            #loadedWorld = gzip.GzipFile(os.getcwd()+'../assets/WORLDS/'+filename, 'rb', 1)
            loadedWorld = open('../assets/WORLDS/'+filename, "r")
            self.boxMessage('Unpickling '+filename+' ...')
            ball = cPickle.load(loadedWorld)
            self.boxMessage('Closing zipfile of '+filename+' ...')
            loadedWorld.close()
            myWorld.installWorldBall('editor', ball)
            self.myMap = myWorld.getMapByName( ball[1] )
        except IOError, message:
            print 'Cannot load world:', filename
            return
    
    def boxMessage(self, message):
        
        msgText = text.Text(message, os.getcwd()+"/FONTS/devinne.ttf", 18, colors.white, colors.gold, True)
        for i in range( 0, 255, 8 ):
            borderBox = pygame.Surface( ( msgText.get_width(), msgText.get_height() ) )
            borderBox.fill( colors.grey )
            borderBox.set_alpha( int(ceil(i*0.1)) )
            msgText.set_alpha(i)
            screen.blit( borderBox, 
                            ( screen.get_width()/2-borderBox.get_width()/2, 150 ) )
            screen.blit( msgText, 
                            ( screen.get_width()/2-borderBox.get_width()/2, 150 ) )
            pygame.display.flip()
            
        #while (pygame.event.wait().type != pygame.MOUSEBUTTONDOWN): pass

    def generateMap(self, type, trials=1):
        level = int( self.getInput('Enter level: ') )
        if type == 'dungeon':
            rooms = int( self.getInput('Enter # of rooms (max 20): ') )
            for i in range(trials):
                MG = mapgen.Generator(self.myMap.getDIM(), level)
                MG.generateMap(rooms)
                self.myMap.installBall( MG.getMapBall( ) )
        elif type == 'maze':
            MG = mazegen.Generator(self.myMap.getDIM(), level)
            MG.generateMap()
            self.myMap.installBall( MG.getMapBall() )
        elif type == 'wilds':
            MG = wilds.Generator(self.myMap.getDIM(), level)
            MG.generateMap( self.getInput('Enter orientation (h)orizontal or (v)ertical: ') )
            self.myMap.installBall( MG.getMapBall() )
        elif type == 'cave':
            MG = cavegen.Generator(self.myMap.getDIM(), level)
            MG.generateMap()
            self.myMap.installBall( MG.getMapBall() )
        else:
            print 'Invalid map type'
    
    def place(self, x, y, nTile):
        if self.myMap.getEntry(x,y) == const.VOID:
            self.myMap.grid[x] = self.myMap.grid[x][:y]+[tile.Tile(x,y,nTile,const.DFLOOR1)]+self.myMap.grid[x][y+1:]
            return
        if self.placeNPC:
            self.addNPC( (x,y) )
        else:
            if self.drawLayer == 'back':
                self.myMap.setTileBG(x, y, nTile)
                return
            if self.currentTile == const.CHEST:
                self.myMap.addChest( (x, y), self.fillChest( [] ))
                param=None
            elif self.currentTile == const.SIGN:
                param = self.getInput('Sign text: ')
            elif self.currentTile in const.doorsList:
                param=None
            else: param=None
            self.myMap.setEntry(x, y, nTile, param)
        
    def removeNPC(self, x, y):
        for n in self.myMap.NPCs:
            if n[0] == (x, y):
                self.myMap.NPCs.remove(n)
                return
        
    def event_handler(self, event):
        (x,y) = self.cursorPos
        self.drawBox( (x,y), colors.black)
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            count = 5
        else:
            count = 1
        if event.key == pygame.K_RIGHT:
            for i in range(count):
                if( x+blocksize < self.myMap.DIM*blocksize ):
                    x += blocksize
                if x < self.myMap.DIM*blocksize and x == 20*blocksize + self.topX*blocksize:
                    self.topX += 1
                if self.drawMode:
                    self.place(x/blocksize,y/blocksize,self.currentTile)
                self.cursorPos = (x,y)
        elif event.key == pygame.K_LEFT:
            for i in range(count):
                if( x-blocksize >= 0 ):
                    x -= blocksize
                if x > 0 and x == self.topX*blocksize:
                    self.topX -= 1
                if self.drawMode:
                    self.place(x/blocksize,y/blocksize,self.currentTile)
                self.cursorPos = (x,y)
        elif event.key == pygame.K_UP:
            for i in range(count):
                if( y-blocksize >= 0 ):
                    y -= blocksize
                if y > 0 and y == self.topY*blocksize:
                    self.topY -= 1
                if self.drawMode:
                    self.place(x/blocksize,y/blocksize,self.currentTile)
                self.cursorPos = (x,y)
        elif event.key == pygame.K_DOWN:
            for i in range(count):
                if( y+blocksize < self.myMap.DIM*blocksize ):
                    y += blocksize
                if y < self.myMap.DIM*blocksize and y == 20*blocksize + self.topY*blocksize:
                    self.topY += 1
                if self.drawMode:
                    self.place(x/blocksize,y/blocksize,self.currentTile)
                self.cursorPos = (x,y)
        elif event.key == pygame.K_p:
            self.loadMap()
        elif event.key == pygame.K_t:
            self.saveMap()
        elif event.key == pygame.K_SPACE:
            self.place(x/blocksize, y/blocksize, self.currentTile)
        elif event.key == pygame.K_ESCAPE:
            os.sys.exit()
        elif event.key == pygame.K_d:
            self.drawMode = not self.drawMode
        elif event.key == pygame.K_s:
            self.saveWorld()
        elif event.key == pygame.K_l:
            self.loadWorld()
        elif event.key == pygame.K_r:
            self.removeMap()
        elif event.key == pygame.K_f:
            self.floodFill(self.currentTile, (x,y) )
        elif event.key == pygame.K_g:
            #self.generateMap( self.getInput('Enter type: dungeon, maze or wilds :'), int(self.getInput('Enter number of trials :')) )
            self.generateMap( self.getInput('Enter type: dungeon, maze, wilds, or cave:') )
        elif event.key == pygame.K_e:
            self.offset += 32
            if self.offset == 256:
                self.offset = 0
        elif event.key == pygame.K_x:
            self.removeNPC( x/blocksize, y/blocksize )
        elif event.key == pygame.K_n:
            print 'NPCs: '
            print self.myMap.NPCs
        elif event.key == pygame.K_i:
            self.getMapInfo()
        elif event.key == pygame.K_m:
            myWorld.currentMap = self.switchMap()
            self.myMap = myWorld.currentMap
            self.cursorPos = (0,0)
            self.topX = 0
            self.topY = 0
        elif event.key == pygame.K_a:
            self.addMap( self.getInput('Enter title of new map: ') )
        elif event.key == pygame.K_c:
            filename = self.getInput('Enter filename for screenshot: ')+".bmp"
            self.updateDisplay('field')
            pygame.image.save(gridField, filename)
        elif event.key == pygame.K_p:
            self.importMap( self.getInput('Enter filename of map: ') )
        elif event.key == pygame.K_RETURN:
            if self.myMap.getEntry(x/blocksize, y/blocksize) == const.CHEST:
                self.fillChest( self.myMap.chests[ (x/blocksize, 
                                                    y/blocksize) ] )
            else: self.tileProperties( (x/blocksize, y/blocksize) )
        elif event.key == pygame.K_PLUS:
            self.currentTile += 1
        elif event.key == pygame.K_MINUS:
            self.currentTile -= 1
        
        # special
        elif event.key == pygame.K_q:
            self.randomTrees()
    
    def select(self, start):
        startX, startY = start
        endX = startX
        endY = startY
        self.selectBoxPoints = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.selectBox = self.selectBoxPoints
                    return (endX, endY)
                elif event.type == pygame.MOUSEMOTION:
                    (tempX, tempY) = pygame.mouse.get_pos()
                    '''
                    if tempX > 600:
                        tempX = 600
                        #pygame.mouse.set_pos([tempX,tempY])
                    if tempY > 600:
                        tempY = 600
                        #pygame.mouse.set_pos([tempX,tempY])
                    '''
                    endX = tempX/blocksize + 1
                    endY = tempY/blocksize + 1
                    #self.updateDisplay()
                    self.selectBoxPoints = ( (startX*blocksize,startY*blocksize), 
                                              (startX*blocksize,(startY+(endY-startY))*blocksize), 
                                              (endX*blocksize,endY*blocksize), 
                                              ((startX+(endX-startX))*blocksize,startY*blocksize) )
                    pygame.draw.lines( gridField, colors.red, True, self.selectBoxPoints, 1 )
                    screen.blit(gridField, (0,0) )
                    pygame.display.flip()
    
    def move(self, start):
        (p1, p2, p3, p4) = self.selectBoxPoints
        sX, sY = start
        xDim = (p3[0]-p1[0])/blocksize
        yDim = (p3[1]-p1[1])/blocksize
        (tempX, tempY) = pygame.mouse.get_pos()
        xOffset = (tempX/blocksize)-(p1[0]/blocksize)
        yOffset = (tempY/blocksize)-(p1[1]/blocksize)
        oldTopX = ( (tempX/blocksize)-xOffset )
        oldTopY = ( (tempY/blocksize)-yOffset )
        newTopX = None
        newTopY = None
        selectionImg = pygame.Surface( (xDim*blocksize, yDim*blocksize) )
        emptyImg = pygame.Surface( (xDim*blocksize, yDim*blocksize) )
        for i in range(xDim):
            for j in range(yDim):
                selectionImg.blit( mapImages[ self.myMap.getEntry(oldTopX+i, oldTopY+j) ], (i*blocksize, j*blocksize) )
                emptyImg.blit( mapImages[ 0 ], (i*blocksize, j*blocksize) )
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if newTopX == None or newTopY == None:
                        return
                    else:
                        self.myMap.mapMove( (sX/blocksize, sY/blocksize), ( xDim, yDim ), (newTopX, newTopY) )
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    return
                elif event.type == pygame.MOUSEMOTION:
                    (tempX, tempY) = pygame.mouse.get_pos()
                    # upper left hand corner
                    newTopX = ( (tempX/blocksize)-xOffset )
                    newTopY = ( (tempY/blocksize)-yOffset )
                    oldTopX = p1[0]/blocksize
                    oldTopY = p1[1]/blocksize
                    if oldTopX == newTopX and oldTopY == newTopY :
                        pass
                    elif 0 <= newTopX*blocksize and (newTopX+ ((p3[0]-p1[0])/blocksize) )*blocksize < 1200 and 0 <= newTopX*blocksize and (newTopY+ ((p3[1]-p1[1])/blocksize) )*blocksize < 1200:
                        self.selectBoxPoints = ( (newTopX*blocksize,newTopY*blocksize), 
                                                 (newTopX*blocksize,(newTopY+ ((p3[1]-p1[1])/blocksize) )*blocksize), 
                                                 ((newTopX+ ((p3[0]-p1[0])/blocksize) )*blocksize,(newTopY+ ((p3[1]-p1[1])/blocksize) )*blocksize), 
                                                 ((newTopX+ ((p3[0]-p1[0])/blocksize) )*blocksize,newTopY*blocksize) )
                        (p1, p2, p3, p4) = self.selectBoxPoints
                        self.updateDisplay('field')
                        gridField.blit( emptyImg, (sX*blocksize, sY*blocksize) )
                        gridField.blit( selectionImg, (newTopX*blocksize, newTopY*blocksize) )
                        pygame.draw.lines( gridField, colors.red, True, self.selectBoxPoints, 1 )
                        screen.blit(gridField, (0,0) )
                        pygame.display.flip()
    def randomTrees(self):
        for i in range(self.myMap.getDIM() ):
            for j in range(self.myMap.getDIM() ):
                if self.myMap.getEntry(i, j) in mapScr.pines:
                    self.myMap.setEntry(i, j, choice(mapScr.pines) )

    def mouseHandler(self, e):
        (mx, my) = e.pos
        if 0 <= mx < gridField.get_width() and 0 <= my < gridField.get_height():
            if e.button == 1:
                #self.drawTile( mx/blocksize, my/blocksize )
                if self.mouseAction == 'draw':
                    self.place(mx/blocksize, my/blocksize, self.currentTile)
                    self.cursorPos = ( (mx/blocksize)*blocksize, (my/blocksize)*blocksize )
                elif self.mouseAction == 'select':
                    if self.selectBoxPoints is not None:
                        (p1, p2, p3, p4) = self.selectBoxPoints
                        if p1[0] <= mx < p3[0] and p1[1] <= my < p3[1]:
                            self.move( (p1[0], p1[1]) )
                        else: 
                            self.selectBoxPoints = None
                            self.cursorPos = ( (mx/blocksize)*blocksize, (my/blocksize)*blocksize )
                    else: self.selection = ( (mx/blocksize, my/blocksize), self.select( (mx/blocksize, my/blocksize) ) )
            elif e.button == 3:
                pass
        elif gridField.get_width()+80 <= mx < gridField.get_width()+180 and 130 <= my < 180:
            self.drawLayers = [self.drawLayers[1]]+[self.drawLayers[0]]
            self.drawLayer = self.drawLayers[0]
        elif gridField.get_width()+50 <= mx < gridField.get_width()+80 and 170 <= my < 200: #NPC placement
            self.placeNPC = not self.placeNPC
        elif gridField.get_width()+50 <= mx < gridField.get_width()+170 and 200 <= my < 440:  
            if e.button == 1:
                self.currentTile = ( self.offset + (mx-gridField.get_width()-45)/blocksize + (my-200)/blocksize * 4 ) #change FG tile
            elif e.button == 3: self.myMap.defaultBkgd = ( self.offset + (mx-gridField.get_width()-45)/blocksize + (my-200)/blocksize * 4 ) #change BG tile
        elif gridField.get_width()+65 <= mx < gridField.get_width()+95 and 500 <= my < 530: # flip through pages
            self.offset -= 32
            if self.offset < 0:
                self.offset = 224
        elif gridField.get_width()+95 <= mx < gridField.get_width()+125 and 500 <= my < 530:
            self.offset += 32
            if self.offset == 256:
                self.offset = 0
        elif gridField.get_width()+50 <= mx < gridField.get_width()+80 and 530 <= my < 560:
            self.myMap.mapCut()
        elif gridField.get_width()+80 <= mx < gridField.get_width()+110 and 530 <= my < 560:
            self.myMap.mapPaste( self.cursorPos )
        elif gridField.get_width()+110 <= mx < gridField.get_width()+140 and 530 <= my < 560:
            self.myMap.mapCopy(self.selection[0],self.selection[1])
        elif gridField.get_width()+65 <= mx < gridField.get_width()+95 and 560 <= my < 590:
            self.mouseAction = 'draw'
        elif gridField.get_width()+95 <= mx < gridField.get_width()+125 and 560 <= my < 590:
            self.mouseAction = 'select'
        
    
    def mouseUpdate(self):
        (mx, my) = pygame.mouse.get_pos()
        if 650 <= mx < 770 and 200 <= my < 440:
            boxPoints = ( (mx,my), (mx,my+blocksize), (mx+blocksize,my+blocksize), (mx+blocksize,my) )
            pygame.draw.lines( screen, colors.red, True, boxPoints, 1 )
    
    def updateDisplay(self, type='all'):
        if type in ['all', 'field']:
            gridField.fill(colors.black)
            for i in range(self.topX, self.topX+40):
                for j in range(self.topY, self.topY+40):
                    fTile = self.myMap.getTileFG(i, j)
                    bTile = self.myMap.getTileBG(i, j)
                    if fTile in const.SOLIDS:
                        if bTile is not None:
                            gridField.blit( mapImages[bTile], ( (i-self.topX)*blocksize,(j-self.topY)*blocksize) )
                        else: gridField.blit( mapImages[self.myMap.defaultBkgd], ( (i-self.topX)*blocksize,(j-self.topY)*blocksize) )
                    gridField.blit( mapImages[fTile], ( (i-self.topX)*blocksize,(j-self.topY)*blocksize) )
                    if fTile in range(const.TABLE1, const.TABLE3+1):
                        try:
                            gridField.blit( accImages[self.myMap.grid[i][j].accessory], ( (i-self.topX)*blocksize+10,
                                                                                          (j-self.topY)*blocksize+5) )
                        except AttributeError:
                            pass
                        except TypeError:
                            pass
                    if (i,j) == self.myMap.heroStart:
                        gridField.blit( mapImages[const.HEROSTART], ( (i-self.topX)*blocksize,(j-self.topY)*blocksize) )
                    if self.myMap.shops is not None:
                        for s in self.myMap.shops:
                            (sX, sY) = s
                            (imgN, ht) = mapScr.siteImgDict[ self.myMap.shops[s][0] ]
                            gridField.blit( mapImages[ imgN ], (sX*blocksize - blocksize - (self.topX * blocksize), sY*blocksize - ( ht*blocksize) - (self.topY * blocksize) ) )
            for n in self.myMap.NPCs:
                (x,y) = n[0]
                try:
                    gridField.blit(self.npcImg[ n[1] ], ((x-self.topX)*blocksize, (y-self.topY)*blocksize) )
                except KeyError:
                    gridField.blit(self.npcImg[ 'duke' ], ((x-self.topX)*blocksize, (y-self.topY)*blocksize) )
            (x,y) = self.cursorPos
            x = x - self.topX*blocksize
            y = y - self.topY*blocksize
            if self.drawMode:
                self.cursorColor = colors.yellow
            else:
                self.cursorColor = colors.white
            if self.selectBoxPoints is not None:
                pygame.draw.lines( gridField, colors.red, True, self.selectBoxPoints, 1 )
    
            boxPoints = ( (x,y), (x,y+blocksize), (x+blocksize,y+blocksize), (x+blocksize,y) )
            pygame.draw.lines( gridField, self.cursorColor, True, boxPoints, 1 )
        if type in ['all', 'bar']:
            self.sideImg, sideRect = load_image.load_image('sidebar.bmp')
            
            if self.placeNPC: self.sideImg.blit(self.npcImg['duke'],(50,50))
            else: self.sideImg.blit(mapImages[self.currentTile],(50,50))
            
            if pygame.font:
                font = pygame.font.SysFont("arial",12)
            
            self.sideImg.blit(mapImages[self.myMap.defaultBkgd],(50,130))
            self.sideImg.blit( font.render(self.drawLayer, 1, colors.white, colors.black ), (80,130) )
            
            if self.mouseAction == 'draw':
                self.sideImg.blit(self.editorImages[5], (50,80) )
            else: self.sideImg.blit(self.editorImages[6], (50,80) )
            self.sideImg.blit(self.npcImg['duke'], (50,170) )
            for i in range(8):
                for j in range(4):
                    self.sideImg.blit(mapImages[self.offset + j + (4*i)], (50+j*blocksize, 200+(i*blocksize)))
            
            toolBox = pygame.Surface( (90, 90) )
            toolBox.blit( self.editorImages[0], (15,0) )
            toolBox.blit( self.editorImages[1], (45,0) )
            toolBox.blit( self.editorImages[2], (0,30) )
            toolBox.blit( self.editorImages[3], (30,30) )
            toolBox.blit( self.editorImages[4], (60,30) )
            toolBox.blit( self.editorImages[5], (15,60) )
            toolBox.blit( self.editorImages[6], (45,60) )
            self.sideImg.blit(toolBox, (50,500) )
            (x,y) = self.cursorPos
            entryBox = pygame.Surface((150,30))
            entryBox.fill(colors.black)
            entry = font.render(str(self.myMap.getEntry( (x+self.topX)/blocksize, (y+self.topY)/blocksize))+' '+'x:'+str(x)+'('+str(x/blocksize)+')'+' y:'+str(y)+'('+str(y/blocksize)+')',1, colors.white, colors.black )
            entryBox.blit(entry,(0,0))
            self.sideImg.blit(entryBox,(50,450))
            if self.drawMode:
                msgBox = pygame.Surface( ( 186, 60 ) )
                msgBox.fill( colors.grey )
                if pygame.font:
                    font = pygame.font.SysFont("arial", 24)
                    msgText = font.render( 'draw', 1, colors.red, colors.yellow )
                    msgBox.blit(msgText, (10,10) )
                self.sideImg.blit( msgBox, (50,100) )
                #pygame.display.flip()
            screen.blit(self.sideImg, (1200,0) )
    

# Set the height and width of the screen
size=[1400,800]
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Ransack Level Editor")

images.load()
mapImages = images.mapImages
accImages = images.accessories

pygame.init()
pygame.key.set_repeat(50, 100)
clock = pygame.time.Clock()

cursorPos = (0,0)

#self.myMap = map.edMap()
myWorld = world.World('editor')
myHandler = Handler(cursorPos)

blocksize = 30

gridField = pygame.Surface( [2*const.DIM*blocksize, 2*const.DIM*blocksize] )

os.sys.setrecursionlimit(15000)


def main():
    myHandler.updateDisplay('all')
    screen.blit(gridField, (0,0) )
    pygame.display.flip()
    while True :
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                myHandler.event_handler(event)
                myHandler.updateDisplay('all')
                screen.blit(gridField, (0,0) )
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:# or event.type == pygame.MOUSEBUTTONUP:
                myHandler.mouseHandler(event)
                myHandler.mouseUpdate()
                myHandler.updateDisplay('all')
                screen.blit(gridField, (0,0) )
                pygame.display.flip()
            if event.type == pygame.QUIT:
                os.sys.exit()
        pygame.time.wait(10)
        #myHandler.updateDisplay()

main()
