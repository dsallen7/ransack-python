from SCRIPTS import mapScr

from UTIL import const

def addDoorway(tile, dir, newRoom, candidateRoom, gen):
    (x1,y1) = tile
    if dir in ['n','s']:
        if newRoom.secret:
            gen.map.setEntry( x1,y1,const.EWFAKE, len(gen.rooms) )
        else: gen.map.setEntry( x1,y1,const.EWDOOR, len(gen.rooms) )
    else:
        if newRoom.secret:
            gen.map.setEntry( x1,y1,const.NSFAKE, len(gen.rooms) )
        else: gen.map.setEntry( x1,y1,const.NSDOOR, len(gen.rooms) )
    candidateRoom.entrances.append( (x1,y1) )
    (x2,y2) = mapScr.dirDict[dir]
    if dir == 'n':
        gen.map.setEntry( x1+x2-1, y1+y2, const.URWALL, len(gen.rooms))
        gen.map.setEntry( x1+x2+1, y1+y2, const.ULWALL, len(gen.rooms))
        
        gen.map.setEntry( x1+x2-1, y1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( x1+x2-1, y1 )) ) ], len(gen.rooms) )
        gen.map.setEntry( x1+x2+1, y1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( x1+x2+1, y1 )) ) ], len(gen.rooms) )
    elif dir == 's':
        gen.map.setEntry( x1+x2-1, y1+y2, const.LRWALL, len(gen.rooms))
        gen.map.setEntry( x1+x2+1, y1+y2, const.LLWALL, len(gen.rooms))
        
        gen.map.setEntry( x1+x2-1, y1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( x1+x2-1, y1 )) ) ], len(gen.rooms) )
        gen.map.setEntry( x1+x2+1, y1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( x1+x2+1, y1 )) ) ], len(gen.rooms) )
    elif dir == 'e':
        gen.map.setEntry( x1+x2, y1+y2-1, const.LRWALL, len(gen.rooms))
        gen.map.setEntry( x1+x2, y1+y2+1, const.URWALL, len(gen.rooms))
        
        gen.map.setEntry( x1, y1+y2-1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( x1, y1+y2-1 )) ) ], len(gen.rooms) )
        gen.map.setEntry( x1, y1+y2+1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( x1, y1+y2+1 )) ) ], len(gen.rooms) )
    elif dir == 'w':
        gen.map.setEntry( x1+x2, y1+y2-1, const.LLWALL, len(gen.rooms))
        gen.map.setEntry( x1+x2, y1+y2+1, const.ULWALL, len(gen.rooms))
        
        gen.map.setEntry( x1, y1+y2-1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( x1, y1+y2-1 )) ) ], len(gen.rooms) )
        gen.map.setEntry( x1, y1+y2+1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( x1, y1+y2+1 )) ) ], len(gen.rooms) )
    gen.map.setEntry( x1+x2, y1+y2, const.DFLOOR1, len(gen.rooms))
    newRoom.entrances.append( (x1+x2,y1+y2) )
    

def checkForNeighbors(room1, room2, gen):
    (xpos, ypos) = room1.getPos()
    (xD, yD) = room1.getDimensions()
    [nFlag, sFlag, eFlag, wFlag] = [False, False, False, False]
    if not room1.secret:
        for i in range( xpos+1, xpos+xD ): # (i, ypos-1) - location of room being considered to add as neighbors
            if gen.map.getEntry( i, ypos ) == const.EWWALL and gen.map.getEntry( i, ypos-1 ) == const.EWWALL and not nFlag:
                    if gen.getRoomByNo( gen.map.getRoomN(i, ypos-1)) is not room2 and not gen.getRoomByNo( gen.map.getRoomN(i, ypos)).secret and not gen.getRoomByNo( gen.map.getRoomN(i, ypos-1)).secret: # to the north
                        if gen.getRoomByNo( gen.map.getRoomN(i, ypos) ) not in gen.getRoomByNo( gen.map.getRoomN(i, ypos-1)).neighbors and gen.getRoomByNo( gen.map.getRoomN(i, ypos-1) ) not in gen.getRoomByNo( gen.map.getRoomN(i, ypos)).neighbors: # to the north
                            gen.map.setEntry( i, ypos, const.EWDOOR, len(gen.rooms) )
                            gen.map.setEntry( i, ypos-1, const.DFLOOR1, len(gen.rooms) )
                            gen.map.setEntry( i-1, ypos-1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( i-1, ypos-1)) ) ], len(gen.rooms) )
                            gen.map.setEntry( i+1, ypos-1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( i+1, ypos-1)) ) ], len(gen.rooms) )
                            gen.map.setEntry( i-1, ypos, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( i-1, ypos)) ) ], len(gen.rooms) )
                            gen.map.setEntry( i+1, ypos, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( i+1, ypos)) ) ], len(gen.rooms) )
                            room1.entrances.append( (i, ypos) )
                            room2.entrances.append( (i, ypos-1) )
                            #gen.map.setEntry( i-1, ypos-1, const.URWALL, len(gen.rooms) )
                            #gen.map.setEntry( i+1, ypos-1, const.ULWALL, len(gen.rooms) )
                            nFlag = True
            elif gen.map.getEntry( i, ypos + yD ) == const.EWWALL and gen.map.getEntry( i, ypos + yD + 1 ) == const.EWWALL and not sFlag:
                    if gen.getRoomByNo( gen.map.getRoomN(i, ypos+yD+1) ) is not room2 and not gen.getRoomByNo( gen.map.getRoomN(i, ypos+yD) ).secret and not gen.getRoomByNo( gen.map.getRoomN(i, ypos+yD+1) ).secret: # south
                        if gen.getRoomByNo( gen.map.getRoomN(i, ypos+yD) ) not in gen.getRoomByNo( gen.map.getRoomN(i, ypos+yD+1) ).neighbors and gen.getRoomByNo( gen.map.getRoomN(i, ypos+yD+1) ) not in gen.getRoomByNo( gen.map.getRoomN(i, ypos+yD) ).neighbors:
                            gen.map.setEntry( i, ypos+yD, const.EWDOOR, len(gen.rooms) )
                            gen.map.setEntry( i, ypos+yD+1, const.DFLOOR1, len(gen.rooms) )
                            gen.map.setEntry( (xpos + xD/2)-1, ypos+yD+1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( (xpos + xD/2)-1, ypos+yD+1 )) ) ], len(gen.rooms) )
                            gen.map.setEntry( (xpos + xD/2)+1, ypos+yD+1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( (xpos + xD/2)+1, ypos+yD+1 )) ) ], len(gen.rooms) )
                            gen.map.setEntry( (xpos + xD/2)-1, ypos+yD, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( (xpos + xD/2)-1, ypos+yD )) ) ], len(gen.rooms) )
                            gen.map.setEntry( (xpos + xD/2)+1, ypos+yD, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( (xpos + xD/2)+1, ypos+yD )) ) ], len(gen.rooms) )
                            room1.entrances.append( (i, ypos+yD) )
                            room2.entrances.append( (i, ypos+yD+1) )
                            #gen.map.setEntry( (xpos + xD/2)-1, ypos+yD+1, const.LRWALL, len(gen.rooms) )
                            #gen.map.setEntry( (xpos + xD/2)+1, ypos+yD+1, const.LLWALL, len(gen.rooms) )
                            sFlag = True
        for i in range( ypos+1, ypos+yD ):
            if gen.map.getEntry( xpos, i ) == const.NSWALL and gen.map.getEntry( xpos-1, i ) == const.NSWALL and not eFlag:
                    if gen.getRoomByNo( gen.map.getRoomN(xpos-1, i) ) is not room2 and not gen.getRoomByNo( gen.map.getRoomN(xpos, i) ).secret and not gen.getRoomByNo( gen.map.getRoomN(xpos-1, i) ).secret: # east
                        if gen.getRoomByNo( gen.map.getRoomN(xpos, i) ) not in gen.getRoomByNo( gen.map.getRoomN(xpos-1, i) ).neighbors and gen.getRoomByNo( gen.map.getRoomN(xpos-1, i) ) not in gen.getRoomByNo( gen.map.getRoomN(xpos, i) ).neighbors:
                            gen.map.setEntry( xpos, i, const.NSDOOR, len(gen.rooms) )
                            gen.map.setEntry( xpos-1, i, const.DFLOOR1, len(gen.rooms) )
                            gen.map.setEntry( xpos-1, i-1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( xpos-1, i-1 )) ) ], len(gen.rooms) )
                            gen.map.setEntry( xpos-1, i+1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( xpos-1, i+1 )) ) ], len(gen.rooms) )
                            gen.map.setEntry( xpos, i-1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( xpos, i-1 )) ) ], len(gen.rooms) )
                            gen.map.setEntry( xpos, i+1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( xpos, i+1 )) ) ], len(gen.rooms) )
                            room1.entrances.append( (xpos, i) )
                            room2.entrances.append( (xpos-1, i) )
                            #gen.map.setEntry( xpos-1, i-1, const.LRWALL, len(gen.rooms) )
                            #gen.map.setEntry( xpos-1, i+1, const.URWALL, len(gen.rooms) )
                            eFlag = True
            elif gen.map.getEntry( xpos+xD, i ) == const.NSWALL and gen.map.getEntry( xpos+xD+1, i ) == const.NSWALL and not wFlag:
                    if gen.getRoomByNo( gen.map.getRoomN(xpos+xD+1, i)) is not room2 and not gen.getRoomByNo( gen.map.getRoomN(xpos+xD, i)).secret and not gen.getRoomByNo( gen.map.getRoomN(xpos+xD+1, i)).secret: # west
                        if gen.getRoomByNo( gen.map.getRoomN(xpos+xD, i) ) not in gen.getRoomByNo( gen.map.getRoomN(xpos+xD+1, i)).neighbors and gen.getRoomByNo( gen.map.getRoomN(xpos+xD+1, i) ) not in gen.getRoomByNo( gen.map.getRoomN(xpos+xD, i)).neighbors:
                            gen.map.setEntry( xpos+xD, i, const.NSDOOR, len(gen.rooms) )
                            gen.map.setEntry( xpos+xD+1, i, const.DFLOOR1, len(gen.rooms) )
                            gen.map.setEntry( xpos+xD+1, i-1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( xpos+xD+1, i-1 )) ) ], len(gen.rooms) )
                            gen.map.setEntry( xpos+xD+1, i+1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( xpos+xD+1, i+1 )) ) ], len(gen.rooms) )
                            gen.map.setEntry( xpos+xD, i-1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( xpos+xD, i-1 )) ) ], len(gen.rooms) )
                            gen.map.setEntry( xpos+xD, i+1, mapScr.wallDict[ mapScr.getMappedNeighborList( gen.map.cardinalNeighbors(( xpos+xD, i+1 )) ) ], len(gen.rooms) )
                            room1.entrances.append( (xpos+xD, i) )
                            room2.entrances.append( (xpos+xD+1, i) )
                            #gen.map.setEntry( xpos+xD+1, i-1, const.LLWALL, len(gen.rooms) )
                            #gen.map.setEntry( xpos+xD+1, i+1, const.ULWALL, len(gen.rooms) )
                            wFlag = True