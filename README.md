ransack-python
==============

Ransack - a Python based roguelike

In very early stages at the moment. Our hero can explore the levels, collect items, and fight monsters.

Move with arrow keys. Battles occur Final Fantasy style. Use battle menu to fight.

's' brings up spell menu and 'i' brings up item inventory. 'w' brings up weapon menu. Select a weapon from here and it will be automatically equipped.
'm' brings up mini-map which displays current level.
't' takes a screenshot.

Stairs lead hero to the next or previous level. If next level has not been visited yet, it will be generated automatically.

The game begins in the 'village'. Currently the village has an item shop (white bldg on right hand side) and blacksmith (brick bldg). Coming soon: inn, temple, magic shop, and probably a tavern. 

On venturing into the dungeon, new levels are automatically generated. Each dungeon has a key which unlocks the door to the next stairs down.

A basic level editor is included. Click the pencil for draw mode and the hand for select mode. In select mode, select a region and move it around the screen. In draw mode, Use 't' to select tiles or select with mouse, move with arrow keys and space bar or point and click to place tiles, and 'd' to toggle draw mode. 's' saves a map and 'l' loads. 'f' flood fills the map with currently selected tile beginning at the location of the cursor. 'g' generates a random map with specified number of rooms. There are cut/copy paste buttons but I haven't implemented them yet.
Note that setting rooms too high may cause the generator to hang if the map is not big enough.

I have created all the artwork for the game, at this point it's quite rudimentary but it will be expanded as the project continues.

Uses sprite sheet code from www.scriptefun.com/transcript-2-using-sprite-sheets-and-drawing-the-background

The level editor uses EzText courtest of pywiz32 - http://www.pygame.org/project-EzText-920-.html

The random generator algorithm is based on the description written here (the actual code is my own):

http://breinygames.blogspot.com/2011/07/random-map-generation.html

As a side note, this project is turning into more of an RPG with roguelike features. Rogue purists may sneer :-P but I look forward to seeing what happens with this thing and I hope you do too.