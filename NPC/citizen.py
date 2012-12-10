import pygame, random, math, os
from UTIL import const, misc

from SCRIPTS import npcScr

from IMG import images

from npc import Npc

from random import choice

class Citizen(Npc):
    def __init__(self, x, y, name, filename, roam=5):
        Npc.__init__(self, x, y, name, filename)
        self.home = (x,y)
        self.roam = 5
        
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
        if misc.eDistance( self.home, (sX + mX, sY + mY)  ) <= self.roam:
            if map.getEntry(sX + mX, sY + mY) in range(25) and (sX + mX, sY + mY) != (hX, hY) and not map.isOccupied(sX + mX, sY + mY):
                self.setXY(sX + mX, sY + mY)
            else: self.moving = False
        else: self.moving = False

class Woodsman(Citizen):
    def __init__(self, x, y, msg, d):
        Citizen.__init__(self, x, y, msg, choice(['woodsman.bmp','woodsman2.bmp']) )
        #self.message = msg
        self.Director = d

class Female(Citizen):
    def __init__(self, x, y, name, gender, level):
        Citizen.__init__(self, x, y, name, choice(['female.bmp','female2.bmp','female3.bmp']) )
        if gender == 'Male':
            self.message = choice( npcScr.femaleToMaleLinesByLevel[level] )
        else: self.message = choice( npcScr.femaleToFemaleLinesByLevel[level] )

class Housewife(Citizen):
    def __init__(self, x, y, name, d):
        Citizen.__init__(self, x, y, name, 'female2.bmp' )
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
                if game.myHero.hasItem(const.CHEESE, 2) and game.myHero.hasItem(const.BREAD, 1):
                    game.myHero.takeItem( const.CHEESE )
                    game.myHero.takeItem( const.CHEESE )
                    game.myHero.takeItem( const.BREAD )
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

class Magician(Citizen):
    def __init__(self, x, y, name):
        Citizen.__init__(self, x, y, name, 'magician.bmp')
        self.roam = 3

class Blacksmith(Citizen):
    def __init__(self, x, y, name):
        Citizen.__init__(self, x, y, name, 'blacksmith.bmp')
        self.roam = 3

class Tramp(Citizen):
    def __init__(self, x, y, name):
        Citizen.__init__(self, x, y, name, 'tramp.bmp')
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