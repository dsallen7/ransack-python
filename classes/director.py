

class Director():
    #0 opening msg
    #1 visit Camden 1st time
    #2 gain audience with Duke
    #3 accept key from duke
    #4
    #5
    #6 enter dungeon level 5 (maze)
    #7
    #8
    #9 approach fortress
    #10
    #11 defeat skeleton king
    def __init__(self):
        self.events = [False]*12
        self.quests = [0]*12
        self.narrator = [False]*12
        
        self.narrationEventsByMapName = {'Village 1' : ("The town of Camden. Used to be a nice place, now it's more like a ghetto. Better watch your back here! By the way, you see that red brick building in the center? That's where you save your game...yea, you might wanna do that!",1),
                                         'Dungeon Level 5' : ("The dungeon suddenly takes an unfamiliar twist as the cavernous rooms are replaced by narrow, labyrinthine passageways.",6),
                                         'Fortress 1': ("Uh-oh. This might be bad. You are standing in what looks like the entrance to Hell. You can feel the heat from the burning sea that surrounds the fortress.",9)
                                         }
    
    def setEvent(self, e):
        self.events[e] = True
        
    def clearEvent(self, e):
        self.events[e] = False
    
    def getEvent(self, e):
        return self.events[e]
    
    def advanceQuest(self, q):
        self.quests[q] += 1
    
    def getNarrartionEventByMapName(self, name):
        try:
            e = self.narrationEventsByMapName[name]
            if not self.getEvent(e[1]):
                self.setEvent(e[1])
                return e[0]
            else: return None
        except KeyError:
            return None
    
    def getNarrartionEventByGameEvent(self):
        pass