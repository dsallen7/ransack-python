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
    
    def getBG(self):
        return self.bg
    def setBG(self, bg):
        self.bg = bg
        
    def getMsgText(self):
        return self.msgText

    def setMsgText(self, txt):
        self.msgText = txt
    
    def getShopID(self):
        return self.shopID
