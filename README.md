ransack-python
==============

Ransack - a Python based roguelike

In very early stages at the moment. Our hero can explore the levels, collect items, and fight monsters. There is only one type of monster right now.

Move with arrow keys. Battles occur Final Fantasy style. Use battle menu to fight.

's' brings up spell menu and 'i' brings up item inventory.
'm' brings up mini-map which displays current level.
't' takes a screenshot.

Stairs lead hero to the next or previous level. If next level has not been visited yet, it will be generated automatically.

The game begins in the 'village' which doesn't actually do anything yet but will soon include shops, temple, etc. as well as interactive citizens (again, think Final Fantasy) On venturing into the dungeon, new levels are automatically generated.

A basic level editor is included. Use 't' to select tiles or select with mouse, move with arrow keys and space bar or point and click to place tiles, and 'd' to toggle draw mode. 's' saves a map and 'l' loads. 'f' flood fills the map with currently selected tile beginning at the location of the cursor. 'g' generates a random map with specified number of rooms.
Note that setting rooms too high may cause the generator to hang if the map is not big enough.

Currently using Nintendo Link sprites for player until I get around to designing my own.

Uses sprite sheet code from www.scriptefun.com/transcript-2-using-sprite-sheets-and-drawing-the-background

The level editor uses EzText courtest of pywiz32 - http://www.pygame.org/project-EzText-920-.html

The random generator algorithm is based on the description written here (the actual code is my own):

http://breinygames.blogspot.com/2011/07/random-map-generation.html