import pygame, random, math, os
from UTIL import const, misc

from SCRIPTS import npcScr

from IMG import images

from npc import Npc

from random import choice

class Citizen(Npc):
    def __init__(self, x, y, message, filename, name=''):
        Npc.__init__(self, x, y, message, filename, name)
        self.home = (x,y)
        self.roam = 5
        self.type = 'citizen'
        
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
                map.clearOccupied(sX, sY)
                map.setOccupied(sX+mX, sY+mY)
            else: self.moving = False
        else: self.moving = False
        #self.dir = 'down'

class Woodsman(Citizen):
    def __init__(self, x, y, message):
        Citizen.__init__(self, x, y, message, choice(['woodsman.bmp','woodsman2.bmp']) )
        self.movingRate = 30

class Female(Citizen):
    def __init__(self, x, y, message, gender, level):
        Citizen.__init__(self, x, y, message, choice(['female.bmp','female2.bmp','female3.bmp']) )
        if gender == 'male':
            self.message = choice( npcScr.femaleToMaleLinesByLevel[level] )
        else: self.message = choice( npcScr.femaleToFemaleLinesByLevel[level] )

class Housewife(Citizen):
    def __init__(self, x, y, message, d):
        Citizen.__init__(self, x, y, message, 'female2.bmp' )
        self.message = "Would you like to complete a task for me?"
        self.Director = d
        self.movingRate = 30
    
    def interact(self, interface, game):
        if game.Director.getQuestStatus(1) == 0:
            if interface.npcDialog(self.message, self.images[8]) == 'Yes':
                game.displayOneFrame()
                interface.npcMessage("Okay. I need a loaf of bread and two wedges of cheese", self.images[8])
                game.displayOneFrame()
                interface.npcMessage("Here's the money.", self.images[8])
                game.Director.advanceQuest(1)
                return ( 'item', const.GOLD, 26)
            else:
                game.displayOneFrame()
                interface.npcMessage("That's too bad!", self.images[8])
            return None
        elif game.Director.getQuestStatus(1) == 1:
            if interface.npcDialog('Did you get those things yet?', self.images[8]) == 'Yes':
                if game.myHero.hasItem(const.CHEESE, 2) and game.myHero.hasItem(const.BREAD, 1):
                    game.myHero.takeItem( const.CHEESE )
                    game.myHero.takeItem( const.CHEESE )
                    game.myHero.takeItem( const.BREAD )
                    game.displayOneFrame()
                    interface.npcMessage("Thanks so much!", self.images[8])
                    game.Director.advanceQuest(1)
                else:
                    game.displayOneFrame()
                    interface.npcMessage("No, you didn't! Now get going.", self.images[8])
                return None
            else:
                game.displayOneFrame()
                interface.npcMessage("Well what are you waiting for?", self.images[8])
                return None
        elif game.Director.getQuestStatus(1) == 2:
            interface.npcMessage("Lovely day, isn't it?", self.images[8])
            return None

class Gardener(Citizen):
    def __init__(self, x, y, message, d):
        Citizen.__init__(self, x, y, message, 'gardener.bmp' )
        self.message = "These badgers are terrorizing my vegetables! Can you get rid of them for me?"
        self.Director = d
        self.movingRate = 30
    
    def interact(self, interface, game):
        if game.Director.getQuestStatus(0) == 0:
            if interface.npcDialog(self.message, self.images[8]) == 'Yes':
                game.displayOneFrame()
                interface.npcMessage("Thanks, you're a doll. Come back when you kill every last one!", self.images[8])
                game.Director.advanceQuest(0)
                return None
            else:
                game.displayOneFrame()
                interface.npcMessage("That's too bad!", self.images[8])
            return None
        elif game.Director.getQuestStatus(0) in [1, 2]: # quest accepted, animals not slain
            interface.npcMessage("You didn't kill them yet!", self.images[8])
        elif game.Director.getQuestStatus(0) == 3: # animals slain
            interface.npcMessage("You're the best! Here's something for your trouble.", self.images[8])
            game.Director.advanceQuest(0)
            return ('item', const.FRUIT1, 5);
        elif game.Director.getQuestStatus(0) == 4: # quest complete
            interface.npcMessage("Gardening is such hard work!", self.images[8])

class genericHousewife(Citizen):
    def __init__(self, x, y, message):
        Citizen.__init__(self, x, y, message, choice(['female.bmp','female2.bmp','female3.bmp']))
        self.roam = 3
        self.movingRate = 40
        self.message = choice( npcScr.genericHousewifeDialogs )

class Magician(Citizen):
    def __init__(self, x, y, name):
        Citizen.__init__(self, x, y, name, choice(['magician.bmp','fmagician.bmp']) )
        self.roam = 3
        self.movingRate = 40

class shopMagician(Citizen):
    def __init__(self, x, y, name, D):
        self.Director = D
        if self.Director.getEvent(4):
            Citizen.__init__(self, x-1, y, name, 'magician.bmp')
        else:
            Citizen.__init__(self, x, y, name, 'magician.bmp')
    
    def update(self, map, heroPos):
        if self.moving == True:
            #print 'Im Moving IT!'
            self.move(self.dir, map, heroPos)
            return True
        self.dir = 'down'
        i = random.randrange(1, self.movingRate)
        if i == 1:
            pass#self.takeStep()
    
    def interact(self, interface, game):
        if game.myHero.maxMP >= 150:
            if not self.Director.getEvent(4):
                interface.npcMessage("Welcome to the Magic Training Institute. You may enter.", self.images[8])
                self.Director.setEvent(4)
                self.moving = True
                self.dir = 'left'
                #self.move('left', game.myMap, game.myHero.getXY())
            else:
                interface.npcMessage("How is your study coming along?", self.images[8])
        else:
            interface.npcMessage("This is the Magic Training Institute. You must have 150 MP to enter! Come back later, newb.", self.images[8])

class Blacksmith(Citizen):
    def __init__(self, x, y, name):
        Citizen.__init__(self, x, y, name, 'blacksmith.bmp')
        self.roam = 3
        self.movingRate = 30
        
class Shopkeep(Citizen):
    def __init__(self, x, y, name):
        Citizen.__init__(self, x, y, name, 'shopkeep.bmp')
        self.roam = 3
        self.movingRate = 30
        
class Tramp(Citizen):
    def __init__(self, x, y, name):
        Citizen.__init__(self, x, y, name, 'tramp.bmp')
        self.dialog = choice( npcScr.trampDialogs )
        self.movingRate = 30
        self.message = self.dialog[0]
        
    def interact(self, interface, game):
        if interface.npcDialog(self.message, self.images[8]) == 'Yes':
            game.displayOneFrame()
            interface.npcMessage(self.dialog[1], self.images[17])
        else:
            game.displayOneFrame()
            interface.npcMessage(self.dialog[2], self.images[17])
        return None
        
class Guard(Citizen):
    
    def __init__(self, x, y, message, name=''):
        Citizen.__init__(self, x, y, message, 'guard.bmp', name)
        self.movingRate = 40
    
    def update(self, map, heroPos):
        if self.moving == True:
            #print 'Im Moving IT!'
            self.move(self.dir, map, heroPos)
            return True
        self.dir = 'down'
        i = random.randrange(1, self.movingRate)
        if i == 1:
            pass#self.takeStep()

class CastleGuard1(Guard):
    
    def __init__(self, x, y, name, D):
        self.Director = D
        if self.Director.getEvent(2):
            Citizen.__init__(self, x-1, y, name, 'guard.bmp')
        else:
            Citizen.__init__(self, x, y, name, 'guard.bmp')
    
    def interact(self, interface, game):
        if game.myHero.level >= 3:
            if not self.Director.getEvent(2):
                interface.npcMessage("You there! The Duke wants to see you. Please go right up.", self.images[17])
                self.Director.setEvent(2)
                self.moving = True
                self.dir = 'left'
                #self.move('left', game.myMap, game.myHero.getXY())
            else:
                interface.npcMessage("Carry on then.", self.images[17])
        else:
            interface.npcMessage("The Duke has no use for weaklings! Come back when you level up a bit.", self.images[8])

class DungeonGuard(Guard):
    
    def __init__(self, x, y, name, D):
        self.Director = D
        if self.Director.getEvent(4):
            Citizen.__init__(self, x+1, y-1, name, 'guard.bmp')
        else:
            Citizen.__init__(self, x, y, name, 'guard.bmp')
    
    def interact(self, interface, game):
        if self.Director.getEvent(4):
            interface.npcMessage("Going in for an adventure, are ya? Have fun getting mangled beyond recognition!", self.images[17])
        else:
            interface.npcMessage("Nobody is to access the Dungeon without the Duke's permission. Now get lost!", self.images[8])

class Duke(Citizen):
    
    def __init__(self, x, y, name, d):
        Citizen.__init__(self, x, y, name, 'duke.bmp')
        self.Director = d
        self.message = "So you're looking for adventure, are you? You heroing types are so predictable *snort* most of you end up as wolf food, anyway!"
        self.message2 = "HOWEVER - I must say that the wretched creature known as Rattlehead has been quite the thorn in my side lately. His minions have been attacking my citizens and poaching my game."
        self.message3 = "Of course, if anyone should rise to the occasion, and bring me the Dark Stone which gives Rattlehead his power - I could make it worth your while. I am, after all, a man of means."
        self.message4 = "So then, warrior, since I can't get any of my own men to go after him - a fine lot they are indeed - what say you take on the challenge?"
        self.message5 = "Very well then, take this Dungeon key and off you go then. You'll find the Dungeon to the southeast of our fair town."
        self.message6 = "Guards, show this well-intentioned young fool to the door."
        self.message7 = "Back so soon? Why, you've barely even set foot in the dungeon! Get out, and don't come back without that stone! Guards!"
    def update(self, map, heropos):
        pass
    def escortPlayerOut(self, game):
        game.getNPCByName('Guard1').moveEnqueue('03311111111')
        game.getNPCByName('Guard2').moveEnqueue('23311111111')
        game.myHero.moveEnqueue('444111111111')
    def interact(self, interface, game):
        if not self.Director.getEvent(4):
            interface.npcMessage(self.message, self.images[8])
            game.displayOneFrame()
            interface.npcMessage(self.message2, self.images[8])
            game.displayOneFrame()
            interface.npcMessage(self.message3, self.images[8])
            game.displayOneFrame()
            if interface.npcDialog(self.message4, self.images[8]) == 'Yes':
                game.displayOneFrame()
                interface.npcMessage(self.message5, self.images[17])
                game.displayOneFrame()
                interface.npcMessage(self.message6, self.images[8])
                self.Director.setEvent(4)
                self.escortPlayerOut(game)
                return ('item', const.KEY, 1)
            else:
                game.displayOneFrame()
                interface.npcMessage("Bah! You would refuse my offer? Get out of my sight, commoner!", self.images[8])
                game.displayOneFrame()
                self.escortPlayerOut(game)
                return None
        else:
            if self.Director.getEvent(11):
                interface.npcMessage("You win the game!", self.images[8])
                return 'win'
            else:
                interface.npcMessage(self.message7, self.images[8])
                game.displayOneFrame()
                self.escortPlayerOut(game)
                return None