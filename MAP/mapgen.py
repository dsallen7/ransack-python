import os, pygame, pickle

from random import choice, randrange

from UTIL import const, colors

#from IMG import images

dirDict = { 'w':(-1,0), 'e':(1,0), 'n':(0,-1), 's':(0,1) }
DefaultWallTile = 29

DEFAULTBKGD = 0

EWDOOR = 38
NSDOOR = 81

EWWALL = 30
NSWALL = 31
URWALL = 27
LRWALL = 75
ULWALL = 40
LLWALL = 51


class Room():
    def __init__(self, xdim, ydim, pos=(0,0), shape='square'):
        self.pos = pos
        self.xdim = xdim
        self.ydim = ydim
        self.grid = [range(xdim) for _ in range(ydim)]
        self.entrances = []
        self.neighbors = []
        self.secret = False
        
        if shape == 'square':
            (xpos, ypos) = self.getPos()
            (xdim, ydim) = self.getDimensions()
            for i in range(1, xdim-1):
                self.setGrid(i, 0, EWWALL)
                self.setGrid(i, ydim-1, EWWALL)
            for i in range(1, ydim-1):
                self.setGrid(0, i, NSWALL)
                self.setGrid(xdim-1, i, NSWALL)
            self.setGrid(0,0, ULWALL)
            self.setGrid(xdim-1,0, URWALL)
            self.setGrid(0,ydim-1, LLWALL)
            self.setGrid(xdim-1,ydim-1, LRWALL)
            for i in range(1,xdim-1):
                for j in range(1,ydim-1):
                    self.setGrid(i, j, 0)
        if shape == 'round':
            (xpos, ypos) = self.getPos()
            self.xdim = 9
            self.ydim = 9
            self.grid = [ [126,126,ULWALL,EWWALL,EWWALL,EWWALL,URWALL,126,126],
                           [126,ULWALL,LRWALL,0,0,0,LLWALL,URWALL,126],
                           [ULWALL,LRWALL,0,0,0,0,0,LLWALL,URWALL],
                           [NSWALL,0,0,0,0,0,0,0,NSWALL],
                           [NSWALL,0,0,0,0,0,0,0,NSWALL],
                           [NSWALL,0,0,0,0,0,0,0,NSWALL],
                           [LLWALL,URWALL,0,0,0,0,0,ULWALL,LRWALL],
                           [126,LLWALL,URWALL,0,0,0,ULWALL,LRWALL,126],
                           [126,126,LLWALL,EWWALL,EWWALL,EWWALL,LRWALL,126,126]
                        ]
        
    def getDimensions(self):
        return (self.xdim, self.ydim)
    
    def getPos(self):
        return self.pos
    
    def setPos(self, pos):
        self.pos = pos
    
    def setGrid(self, x, y, e):
        #self.grid[y] = self.grid[y][:x] + [e] + self.grid[y][x+1:]
        self.grid[y][x] = e
    
    def getGrid(self, x, y):
        return self.grid[y][x]

class Map():
    def __init__(self, DIM, level=1):
        self.grid = []
        for i in range(DIM):
            self.grid += [[126]*DIM]
        self.DIM = DIM
        self.copyText = []
        self.level = level
        self.chests = {}
        self.shops = None
    
    def rollDie(self, target, range):
        d = randrange(range)
        if target >= d:
            return True
        else:
            return False
    
    def setMapEntry(self, x, y, e):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            self.grid[y] = self.grid[y][:x] + [e] + self.grid[y][x+1:]
    
    def getMapEntry(self, x, y):
        if 0 <= x < self.DIM and 0 <= y < self.DIM:
            return self.grid[y][x]
        else: return -1
    
    def genRoom(self, pos=(0,0), shape='square' ):
        return Room( randrange(5,8), randrange(5,8), pos, shape )
    
    
    # find a random exterior wall tile, see which way we're going
    def branchTile(self, room):
        (xpos, ypos) = room.getPos()
        (xdim, ydim) = room.getDimensions()
        candidateList = []
        for i in range(1,xdim-1):
            if self.getMapEntry(i+xpos,ypos) == const.EWWALL:
                candidateList += [(i+xpos,ypos)] + [(i+xpos,ypos+ydim-1)]
        for i in range(1,ydim-1):
            if self.getMapEntry(xpos,i+ypos) == const.NSWALL:
                candidateList += [(xpos,i+ypos)] + [(xpos+xdim-1,i+ypos)]
        cand = choice(candidateList)
        if cand[0] == xpos:
            return (cand, 'w')
        elif cand[0] == xpos+xdim-1:
            return (cand, 'e')
        elif cand[1] == ypos:
            return (cand, 'n')
        elif cand[1] == ypos+ydim-1:
            return (cand, 's')
    
    def checkNewRoom(self, newRoom, tile, dir):
        (xpos, ypos) = tile
        (xdim, ydim) = newRoom.getDimensions()
        if xpos + xdim + 1 >= self.DIM or ypos + ydim + 1 >= self.DIM:
            return False
        if xpos - xdim - 1 < 0 or ypos - ydim - 1 < 0:
            return False
        if dir == 'n':
            newRoomPos = ( xpos - xdim/2, (ypos - ydim) )
        elif dir == 's':
            newRoomPos = ( xpos - xdim/2, ypos + 1 )
        elif dir == 'w':
            newRoomPos = ( (xpos - xdim), ypos - ydim/2 )
        elif dir == 'e':
            newRoomPos = ( xpos + 1, ypos - ydim/2 )
        for i in range(newRoomPos[0], newRoomPos[0]+xdim):
            for j in range(newRoomPos[1], newRoomPos[1]+ydim):
                if self.getMapEntry(i, j) != 126:
                    return False
        newRoom.setPos(newRoomPos)
        return True
    
    def generateMap(self, maxRooms):
        rooms = []
        startingRoom = self.genRoom((0,0),'round')
        (xdim, ydim) = startingRoom.getDimensions()
        startingRoom.setPos( ( (self.DIM/2)-(xdim/2), (self.DIM/2)-(ydim/2) ) )
        self.addRoom(startingRoom, startingRoom.getPos() )
        rooms += [startingRoom]
        self.secretRooms = []
        
        while len(rooms) < maxRooms:
        
            # 4 select random room
            
            candidateRoom = choice(rooms)
            
            # 5 select random wall tile from above room
            
            tile, dir = self.branchTile(candidateRoom)
            
            # 6 generate new room
            '''
            if len(rooms) in [5,10,15]:
                newRoom = self.genRoom((0,0), 'round')
            else: newRoom = self.genRoom()
            '''
            newRoom = self.genRoom()
            
            # 7 see if new room fits next to selected room
            if self.checkNewRoom(newRoom, tile, dir):
                startingRoom.setPos( ( (self.DIM/2)-(xdim/2), (self.DIM/2)-(ydim/2) ) )
            # 8  if yes - continue, if not go back to step 4
            
            # 9 add new room to map and list of rooms
                self.addRoom(newRoom, newRoom.getPos() )
                rooms += [newRoom]
            
            # 9.a add rooms as neighbors
                candidateRoom.neighbors.append(newRoom)
                newRoom.neighbors.append(candidateRoom)
            # 9.b make room secret?
                if len(rooms) == maxRooms - 1:
                    newRoom.secret = True
                    self.secretRooms.append(newRoom)
                
            #10 create doorway into new room
                (x1,y1) = tile
                if dir in ['n','s']:
                    if newRoom.secret:
                        self.setMapEntry( x1,y1,const.EWFAKE )
                    else: self.setMapEntry( x1,y1,const.EWDOOR )
                else:
                    if newRoom.secret:
                        self.setMapEntry( x1,y1,const.NSFAKE )
                    else: self.setMapEntry( x1,y1,const.NSDOOR )
                candidateRoom.entrances.append( (x1,y1) )
                (x2,y2) = dirDict[dir]
                if dir == 'n':
                    self.setMapEntry( x1+x2-1, y1+y2, const.URWALL)
                    self.setMapEntry( x1+x2+1, y1+y2, const.ULWALL)
                elif dir == 's':
                    self.setMapEntry( x1+x2-1, y1+y2, const.LRWALL)
                    self.setMapEntry( x1+x2+1, y1+y2, const.LLWALL)
                elif dir == 'e':
                    self.setMapEntry( x1+x2, y1+y2-1, const.LRWALL)
                    self.setMapEntry( x1+x2, y1+y2+1, const.URWALL)
                elif dir == 'w':
                    self.setMapEntry( x1+x2, y1+y2-1, const.LLWALL)
                    self.setMapEntry( x1+x2, y1+y2+1, const.ULWALL)
                self.setMapEntry( x1+x2, y1+y2, 0)
                newRoom.entrances.append( (x1+x2,y1+y2) )
            # 11 repeat step 4
            
        # set staircases
        '''
        choice1 = choice(rooms)
        (xpos, ypos) = choice1.getPos()
        (xdim, ydim) = choice1.getDimensions()
        self.setMapEntry( xpos + xdim/2, ypos + ydim/2, 120)
        self.POE = ( xpos + xdim/2, ypos + ydim/2 )
        rooms.remove(choice1)
        '''
        # down
        choice2 = choice(rooms)
        # find room with only 1 entrance
        # WARNING: this algorithm not guaranteed to stop.
        while len(choice2.entrances) > 1 or choice2.secret:
            choice2 = choice(rooms)
        (xpos, ypos) = choice2.getPos()
        (xdim, ydim) = choice2.getDimensions()
        (doorX, doorY) = choice2.entrances[0]
        self.setMapEntry( xpos + xdim/2, ypos + ydim/2, 121)
        self.setMapEntry( doorX, doorY, 116)
        self.POEx = ( xpos + xdim/2, ypos + ydim/2 )
        
        # up
        choice1 = choice2.neighbors[0]
        (xpos, ypos) = choice1.getPos()
        (xdim, ydim) = choice1.getDimensions()
        self.setMapEntry( xpos + xdim/2, ypos + ydim/2, 120)
        self.POE = ( xpos + xdim/2, ypos + ydim/2 )
        rooms.remove(choice1)
        
        rooms.remove(choice2)
        
        # add key for door
        keyRoom = choice(rooms)
        (xpos, ypos) = keyRoom.getPos()
        (xdim, ydim) = keyRoom.getDimensions()
        self.setMapEntry( xpos + xdim/2, ypos + ydim/2, 98)
        rooms.remove(keyRoom)
        
        # set hero starting location - optional
        choice3 = choice(rooms)
        (xpos, ypos) = choice3.getPos()
        (xdim, ydim) = choice3.getDimensions()
        self.hs = ( xpos + xdim/2, ypos + ydim/2 )
        rooms.remove(choice3)
        
        #add chests
        chestlist = []
        for i in range(maxRooms/5):
            choice4 = choice(rooms)
            (xpos, ypos) = choice4.getPos()
            (xdim, ydim) = choice4.getDimensions()
            chestItems = []
            if self.rollDie(0,2) and self.rollDie(0,2):
                #gold
                chestItems = [(13,randrange(15,30))]
            elif self.rollDie(0,2):
                #chestItems = [(23,randrange(15,30))]
                chestItems.append((0,1))
            elif self.rollDie(0,2):
                #chestItems = [(23,randrange(15,30))]
                chestItems.append((1,1))
            else:
                #chestItems = [(23,randrange(15,30))]
                chestItems.append((4,1))
            self.setMapEntry( xpos + xdim/2, ypos + ydim/2, 110)
            chestlist += [( ( xpos + xdim/2, ypos + ydim/2), chestItems )]
            rooms.remove(choice4)
        for r in self.secretRooms:
            (xpos, ypos) = r.getPos()
            (xdim, ydim) = r.getDimensions()
            self.setMapEntry( xpos + xdim/2, ypos + ydim/2, 110)
            chestlist += [( ( xpos + xdim/2, ypos + ydim/2), [(randrange(31,34),0)] )]
            
        self.chests = dict(chestlist)
        print self.chests
        
    
    def getMapBall(self):
        return (self.grid, DEFAULTBKGD, self.POE, self.POEx, self.POE, self.shops, self.chests )
    
    def saveMap(self):
        ball = self.getMapBall()
        try:
            save = open('rmap.dat', "w")
            pickle.dump(ball, save)
            save.close()
        except pygame.error, message:
            print 'Cannot save map:', name
            raise SystemExit, message
    
    def mapCut(self, x, y):
        pass
    
    def mapCopy(self, x, y):
        pass
    
    def mapPaste(self, pos):
        (sX, sY) = pos
        copyText = self.copyText
        for i in range( len(copyText[0]) ):
            for j in range( len(copyText) ):
                self.setMapEntry(sX+i, sY+j, copyText[j][i] )
    
    def addRoom(self, room, pos):
        self.copyText = room.grid
        self.mapPaste( pos )
    
    def draw(self):
        gridField.fill( [0,0,0] )
        for i in range(DIM):
            for j in range(DIM):
                gridField.blit( images.mapImages[myMap.getMapEntry(i,j)], (i*blocksize,j*blocksize) )

        screen.blit(gridField, (0,0) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass