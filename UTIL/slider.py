class Slider:
    
    def __init__(self, xLoc, yLoc, value=4, max=9):
        self.xLoc = xLoc
        self.yLoc = yLoc
        
        self.value = value
        self.max = max
    
        self.sliding = False
    
    def getXLoc(self):
        return self.xLoc
    
    def getYLoc(self):
        return self.yLoc
    
    def getValue(self):
        return self.value
    
    def setValue(self, v):
        self.value = v
    
    def getMax(self):
        return self.max