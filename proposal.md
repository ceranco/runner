# Description
## Overview
The game will be a 2D endless runner where the player must jump in time to avoid obstacles and monsters (optional) while collecting power-ups to get
as far as possible.  

One of the reasons I chose a runner is that I feel like the core mechanics can be worked on and then additional power-ups, monsters and visuals may be added as time permits.

## Mechanics
The player will be controlled with one a single button for jumping, but the behavior may change according to the current power-up.  
For simplicity, only one power-up may be used at a time, and they will be randomly generated along the run.  
Power-ups expire after a set amount of time.

**possible power-ups:**
* Double jump - allows the player to jump once while in the air
* Long jump - changes the height (and thus the duration) of the jump.
* Extra life - for the duration of the power-up the player has **one** extra chance.
* Semi invulnerabilty - the player cannot be affected by monsters.

**possible monster behaviors:**
* Static on-ground - the monster doesn't change it's position and requires jumping over.
* Static in-air - the monster doesn't change it's position and requres passing under.
* Alternating - the monster changes it's position vertically.

**possible obstacles:**
* Fall - a break in the landscape (basically a pit) that falling into means instant death.
* Static on-ground / in-air - just like the monsters.

## Setting
The setting of the game mainly depends on which assets I can find (I'm not very artsy unfortunately), but the ideas I currently have are:
* Jungle
* Cityscape
* Cave

The final name of the game, obstacles, monsters and visuals will all be dependent on the setting however the core mechanics will stay the same.

# Features
* The game will have an intro screen, and can start a run by using the jump key.
* The game will have a player which runs to the right while the environment is continuously generated.
* There will be different power-ups which can be picked up and affect the behavior of the character in some way.
* The player can jump by using the spacebar key.
* The score for a specific run increases as long as player is alive.
* The speed of the players movement gradually increases the longer he is alive.
* The player dies when he can't avoid an obstacle (unless a power-up changes the behavior).
* At the end of a run, the final score is displayed with the option to start a new run by using the jump key.
* The players running will be animated.
* The monsters will be animated.
* There will be an indication on the screen during a run which shows the current score, active power-up, and how long until the power-up expires.
* The game objects will use actual assets and not just Processing shape primitives.

# Task List
1. Intro & end of run screens -  these are basically copy & paste from the dragster assignment.
2. Create a player with placeholder graphics (a rectangle).  
   The player can jump using the jump key.
3. Create the landscape with placeholder graphics (a differently colored rectangle).  
   Add support for breaks (pits) in the landscape.
4. Start "moving the player" (actually moving the landscape as the player stays in the same horizontal location) while generating new landscape.
5. Add collision logic for the player - this is basically an expansion of the jump feature.  
   If the player isn't on the land, it starts falling down. If the player goes offscreen vertically or has a collision horizontally, it detects that as a collision
   and signals (by printing to the console).
6. Add static obstacles to be randomly generated with placeholder graphics (more rectangels ;)), and include them in collision logic.
7. (Optional) - monsters are basically animated obstacles, so add vertical movement support for obstacles if I want the previously defined alternating monster mechanics.
8. Add support for the double-jump power-up with placeholder grahics (a circle this time :)), and try to do it in a such a way that adding more power-ups should be easy.  
   My current idea is to expose hooks for the two main events in the game - jumping and collision. The currently active powerup will be notified that the event occoured and 
   can change the state of the player as needed.
9. Add a score counter.
10. Put all the screens together and have a simple game loop.
11. Add graphics assets.
12. Add support for player and monster animation (using sprite sheets).
13. Add support for more power-ups and monsters, and polish the graphics and mechanics as time permits.
