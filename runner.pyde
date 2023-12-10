import random

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

JUMP_KEY = " "
JUMP_KEY_NAME = "SPACE"

BLACK = color(0)
WHITE = color(255)
RED = color(255, 0, 0)
GREEN = color(0, 255, 0)
BLUE = color(0, 0, 255)

GROUND_HEIGHT = 700
INITIAL_VELOCITY = 7
INITIAL_JUMP_VELOCITY = -10
FINAL_JUMP_VELOCITY = -20
JUMP_LEN = 150
GRAVITY = 1.01

SEGMENT_REGULAR = 0
SEGMENT_PIT = 1
SEGMENT_TYPES = [SEGMENT_REGULAR, SEGMENT_PIT]

OBSTACLE_GROUND = 0
OBSTACLE_AIR = 1
OBSTACLE_TYPES = [None, OBSTACLE_GROUND, OBSTACLE_AIR]
OBSTACLE_PROBS = [15, 3, 2]

FALL_THRESHHOLD = 30

screen = None
itr = 0

def setup():
    size(WINDOW_WIDTH, WINDOW_HEIGHT)
    
    global screen
    # screen = TitleScreen()
    screen = GameScreen()
    # screen = EndScreen("test")
    
def draw():
    global itr
    
    background(WHITE)
    # print("UPDATE " + str(itr))
    screen.update()
    
    # print("SHOW " + str(itr))
    screen.show()
    
    itr += 1
    
def keyPressed():
    screen.key_pressed()
    
def keyReleased():
    screen.key_released()    

class Screen(object):
    """Base class for all 'screens' in the game; exposes a update -> show cycle with key pressed / released event handling."""
    
    def update(self):
        pass
    
    def show(self):
        pass
        
    def key_pressed(self):
        pass
        
    def key_released(self):
        pass
            
        
class TitleScreen(Screen):
    """The initial game screen."""
    
    def show(self):
        textSize(72)
        fill(BLACK)
        textAlign(CENTER, CENTER)
        text("Press " + JUMP_KEY_NAME + " to start!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        
    def key_pressed(self):
        if key == JUMP_KEY:
            global screen
            screen = GameScreen()
        
class GameScreen(Screen):
    """The game itself."""
    def __init__(self):
        self.space_pressed = False
        self.landscape = Landscape()
        self.player = Player(self.landscape)
        
    def update(self):
        self.player.update()
        self.landscape.update()
    
    def show(self):
        self.player.show()
        self.landscape.show()
            
    def key_pressed(self):
        if key == JUMP_KEY:
            self.player.jump_press()
            self.space_pressed = True
            
    def key_released(self):
        if key == JUMP_KEY:
            self.player.jump_release()
            self.space_pressed = False


class EndScreen(Screen):
    """The end-of-run screen, which can draw itself ontop of another screen."""
    
    def __init__(self, message, prev_screen = None):
        """Creates a new end-of-run screen, which will (optionally) draw itself ontop of the given screen with the given message."""
        self.message = message
        self.prev_screen = prev_screen
        
    def show(self):
        if self.prev_screen is not None:
            self.prev_screen.show()

        fill(BLACK)
        textSize(128)
        textAlign(CENTER, CENTER)
        text(self.message, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
        textSize(72)
        text("Press " + JUMP_KEY_NAME + " to start!", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150)

        
    def key_pressed(self):
        if key == JUMP_KEY:
            global screen
            screen = GameScreen()
            
            
class Player(object):
    """The controllable player."""
    
    def __init__(self, landscape):
        self.size = PVector(50, 100)
        self.position = PVector(150, GROUND_HEIGHT - self.size.y)
        self.velocity = PVector()
        self.landscape = landscape
        self.on_land = True
        self.mid_jump = False
        self.jump_started = 0
    
    def update(self):
        self.position += self.velocity
        self.velocity.y += GRAVITY
        
        if self.mid_jump:
            delta = millis() - self.jump_started
        
            self.velocity.y = self._get_jump_velocity(delta)
            self.mid_jump &= delta <= JUMP_LEN
        
        # Check if on land
        is_land_segment = self.landscape.segment_type_at(self.position.x + self.size.x // 2) == SEGMENT_REGULAR 
        self.on_land = is_land_segment and 0 <= self.position.y + self.size.y - self.landscape.height <= FALL_THRESHHOLD
        
        if self.on_land:
            self.position.y = self.landscape.height - self.size.y
            self.velocity.y = 0
            
        # Check collisions - either with land or obstacles.
        if is_land_segment and not self.on_land and self.landscape.height <= self.position.y + self.size.y:
            print("BOOM")
            self.position.y = self.landscape.height - self.size.y
            self.on_land = True

        
    def show(self):
        rectMode(CORNER)
        fill(RED)
        noStroke()
        rect(self.position.x, self.position.y, self.size.x, self.size.y)
        
    def jump_press(self):
        """
        Start jumping.
        
        The vertical velocity will increase up to a set maximum as long as `jump_release` is not called.
        In this way, the height of the jump may be controlled to allow for more granular control of the player.
        """
        if self.on_land:
            self.mid_jump = True
            self.jump_started = millis()
            self.velocity.y = INITIAL_JUMP_VELOCITY
            self.on_land = False
            
    def jump_release(self):
        """Stop jumping."""
        if self.mid_jump:
            delta = millis() - self.jump_started
            self.velocity.y = self._get_jump_velocity(delta)
            
        self.mid_jump = False
        
                
    def _get_jump_velocity(self, delta):
        """Calculates the jump velocity matching a jump key press of delta milliseconds."""
        ratio = min(1.0, float(delta) / JUMP_LEN)
        return map(ratio * FINAL_JUMP_VELOCITY, 0, FINAL_JUMP_VELOCITY, INITIAL_JUMP_VELOCITY, FINAL_JUMP_VELOCITY)
        
        
        
class Landscape(object):
    """
    The environment, which consistes of the landscape that the player runs on and the obstacles.
    
    The logical representation of the landscape will be an array that always has at least 11 elements, where each 
    element's width is exactly 1/10 of the window size.
    As the landscape scrolls by, old segments will be discarded and new segment generated dynamically.
    An obstacle array of exactly 11 is also generated, with at most one obstacle per segment.
    
    At any given point, at most (parts of) 11 segments will be seen.
    """
    
    def __init__(self):
        self.height = GROUND_HEIGHT
        self.width = WINDOW_WIDTH
        self.position = 5
        self.velocity = INITIAL_VELOCITY
        self.num_segments = 10
        self.segments = [SEGMENT_REGULAR for _ in range(self.num_segments + 1)]
        self.obstacles = [None for _ in self.segments]
        self.gap = self.width // self.num_segments
                
    def update(self):
        self.position += self.velocity
        
        if self.position >= self.gap:
            # Generate a new segment and an optional obstacles.
            self.position -= self.gap
            del self.segments[0]
            del self.obstacles[0]
            
            # Only generate new terrain if needed.
            if len(self.segments) == self.num_segments:
                new_segments, new_obstacles = self.random_configuration()
                
                self.segments += new_segments
                self.obstacles += new_obstacles
            
        for obstacle in self.obstacles:
            if obstacle is not None:
                obstacle.update()
        
    def show(self):
        pushStyle()
        rectMode(CORNER)
        fill(BLUE)
        noStroke()
        
        # Add some lines to see the landscape moving
  
        x = -self.position
        for segment, obstacle in zip(self.segments, self.obstacles):
            if segment == SEGMENT_REGULAR:
                rect(x, self.height, self.gap, WINDOW_HEIGHT - self.height)
                
            elif segment == SEGMENT_PIT:
                pass
                
            if obstacle is not None:
                obstacle.show(x + self.gap // 2 - obstacle.size.x // 2)
                
            pushStyle()
            stroke(WHITE)
            strokeWeight(5)
            line(x, self.height, x, WINDOW_HEIGHT)
            popStyle()
            x += self.gap

        popStyle()
            
    def segment_type_at(self, x):
        """Get the segment type in the given x coordinate."""
        idx = int(x + self.position) // self.gap 

        return self.segments[idx]
    
    def random_configuration(self):
        """
        Generate a random environment configuration, which is a sequence of 0, 1 or 2 pits enclosed in regular landscape (only 1 segment for 0 pits).
        For each configuration there is at most 1 obstacle on the regular segments.
        """
        num_pits = random_choice([0, 1, 2], [14, 5, 3])
        segments = [SEGMENT_REGULAR] + [SEGMENT_PIT] * num_pits + ([SEGMENT_REGULAR] if num_pits > 0 else [])
        
        obstacle_idx = random.randint(-1, 0)
        obstacle_type = random_choice(OBSTACLE_TYPES, OBSTACLE_PROBS) if num_pits < 2 else None
        obstacles = [None] * len(segments)
        obstacles[obstacle_idx] = Obstacle(obstacle_type) if obstacle_type is not None else None 
                    
        return segments, obstacles
        
    
class Obstacle(object):
    def __init__(self, type):
        self.type = type
        self.size = PVector(100, 100)
        
        if self.type == OBSTACLE_GROUND:
            self.y = GROUND_HEIGHT - self.size.y
            
        elif self.type == OBSTACLE_AIR:
            self.y = 200
            
    def update(self):
        # Placeholder for animation support and / or vertical movement support.
        pass    
    
        
    def show(self, x):
        pushStyle()
        
        rectMode(CORNER)
        fill(GREEN)
        noStroke()
        rect(x, self.y, self.size.x, self.size.y)
        
        popStyle()
      
def random_choice(ls, probs):
    assert(len(ls) == len(probs))
    
    total = sum(probs)
    probs = [float(p) / total for p in probs]
    
    rnd = random.uniform(0, 1)
    
    threshold = 0
    for idx, p in enumerate(probs):
        if threshold <= rnd <= threshold + p:
            return ls[idx]
        threshold += p
        
    return ls[-1]
