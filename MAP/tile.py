class Tile():
    
    def __init__(self, x, y, fg, bg=None):
        self.x = x
        self.y = y
        self.fg = fg
        self.bg = bg
        self.lit = True
        self.occupied = False
    
    def getXY(self):
        return (self.x, self.y)
    def setXY(self, x, y):
        self.x = x
        self.y = y
    
    def getFG(self):
        return self.fg
    def setFG(self, fg):
        self.fg = fg