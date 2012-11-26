from UTIL import const

class menuBox:
    
    def __init__(self, x, y, item):
        self.locX = x
        self.locY = y
        self.sizeX = const.blocksize
        self.sizeY = const.blocksize
        self.type = 'menuBox'
        self.item = item
    
    def hit(self, x, y):
        if self.locX <= x < self.locX+self.sizeX and self.locY <= y < self.locY+self.sizeY:
            return True
        else: return False
        