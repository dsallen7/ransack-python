from UTIL import const

class Ticker():
    
    def __init__(self):
        self.count = 0
        self.timeRate = const.timeRate
    
    def tick(self, ticks):
        self.count = self.count + (self.timeRate * ticks)
    
    def getTicks(self):
        return self.count
    
    def getSecs(self):
        return self.count % 60
    
    def getMins(self):
        return self.count / 60
    
    def getHours(self):
        return self.count / 3600
    
    def getDays(self):
        return self.count / 86400
    
    def getCount(self):
        return self.count
    
    def setTimeRate(self, tr):
        self.timeRate = tr