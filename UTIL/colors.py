from UTIL import const

black    = [  0,  0,  0]
offblack = [ 16, 16, 16]
white    = [255,255,255]
offwhite = [192,192,192]
blue     = [  0,  0,192]
dkblue   = [  0,  0,128]
green    = [  0,193,  0]
dkgreen  = [  0,128,  0] 
red      = [192,  0,  0]
dkred    = [128,  0,  0]
brickred = [128,  0,  0]
yellow   = [255,255,  0]
gold     = [127,127,  0]
grey     = [ 64, 64, 64]
ltgrey   = [192,192,192]
brown    = [ 87, 43,  0]
violet   = [192,  0,192]
purple   = [ 64,  0, 64]
ltyellow = [255,255,128]

colorDict = {
             -1:0, 0:10, 1:11, 3:3, 4:11, 5:11, 6:11, 7:11,
              8:10, 9:3, 10:5, 11:5, 12:7, 13:7, 14:8, 15:8,
              16:6, 17:12, 18:11, 19:11, 20:10, 21:10, 22:10, 23:10,
              24:1, 25:1, 26:6, 27:3, 28:3, 29:10, 30:3, 31:3,
              32:3, 33:3, 34:3, 35:3, 36:3, 37:3, 38:6, 39:3,
              40:3, 41:1, 42:5, 42:5, 43:5, 44:5, 45:5, 46:5, 47:5,
              48:1, 49:1, 50:1, 51:3, 52:8, 53:6, 54:6, 55:3,
              56:11, 57:6, 58:6, 59:1, 60:8, 61:3, 62:8, 63:1,
              64:5, 65:9, 66:9, 67:9, 68:9, 69:9, 70:9, 71:4,
              72:5, 73:5, 74:6, 75:3, 76:3, 77:6, 
              80:3, 81:3, 82:3, 84:3,
              92:4, 95:4,
              98:2, 99:6, 100:6,
              110:6, 111:6,
              112:3, 116:3, 117:3, 118:3, const.EWWALL:3, const.NSWALL:3, const.ULWALL:3, const.URWALL:3, const.LLWALL:3,
              const.LRWALL:3, const.EWFAKE:11, const.NSFAKE:11, const.EWDOOR:6, const.NSDOOR:6,
              const.STAIRUP:3, const.STAIRDN:3, 126:0, const.VOID:5,
              const.CHAIR1 : 6, const.CHAIR2 : 6, const.TABLE1 : 6, const.TABLE2 : 6
                   }

mapColors = [black,    #0
             brickred, #1
             yellow,   #2
             grey,     #3
             red,      #4
             white,    #5
             brown,    #6
             green,    #7
             dkgreen,  #8
             blue,     #9
             offblack, #10
             ltgrey,   #11
             ltyellow] #12