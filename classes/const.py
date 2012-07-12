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
EXIT = 4
FRUIT = 5
HPOTION = 6
MPOTION = 7
SPELLBOOK = 8
CHEST = 9
HEROSTART = 10

# Spells
HEAL = 0
FRBL = 1

# Items
HPOT_I = 0
MPOT_I = 1
FRUT_I = 2

# Messages to display for item found
itemMsgs = { 2: 'You found a key!',
             5: 'You found a piece of fruit.',
             6: 'You found a healing potion.',
             7: 'You found a magic potion',
             8: 'You found a spellbook.' }

# Define the colors we will use in RGB format
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]
brickred = [128, 0, 0]
yellow = [127, 127, 0]
grey = [32, 32, 32]
brown = [64, 64, 0]