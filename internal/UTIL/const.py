# Constant variables for Ransack game

scaleFactor = 1

def setScaleFactor(sF):
    scaleFactor = sF

# Size of a "block" unit
blocksize = 30
miniblocksize = 15

gameBoardOffset = 75

# max of stats (str, int, dex)

maxStats = 80

timeRate = 6

maxLineWidth = 24

shopTextFontSize = 14

DIM = 20

#N,S,W,E
CARDINALS = [ (0,-1), (0,1), (-1,0), (1,0) ]

#NW,N,NE,W,E,SW,S,SE
ALLNBRS = [ (-1,-1), (0,-1), (1,-1), 
            (-1,0), (1,0), 
            (-1,1), (0,1), (1,1)  ]
HALFDIM = 10

# Map tiles
DFLOOR1 = 0
DFLOOR2 = 1
DFLOOR3 = 2
DFLOOR4 = 3
FFLOOR1 = 4
FFLOOR1 = 5
FFLOOR1 = 6
FFLOOR1 = 7
ROAD1   = 8
ROAD2   = 9

GRASS1  = 12
GRASS2  = 13
GRASS3  = 14
GRASS4  = 15

BRICK1  = 32

STONE1 = 36

TOWERDOOR = 40
HOUSEDOOR1 = 41
TOWNHALLDOOR = 42
ITEMSDOOR = 43
MAGICDOOR = 44
ARMRYDOOR = 45
BLKSMDOOR = 46
TAVRNDOOR = 47

PINE1    = 52
PINE2    = 53
PINE3    = 54
PINE4    = 55

OAK     = 53

EWDOORO = 19
NSDOORO = 18


EWWALL_W  = 128
NSWALL_W  = 129
LRWALL_W  = 130
LLWALL_W  = 131

STAGHEAD = 132

COUNTER_EW = 133
COUNTER_NS = 135

EWWALL  = 136
NSWALL  = 137
ULWALL  = 138
URWALL  = 139
LLWALL  = 140
LRWALL  = 141

EWFAKE  = 142
NSFAKE  = 143

EWDOOR  = 144
NSDOOR  = 147

CAVEWALL1 = 152

SIGN    = 75

WELLSP  = 76

BLOCK = 56

doorsList = [ITEMSDOOR, MAGICDOOR, ARMRYDOOR, BLKSMDOOR, TAVRNDOOR, TOWNHALLDOOR, HOUSEDOOR1, BLOCK]


WSWORD = 104
SSWORD = 105
AXE    = 106
LSWORD = 107
TSWORD = 108
VAXE   = 109
GSWORD = 110
RING   = 111

AMULET = 112
CLOAK = 113
BOOTS = 114

HELMET = 119

LSHIRT = 120
LMAIL  = 121
CMAIL  = 122
SPLATE = 123
TPLATE = 124

WSHIELD = 125
ISHIELD = 126
SSHIELD = 127

COLUMN1 = 150
COLUMN2 = 151

LOGBOOK = 200
BOOKSHELF = 201
CHINASHELF = 202
CHAIR1 = 208

CHAIR2 = 209

TABLE1 = 210
TABLE2 = 211
TABLE3 = 212

GVEG = 214
GMEAT = 215

FRUIT1    = 216
CHEESE    = 217
MEAT2     = 219
BREAD     = 220
ANTIDOTE  = 221
SHP       = 222
MHP       = 223
LHP       = 224
SMP       = 225
MMP       = 226
LMP       = 227
KEY       = 228
GOLD      = 229
SPELLBOOK = 230
PARCHMENT = 231

CERTIFICATE = 232

LANTERN = 233

SAVECERT = 0
RETURNCERT = 1

DOOR      = 240

POISON = 250
DAMNATION = 251

STAIRUP   = 248
STAIRDN   = 249

GAMEITEMS = [LANTERN]

CHEST     = 252
OCHEST    = 253

VOID      = 254
HEROSTART = 255

# Spells
# L1
HEAL = 0
DART = 1
# L2
HEL2 = 5
FRBL = 6
TLPT = 7
# L3
HEL3 = 10
ICBL = 11
ASCD = 12
# L4
HEL4 = 15
EXTD = 16
FBL2 = 17
# L5
HEL5 = 20
RTRN = 21
IBL2 = 22
# L6
HEL6 = 25
GNCD = 26
FBL3 = 27

# Items
FRUIT1_I = 0
FRUIT2_I = 1
MEAT1_I = 3
MEAT2_I = 4
BREAD1_I = 5
BREAD2_I = 6
SHP_I     = 92
MHP_I       = 93
LHP_I       = 94
SMP_I       = 95
MMP_I       = 96
LMP_I       = 97

SOLIDS = range(BRICK1, HOUSEDOOR1)+range(TAVRNDOOR, 88)+range(EWWALL_W, FRUIT1)

# List of maps in dungeon
mapList = ['castle2.dat','castle1.dat','village1.dat','village2.dat']#,'map.dat', 'map2.dat']

fMapList = ['fortress1.dat', 'fortress2.dat']

# Messages to display for item found
itemMsgs = { FRUIT1: 'You found a piece of fruit.',
             SHP: 'You found a healing potion.',
             SMP: 'You found a magic potion',
             KEY: 'You found a key!',
             SPELLBOOK: 'You found a spellbook.' }

scrollingDict = { 'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0), None : (0,0) }
imgDict       = { 'up': 0, 'down': 2, 'left': 4, 'right': 6 }
walkingList = [ 1, 9, -1, -9 ]

darkMaps = ['dungeon', 'maze', 'fortress', 'cave']

# Define the colors we will use in RGB format
black = [  0,  0,  0]
offblack = [16, 16, 16]
white = [255,255,255]
blue =  [  0,  0,192]
dkblue =  [  0,  0,128]
green = [  0,193,  0]
dkgreen = [0, 128, 0] 
red =   [192,  0,  0]
dkred = [128, 0, 0]
brickred = [128, 0, 0]
yellow = [255, 255, 0]
gold = [127, 127, 0]
grey = [64, 64, 64]
ltgrey = [128,128,128]
brown = [87, 43, 0]
violet = [192, 0, 192]
purple = [64, 0, 64]