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


SEGMENT_REGULAR = 0
SEGMENT_PIT = 1
SEGMENT_TYPES = [SEGMENT_REGULAR, SEGMENT_PIT]


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
        self.velocity.y += 1.01
        
        if self.mid_jump:
            delta = millis() - self.jump_started
        
            self.velocity.y = self._get_jump_velocity(delta)
            self.mid_jump &= delta <= JUMP_LEN
            print(self.velocity.y)
        
        # Check if on land
        self.on_land = ((self.landscape.segment_type_at(self.position.x + self.size.x // 2) == SEGMENT_REGULAR) and
                        self.position.y >= self.landscape.height - self.size.y)
        if self.on_land:
            self.position.y = self.landscape.height - self.size.y
            self.velocity.y = 0

        
    def show(self):
        rectMode(CORNER)
        fill(RED)
        noStroke()
        rect(self.position.x, self.position.y, self.size.x, self.size.y)
        
    def jump_press(self):
        """Start jumping."""
        if self.on_land:
            self.mid_jump = True
            self.jump_started = millis()
            self.velocity.y = INITIAL_JUMP_VELOCITY
            self.on_land = False
            
    def jump_release(self):
        """Stop jumping."""
        if self.mid_jump:
            self.velocity.y = self._get_jump_velocity(millis() - self.jump_started)
            print(self.velocity.y)
            
        self.mid_jump = False
        
                
    def _get_jump_velocity(self, delta):
        """Calculates the jump velocity matching a jump key press of delta milliseconds."""
        ratio = min(1.0, float(delta) / JUMP_LEN)
        return map(ratio * FINAL_JUMP_VELOCITY, 0, FINAL_JUMP_VELOCITY, INITIAL_JUMP_VELOCITY, FINAL_JUMP_VELOCITY)
        
        
        
class Landscape(object):
    """
    The landscape that the player runs on.
    
    The logical representation of the landscape will be an array that always has at least 11 elements, where each 
    element's width is exactly 1/10 of the window size.
    As the landscape scrolls by, old segments will be discarded and new segment generated dynamically.
    
    At any given point, at most (parts of) 11 segments will be seen.
    """
    
    def __init__(self):
        self.height = GROUND_HEIGHT
        self.width = WINDOW_WIDTH
        self.position = 5
        self.velocity = INITIAL_VELOCITY
        self.num_segments = 10
        self.segments = [SEGMENT_REGULAR for _ in range(self.num_segments + 1)]
        self.gap = self.width // self.num_segments
        
    def update(self):
        self.position += self.velocity
        
        if self.position >= self.gap:
            self.position -= self.gap
            del self.segments[0]
            
            # Make sure that no more than 2 continous segments are pits.
            if all([seg == SEGMENT_PIT for seg in self.segments[-2:]]):
                self.segments.append(SEGMENT_REGULAR)
            else:
                self.segments.append(random.choice(SEGMENT_TYPES))
        
    def show(self):
        pushStyle()
        rectMode(CORNER)
        fill(BLUE)
        noStroke()
        
        # Add some lines to see the landscape moving
  
        x = -self.position
        for segment in self.segments:
            if segment == SEGMENT_REGULAR:
                rect(x, self.height, self.gap, WINDOW_HEIGHT - self.height)
                
            elif segment == SEGMENT_PIT:
                pass
                
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
