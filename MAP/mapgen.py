import os, pygame, cPickle

from random import choice, randrange
from MAP import map, tile, room
from UTIL import const, colors, misc

from SCRIPTS import enemyScr, mapScr

#from IMG import images

dirDict = { 'w':(-1,0), 'e':(1,0), 'n':(0,-1), 's':(0,1) }
DefaultWallTile = 29

DEFAULTBKGD = 0

class Generator():
    
    def __init__(self, DIM, level=1):
        self.map = map.genMap(DIM, level, 'Dungeon Level '+str(level) )
        self.map.type = 'dungeon'
        self.copyText = []
        self.level = level
        
    def genRoom(self, pos=(0,0), shape='square' ):
        return room.Room( randrange(5,8), randrange(5,8), pos, shape )
    
    # find a random exterior wall tile, see which way we're going
    def branchTile(self, map, room):
        (xpos, ypos) = room.getPos()
        (xdim, ydim) = room.getDimensions()
        candidateList = []
        for i in range(1,xdim-1):
            if map.getEntry(i+xpos,ypos) == const.EWWALL:
                candidateList += [(i+xpos,ypos)] + [(i+xpos,ypos+ydim-1)]
        for i in range(1,ydim-1):
            if map.getEntry(xpos,i+ypos) == const.NSWALL:
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
    
    def checkNewRoom(self, map, newRoom, tile, dir):
        (xpos, ypos) = tile
        (xdim, ydim) = newRoom.getDimensions()
        if xpos + xdim + 1 >= map.DIM or ypos + ydim + 1 >= map.DIM:
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
                if map.getEntry(i, j) != const.VOID:
                    return False
        newRoom.setPos(newRoomPos)
        return True
    
    def generateMap(self, maxRooms):
        self.rooms = []
        startingRoom = self.genRoom( (0,0),'round')
        (xdim, ydim) = startingRoom.getDimensions()
        startingRoom.setPos( ( (self.map.DIM/2)-(xdim/2), (self.map.DIM/2)-(ydim/2) ) )
        self.rooms += [startingRoom]
        self.addRoom(self.map, startingRoom, startingRoom.getPos() )
        self.secretRooms = []
        
        while len(self.rooms) < maxRooms:
            # 4 select random room
            
            candidateRoom = choice(self.rooms)
            
            # 5 select random wall tile from above room
            
            tile, dir = self.branchTile(self.map, candidateRoom)
            
            # 6 generate new room
            '''
            if len(rooms) in [5,10,15]:
                newRoom = self.genRoom((0,0), 'round')
            else: newRoom = self.genRoom()
            '''
            newRoom = self.genRoom( )
            
            # 7 see if new room fits next to selected room
            if self.checkNewRoom(self.map, newRoom, tile, dir):
                startingRoom.setPos( ( (self.map.DIM/2)-(xdim/2), (self.map.DIM/2)-(ydim/2) ) )
            # 8  if yes - continue, if not go back to step 4
            
            # 9 add new room to map and list of rooms
                self.rooms += [newRoom]
                self.addRoom(self.map, newRoom, newRoom.getPos() )
            
            # 9.a add rooms as neighbors
                candidateRoom.neighbors.append(newRoom)
                newRoom.neighbors.append(candidateRoom)
            # 9.b make room secret?
                if len(self.rooms) == maxRooms - 1:
                    newRoom.secret = True
                    self.secretRooms.append(newRoom)
                
            #10 create doorway into new room
                (x1,y1) = tile
                if dir in ['n','s']:
                    if newRoom.secret:
                        self.map.setEntry( x1,y1,const.EWFAKE, len(self.rooms) )
                    else: self.map.setEntry( x1,y1,const.EWDOOR, len(self.rooms) )
                else:
                    if newRoom.secret:
                        self.map.setEntry( x1,y1,const.NSFAKE, len(self.rooms) )
                    else: self.map.setEntry( x1,y1,const.NSDOOR, len(self.rooms) )
                candidateRoom.entrances.append( (x1,y1) )
                (x2,y2) = dirDict[dir]
                if dir == 'n':
                    self.map.setEntry( x1+x2-1, y1+y2, const.URWALL, len(self.rooms))
                    self.map.setEntry( x1+x2+1, y1+y2, const.ULWALL, len(self.rooms))
                elif dir == 's':
                    self.map.setEntry( x1+x2-1, y1+y2, const.LRWALL, len(self.rooms))
                    self.map.setEntry( x1+x2+1, y1+y2, const.LLWALL, len(self.rooms))
                elif dir == 'e':
                    self.map.setEntry( x1+x2, y1+y2-1, const.LRWALL, len(self.rooms))
                    self.map.setEntry( x1+x2, y1+y2+1, const.URWALL, len(self.rooms))
                elif dir == 'w':
                    self.map.setEntry( x1+x2, y1+y2-1, const.LLWALL, len(self.rooms))
                    self.map.setEntry( x1+x2, y1+y2+1, const.ULWALL, len(self.rooms))
                self.map.setEntry( x1+x2, y1+y2, 0, len(self.rooms))
                newRoom.entrances.append( (x1+x2,y1+y2) )
            # 10a check to see if more neighbors can be added
                (xpos, ypos) = newRoom.getPos()
                (xD, yD) = newRoom.getDimensions()
                [nFlag, sFlag, eFlag, wFlag] = [False, False, False, False]
                for i in range( xpos+1, xpos+xD ):
                    if self.map.getEntry( i, ypos ) == const.EWWALL:
                        if self.map.getEntry( i, ypos-1 ) == const.EWWALL and not nFlag:
                            if self.getRoomByNo( self.map.getRoomN(i, ypos-1)) is not candidateRoom: # to the north
                                if self.getRoomByNo( self.map.getRoomN(i, ypos) ) not in self.getRoomByNo( self.map.getRoomN(i, ypos-1)).neighbors and self.getRoomByNo( self.map.getRoomN(i, ypos-1) ) not in self.getRoomByNo( self.map.getRoomN(i, ypos)).neighbors: # to the north
                                    self.map.setEntry( i, ypos, const.EWDOOR, len(self.rooms) )
                                    self.map.setEntry( i, ypos-1, const.DFLOOR1, len(self.rooms) )
                                    #self.map.setEntry( i-1, ypos-1, const.URWALL, len(self.rooms) )
                                    #self.map.setEntry( i+1, ypos-1, const.ULWALL, len(self.rooms) )
                                    nFlag = True
                    elif self.map.getEntry( i, ypos + yD ) == const.EWWALL:
                        if self.map.getEntry( i, ypos + yD + 1 ) == const.EWWALL and not sFlag:
                            if self.getRoomByNo( self.map.getRoomN(i, ypos+yD+1) ) is not candidateRoom: # south
                                if self.getRoomByNo( self.map.getRoomN(i, ypos+yD) ) not in self.getRoomByNo( self.map.getRoomN(i, ypos+yD+1) ).neighbors and self.getRoomByNo( self.map.getRoomN(i, ypos+yD+1) ) not in self.getRoomByNo( self.map.getRoomN(i, ypos+yD) ).neighbors:
                                    self.map.setEntry( i, ypos+yD, const.EWDOOR, len(self.rooms) )
                                    self.map.setEntry( i, ypos+yD+1, const.DFLOOR1, len(self.rooms) )
                                    #self.map.setEntry( (xpos + xD/2)-1, ypos+yD+1, const.LRWALL, len(self.rooms) )
                                    #self.map.setEntry( (xpos + xD/2)+1, ypos+yD+1, const.LLWALL, len(self.rooms) )
                                    sFlag = True
                for i in range( ypos+1, ypos+yD ):
                    if self.map.getEntry( xpos, i ) == const.NSWALL:
                        if self.map.getEntry( xpos-1, i ) == const.NSWALL and not eFlag:
                            if self.getRoomByNo( self.map.getRoomN(xpos-1, i) ) is not candidateRoom: # east
                                if self.getRoomByNo( self.map.getRoomN(xpos, i) ) not in self.getRoomByNo( self.map.getRoomN(xpos-1, i) ).neighbors and self.getRoomByNo( self.map.getRoomN(xpos-1, i) ) not in self.getRoomByNo( self.map.getRoomN(xpos, i) ).neighbors:
                                    self.map.setEntry( xpos, i, const.NSDOOR, len(self.rooms) )
                                    self.map.setEntry( xpos-1, i, const.DFLOOR1, len(self.rooms) )
                                    #self.map.setEntry( xpos-1, i-1, const.LRWALL, len(self.rooms) )
                                    #self.map.setEntry( xpos-1, i+1, const.URWALL, len(self.rooms) )
                                    eFlag = True
                    elif self.map.getEntry( xpos+xD, i ) == const.NSWALL:
                        if self.map.getEntry( xpos+xD+1, i ) == const.NSWALL and not wFlag:
                            if self.getRoomByNo( self.map.getRoomN(xpos+xD+1, i)) is not candidateRoom: # west
                                if self.getRoomByNo( self.map.getRoomN(xpos+xD, i) ) not in self.getRoomByNo( self.map.getRoomN(xpos+xD+1, i)).neighbors and self.getRoomByNo( self.map.getRoomN(xpos+xD+1, i) ) not in self.getRoomByNo( self.map.getRoomN(xpos+xD, i)).neighbors:
                                    self.map.setEntry( xpos+xD, i, const.NSDOOR, len(self.rooms) )
                                    self.map.setEntry( xpos+xD+1, i, const.DFLOOR1, len(self.rooms) )
                                    #self.map.setEntry( xpos+xD+1, i-1, const.LLWALL, len(self.rooms) )
                                    #self.map.setEntry( xpos+xD+1, i+1, const.ULWALL, len(self.rooms) )
                                    wFlag = True
            
            #candidateTileN = self.myMap.grid[xpos + xdim/2][ypos]
            #candidateTileS = self.myMap.grid[xpos + xdim/2][ypos + ydim]
            #candidateTileE = self.myMap.grid[xpos + xdim][ypos + ydim/2]
            #candidateTileW = self.myMap.grid[xpos][ypos + ydim/2]
                
            # 11 repeat step 4
            
        # set staircases
        '''
        choice1 = choice(rooms)
        (xpos, ypos) = choice1.getPos()
        (xdim, ydim) = choice1.getDimensions()
        self.map.setEntry( xpos + xdim/2, ypos + ydim/2, 120)
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
        self.map.setEntry( xpos + xdim/2, ypos + ydim/2, const.STAIRDN, len(self.rooms))
        self.map.setEntry( doorX, doorY, const.DOOR, len(self.rooms))
        self.map.pointOfExit = ( xpos + xdim/2, ypos + ydim/2 )
        
        # up
        choice2 = choice1.neighbors[0]
        (xpos, ypos) = choice2.getPos()
        (xdim, ydim) = choice2.getDimensions()
        self.map.setEntry( xpos + xdim/2, ypos + ydim/2, const.STAIRUP, len(self.rooms))
        self.map.pointOfEntry = ( xpos + xdim/2, ypos + ydim/2 )
        self.map.heroStart = ( xpos + xdim/2, ypos + ydim/2 )
        self.rooms.remove(choice1)
        
        self.rooms.remove(choice2)
        # add key for door
        keyRoom = choice(self.rooms)
        (xpos, ypos) = keyRoom.getPos()
        (xdim, ydim) = keyRoom.getDimensions()
        self.map.setEntry( xpos + xdim/2, ypos + ydim/2, const.KEY, len(self.rooms))
        self.rooms.remove(keyRoom)
        # set hero starting location - optional
        choice3 = choice(self.rooms)
        (xpos, ypos) = choice3.getPos()
        (xdim, ydim) = choice3.getDimensions()
        self.map.hs = ( xpos + xdim/2, ypos + ydim/2 )
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
            self.map.setEntry( xpos + xdim/2, ypos + ydim/2, const.CHEST, len(self.rooms))
            chestlist += [( ( xpos + xdim/2, ypos + ydim/2), chestItems )]
            self.rooms.remove(choice4)
        
        for room in self.secretRooms:
            (xpos, ypos) = room.getPos()
            (xdim, ydim) = room.getDimensions()
            self.map.setEntry( xpos + xdim/2, ypos + ydim/2, const.CHEST, len(self.rooms))
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
                               [sItem] )]
            
        self.map.chests = dict(chestlist)
        # add enemies
        while len(self.rooms) > 0:
            room = choice(self.rooms)
            (xpos, ypos) = room.getPos()
            (xdim, ydim) = room.getDimensions()
            self.map.NPCs.append( (( xpos + xdim/2, 
                                     ypos + ydim/2), 
                                   choice(enemyScr.enemiesByLevel[self.map.level] ) ) )
            self.rooms.remove(room)
               
    def addRoom(self, map, room, pos):
        room.serial = len(self.rooms)
        map.copyText = room.grid
        map.mapPaste( pos, len(self.rooms) )
    
    def getMapBall(self):
        return self.map.getMapBall()
    
    def getRoomByNo(self, N):
        for r in self.rooms:
            if r.serial == N:
                return r
    
    def draw(self):
        gridField.fill( [0,0,0] )
        for i in range(DIM):
            for j in range(DIM):
                gridField.blit( images.mapImages[myMap.getMapEntry(i,j)], (i*blocksize,j*blocksize) )

        screen.blit(gridField, (0,0) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass