ransack-python
==============

Ransack - a Python based roguelike

In mid-early stage at the moment. Our hero can explore the levels, collect items, fight monsters, and interact with the townspeople.

Coming soon: Ransack for Android. I've gotten it to run on an Android emulator using Pygame Subset for Android, there's still a mountain of issues to work out, but I'll keep all updates posted here.

Move with arrow keys. Monsters are found in the dungeon. Approach a monster and press Enter to commence battle, the monsters can also initiate battle

'c' brings up spell menu and 'i' brings up item inventory. 'a'/'w' brings up armor/weapon menu. Select a weapon/armor from here and it will be automatically equipped. If it is currently equipped, it will not be listed in the weapon or armor menu.
'm' brings up mini-map which displays current level. 's' shows character stats.
't' takes a screenshot.

The game begins in the 'village'. Currently the village has an item shop, magic shop, tavern, blacksmith, and armory. You can save your game but only at the Inn/Tavern which is the three story building.

On venturing into the dungeon, new levels are automatically generated. Each dungeon has a key which unlocks the door to the next stairs down. Try to find the 'secret' dungeon rooms (hint: look at the minimap)

Stairs lead hero to the next or previous level. If next level has not been visited yet, it will be generated automatically. The game culminates in a fortress level with a boss (which I haven't designed yet).

A basic level editor is included. Click the pencil for draw mode and the hand for select mode. In select mode, select a region and move it around the screen. In draw mode, Use 't' to select tiles or select with mouse, move with arrow keys and space bar or point and click to place tiles, and 'd' to toggle draw mode. If you place the door to a shop it will ask you for the level and then draw the entire shop at that location. 's' saves a map and 'l' loads. 'f' flood fills the map with currently selected tile beginning at the location of the cursor. 'g' generates a random map with specified number of rooms. Click the little naked guy to place non-player characters. The types currently implemented are 'guard', 'female' and 'skeleton'
. There are cut/copy paste buttons but I haven't implemented them yet.
Note that setting rooms too high may cause the generator to hang if the map is not big enough.

I have created all the artwork for the game, at this point it's quite rudimentary but it will be expanded as the project continues.

Uses sprite sheet code from www.scriptefun.com/transcript-2-using-sprite-sheets-and-drawing-the-background

The level editor uses EzText courtest of pywiz32 - http://www.pygame.org/project-EzText-920-.html

The random generator algorithm is based on the description written here (the actual code is my own):
http://breinygames.blogspot.com/2011/07/random-map-generation.html

The fonts used ingame are Spinal Tap (http://www.rockbandfonts.com/), Chancery Gothic and Courier.

As a side note, this project is turning into more of an RPG with roguelike features. Rogue purists may sneer :-P but I look forward to seeing what happens with this thing and I hope you do too.