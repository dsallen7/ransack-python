import os
import pygame
import pickle

from random import choice, randrange
from MAP import generalmap, tile
from ROOM import room, roomtools
from UTIL import const, colors, misc

from SCRIPTS import enemyScr, mapScr


DefaultWallTile = 29

DEFAULTBKGD = 0

class Generator():

    def __init__(self, DIM, level=1):
        self.generalmap = generalmap.genMap(DIM, level, 'Dungeon Level ' + str(level))
        self.generalmap.type = 'dungeon'
        self.copyText = []
        self.level = level

    def genRoom(self, pos=(0,0), shape='square' ):
        return room.Room(randrange(5,8), randrange(5,8), pos, shape)

    # find a random exterior wall tile, see which way we're going
    def branchTile(self, generalmap, room):
        (xpos, ypos) = room.getPos()
        (xdim, ydim) = room.getDimensions()
        candidateList = [ ]
        #room.printGrid()
        for i in range(1,xdim-1):
            #print generalmap.getEntry(i+xpos,ypos), room.getGrid(i,0).getFG()
            if generalmap.getEntry(i+xpos,ypos) == const.EWWALL:
                candidateList += [(i+xpos,ypos)]
            #print generalmap.getEntry(i+xpos,ypos+ydim-1), room.getGrid(i,ydim-1).getFG()
            if generalmap.getEntry(i+xpos,ypos+ydim-1) == const.EWWALL:
                candidateList += [(i+xpos,ypos+ydim-1)]
        for i in range(1,ydim-1):
            #print generalmap.getEntry(xpos,i+ypos), room.getGrid(0,i).getFG()
            if generalmap.getEntry(xpos,i+ypos) == const.NSWALL:
                candidateList += [(xpos,i+ypos)]
            #print generalmap.getEntry(xpos+xdim-1,i+ypos), room.getGrid(xdim-1,i).getFG()
            if generalmap.getEntry(xpos+xdim-1,i+ypos) == const.NSWALL:
                candidateList += [(xpos+xdim-1,i+ypos)]
        
        #print candidateList
        cand = choice(candidateList)
        if cand[0] == xpos:
            return (cand, 'w')
        elif cand[0] == xpos+xdim-1:
            return (cand, 'e')
        elif cand[1] == ypos:
            return (cand, 'n')
        elif cand[1] == ypos+ydim-1:
            return (cand, 's')
    
    def checkNewRoom(self, generalmap, newRoom, tile, dir):
        print tile
        (xpos, ypos) = tile
        (xdim, ydim) = newRoom.getDimensions()
        if xpos + xdim + 1 >= generalmap.DIM or ypos + ydim + 1 >= generalmap.DIM:
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
                if generalmap.getEntry(i, j) != const.VOID:
                    return False
        newRoom.setPos(newRoomPos)
        return True
    
    def generateMap(self, maxRooms):
        self.rooms = []
        startingRoom = self.genRoom((0,0),'round')
        (xdim, ydim) = startingRoom.getDimensions()
        startingRoom.setPos( ( (self.generalmap.DIM/2)-(xdim/2), (self.generalmap.DIM/2) - (ydim/2)))
        self.rooms += [startingRoom]
        self.addRoom(self.generalmap, startingRoom, startingRoom.getPos() )
        self.secretRooms = []
        
        while len(self.rooms) < maxRooms:
            # 4 select random room
            
            candidateRoom = choice(self.rooms)
            
            # 5 select random wall tile from above room
            
            tile, dir = self.branchTile(self.generalmap, candidateRoom)
            
            # 6 generate new room
            '''
            if len(rooms) in [5,10,15]:
                newRoom = self.genRoom((0,0), 'round')
            else: newRoom = self.genRoom()
            '''
            newRoom = self.genRoom( )
            
            # 7 see if new room fits next to selected room
            if self.checkNewRoom(self.generalmap, newRoom, tile, dir):
                startingRoom.setPos( ( (self.generalmap.DIM/2)-(xdim/2), (self.generalmap.DIM/2)-(ydim/2) ) )
            # 8  if yes - continue, if not go back to step 4
            
            # 9 add new room to generalmap and list of rooms
                self.rooms += [newRoom]
                self.addRoom(self.generalmap, newRoom, newRoom.getPos() )
            
            # 9.a add rooms as neighbors
                candidateRoom.neighbors.append(newRoom)
                newRoom.neighbors.append(candidateRoom)
            # 9.b make room secret?
                if len(self.rooms) == maxRooms - 1:
                    newRoom.secret = True
                    self.secretRooms.append(newRoom)
                
            #10 create doorway into new room
                roomtools.addDoorway(tile, dir, newRoom, candidateRoom, self)
            # 10a check to see if more neighbors can be added
                roomtools.checkForNeighbors(newRoom, candidateRoom, self)
                
            # 11 repeat step 4
            
        # set staircases
        '''
        choice1 = choice(rooms)
        (xpos, ypos) = choice1.getPos()
        (xdim, ydim) = choice1.getDimensions()
        self.generalmap.setEntry( xpos + xdim/2, ypos + ydim/2, 120)
        self.POE = ( xpos + xdim/2, ypos + ydim/2 )
        rooms.remove(choice1)
        '''
        # down
        choice1 = choice(self.rooms)
        # find room with only 1 entrance to place stairs leading down and dungeon door
        # WARNING: this algorithm not guaranteed to stop.
        while len(choice1.entrances) > 1 or choice1.secret or choice1.neighbors[0].secret:
            choice1 = choice(self.rooms)
        (xpos, ypos) = choice1.getPos()
        (xdim, ydim) = choice1.getDimensions()
        (doorX, doorY) = choice1.entrances[0]
        self.generalmap.setEntry( xpos + xdim/2, ypos + ydim/2, const.STAIRDN, len(self.rooms))
        self.generalmap.setEntry( doorX, doorY, const.DOOR, len(self.rooms))
        self.generalmap.pointOfExit = ( xpos + xdim/2, ypos + ydim/2 )
        
        # up
        choice2 = choice1.neighbors[0]
        (xpos, ypos) = choice2.getPos()
        (xdim, ydim) = choice2.getDimensions()
        self.generalmap.setEntry( xpos + xdim/2, ypos + ydim/2, const.STAIRUP, len(self.rooms))
        self.generalmap.pointOfEntry = ( xpos + xdim/2, ypos + ydim/2 )
        self.generalmap.heroStart = ( xpos + xdim/2, ypos + ydim/2 )
        self.rooms.remove(choice1)
        
        self.rooms.remove(choice2)
        # set hero starting location - optional
        choice3 = choice(self.rooms)
        (xpos, ypos) = choice3.getPos()
        (xdim, ydim) = choice3.getDimensions()
        self.generalmap.hs = ( xpos + xdim/2, ypos + ydim/2 )
        self.rooms.remove(choice3)
        
        #add chests
        chestlist = []
        for i in range(maxRooms/5):
            choice4 = choice(self.rooms)
            (xpos, ypos) = choice4.getPos()
            (xdim, ydim) = choice4.getDimensions()
            chestItems = []
            '''
            if misc.rollDie(0, 2):
                chestItems.append( (randrange(26,29), self.level/4,
                                                               [randrange( (self.level/4)+1, (self.level/4)+3 ),
                                                                randrange( (self.level/4)+1, (self.level/4)+3 ),
                                                                randrange( (self.level/4)+1, (self.level/4)+3 )] ) )
            else: chestItems.append( (randrange(31,34), self.level/4, randrange(0, 3) ) )
            '''
            chestItems.append( (const.PARCHMENT, choice(mapScr.parchByLevel[self.level]) ) )
            if misc.rollDie(0, 2):
                chestItems.append( (const.GOLD, choice( range(15, 50)+range(15,30) ) ))
            self.generalmap.setEntry( xpos + xdim/2, ypos + ydim/2, const.CHEST, len(self.rooms))
            chestlist += [( ( xpos + xdim/2, ypos + ydim/2), chestItems )]
            self.rooms.remove(choice4)
        
        for room in self.secretRooms:
            (xpos, ypos) = room.getPos()
            (xdim, ydim) = room.getDimensions()
            self.generalmap.setEntry( xpos + xdim/2, ypos + ydim/2, const.CHEST, len(self.rooms))
            sItem = choice( mapScr.specialByLevel[self.level] )
            if sItem in range(const.WSWORD, const.RING):
                mods = [randrange( (self.level/4)+1, 
                                   (self.level/4)+3 ),
                        randrange( (self.level/4)+1, 
                                   (self.level/4)+3 ),
                        randrange( (self.level/4)+1, 
                                   (self.level/4)+3 )]
                chestlist += [( ( xpos + xdim/2, 
                                  ypos + ydim/2), 
                                [ (sItem, mods)] )]
            elif sItem in range(const.HELMET, const.SSHIELD+1):
                chestlist += [ ( ( xpos + xdim/2, 
                                   ypos + ydim/2), 
                               [(sItem,None)] )]
            
        self.generalmap.chests = dict(chestlist)
        # add enemies
        while len(self.rooms) > 1:
            room = choice(self.rooms)
            (xpos, ypos) = room.getPos()
            (xdim, ydim) = room.getDimensions()
            self.generalmap.NPCs.append( (( xpos + xdim/2, 
                                     ypos + ydim/2), 
                                   choice(enemyScr.enemiesByDungeonLevel[self.generalmap.level] ) ) )
            self.rooms.remove(room)
        
        # add key for door
        keyRoom = self.rooms[0]
        (xpos, ypos) = keyRoom.getPos()
        (xdim, ydim) = keyRoom.getDimensions()
        self.generalmap.setEntry( xpos + xdim/2, ypos + ydim/2, const.KEY, len(self.rooms))
        self.rooms.remove(keyRoom)
               
    def addRoom(self, generalmap, room, pos):
        room.serial = len(self.rooms)
        generalmap.copyText = room.grid
        generalmap.mapPaste(pos, len(self.rooms))

    def getMapBall(self):
        return self.generalmap.getMapBall()

    def getRoomByNo(self, N):
        for r in self.rooms:
            if r.serial == N:
                return r

    def addDoorway(self, t1, t2):
        pass

    def draw(self):
        gridField.fill([0,0,0])
        for i in range(DIM):
            for j in range(DIM):
                gridField.blit(images.mapImages[myMap.getMapEntry(i,j)], (i*blocksize,j * blocksize))

        screen.blit(gridField, (0,0) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN):
            pass
