# Constant variables for Ransack game

# Size of a "block" unit
blocksize = 30
miniblocksize = 15

DIM = 20

HALFDIM = 10

# Map tiles
DFLOOR1   = 0
DFLOOR2   = 1
DFLOOR3   = 2
DFLOOR4   = 3
FFLOOR1   = 4
FFLOOR1   = 5
FFLOOR1   = 6
FFLOOR1   = 7
ROAD1     = 8
ROAD2     = 9

BRICK1    = 24

TREE1     = 51

WELLSP    = 55

FRUIT1    = 86
FRUIT2    = 87
MEAT1     = 88
MEAT2     = 89
BREAD1    = 90
BREAD1    = 91
SHP       = 92
MHP       = 93
LHP       = 94
SMP       = 95
MMP       = 96
LMP       = 97
KEY       = 98
SPELLBOOK = 100
CHEST     = 110
OCHEST    = 111
DOOR      = 116
STAIRUP   = 120
STAIRDN   = 121
VOID      = 126
HEROSTART = 127

# Spells
HEAL = 0
FRBL = 1

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
KEY       = 98


# List of maps in dungeon
mapList = ['village1.dat','village2.dat']#,'map.dat', 'map2.dat']

# Messages to display for item found
itemMsgs = { 86: 'You found a piece of fruit.',
             92: 'You found a healing potion.',
             95: 'You found a magic potion',
             98: 'You found a key!',
             100: 'You found a spellbook.' }

# Define the colors we will use in RGB format
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,193,  0]
dkgreen = [0, 128, 0] 
red =   [255,  0,  0]
brickred = [128, 0, 0]
yellow = [127, 127, 0]
grey = [32, 32, 32]
brown = [139, 69, 19]