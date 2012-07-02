import pygame
import os
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

class PyManMain:
    """The Main PyMan Class - This class handles the main 
    initialization and creating of the Game."""
    
    def __init__(self, width=640,height=480):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width = width
        self.height = height
        """Create the Screen"""
        self.screen = pygame.display.set_mode((self.width, self.height))

class hero(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.images = range(4)
        self.images[0], self.rect = load_image('link_u.bmp', -1)
        self.images[1], self.rect = load_image('link_d.bmp', -1)
        self.images[2], self.rect = load_image('link_l.bmp', -1)
        self.images[3], self.rect = load_image('link_r.bmp', -1)
        
        self.image = self.images[1]
        self.rect = (17, 23, 17, 23)
        #Height: 23
        #Width: 17

    def event_handler(self, event):
        if event.type == pygame.KEYUP:
            self.move(pygame.key.name(event.key))

    def checkMap(self, x, y):
        if myMap.maptext[x/17][y/23] == 'x':
            return True
        elif myMap.maptext[x/17][y/23] == 'o':
            return False
        elif myMap.maptext[x/17][y/23] == 'f':
            return 'f'

    def move(self, direction):
        x1,y1,x2,y2 = self.rect
        if direction == 'up':
            if (y1 > 0) and (self.checkMap(x1,y1-y2) != True):
                self.image = self.images[0]
                self.rect = (x1, y1-y2,x2,y2)
        elif direction == 'down':
            if (y1 < 500) and (self.checkMap(x1,y1+y2) != True):
                self.image = self.images[1]
                self.rect = (x1, y1+y2,x2,y2)
        elif direction == 'left':
            if (x1 > 0) and (self.checkMap(x1-x2,y1) != True):
                self.image = self.images[2]
                self.rect = (x1-x2, y1,x2,y2)
        elif direction == 'right':
            if (x1 < 500) and (self.checkMap(x1+x2,y1) != True):
                self.image = self.images[3]
                self.rect = (x1+x2, y1,x2,y2)
        x1,y1,x2,y2 = self.rect
        if self.checkMap(x1,y1) == 'f':
            myMap.getItem(x1/17,y1/23)

class hud():
    def __init__(self):
        self.box = pygame.Surface((170, 50))
        self.box.fill( yellow )
        self.playerscore = 0
        self.playerlife = 50

    def update(self):
        screen.blit(self.box, (0,230) )
        if pygame.font:
            font = pygame.font.Font(None, 24)
            text = font.render( "Score: "+str(self.playerscore), 1, red)
            self.box.blit(text, (0,0) )
            text = font.render( "Life: ", 1, red)
            self.box.blit(text, (0,25) )
        lifebar = pygame.Surface((self.playerlife,10))
        lifebar.fill(red)
        self.box.blit(lifebar, (30,30) )
            
    def getItem(self,type):
        if type == 'f':
            if self.playerlife < 90:
                self.playerlife += 10
            else:
                self.playerlife = 100
            self.playerscore += 10

class map():
    def __init__(self):
        self.mapfile = open('map.dat', 'r')
        self.maptext = self.mapfile.readlines()
        self.images = range(2)
        self.images[0], self.rect = load_image('brick1.bmp', -1)
        self.images[1], self.rect = load_image('fruit_s.bmp', -1)
        
        self.image = self.images[0]
        
    def redraw(self):
        for x in range(0,len(self.maptext)):
            for y in range(0,len(self.maptext[x])):
                if self.maptext[x][y] == 'x':
                    self.image = self.images[0]
                    screen.blit(self.image, (x*17,y*23), area=(0,0,17,23), special_flags = 0)
                elif self.maptext[x][y] == 'f':
                    self.image = self.images[1]
                    screen.blit(self.image, (x*17,y*23), area=(0,0,17,23), special_flags = 0)

    def getItem(self, x, y):
        myHud.getItem(self.maptext[x][y])
        self.maptext[x] = self.maptext[x][:y]+'o'+self.maptext[x][y+1:]

class item():
    def __init__(self):
        self.type = None
        
class badguy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('goomba.bmp', -1)
        self.location = (x,y)
        self.rect = (x,y,17,23)

    def checkMap(self, x, y):
        if myMap.maptext[x/17][y/23] == 'o':
            return False

    def move(self):
        x,y = self.location
        m = random.randrange(1,5)
        if m == 1: # up
            if (y > 0) and (self.checkMap(x,y-23) == False):
                self.location = (x, y-23)
        elif m == 2: # down
            if (y < 500) and (self.checkMap(x,y+23) == False):
                self.location = (x, y+23)
        elif m == 2: # left
            if (y < 500) and (self.checkMap(x-17,y) == False):
                self.location = (x-17, y)
        elif m == 2: # right
            if (y < 500) and (self.checkMap(x+17,y) == False):
                self.location = (x+17, y)
                
        x,y = self.location
        self.rect = (x,y, 17, 23)

# Set the height and width of the screen
size=[500,500]
screen=pygame.display.set_mode(size)

if not pygame.font: print 'Warning, fonts disabled'

pygame.display.set_caption("ROGUE")

background = pygame.Surface([170,230])
background = background.convert()
background.fill((250, 250, 250))

pygame.init()
clock = pygame.time.Clock()
random.seed()

# Define the colors we will use in RGB format
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]
yellow = [255, 255, 127]

myHero = hero()
myMap = map()
myHud = hud()
myBad = badguy(51,69)

allsprites = pygame.sprite.RenderPlain((myHero, myBad))


while True:
    clock.tick(30)
    for event in pygame.event.get():
        myHero.event_handler(event)
        if event.type == pygame.QUIT:
            os.sys.exit()
    screen.blit(background, (0, 0))
    allsprites.update()
    allsprites.draw(screen)
    myMap.redraw()
    myHud.update()
    myBad.move()
    pygame.display.flip()