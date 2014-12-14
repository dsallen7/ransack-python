# A dictionary assigning item ID numbers to functions which
# carry out the effects of the spells

from UTIL import const
from SCRIPTS import spellScr


class Spell():

    def __init__(self, type):
        self.type = type
        self.img = type + 102
        self.cost = spellScr.costDict[self.type]
        self.level = 0
        self.name = 'spell'
        self.desc = spellScr.descDict[self.type]
        self.castMsg = spellScr.castMsgs[self.type]
        self.castTime = spellScr.timeDict[self.type]

    def getType(self):
        return self.type

    def getImg(self):
        return self.img

    def getLevel(self):
        return self.level

    def getDesc(self):
        return self.desc

    def getCastMsg(self):
        return self.castMsg

    def getCastTime(self):
        return self.castTime

    def execute(self, hero, hud, battle):
        hero.currMP = hero.currMP - self.cost
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX,
            psn] = hero.getPlayerStats()
        stats = [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn]
        fn = spellScr.spellDict[(self.getType(), battle)]
        stats = fn(stats)
        [cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys, cEX, nEX, psn] = stats
        hero.setPlayerStats((cHP, mHP, cMP, mMP, sth, dex, itl, scr, kys,
            cEX, nEX, psn))
