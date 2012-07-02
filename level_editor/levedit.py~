from pygame import *
import pygame
import os
import pickle
import random

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
        self.playerLoc = None
    
    def setEntry(self, x, y, e):
        if e == 9:
            if self.playerLoc == None:
                self.playerLoc = (x,y)
            else:
                (px,py) = self.playerLoc
                self.setEntry(px,py,0)
                self.playerLoc = (x,y)
        self.grid[y] = self.grid[y][:x] + [e] + self.grid[y][x+1:]
    
    def getEntry(self, x, y):
        return self.grid[y][x]
    
    def getGrid(self):
        return self.grid
    
    def installGrid(self, newGrid):
        self.grid = newGrid

class Handler():
    
    def __init__(self, cPos):
        self.cursorPos = cPos
        self.currentTile = 0
        self.sideImg, sideRect = load_image('sidebar.bmp')
        self.drawMode = False
        self.cursorColor = white
    
    def drawBox(self, pos, color):
        (x,y) = pos
        boxPoints = ( (x,y), (x,y+blocksize), (x+blocksize,y+blocksize), (x+blocksize,y) )
        pygame.draw.lines( gridField, color, True, boxPoints, 1 )
        
    
    def switchTile(self):
        self.currentTile += 1
        self.currentTile = self.currentTile % 10
    
    def saveMap(self):
        grid = myMap.getGrid()
        save = open("map.dat", "w")
        pickle.dump(grid, save)
        save.close()
    
    def loadMap(self):
        save = open("map.dat", "r")
        grid = pickle.load(save)
        save.close()
        myMap.installGrid(grid)

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
        if self.drawMode:
            myMap.setEntry(x/blocksize,y/blocksize,self.currentTile)
        self.cursorPos = (x,y)

    def updateDisplay(self):
        for i in range(DIM):
            for j in range(DIM):
                #if myMap.getEntry(i,j) == 0:
                #    images[myMap.getEntry(i,j)] = pygame.transform.rotate(images[myMap.getEntry(i,j)],90)
                #    gridField.blit( images[myMap.getEntry(i,j)], (i*blocksize,j*blocksize) )
                #else:
                gridField.blit( images[myMap.getEntry(i,j)], (i*blocksize,j*blocksize) )
        (x,y) = self.cursorPos
        if self.drawMode:
            self.cursorColor = yellow
        else:
            self.cursorColor = white
        boxPoints = ( (x,y), (x,y+blocksize), (x+blocksize,y+blocksize), (x+blocksize,y) )
        pygame.draw.lines( gridField, self.cursorColor, True, boxPoints, 1 )
        self.sideImg, sideRect = load_image('sidebar.bmp')
        self.sideImg.blit(images[self.currentTile],(50,50))
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

images = range(10)


imageNames = ['floor.bmp','brick2.bmp','key.bmp','door.bmp','exit.bmp','fruit_s.bmp','hpotion.bmp','spellbook.bmp','chest.bmp','link_d.bmp']

for i in range(10):
    images[i], r = load_image(imageNames[i])

myMap = Map()
myHandler = Handler(cursorPos)

blocksize = 30

gridField = pygame.Surface( [DIM*blocksize, DIM*blocksize] )

def main():
    while True :
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                myHandler.event_handler(event)
        myHandler.updateDisplay()
        screen.blit(gridField, (0,0) )
        pygame.display.flip()

main()