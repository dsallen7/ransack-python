import math


def Distance(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return max( abs(y2-y1), abs(x2-x1)  )

def DistanceX(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return abs(x2-x1)
def DistanceY(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return abs(y2-y1)