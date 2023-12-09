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
    print("UPDATE " + str(itr))
    screen.update()
    
    print("SHOW " + str(itr))
    screen.show()
    
    itr += 1
    
def keyPressed():
    screen.key_pressed()
    
    
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
        self.player = Player()
        
    def update(self):
        self.player.update()
    
    def show(self):
        self.player.show()
            
    def key_pressed(self):
        if key == JUMP_KEY:
            self.space_pressed = True
            
    def key_released(self):
        if key == JUMP_KEY:
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
    def __init__(self):
        self.size = PVector(50, 100)
        self.position = PVector(150, GROUND_HEIGHT - self.size.y)
    
    def update(self):
        pass
        
    def show(self):
        rectMode(CORNER)
        fill(RED)
        noStroke()
        rect(self.position.x, self.position.y, self.size.x, self.size.y)
        
