

class Director():
    def __init__(self):
        self.events = [False]*12
        #0 
        #1 
        #2 gain audience with Duke
        #3 
        #4 duke grants access to dungeon
        #5 gain access to MTI
        #6 
        #7
        #8
        #9 
        #10
        #11 defeat skeleton king
        self.narrations = [False]*12
        #0 opening msg
        #1 visit Camden 1st time
        #2 enter Duke's chamber
        #6 enter dungeon level 5 (maze)
        #9 approach fortress
        self.quests = [0]*12
        #0 defeat animals in garden
        #-0.0 quest not accepted
        #-0.1 quest accepted, none killed
        #-0.2 quest accepted, one killed
        #-0.3 quest accepted, both killed
        #-0.4 quest completed
        #1 get items for housewife
        #-1.0 quest not accepted
        #-1.1 quest accepted, items not bought
        self.narrator = [False]*12
        
        self.narrationEventsByMapName = {'Village 1' : ("The town of Camden. Used to be a nice place, now it's more like a ghetto. Better watch your back here! By the way, you see that red brick building in the center? That's where you save your game...yea, you might wanna do that!",1),
                                         'Castle 2' : ("As you enter the Duke's chamber, you are astounded by the opulence you see everywhere, in sharp contrast to the rude lifestyles of the villagers. The Duke himself is a fat, arrogant looking man, and you get an uneasy feeling as he summons you to approach.",2),
                                         'Dungeon Level 5' : ("The dungeon suddenly takes an unfamiliar twist as the cavernous rooms are replaced by narrow, labyrinthine passageways.",6),
                                         'Fortress 1': ("Uh-oh. This might be bad. You are standing in what looks like the entrance to Hell. You can feel the heat from the burning sea that surrounds the fortress.",9)
                                         }
        self.narrationEvensByNumber = {0:"You took care of those runts like they were nothing. Garden variety is more like it. Now let's go find some real action!"
                                       
                                       }
    
    def setEvent(self, e):
        self.events[e] = True

    def clearEvent(self, e):
        self.events[e] = False

    def getEvent(self, e):
        return self.events[e]
    
    def getNarr(self, n):
        return self.narrations[n]

    def setNarr(self, n):
        self.narrations[n] = True
    
    def advanceQuest(self, q):
        self.quests[q] += 1

    def getQuestStatus(self, q):
        return self.quests[q]
    
    def getNarrartionEventByMapName(self, name):
        try:
            e = self.narrationEventsByMapName[name]
            if not self.getNarr(e[1]):
                self.setNarr(e[1])
                return e[0]
            else: return None
        except KeyError:
            return None
    
    def getNarrartionEventByGameEvent(self):
        pass
