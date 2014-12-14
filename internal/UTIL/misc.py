import math, types, random
from random import choice

def Distance(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return max( abs(y2-y1), abs(x2-x1)  )

def eDistance(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return abs(y2-y1) + abs(x2-x1)

def DistanceX(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return abs(x2-x1)
def DistanceY(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return abs(y2-y1)

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring) and type(el) is not types.TupleType and type(el) is not types.NoneType:
            result.extend(flatten(el))
        elif type(el) is types.TupleType:
            result.append(el)
    return result

def weightedChoice(choices):
        choicesList = []
        for c in choices:
            choicesList += [c[1]]*c[0]
        return choice(choicesList)


def rollDie(target, range):
    d = random.randrange(range)
    if target >= d:
        return True
    else:
        return False

def armorIsCategory(armor, cat):
    from SCRIPTS import armorScr
    return cat == armorScr[armor.getType() ]