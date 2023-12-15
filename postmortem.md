As always in life, I wish I had more time to polish this up, as while it is currently playable, it could be much better with not too much more work.

# Initial Design
I designed the game to use the update-render pattern by abstracting the logic into "screens".
The main loop calls the current screen's update method, and then the show method.
Each screen can also handle the key-down and key-up events by implementing the matching method.

The game is split into three screens - Title screen, Game screen and End screen.  
As their name suggest, the title screen and end screen don't do much more than show a message while prompting the user to press a button to continue.  
The game screen, on the other hand, is where most of the game logic is actually implemented.

The main logical components we have are:
* The `Player` class - which keeps track of the vertical movement of the player, and the powerup in use (if any)
* The `Landscape` class - which handles the "horizontal movement" of the player (in practice, only the land is moving while the player stays in place) and generating the land, obstacles and powerups.

My design for the land generation was as follows:
* Split screen into 10 segments.
* Each segment can be either regular or a pit.
* Each regular segment may have an obstacle (static or moving) or a powerup (or nothing).

The collision detection is done by using rectangles to approximate the player and obstacles, and a circle for powerups.

There are some more classes which help with showing the assets, such as the `SpriteSheet` class which is used for animating the player and the enemies.

# Changes in the design
The design stayed pretty much the same throughout the development, except with regards for land generation:
* I needed to handle cases where 3 pits were generated in a row, as a jump cannot pass over that.
* I needed to handle cases where obstacles made pits impossible to pass.

My current design only partially fixes these faults, and works as follows:
Instead of generating the land segment-by-segment, generate a "configuration" - which is a series of segments such that:
* The series consists of 0-2 pit segments surrounded by regular segments (only one regular in case of 0 pits).
* There may only be an obstacle on one side of the pits, and no obstacle if there are 2 pit segments.
* There may be a powerup on one of the regular segments that do not contain an obstacle.

While this works much better, it still has problems:
* Impassible situations may be generated with low probability (for example 3 single-segment configuration with an enemy on each one.
* It's hard to control the probabilites of obstacles / powerups correctly, as different configurations have different sizes.


# Things that went well
The update-render pattern in combination with seperation into screens was very comfortable to work with.  
Also, my `SpriteSheet` abstraction turned out well and made it very simple to try and test different spritesheets.  

# Things that went less well

## Precise jumping
I wanted to have the hieght of the jump be affected by the length of the press on the jump key.  
While I do have a working solution I'm not very satisfied with it, as it is clumsy and finicky and doesn't feel exactly correct - I currently
do linear interpolation between and initial and a max value according to how long the key is pressed, which doesn't feel very realistic.


## Hit boxes
Because the sprites are not exactly sized to the hit boxes used, sometimes collisions are detected in a frustrating fashion.  
The way I'm currently handling this is very ad-hoc (with different sizes for the display and the collision detection) and I would have preferred to have a more sytematic and orderly way to handle it.

## RNG
The way I choose which obstacles / powerups to generate is random and only considers the current configuration.  
I would prefer to implement a method that has a more global outlook and can tweak probabilities in a more meaningful fashion.

# What I learned
While I have made some toy games in the past, this is the first time I've used actual assets, and the difference between seeing brightly colored boxes jumping around and actual figures jumping around is astounding.  
I've learned to use spritesheets and the difficulty of handling hit-boxes in a convincing fashion.

# The future
I would like to work on all the mechanisms I've described above and make them feel satisfying.  
I would also really like to learn how to correctly generate terrain to ensure that it is possible to pass it.  
In addition, I would like to port this project into a proper programming environment such that it may be split into multiple files, as in the last parts of development I found it hard to keep track (the file was getting too big).
