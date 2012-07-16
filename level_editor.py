from pygame import *
from types import *
import pygame, os, pickle, random, eztext, const
from const import *
from IMG import images

from MAP import mapgen

from UTIL import queue

# Eztext courtesy of http://www.pygame.org/project-EzText-920-.html

#NSWE
CARDINALS = [ (0,-1), (0,1), (-1,0), (1,0) ]

def load_image(name, colorkey=None):
    fullname = os.path.join('IMG', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

class subMap():
    def __init__(self):
        self.DIMX = 4
        self.DIMY = 5
        self.maptext = []
        self.portal = (0,0)
        for i in range(DIMX):
            self.maptext += [0]*DIMY

class Map():
    
    def __init__(self, DIM=20):
        self.grid = []
        self.DIM = DIM
        for i in range(self.DIM):
            self.grid += [self.DIM*[0]]
        self.heroStart = None
        self.pointOfEntry = None
        self.pointOfExit = None
        self.portals = []
        self.chests = {}
    
    def setEntry(self, x, y, e):
        if e == HEROSTART:
            if self.heroStart == None:
                self.heroStart = (x,y)
            else:
                (px,py) = self.heroStart
                self.setEntry(px,py,0)
                self.heroStart = (x,y)
        if e == STAIRUP:
            if self.pointOfEntry == None:
                self.pointOfEntry = (x,y)
            else:
                (px,py) = self.pointOfEntry
                self.setEntry(px,py,0)
                self.pointOfEntry = (x,y)
        if e == STAIRDN:
            if self.pointOfExit == None:
                self.pointOfExit = (x,y)
            else:
                (px,py) = self.pointOfExit
                self.setEntry(px,py,0)
                self.pointOfExit = (x,y)
        self.grid[y] = self.grid[y][:x] + [e] + self.grid[y][x+1:]
    
    def getEntry(self, x, y):
        if x in range(self.DIM) and y in range(self.DIM):
            return self.grid[y][x]
        else:
            return -1
    
    def getGrid(self):
        return self.grid
    
    def installBall(self, ball):
        (grid, poe, poex, hs, chests) = ball
        self.grid = grid
        self.heroStart = hs
        self.pointOfEntry = poe
        self.pointOfExit = poex
        self.chests = chests
    
    def getMapBall(self):
        return (self.grid, self.pointOfEntry, self.pointOfExit, self.heroStart, self.chests)
    
    
    def changeDimensions(self, nDim):
        # expanding
        if nDim > self.DIM:
            for i in range(nDim):
                if i < self.DIM:
                    self.grid[i] = self.grid[i] + [0]*(nDim-self.DIM)
                else: self.grid.append( [0]*nDim )
        #shrinking
        elif self.DIM > nDim:
            self.grid = self.grid[:nDim]
            for i in range(nDim):
                self.grid[i] = self.grid[i][:nDim]
        #same
        else: return
        self.DIM = nDim
        self.cursorPos = (0,0)

class Handler():
    
    def __init__(self, cPos):
        self.cursorPos = cPos
        self.currentTile = 0
        self.sideImg, sideRect = load_image('sidebar.bmp')
        self.drawMode = False
        self.cursorColor = white
        self.offset = 0
        self.numImages = len(images.mapImages)
        self.topX = 0
        self.topY = 0
        self.visited = []
        
        self.BFSQueue = queue.Queue()
    
    def drawBox(self, pos, color):
        (x,y) = pos
        boxPoints = ( (x,y), (x,y+blocksize), (x+blocksize,y+blocksize), (x+blocksize,y) )
        pygame.draw.lines( gridField, color, True, boxPoints, 1 )

    def switchTile(self):
        self.currentTile += 1
        self.currentTile = self.currentTile % self.numImages
    
    def flatten(self, x):
        result = []
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, basestring) and type(el) is not TupleType and type(el) is not NoneType:
                result.extend(self.flatten(el))
            elif type(el) is TupleType:
                result.append(el)
        return result
    
    #@tail_call_optimized
    def floodFillBFS(self,pieceLocation):
        if (pieceLocation == None):
            return
        (x,y) = pieceLocation
        entryList = []
        for (Cx,Cy) in CARDINALS:
            if (myMap.getEntry(x,y) == myMap.getEntry(x+Cx,y+Cy) and (x+Cx,y+Cy) not in self.visited and ~self.BFSQueue.has( (x+Cy, y+Cy) ) ):
                self.BFSQueue.push( (x+Cx, y+Cy) )
                entryList += [ (x+Cx,y+Cy) ]
                self.visited += [ (x+Cx,y+Cy) ]
            else:
                entryList += [ None ]
        if ( entryList == [None,None,None,None] ):
            return (x,y)
        else:
            return [ (x, y) ] + [ self.floodFillBFS(self.BFSQueue.pop()) ] + [self.floodFillBFS(self.BFSQueue.pop()) ] + [self.floodFillBFS(self.BFSQueue.pop()) ] + [self.floodFillBFS(self.BFSQueue.pop()) ]
            #return [ (x,y) ] + [self.floodFillBFS(entryList[0])] + [self.floodFillBFS(entryList[1])] + [self.floodFillBFS(entryList[2])] + [self.floodFillBFS(entryList[3])]

    def floodFill(self, tile, start):
        (x,y) = start
        x = x / blocksize
        y = y / blocksize
        self.visited = [ (x,y) ]
        self.BFSQueue.reset()
        floodArea = self.flatten( self.floodFillBFS( (x,y) ) )
        floodArea = list( set(floodArea) )
        for entry in floodArea:
            (x,y) = entry
            myMap.setEntry(x,y,tile)
    
    def getInput(self, msg):
        #get file name
        input = None
        txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt=msg)
        inputWindow = pygame.Surface( (300,100) )
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
                if event.type == KEYDOWN:
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
    
    def getFilename(self):
        return self.getInput('Enter filename: ')
    
    def saveMap(self):
        filename = self.getFilename()
        ball = myMap.getMapBall()
        try:
            save = open(filename, "w")
            pickle.dump(ball, save)
            save.close()
        except pygame.error, message:
            print 'Cannot save map:', name
            raise SystemExit, message
    
    def loadMap(self):
        filename = self.getFilename()
        try:
            save = open(filename, "r")
            ball = pickle.load(save)
            save.close()
            myMap.installBall(ball)
        except pygame.error, message:
            print 'Cannot load map:', name
            raise SystemExit, message
    
    def generateMap(self, rooms):
        newMap = mapgen.Map(myMap.DIM)
        newMap.generateMap(rooms)
        myMap.installBall( newMap.getMapBall() )

    def event_handler(self, event):
        (x,y) = self.cursorPos
        self.drawBox( (x,y), black)
        if event.key == pygame.K_RIGHT:
            if( x+blocksize < myMap.DIM*blocksize ):
                x += blocksize
            if x < myMap.DIM*blocksize and x == 20*blocksize + self.topX*blocksize:
                self.topX += 1
        if event.key == pygame.K_LEFT:
            if( x-blocksize >= 0 ):
                x -= blocksize
            if x > 0 and x == self.topX*blocksize:
                self.topX -= 1
        if event.key == pygame.K_UP:
            if( y-blocksize >= 0 ):
                y -= blocksize
            if y > 0 and y == self.topY*blocksize:
                self.topY -= 1
        if event.key == pygame.K_DOWN:
            if( y+blocksize < myMap.DIM*blocksize ):
                y += blocksize
            if y < myMap.DIM*blocksize and y == 20*blocksize + self.topY*blocksize:
                self.topY += 1
        if event.key == pygame.K_t:
            self.switchTile()
        if event.key == pygame.K_SPACE:
            myMap.setEntry(x/blocksize,y/blocksize,self.currentTile)
        if event.key == pygame.K_ESCAPE:
            os.sys.exit()
        if event.key == pygame.K_d:
            self.drawMode = not self.drawMode
        if event.key == pygame.K_s:
            self.saveMap()
        if event.key == pygame.K_l:
            self.loadMap()
        if event.key == pygame.K_f:
            self.floodFill(self.currentTile, (x,y) )
        if event.key == pygame.K_g:
            self.generateMap( int ( self.getInput('Enter number of rooms: ') ))
        if event.key == pygame.K_c:
            myMap.changeDimensions( int ( self.getInput('Enter new dimension: ') ))
        if event.key == pygame.K_e:
            self.offset += 32
            if self.offset == 128:
                self.offset = 0
        if self.drawMode:
            myMap.setEntry(x/blocksize,y/blocksize,self.currentTile)
        self.cursorPos = (x,y)
        print self.topX, self.topY
    
    def mouseHandler(self, e):
        (mx, my) = pygame.mouse.get_pos()
        if 0 <= mx < 600 and 0 <= my < 600:
            myMap.setEntry(mx/blocksize,my/blocksize,self.currentTile)
            self.cursorPos = ( (mx/blocksize)*blocksize, (my/blocksize)*blocksize )
        if 650 <= mx < 770 and 200 <= my < 440:
            self.currentTile = self.offset + (mx-650)/blocksize + (my-200)/blocksize * 4
        
    
    def mouseUpdate(self):
        (mx, my) = pygame.mouse.get_pos()
        if 650 <= mx < 770 and 200 <= my < 440:
            boxPoints = ( (mx,my), (mx,my+blocksize), (mx+blocksize,my+blocksize), (mx+blocksize,my) )
            pygame.draw.lines( screen, red, True, boxPoints, 1 )
    
    def updateDisplay(self):
        gridField.fill(black)
        for i in range(self.topX, self.topX+20):
            for j in range(self.topY, self.topY+20):
                gridField.blit( images.mapImages[myMap.getEntry(i,j)], ( (i-self.topX)*blocksize,(j-self.topY)*blocksize) )
        (x,y) = self.cursorPos
        x = x - self.topX*blocksize
        y = y - self.topY*blocksize
        if self.drawMode:
            self.cursorColor = yellow
        else:
            self.cursorColor = white
        boxPoints = ( (x,y), (x,y+blocksize), (x+blocksize,y+blocksize), (x+blocksize,y) )
        pygame.draw.lines( gridField, self.cursorColor, True, boxPoints, 1 )
        self.sideImg, sideRect = load_image('sidebar.bmp')
        self.sideImg.blit(images.mapImages[self.currentTile],(50,50))
        for i in range(8):
            for j in range(4):
                self.sideImg.blit(images.mapImages[self.offset + j + (4*i)], (50+j*blocksize, 200+(i*blocksize)))
        
        (x,y) = self.cursorPos
        entryBox = pygame.Surface((30,30))
        entryBox.fill(black)
        if pygame.font:
            font = pygame.font.SysFont("arial",20)
            entry = font.render(str(myMap.getEntry( (x+self.topX)/blocksize, (y+self.topY)/blocksize)),1, white, black )
            entryBox.blit(entry,(0,0))
            self.sideImg.blit(entryBox,(80,50))
        if self.drawMode:
            msgBox = pygame.Surface( ( 186, 60 ) )
            msgBox.fill( grey )
            if pygame.font:
                font = pygame.font.SysFont("arial", 24)
                msgText = font.render( 'draw', 1, red, yellow )
                msgBox.blit(msgText, (10,10) )
            self.sideImg.blit( msgBox, (50,100) )
            #pygame.display.flip()
        screen.blit(self.sideImg, (600,0) )

# Set the height and width of the screen
size=[800,800]
screen=pygame.display.set_mode(size)

images.load()
pygame.init()
clock = pygame.time.Clock()

cursorPos = (0,0)

myMap = Map()
myHandler = Handler(cursorPos)

blocksize = 30

gridField = pygame.Surface( [DIM*blocksize, DIM*blocksize] )

os.sys.setrecursionlimit(15000)


def main():
    while True :
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                myHandler.event_handler(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                myHandler.mouseHandler(event)
            if event.type == pygame.QUIT:
                os.sys.exit()
        myHandler.mouseUpdate()
        myHandler.updateDisplay()
        screen.blit(gridField, (0,0) )
        pygame.display.flip()

main()