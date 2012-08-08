import os, pygame, pickle

from random import choice, randrange

#from IMG import images

dirDict = { 'w':(-1,0), 'e':(1,0), 'n':(0,-1), 's':(0,1) }
DefaultWallTile = 29

class Room():
    def __init__(self, xdim, ydim, pos=(0,0), shape='Square'):
        self.pos = pos
        self.xdim = xdim
        self.ydim = ydim
        self.grid = [range(xdim) for _ in range(ydim)]
        self.entrances = []
        
        if shape == 'square':
            (xpos, ypos) = self.getPos()
            (xdim, ydim) = self.getDimensions()
            for i in range(xdim):
                self.setGrid(i, 0, DefaultWallTile)
                self.setGrid(i, ydim-1, DefaultWallTile)
            for i in range(ydim):
                self.setGrid(0, i, DefaultWallTile)
                self.setGrid(xdim-1, i, DefaultWallTile)
            for i in range(1,xdim-1):
                for j in range(1,ydim-1):
                    self.setGrid(i, j, 0)
        
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
    def __init__(self, DIM):
        self.grid = []
        for i in range(DIM):
            self.grid += [[126]*DIM]
        self.DIM = DIM
        self.copyText = []
        
        self.chests = {}
    
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
    
    def genRoom(self, pos=(0,0) ):
        return Room( randrange(5,8), randrange(5,8), pos, shape='square' )
        
    def branchTile(self, room):
        (xpos, ypos) = room.getPos()
        (xdim, ydim) = room.getDimensions()
        candidateList = []
        for i in range(1,xdim-1):
            candidateList += [(i+xpos,ypos)] + [(i+xpos,ypos+ydim-1)]
        for i in range(1,ydim-1):
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
        startingRoom = self.genRoom()
        (xdim, ydim) = startingRoom.getDimensions()
        startingRoom.setPos( ( (self.DIM/2)-(xdim/2), (self.DIM/2)-(ydim/2) ) )
        self.addRoom(startingRoom, startingRoom.getPos() )
        rooms += [startingRoom]
        
        while len(rooms) < maxRooms:
        
            # 4 select random room
            
            candidateRoom = choice(rooms)
            
            # 5 select random wall tile from above room
            
            tile, dir = self.branchTile(candidateRoom)
            
            # 6 generate new room
            
            newRoom = self.genRoom()
            
            # 7 see if new room fits next to selected room
            if self.checkNewRoom(newRoom, tile, dir):
                startingRoom.setPos( ( (self.DIM/2)-(xdim/2), (self.DIM/2)-(ydim/2) ) )
            # 8  if yes - continue, if not go back to step 4
            
            # 9 add new room to map and list of rooms
                self.addRoom(newRoom, newRoom.getPos() )
                rooms += [newRoom]
                
            #10 create doorway into new room
                (x1,y1) = tile
                self.setMapEntry( x1,y1,38 )
                candidateRoom.entrances.append( (x1,y1) )
                (x2,y2) = dirDict[dir]
                self.setMapEntry( x1+x2, y1+y2, 0)
                newRoom.entrances.append( (x1+x2,y1+y2) )
            # 11 repeat step 4
            
        # set staircases
        # up
        choice1 = choice(rooms)
        (xpos, ypos) = choice1.getPos()
        (xdim, ydim) = choice1.getDimensions()
        self.setMapEntry( xpos + xdim/2, ypos + ydim/2, 120)
        self.POE = ( xpos + xdim/2, ypos + ydim/2 )
        rooms.remove(choice1)
        # down
        choice2 = choice(rooms)
        # find room with only 1 entrance
        # WARNING: this algorithm not guaranteed to stop.
        while len(choice2.entrances) > 1:
            choice2 = choice(rooms)
        (xpos, ypos) = choice2.getPos()
        (xdim, ydim) = choice2.getDimensions()
        (doorX, doorY) = choice2.entrances[0]
        self.setMapEntry( xpos + xdim/2, ypos + ydim/2, 121)
        self.setMapEntry( doorX, doorY, 116)
        self.POEx = ( xpos + xdim/2, ypos + ydim/2 )
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
        self.chests = dict(chestlist)
        
    
    def getMapBall(self):
        return (self.grid, self.POE, self.POEx, self.POE, self.chests )
    
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