import pygame

class GameEngine:
    def __init__(self, graph_engine, input_controller, game_field, player, npc, npc2, *, fps=60):
        self.graph_engine = graph_engine
        self.game_field = game_field
        self.player = player
        self.npc = npc
        self.npc2 = npc2
        self.fps = fps
        self.input_controller = input_controller
        self.clock = pygame.time.Clock()
        self.running = False
    
    def update_state(self, pressed_keys, dt):
        self.npc.move(self.game_field, dt)
        self.npc2.move(self.game_field, dt)
        self.player.move("a" in pressed_keys, "d" in pressed_keys, 
                        "w" in pressed_keys, "s" in pressed_keys, 
                        self.game_field, dt)
        if "q" in pressed_keys:
            self.running = False
    
    def render_state(self):
        self.graph_engine.start_frame()
        self.graph_engine.render_circle(self.player.x, self.player.y, 20, "red")
        self.graph_engine.render_circle(self.npc.x, self.npc.y, 20, "blue")
        self.graph_engine.render_circle(self.npc2.x, self.npc2.y, 20, "green")
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