class Queue():
    
    def __init__(self):
        self.Q = []
    
    def push(self, e):
        self.Q.append(e)
    
    def pop(self):
        if len(self.Q) == 0:
            return None
        else: return self.Q.pop(0)
    
    def has(self, e):
        return e in self.Q
    
    def reset(self):
        self.Q = []
    
    def isEmpty(self):
        if len(self.Q) == 0:
            return True
        else: return False
    
    def size(self):
        return len(self.Q)