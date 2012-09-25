

class Director():
    
    def __init__(self):
        self.events = [False]*12
        print self.events
    
    def setEvent(self, e):
        self.events[e] = True
        
    def clearEvent(self, e):
        self.events[e] = False
    
    def getEvent(self, e):
        return self.events[e]