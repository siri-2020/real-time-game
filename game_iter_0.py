import pygame

class InputController:
    def __init__(self):
        pass
    
    def get_pressed_keys(self):
        keys = pygame.key.get_pressed()
        pressed = []
        if keys[pygame.K_w]:
            pressed.append("w")
        if keys[pygame.K_s]:
            pressed.append("s")
        if keys[pygame.K_a]:
            pressed.append("a")
        if keys[pygame.K_d]:
            pressed.append("d")
        if keys[pygame.K_q]:
            pressed.append("q")
        return pressed

class GameField:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
    
    def clamp(self, x, y):
        return (max(self.x_min, min(self.x_max, x)), 
                max(self.y_min, min(self.y_max, y)),
                self.x_min > x or self.x_max < x, 
                self.y_min > y or self.y_max < y)

class Player:
    def __init__(self, x, y, speed_x=300, speed_y=300):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def move(self, left, right, up, down, game_field, dt):
        self.x += self.speed_x * dt * right - self.speed_x * dt * left
        self.y += self.speed_y * dt * down - self.speed_y * dt * up
        self.x, self.y, _, _ = game_field.clamp(self.x, self.y)

class NPC:
    def __init__(self, x, y, speed_x=100, speed_y=100):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def move(self, game_field, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt
        self.x, self.y, x_edge, y_edge = game_field.clamp(self.x, self.y)
        if x_edge:
            self.speed_x = -self.speed_x
        if y_edge:
            self.speed_y = -self.speed_y

class GraphicsEngine:
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game Engine")
        self.width = width
        self.height = height
    
    def start_frame(self):
        self.screen.fill("purple")
    
    def show_frame(self):
        pygame.display.flip()
    
    def render_circle(self, x, y, radius, color):
        pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)

class GameEngine:
    def __init__(self, graph_engine, input_controller, game_field, player, npc, *, fps=60):
        self.graph_engine = graph_engine
        self.game_field = game_field
        self.player = player
        self.npc = npc
        self.fps = fps
        self.input_controller = input_controller
        self.clock = pygame.time.Clock()
        self.running = False
    
    def update_state(self, pressed_keys, dt):
        self.npc.move(self.game_field, dt)
        self.player.move("a" in pressed_keys, "d" in pressed_keys, 
                        "w" in pressed_keys, "s" in pressed_keys, 
                        self.game_field, dt)
        if "q" in pressed_keys:
            self.running = False
    
    def render_state(self):
        self.graph_engine.start_frame()
        self.graph_engine.render_circle(self.player.x, self.player.y, 20, "red")
        self.graph_engine.render_circle(self.npc.x, self.npc.y, 20, "blue")
        self.graph_engine.show_frame()
    
    def run_game(self):
        self.running = True
        while self.running:
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Get input and update
            pressed_keys = self.input_controller.get_pressed_keys()
            dt = self.clock.tick(self.fps) / 1000
            self.update_state(pressed_keys, dt)
            
            # Render
            self.render_state()
        
        pygame.quit()

if __name__ == "__main__":
    game_field = GameField(0, 0, 1280, 720)
    player = Player(640, 360)
    npc = NPC(200, 200, 100, 150)
    graph_engine = GraphicsEngine(1280, 720)
    input_controller = InputController()
    game_engine = GameEngine(graph_engine, input_controller, game_field, player, npc, fps=60)
    game_engine.run_game()