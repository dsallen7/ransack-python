#!/usr/bin/env python
# -*- coding: utf-8 -*-

from types import *
import pygame
import os
import cPickle
import random
import gzip

from MAP import mapgen, mazegen, generalmap

from UTIL import queue, const, colors, eztext, load_image, misc
from IMG import images


displayOpts = ['fore', 'back', 'both']


# Eztext courtesy of http://www.pygame.org/project-EzText-920-.html
class Handler():

    def __init__(self, cPos):
        self.cursorPos = cPos
        self.currentTile = 0
        self.sideImg, sideRect = load_image.load_image('sidebar.bmp')
        self.npcImg = pygame.Surface((30, 30))
        self.npcImg.fill(colors.red)
        #self.npcImg, npcR = load_image('npc.bmp')
        self.drawMode = False
        self.cursorColor = colors.white
        self.offset = 0
        self.numImages = len(mapImages)
        self.topX = 0
        self.topY = 0
        self.visited = []

        self.BFSQueue = queue.Queue()

        self.mouseAction = 'draw'
        self.selecting = False

        self.selectBoxPoints = None

        self.placeNPC = False

    def drawBox(self, pos, color):
        (x, y) = pos
        boxPoints = ((x, y), (x, y + blocksize),
                     (x + blocksize, y + blocksize), (x + blocksize, y))
        pygame.draw.lines(gridField, color, True, boxPoints, 1)

    def switchTile(self):
        self.currentTile += 1
        self.currentTile = self.currentTile % self.numImages

    #@tail_call_optimized
    def floodFillBFS(self, pieceLocation):
        if (pieceLocation is None):
            return
        (x, y) = pieceLocation
        entryList = []
        for (Cx, Cy) in const.CARDINALS:
            if (myMap.getEntry(x, y) == myMap.getEntry(x + Cx, y + Cy)
                    and (x + Cx, y + Cy) not in self.visited
                    and ~self.BFSQueue.has((x + Cy, y + Cy))):
                self.BFSQueue.push((x + Cx, y + Cy))
                entryList += [(x + Cx, y + Cy)]
                self.visited += [(x + Cx, y + Cy)]
            else:
                entryList += [None]
        if (entryList == [None, None, None, None]):
            return (x, y)
        else:
            return [(x, y)] + [self.floodFillBFS(self.BFSQueue.pop())] \
                + [self.floodFillBFS(self.BFSQueue.pop())] \
                + [self.floodFillBFS(self.BFSQueue.pop())] \
                + [self.floodFillBFS(self.BFSQueue.pop())]

    def floodFill(self, tile, start):
        (x, y) = start
        x = x / blocksize
        y = y / blocksize
        self.visited = [(x, y)]
        self.BFSQueue.reset()
        floodArea = misc.flatten(self.floodFillBFS((x, y)))
        floodArea = list(set(floodArea))
        for entry in floodArea:
            (x, y) = entry
            myMap.setEntry(x, y, tile)

    def getInput(self, msg):
        #get file name
        input = None
        txtbx = eztext.Input(maxlength=300, color=(255, 0, 0), prompt=msg)
        inputWindow = pygame.Surface((1200, 100))
        while input is None:
            # make sure the program is running at 30 fps
            clock.tick(30)

            # events for txtbx
            events = pygame.event.get()
            # process other events
            for event in events:
                # close it x button si pressed
                if event.type == pygame.QUIT:
                        os.sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input = txtbx.getValue()

            # clear the screen
            inputWindow.fill((25, 25, 25))
            # update txtbx
            txtbx.update(events)
            # blit txtbx on the sceen
            txtbx.draw(inputWindow)
            gridField.blit(inputWindow, (100, 100))
            screen.blit(gridField, (0, 0))
            # refresh the display
            pygame.display.flip()
        return input

    def fillChest(self):
        menuBox = pygame.Surface((150, 250))
        itemsList = range(86, 102) + [112, 113, 114, 117, 117]
        for i in range(len(itemsList)):
            menuBox.blit(mapImages[itemsList[i]],
                         (15 + ((i) % 4) * blocksize,
                         50 + ((i) / 4) * blocksize))
        chestItems = []
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return chestItems
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mx, my) = event.pos
                    if 115 <= mx < 235 and 150 <= my < 330:
                        itemNum = itemsList[(mx - 115) / blocksize
                            + (my - 150) / blocksize * 4]
                        if itemNum in range(86, 99):
                            chestItems.append((itemNum - const.FRUIT1, 1))
                        elif itemNum == const.GOLD:
                            chestItems.append((itemNum - const.FRUIT1,
                                int(self.getInput('Enter amount of gold: '))))
                        elif (itemNum == const.SPELLBOOK
                                or itemNum == const.PARCHMENT):
                            chestItems.append((itemNum - const.FRUIT1,
                                int(self.getInput('Enter spell number: '))))
                        elif itemNum in [112, 113, 114]:
                            chestItems.append((itemNum - const.FRUIT1,
                                int(self.getInput("Enter weapon level: ")),
                                [int(self.getInput("Enter plus Str: ")),
                                int(self.getInput("Enter plus Int: ")),
                                int(self.getInput("Enter plus Dex "))]))
                        elif itemNum in [const.SHIELD, const.BPLATE,
                                const.HELMET]:
                            chestItems.append((itemNum - const.FRUIT1,
                                int(self.getInput("Enter armor level: ")),
                                int(self.getInput("Enter resist: "))))
            for item in chestItems:
                menuBox.blit(mapImages[item[0] + const.FRUIT1],
                            (len(chestItems) * blocksize, 15))
            screen.blit(menuBox, (100, 100))
            pygame.display.flip()

    def getFilename(self):
        return self.getInput('Enter filename: ')

    def saveMap(self):
        filename = self.getFilename()
        ball = myMap.getMapBall()
        try:
            save = gzip.GzipFile(os.getcwd() + '/MAP/LEVELS/' + filename, 'wb')
            cPickle.dump(ball, save)
            save.close()
        except IOError, message:
            print 'Cannot load map:', filename
            return

    def loadMap(self):
        filename = self.getFilename()
        try:
            save = gzip.GzipFile(os.getcwd() + '/MAP/LEVELS/' + filename, 'rb')
            ball = cPickle.load(save)
            save.close()
            myMap.installBall(ball)
        except IOError, message:
            print 'Cannot load map:', filename
            return

    def generateMap(self, rooms):
        if rooms > 0:
            MG = mapgen.Generator(myMap.DIM)
            MG.generateMap(rooms)
            myMap.installBall(MG.getMapBall())
        else:
            MG = mazegen.Generator(myMap.DIM, 1)
            MG.generateMap()
            myMap.installBall(MG.getMapBall())

    def place(self, x, y, tile):
        if self.placeNPC:
            myMap.NPCs.append(((x, y), self.getInput('Enter NPC type: '),
                                       self.getInput('Enter message: ')))
        else:
            if self.currentTile == const.CHEST:
                myMap.addChest((x, y), self.fillChest())
                level = None
            elif self.currentTile == const.ITEMSDOOR:
                level = int(self.getInput('Itemshop level: '))
            elif self.currentTile == const.ARMRYDOOR:
                level = int(self.getInput('Armory level: '))
            elif self.currentTile == const.BLKSMDOOR:
                level = int(self.getInput('Blacksmith level: '))
            elif self.currentTile == const.MAGICDOOR:
                level = int(self.getInput('Magicshop level: '))
            else:
                level = None
            myMap.setEntry(x, y, tile, level)

    def removeNPC(self, x, y):
        for n in myMap.NPCs:
            if n[0] == (x, y):
                myMap.NPCs.remove(n)
                return

    def event_handler(self, event):
        (x, y) = self.cursorPos
        self.drawBox((x, y), colors.black)
        if event.key == pygame.K_RIGHT:
            if (x + blocksize < myMap.DIM * blocksize):
                x += blocksize
            if (x < myMap.DIM * blocksize and x == 20 * blocksize
                + self.topX * blocksize):
                self.topX += 1
        if event.key == pygame.K_LEFT:
            if (x - blocksize >= 0):
                x -= blocksize
            if x > 0 and x == self.topX * blocksize:
                self.topX -= 1
        if event.key == pygame.K_UP:
            if (y - blocksize >= 0):
                y -= blocksize
            if y > 0 and y == self.topY * blocksize:
                self.topY -= 1
        if event.key == pygame.K_DOWN:
            if (y + blocksize < myMap.DIM * blocksize):
                y += blocksize
            if (y < myMap.DIM * blocksize
                and y == 20 * blocksize + self.topY * blocksize):
                self.topY += 1
        if event.key == pygame.K_t:
            self.switchTile()
        if event.key == pygame.K_SPACE:
            self.place(x / blocksize, y / blocksize, self.currentTile)
        if event.key == pygame.K_ESCAPE:
            os.sys.exit()
        if event.key == pygame.K_d:
            self.drawMode = not self.drawMode
        if event.key == pygame.K_s:
            self.saveMap()
        if event.key == pygame.K_l:
            self.loadMap()
        if event.key == pygame.K_f:
            self.floodFill(self.currentTile, (x, y))
        if event.key == pygame.K_g:
            self.generateMap(int(self.getInput('Enter number of rooms: ')))
        if event.key == pygame.K_c:
            myMap.changeDimensions(int(self.getInput('Enter new dimension: ')))
        if event.key == pygame.K_e:
            self.offset += 32
            if self.offset == 128:
                self.offset = 0
        if event.key == pygame.K_x:
            self.removeNPC(x / blocksize, y / blocksize)
        if event.key == pygame.K_n:
            print 'NPCs: '
            print myMap.NPCs
        if self.drawMode:
            myMap.setEntry(x / blocksize, y / blocksize, self.currentTile)
        self.cursorPos = (x, y)

    def select(self, start):
        startX, startY = start
        endX = startX
        endY = startY
        self.selectBoxPoints = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.selectBox = self.selectBoxPoints
                    return (endX, endY)
                (tempX, tempY) = pygame.mouse.get_pos()
                if tempX > 600:
                    tempX = 600
                    pygame.mouse.set_pos([tempX, tempY])
                if tempY > 600:
                    tempY = 600
                    pygame.mouse.set_pos([tempX, tempY])
                endX = tempX / blocksize + 1
                endY = tempY / blocksize + 1
                self.updateDisplay()
                self.selectBoxPoints = ((startX * blocksize,
                                         startY * blocksize),
                                         (startX * blocksize,
                                         (startY + (endY - startY))
                                          * blocksize),
                                         (endX * blocksize, endY * blocksize),
                                         ((startX + (endX - startX))
                                         * blocksize, startY * blocksize))
                pygame.draw.lines(gridField, colors.red, True,
                                  self.selectBoxPoints, 1)
                screen.blit(gridField, (0, 0))
                pygame.display.flip()

    def move(self, start):
        (p1, p2, p3, p4) = self.selectBoxPoints
        sX, sY = start
        xDim = (p3[0] - p1[0]) / blocksize
        yDim = (p3[1] - p1[1]) / blocksize
        (tempX, tempY) = pygame.mouse.get_pos()
        xOffset = (tempX / blocksize) - (p1[0] / blocksize)
        yOffset = (tempY / blocksize) - (p1[1] / blocksize)
        oldTopX = ((tempX / blocksize) - xOffset)
        oldTopY = ((tempY / blocksize) - yOffset)
        newTopX = None
        newTopY = None
        selectionImg = pygame.Surface((xDim * blocksize, yDim * blocksize))
        emptyImg = pygame.Surface((xDim * blocksize, yDim * blocksize))
        for i in range(xDim):
            for j in range(yDim):
                selectionImg.blit(mapImages[myMap.getEntry(oldTopX + i,
                    oldTopY + j)], (i * blocksize, j * blocksize))
                emptyImg.blit(mapImages[0], (i * blocksize, j * blocksize))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if newTopX is None or newTopY is None:
                        return
                    else:
                        myMap.mapMove((sX / blocksize, sY / blocksize),
                            (xDim, yDim), (newTopX, newTopY))
                        return
                elif (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 3):
                    return
                elif event.type == pygame.MOUSEMOTION:
                    (tempX, tempY) = pygame.mouse.get_pos()
                    # upper left hand corner
                    newTopX = ((tempX / blocksize) - xOffset)
                    newTopY = ((tempY / blocksize) - yOffset)
                    oldTopX = p1[0] / blocksize
                    oldTopY = p1[1] / blocksize
                    if oldTopX == newTopX and oldTopY == newTopY:
                        pass
                    elif (0 <= newTopX * blocksize and (newTopX +
                            ((p3[0] - p1[0]) / blocksize))
                            * blocksize < 1200 and
                            0 <= newTopX * blocksize and
                            (newTopY + ((p3[1] - p1[1]) / blocksize))
                            * blocksize < 1200):
                        self.selectBoxPoints = (
                            (newTopX * blocksize, newTopY * blocksize),
                            (newTopX * blocksize, (newTopY + ((p3[1] - p1[1])
                            / blocksize)) * blocksize),
                            ((newTopX + ((p3[0] - p1[0]) / blocksize))
                            * blocksize, (newTopY + ((p3[1] - p1[1])
                            / blocksize)) * blocksize),
                            ((newTopX + ((p3[0] - p1[0]) / blocksize))
                            * blocksize, newTopY * blocksize))
                        (p1, p2, p3, p4) = self.selectBoxPoints
                        self.updateDisplay()
                        gridField.blit(emptyImg, (sX * blocksize,
                                                  sY * blocksize))
                        gridField.blit(selectionImg, (newTopX * blocksize,
                                                      newTopY * blocksize))
                        pygame.draw.lines(gridField, colors.red, True,
                                          self.selectBoxPoints, 1)
                        screen.blit(gridField, (0, 0))
                        pygame.display.flip()

    def mouseHandler(self, e):
        (mx, my) = e.pos
        if (0 <= mx < gridField.get_width()
                and 0 <= my < gridField.get_height()):
            if e.button == 1:
                if self.mouseAction == 'draw':
                    if self.placeNPC:
                        myMap.NPCs.append(((mx / blocksize, my / blocksize),
                                          self.getInput('Enter NPC type: '),
                                          self.getInput('Enter message: ')))
                    else:
                        if self.currentTile == const.CHEST:
                            myMap.addChest((mx / blocksize, my / blocksize),
                                           self.fillChest())
                            level = None
                        elif self.currentTile == const.ITEMSDOOR:
                            level = int(self.getInput('Itemshop level: '))
                        elif self.currentTile == const.ARMRYDOOR:
                            level = int(self.getInput('Armory level: '))
                        elif self.currentTile == const.BLKSMDOOR:
                            level = int(self.getInput('Blacksmith level: '))
                        elif self.currentTile == const.MAGICDOOR:
                            level = int(self.getInput('Magicshop level: '))
                        else:
                            level = None
                        myMap.setEntry(mx / blocksize, my / blocksize,
                                       self.currentTile, level)
                    self.cursorPos = ((mx / blocksize) * blocksize,
                                     (my / blocksize) * blocksize)
                elif self.mouseAction == 'select':
                    if self.selectBoxPoints is not None:
                        (p1, p2, p3, p4) = self.selectBoxPoints
                        if p1[0] <= mx < p3[0] and p1[1] <= my < p3[1]:
                            self.move((p1[0], p1[1]))
                        else:
                            self.selection = ((mx / blocksize,
                                my / blocksize), self.select((mx / blocksize,
                                my / blocksize)))
                    else:
                        self.selection = ((mx / blocksize, my / blocksize),
                            self.select((mx / blocksize, my / blocksize)))
            elif e.button == 3:
                pass
        elif (gridField.get_width() + 50 <= mx < gridField.get_width() + 80
                and 170 <= my < 200):
            self.placeNPC = not self.placeNPC
        elif (gridField.get_width() + 50 <= mx < gridField.get_width() + 170
                and 200 <= my < 440):
            if e.button == 1:
                self.currentTile = (self.offset + (mx - gridField.get_width()
                    - 45) / blocksize + (my - 200) / blocksize * 4)
            elif e.button == 3:
                myMap.defaultBkgd = (self.offset + (mx - gridField.get_width()
                    - 45) / blocksize + (my - 200) / blocksize * 4)
        elif (gridField.get_width() + 65 <= mx < gridField.get_width() + 95
                and 500 <= my < 530):
            self.offset -= 32
            if self.offset < 0:
                self.offset = 96
        elif (gridField.get_width() + 95 <= mx < gridField.get_width() + 125
                and 500 <= my < 530):
            self.offset += 32
            if self.offset == 128:
                self.offset = 0
        elif (gridField.get_width() + 50 <= mx < gridField.get_width() + 80
                and 530 <= my < 560):
            myMap.mapCut()
        elif (gridField.get_width() + 80 <= mx < gridField.get_width() + 110
                and 530 <= my < 560):
            myMap.mapCopy(self.selection)
        elif (gridField.get_width() + 110 <= mx < gridField.get_width() + 140
                and 530 <= my < 560):
            myMap.mapPaste()
        elif (gridField.get_width() + 65 <= mx < gridField.get_width() + 95
                and 560 <= my < 590):
            self.mouseAction = 'draw'
        elif (gridField.get_width() + 95 <= mx < gridField.get_width() + 125
                and 560 <= my < 590):
            self.mouseAction = 'select'

    def mouseUpdate(self):
        (mx, my) = pygame.mouse.get_pos()
        if 650 <= mx < 770 and 200 <= my < 440:
            boxPoints = ((mx, my), (mx, my + blocksize),
                        (mx + blocksize, my + blocksize),
                        (mx + blocksize, my))
            pygame.draw.lines(screen, colors.red, True, boxPoints, 1)

    def updateDisplay(self):
        gridField.fill(colors.black)
        for i in range(self.topX, self.topX + 40):
            for j in range(self.topY, self.topY + 40):
                if myMap.getEntry(i, j) in range(24, 86):
                    gridField.blit(mapImages[myMap.defaultBkgd],
                    ((i - self.topX) * blocksize, (j - self.topY) * blocksize))
                gridField.blit(mapImages[myMap.getEntry(i, j)],
                    ((i - self.topX) * blocksize, (j - self.topY) * blocksize))
                if (i, j) == myMap.heroStart:
                    gridField.blit(mapImages[const.HEROSTART],
                     ((i - self.topX) * blocksize,
                     (j - self.topY) * blocksize))
                if myMap.shops is not None:
                    for s in myMap.shops:
                        if myMap.shops[s][0] == 'itemshop':
                            (sX, sY) = s
                            gridField.blit(mapImages[128],
                             (sX * blocksize - blocksize,
                              sY * blocksize - (2 * blocksize)))
                        if myMap.shops[s][0] == 'magicshop':
                            (sX, sY) = s
                            gridField.blit(mapImages[129],
                             (sX * blocksize - blocksize,
                              sY * blocksize - (2 * blocksize)))
                        if myMap.shops[s][0] == 'blacksmith':
                            (sX, sY) = s
                            gridField.blit(mapImages[130],
                             (sX * blocksize - blocksize,
                              sY * blocksize - (2 * blocksize)))
                        if myMap.shops[s][0] == 'armory':
                            (sX, sY) = s
                            gridField.blit(mapImages[131],
                             (sX * blocksize - blocksize,
                              sY * blocksize - (2 * blocksize)))
                        if myMap.shops[s][0] == 'tavern':
                            (sX, sY) = s
                            gridField.blit(mapImages[132],
                             (sX * blocksize - blocksize,
                              sY * blocksize - (3 * blocksize)))
        for n in myMap.NPCs:
            (x, y) = n[0]
            gridField.blit(self.npcImg, ((x - self.topX) * blocksize,
                (y - self.topY) * blocksize))
        (x, y) = self.cursorPos
        x = x - self.topX * blocksize
        y = y - self.topY * blocksize
        if self.drawMode:
            self.cursorColor = colors.yellow
        else:
            self.cursorColor = colors.white
        if self.selectBoxPoints is not None:
            pygame.draw.lines(gridField, colors.red, True,
                              self.selectBoxPoints, 1)

        boxPoints = ((x, y), (x, y + blocksize),
            (x + blocksize, y + blocksize), (x + blocksize, y))
        pygame.draw.lines(gridField, self.cursorColor, True, boxPoints, 1)
        self.sideImg, sideRect = load_image.load_image('sidebar.bmp')
        if self.placeNPC:
            self.sideImg.blit(self.npcImg, (50, 50))
        else:
            self.sideImg.blit(mapImages[self.currentTile], (50, 50))
        self.sideImg.blit(mapImages[myMap.defaultBkgd], (50, 130))
        if self.mouseAction == 'draw':
            self.sideImg.blit(images.editorImages[5], (50, 80))
        else:
            self.sideImg.blit(images.editorImages[6], (50, 80))
        self.sideImg.blit(self.npcImg, (50, 170))
        for i in range(8):
            for j in range(4):
                self.sideImg.blit(mapImages[self.offset + j + (4 * i)],
                    (50 + j * blocksize, 200 + (i * blocksize)))

        toolBox = pygame.Surface((90, 90))
        toolBox.blit(images.editorImages[0], (15, 0))
        toolBox.blit(images.editorImages[1], (45, 0))
        toolBox.blit(images.editorImages[2], (0, 30))
        toolBox.blit(images.editorImages[3], (30, 30))
        toolBox.blit(images.editorImages[4], (60, 30))
        toolBox.blit(images.editorImages[5], (15, 60))
        toolBox.blit(images.editorImages[6], (45, 60))
        self.sideImg.blit(toolBox, (50, 500))
        (x, y) = self.cursorPos
        entryBox = pygame.Surface((150, 30))
        entryBox.fill(colors.black)
        if pygame.font:
            font = pygame.font.SysFont("arial", 20)
            entry = font.render(str(myMap.getEntry((x + self.topX) / blocksize,
                (y + self.topY) / blocksize)) + ' ' + 'x:' + str(x) + ' y:'
                 + str(y), 1, colors.white, colors.black)
            entryBox.blit(entry, (0, 0))
            self.sideImg.blit(entryBox, (80, 50))
        if self.drawMode:
            msgBox = pygame.Surface((186, 60))
            msgBox.fill(colors.grey)
            if pygame.font:
                font = pygame.font.SysFont("arial", 24)
                msgText = font.render('draw', 1, colors.red, colors.yellow)
                msgBox.blit(msgText, (10, 10))
            self.sideImg.blit(msgBox, (50, 100))
            #pygame.display.flip()
        screen.blit(self.sideImg, (1200, 0))


# Set the height and width of the screen
size = [1400, 800]
screen = pygame.display.set_mode(size)

images.load()
mapImages = images.mapImages
pygame.init()
pygame.key.set_repeat(50, 100)
clock = pygame.time.Clock()

cursorPos = (0, 0)

myMap = generalmap.edMap()
myHandler = Handler(cursorPos)

blocksize = 30

gridField = pygame.Surface([2 * const.DIM * blocksize,
                           2 * const.DIM * blocksize])

os.sys.setrecursionlimit(15000)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                myHandler.event_handler(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # or event.type == pygame.MOUSEBUTTONUP:
                myHandler.mouseHandler(event)
            if event.type == pygame.QUIT:
                os.sys.exit()
        myHandler.mouseUpdate()
        myHandler.updateDisplay()
        screen.blit(gridField, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    main()
