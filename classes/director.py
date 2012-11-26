

class Director():
    
    def __init__(self):
        self.events = [False]*12
        self.quests = [0]*12
        self.narrator = [False]*12
    
    def setEvent(self, e):
        self.events[e] = True
        
    def clearEvent(self, e):
        self.events[e] = False
    
    def getEvent(self, e):
        return self.events[e]
    
    def advanceQuest(self, q):
        self.quests[q] += 1
    
    def getNarrartionEvent(self):
        for i in range( len( self.narrator ) ):
            if self.narrator[i] == False:
                self.narrator[i] = True
                return i