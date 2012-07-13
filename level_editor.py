from pygame import *
from types import *
import pygame, os, pickle, random, eztext, const
from const import *
from IMG import images

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

DIM = 20

# Define the colors we will use in RGB format
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]
yellow = [127, 127, 0]
grey = [32, 32, 32]


class Map():
    
    def __init__(self):
        self.grid = []
        for i in range(DIM):
            self.grid += [DIM*[0]]
        self.heroStart = None
        self.pointOfEntry = None
        self.pointOfExit = None
    
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
        if x in range(DIM) and y in range(DIM):
            return self.grid[y][x]
        else:
            return -1
    
    def getGrid(self):
        return self.grid
    
    def installBall(self, ball):
        (grid, hs, poe, poex, ssidx) = ball
        self.grid = grid
        self.heroStart = hs
        self.pointOfEntry = poe
        self.pointOfExit = poex
        myHandler.selectSheet(ssidx)
    
    def getMapBall(self):
        return (self.grid, self.heroStart, self.pointOfEntry, self.pointOfExit, myHandler.ss_idx)

class Handler():
    
    def __init__(self, cPos):
        self.cursorPos = cPos
        self.currentTile = 0
        self.sideImg, sideRect = load_image('sidebar.bmp')
        self.drawMode = False
        self.cursorColor = white
        self.ss_idx = 0
        self.sslist = [images.mapImages, images.villageImages]
        
        self.tileSheet = self.sslist[self.ss_idx]
        
        self.numImages = len(self.tileSheet)
        
        self.visited = []
        
        self.BFSQueue = queue.Queue()
    
    def selectSheet(self, sheet):
        self.ss_idx = sheet
        self.currentTile = 0
        self.tileSheet = self.sslist[self.ss_idx]
        self.numImages = len(self.tileSheet)
    
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
    
    def getFilename(self):
        #get file name
        filename = None
        txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt='Enter filename: ')
        inputWindow = pygame.Surface( (300,100) )
        while filename == None:
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
                        filename = txtbx.getValue()

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
        return filename
    
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

    def event_handler(self, event):
        (x,y) = self.cursorPos
        self.drawBox( (x,y), black)
        if event.key == pygame.K_RIGHT:
            if( x+blocksize < DIM*blocksize ):
                x += blocksize
        if event.key == pygame.K_LEFT:
            if( x-blocksize >= 0 ):
                x -= blocksize
        if event.key == pygame.K_UP:
            if( y-blocksize >= 0 ):
                y -= blocksize
        if event.key == pygame.K_DOWN:
            if( y+blocksize < DIM*blocksize ):
                y += blocksize
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
        if event.key == pygame.K_e:
            self.ss_idx += 1
            if self.ss_idx == len(self.sslist):
                self.ss_idx = 0
            self.selectSheet(self.ss_idx)
        if self.drawMode:
            myMap.setEntry(x/blocksize,y/blocksize,self.currentTile)
        self.cursorPos = (x,y)

    def updateDisplay(self):
        for i in range(DIM):
            for j in range(DIM):
                gridField.blit( self.tileSheet[myMap.getEntry(i,j)], (i*blocksize,j*blocksize) )
        (x,y) = self.cursorPos
        if self.drawMode:
            self.cursorColor = yellow
        else:
            self.cursorColor = white
        boxPoints = ( (x,y), (x,y+blocksize), (x+blocksize,y+blocksize), (x+blocksize,y) )
        pygame.draw.lines( gridField, self.cursorColor, True, boxPoints, 1 )
        self.sideImg, sideRect = load_image('sidebar.bmp')
        self.sideImg.blit(self.tileSheet[self.currentTile],(50,50))
        
        entryBox = pygame.Surface((30,30))
        entryBox.fill(black)
        if pygame.font:
            font = pygame.font.SysFont("arial",20)
            entry = font.render(str(myMap.getEntry(x/blocksize,y/blocksize)),1, white, black )
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
        screen.blit(self.sideImg, (DIM*blocksize,0) )

# Set the height and width of the screen
size=[800,800]
screen=pygame.display.set_mode(size)

pygame.init()
clock = pygame.time.Clock()

cursorPos = (0,0)

myMap = Map()
myHandler = Handler(cursorPos)

blocksize = 30

gridField = pygame.Surface( [DIM*blocksize, DIM*blocksize] )

os.sys.setrecursionlimit(15000)

images.load()

def main():
    while True :
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                myHandler.event_handler(event)
            if event.type == pygame.QUIT:
                os.sys.exit()
        myHandler.updateDisplay()
        screen.blit(gridField, (0,0) )
        pygame.display.flip()

main()