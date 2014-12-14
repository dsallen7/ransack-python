class Flash():
    
    def __init__(self, loc, size, cycles):
        
        self.loc = loc
        self.size = size
        self.cycles = cycles
        self.alpha = cycles * 51
    
    def cycle(self):
        if self.cycles == 0:
            return False
        else:
            self.cycles = self.cycles - 1
            self.alpha = self.cycles * 51
            return True