import pygame, random, math, os
from UTIL import const, misc

from SCRIPTS import npcScr

from IMG import images

from random import choice

class npc(pygame.sprite.Sprite):
    
    def __init__(self, x, y, message, imgFile):
        self.X = x
        self.Y = y
        self.images = images.loadNPC(imgFile)
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.imgIdx = 2
        self.image = self.images[self.imgIdx]
        self.dir = 'down'
        self.moving = False
        self.message = message
        self.setRect(x * const.blocksize, y * const.blocksize, const.blocksize, const.blocksize)
    
    def setRect(self, x1, y1, x2, y2):
        self.rect = (x1, y1, x2, y2)
    def getRect(self):
        return self.rect
    def getXY(self):
        return (self.X, self.Y)
    def setXY(self, x, y):
        self.X = x
        self.Y = y
    
    def takeStep(self):
        self.imgIdx = (1 - (self.imgIdx % 2)) + (2 * (self.imgIdx / 2))
        self.image = self.images[self.imgIdx]
    
    def interact(self, interface, game):
        interface.npcMessage(self.message, self.images[8])
        return None
    
    def move(self, dir, map, heroPos):
        (hX, hY) = heroPos
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        self.moving = True
        (sX, sY) = self.getXY()
        self.dir = dir
        (mX, mY) = const.scrollingDict[dir]
        self.imgIdx = const.imgDict[dir]
        self.image = self.images[self.imgIdx]
        if map.getEntry(sX + mX, sY + mY) in range(25) and (sX + mX, sY + mY) != (hX, hY) and not map.isOccupied(sX + mX, sY + mY):
            self.setXY(sX + mX, sY + mY)
        else: self.moving = False
    
    def update(self, map, heroPos):
        i = random.randrange(1, 20)
        if i == 5:
            self.move(random.choice(['up', 'down', 'left', 'right']), map, heroPos)
            return True
        else: return False
    
    def shiftOnePixel(self, dir, sign):
        (x1, y1, x2, y2) = self.rect
        if dir == 'up':
            self.setRect(x1, y1 + sign, x2, y2)
        if dir == 'down':
            self.setRect(x1, y1 - sign, x2, y2)
        if dir == 'left':
            self.setRect(x1 + sign, y1, x2, y2)
        if dir == 'right':
            self.setRect(x1 - sign, y1, x2, y2)

class Citizen(npc):
    def __init__(self, x, y, name, filename):
        npc.__init__(self, x, y, name, filename)

class Female(Citizen):
    def __init__(self, x, y, name, gender, level):
        npc.__init__(self, x, y, name, choice(['female.bmp','female2.bmp','female3.bmp']) )
        if gender == 'Male':
            self.message = choice( npcScr.femaleToMaleLinesByLevel[level] )
        else: self.message = choice( npcScr.femaleToFemaleLinesByLevel[level] )

class Housewife(Citizen):
    def __init__(self, x, y, name, d):
        npc.__init__(self, x, y, name, 'female2.bmp' )
        self.message = "Would you like to complete a task for me?"
        self.Director = d
    
    def interact(self, interface, game):
        if game.Director.quests[0] == 0:
            if interface.npcDialog(self.message, self.images[8]) == 'Yes':
                game.displayOneFrame()
                interface.npcMessage("Okay. I need a loaf of bread and two wedges of cheese", self.images[8])
                game.displayOneFrame()
                interface.npcMessage("Here's the money.", self.images[8])
                game.Director.advanceQuest(0)
                return ( 'item', const.GOLD, 26)
            else:
                game.displayOneFrame()
                interface.npcMessage("That's too bad!", self.images[8])
            return None
        elif game.Director.quests[0] == 1:
            if interface.npcDialog('Did you get those things yet?', self.images[8]) == 'Yes':
                if game.myHero.hasItem(const.CHEESE, 2) and game.myHero.hasItem(const.BREAD1, 1):
                    game.myHero.takeItem(const.CHEESE)
                    game.myHero.takeItem(const.CHEESE)
                    game.myHero.takeItem(const.BREAD1)
                    game.displayOneFrame()
                    interface.npcMessage("Thanks so much!", self.images[8])
                    game.Director.advanceQuest(0)
                else:
                    game.displayOneFrame()
                    interface.npcMessage("No, you didn't! Now get going.", self.images[8])
                return None
            else:
                game.displayOneFrame()
                interface.npcMessage("Well what are you waiting for?", self.images[8])
                return None
        elif game.Director.quests[0] == 2:
            interface.npcMessage("Lovely day, isn't it?", self.images[8])
            return None

class Tramp(Citizen):
    def __init__(self, x, y, name):
        npc.__init__(self, x, y, name, 'tramp.bmp')
    def interact(self, interface, game):
        if interface.npcDialog(self.message, self.images[8]) == 'Yes':
            game.displayOneFrame()
            interface.npcMessage('Great!', self.images[8])
        else:
            game.displayOneFrame()
            interface.npcMessage("That's too bad!", self.images[8])
        return None
        
class Guard(Citizen):
    
    def __init__(self, x, y, name):
        Citizen.__init__(self, x, y, name, 'guard.bmp')
        #self.type
    
    def update(self, map, heropos):
        i = random.randrange(1, 6)
        if i == 5:
            self.takeStep()

class King(Citizen):
    
    def __init__(self, x, y, name, d):
        Citizen.__init__(self, x, y, name, 'king.bmp')
        self.Director = d
        self.message = "Times are rough, we could really use a hero! You wanna take on the Skeleton King for us?"
    
    def update(self, map, heropos):
        pass
    
    def interact(self, interface, game):
        if not self.Director.getEvent(0):
            if interface.npcDialog(self.message, self.images[8]) == 'Yes':
                game.displayOneFrame()
                interface.npcMessage("Awesome, man! Here is the key you will need to access the Dungeon.", self.images[8])
                self.Director.setEvent(0)
                return ('item', const.KEY)
            else:
                game.displayOneFrame()
                interface.npcMessage("Hey, that's a shame buddy; please return if you have a change of heart!", self.images[8])
                return None
        else:
            if self.Director.getEvent(11):
                interface.npcMessage("You win the game!", self.images[8])
                return 'win'
            else:
                interface.npcMessage("Let's get going! Skeleton King ain't gonna slay himself!", self.images[8])
                return None
class Inanimate(npc):
    def __init__(self, x, y, name, filename):
        npc.__init__(self, x, y, name, filename)

class Firepit(Inanimate):
    def __init__(self, x, y, name):
        Inanimate.__init__(self, x, y, name, 'firepit.bmp')
        self.message = 'The fire glows brightly.'
    
    def update(self, map, hero):
        i = random.randrange(1, 6)
        if i == 5:
            self.imgIdx = ( self.imgIdx + 1 ) % 8
            self.image = self.images[self.imgIdx]
        
class Enemy(npc):
    def __init__(self, x, y, name, filename, mID):
        npc.__init__(self, x, y, name, filename)
        self.name = name
        self.turn = False
        self.confused = 0
        self.ID = mID
    
    def move(self, dir, map, heroPos):
        (hX, hY) = heroPos
        self.moving = True
        (sX, sY) = self.getXY()
        (mX, mY) = const.scrollingDict[dir]
        self.dir = dir
        sX += mX
        sY += mY
        if map.getEntry(sX, sY) in range(25):
            if (sX, sY) != (hX, hY):
                self.setXY(sX, sY)
            else:
                self.moving = False
                return 'battle'
        else: 
            self.moving = False
            return False
        self.imgIdx = const.imgDict[dir]
        self.image = self.images[self.imgIdx]
        return True
    def seek(self, map, heroPos):
        (sX, sY) = self.getXY()
        (hX, hY) = heroPos
        if misc.DistanceX(self.getXY(), heroPos) > misc.DistanceY(self.getXY(), heroPos):
            if hX > sX:
                return self.move('right', map, heroPos)
            else:
                return self.move('left', map, heroPos)
        else:
            if hY > sY:
                return self.move('down', map, heroPos)
            else:
                return self.move('up', map, heroPos)
    
    def interact(self, interface, game):
        interface.boxMessage('The battle is joined!')
        return 'battle'
    def update(self, map, heroPos):
        if self.confused > 0:
            imgCopy = self.image.copy()
            imgCopy.blit( self.images[8],(0,0) )
            if self.confused/2 == 0:
                self.image = imgCopy
            else: self.image = self.images[self.imgIdx]
            self.confused -= 1
            return True
        (hX, hY) = heroPos
        hX = hX / const.blocksize
        hY = hY / const.blocksize
        heroPos = (hX, hY)
        if misc.Distance(self.getXY(), heroPos) < 3:
            self.turn = not self.turn
            if self.turn:
                return self.seek(map, heroPos)
        else:
            i = random.randrange(1, 10)
            if i == 5:
                return self.move(random.choice(['up', 'down', 'left', 'right']), map, heroPos)
    def confuse(self, t):
        self.confused = t
    def getID(self):
        return self.ID
    
class skeletonKing(Enemy):
    
    def __init__(self, x, y, name, filename, mID, d):
        
        Enemy.__init__(self, x, y, name, filename, mID)
        self.Director = d
        
    def interact(self, interface, game):
        interface.npcMessage('Welcome to your death!', self.images[2])
        return 'battle'
    
    def update(self, map, heropos):
        i = random.randrange(1, 6)
        if i == 5:
            self.takeStep()
    def die(self):
        self.Director.setEvent(11)

def newNpc( n, game ):
    (x,y) = n[0]
    if n[1] == 'guard':
        return Guard(x, y, n[2])
    elif n[1] == 'female':
        return Female(x, y, n[2], game.myHero.gender, game.myHero.level )
    elif n[1] == 'firepit':
        return Firepit(x, y, n[2])
    elif n[1] == 'tramp':
        return Tramp(x, y, n[2])
    elif n[1] == 'king':
        return King(x, y, n[2], game.Director)
    elif n[1] == 'housewife':
        return Housewife(x, y, n[2], game.Director)
    # enemies
    elif n[1] == 'skeletonking':
        return skeletonKing(x, y, 'Skeleton King', 'skeleton.bmp', n, game.Director)
    else:
        i = npcScr.enemyDict[ n[1] ]
        return Enemy(x, y, i[0], i[1], n)