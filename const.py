# Constant variables for Ransack game

# Size of a "block" unit
blocksize = 30
miniblocksize = 15

DIM = 20

HALFDIM = 10

# Map tiles
FLOOR = 0
WALL = 1
KEY = 2
DOOR = 3
STAIRUP = 4
STAIRDN = 5
FRUIT = 6
HPOTION = 7
MPOTION = 8
SPELLBOOK = 9
CHEST = 10
HEROSTART = 11

# Spells
HEAL = 0
FRBL = 1

# Items
HPOT_I = 0
MPOT_I = 1
FRUT_I = 2

# List of maps in dungeon
mapList = ['village1.dat','village2.dat','map.dat', 'map2.dat']

# Messages to display for item found
itemMsgs = { 2: 'You found a key!',
             6: 'You found a piece of fruit.',
             7: 'You found a healing potion.',
             8: 'You found a magic potion',
             9: 'You found a spellbook.' }

# Define the colors we will use in RGB format
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]
brickred = [128, 0, 0]
yellow = [127, 127, 0]
grey = [32, 32, 32]
brown = [139, 69, 19]