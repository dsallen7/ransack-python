class badguy(pygame.sprite.Sprite):
    def __init__(self,x,y, nGame):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('goomba.bmp', -1)
        self.location = (x,y)
        self.rect = (x,y,blocksize,blocksize)
        
        self.newGame = nGame
        
    def checkMap(self, x, y):
        (a,b,c,d) = self.newGame.myHero.rect
        if x == a and y == b:
            return 'p'
        if self.newGame.myMap.maptext[x/blocksize][y/blocksize] == 0:
            return False

    def hurtPlayer(self):
        self.newGame.myHud.hurt()
        
    def die(self):
        x,y = self.location
        self.newGame.myMap.updateUnit(x/blocksize,y/blocksize,'o')
        
    def move(self):
        n = random.randrange(1,5)
        if n != 2:
            #to slow badguys down
            return
        x,y = self.location
        m = random.randrange(1,5)
        moveX = 0
        moveY = 0
        if m == 1: # up
            moveY = -blocksize
        elif m == 2: # down
            moveY = blocksize
        elif m == 3: # left
            moveX = -blocksize
        elif m == 4: # right
            moveX = blocksize
        
        if self.checkMap( (x + moveX), (y + moveY) ) == 'p':
            self.hurtPlayer()
        elif (0 < y < 500) and (0 < x < 500) and (self.checkMap( (x + moveX), (y + moveY) ) == False):
            self.newGame.myMap.updateUnit(x/blocksize,y/blocksize,'o')
            self.location = ( (x + moveX), (y + moveY) )
            self.newGame.myMap.updateUnit( (x + moveX)/blocksize,(y + moveY)/blocksize,'b')
        
        x,y = self.location
        self.rect = (x,y, blocksize, blocksize)
            #move in direction of player
    def seek(self):
        pass