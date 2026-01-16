import pygame
import math
import random

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
        if keys[pygame.K_LEFT]:
            pressed.append("left")
        if keys[pygame.K_RIGHT]:
            pressed.append("right")
        if keys[pygame.K_SPACE]:
            pressed.append("fire")
        return pressed


class GameField:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
    
    def clamp(self, x, y):
        return (
            max(self.x_min, min(self.x_max, x)),
            max(self.y_min, min(self.y_max, y)),
            self.x_min > x or self.x_max < x,
            self.y_min > y or self.y_max < y
        )
    
    def inside(self, x, y):
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max


class Player:
    def __init__(self, x, y, speed=300):
        self.x = x
        self.y = y
        self.angle = 0.0
        self.speed = speed
    
    def move(self, left, right, up, down, game_field, dt):
        dx = self.speed * dt * (right - left)
        dy = self.speed * dt * (down - up)
        self.x, self.y, _, _ = game_field.clamp(self.x + dx, self.y + dy)
    
    def rotate(self, left, right, dt):
        if left:
            self.angle -= 3 * dt
        if right:
            self.angle += 3 * dt


class NPC:
    def __init__(self, x, y, speed_x, speed_y):
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


class Bullet:
    def __init__(self, x, y, angle, speed=600):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
    
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt


class GraphicsEngine:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game Engine")
    
    def start_frame(self):
        self.screen.fill("black")
    
    def show_frame(self):
        pygame.display.flip()
    
    def render_circle(self, x, y, radius, color):
        pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)
    
    def render_player(self, x, y, angle):
        pygame.draw.circle(self.screen, "red", (int(x), int(y)), 20)
        tip = (
            x + math.cos(angle) * 30,
            y + math.sin(angle) * 30
        )
        pygame.draw.line(self.screen, "yellow", (x, y), tip, 3)


class GameEngine:
    def __init__(self, graph_engine, input_controller, game_field, player, *, fps=60):
        self.graph_engine = graph_engine
        self.input_controller = input_controller
        self.game_field = game_field
        self.player = player
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = False
        self.npcs = []
        self.bullets = []
        self.spawn_timer = 0
    
    def spawn_npc(self, x=None, y=None):
        if x is None:
            x = random.randint(self.game_field.x_min, self.game_field.x_max)
            y = random.randint(self.game_field.y_min, self.game_field.y_max)
        self.npcs.append(NPC(x, y, random.choice([-120, 120]), random.choice([-150, 150])))
    
    def update_state(self, pressed, dt):
        self.spawn_timer += dt
        if self.spawn_timer > 2:
            self.spawn_npc()
            self.spawn_timer = 0
        
        self.player.rotate("left" in pressed, "right" in pressed, dt)
        self.player.move("a" in pressed, "d" in pressed,
                         "w" in pressed, "s" in pressed,
                         self.game_field, dt)
        
        if "fire" in pressed:
            self.bullets.append(Bullet(self.player.x, self.player.y, self.player.angle))
        
        for npc in self.npcs:
            npc.move(self.game_field, dt)
        
        for bullet in self.bullets:
            bullet.update(dt)
        
        self.bullets = [b for b in self.bullets if self.game_field.inside(b.x, b.y)]
        
        remaining_npcs = []
        for npc in self.npcs:
            hit = False
            for bullet in self.bullets:
                if (npc.x - bullet.x) ** 2 + (npc.y - bullet.y) ** 2 < 20 ** 2:
                    hit = True
                    self.bullets.remove(bullet)
                    break
            if not hit:
                remaining_npcs.append(npc)
        self.npcs = remaining_npcs
        
        if "q" in pressed:
            self.running = False
    
    def render_state(self):
        self.graph_engine.start_frame()
        self.graph_engine.render_player(self.player.x, self.player.y, self.player.angle)
        for npc in self.npcs:
            self.graph_engine.render_circle(npc.x, npc.y, 20, "blue")
        for bullet in self.bullets:
            self.graph_engine.render_circle(bullet.x, bullet.y, 5, "white")
        self.graph_engine.show_frame()
    
    def run_game(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.spawn_npc(x, y)
            
            pressed = self.input_controller.get_pressed_keys()
            dt = self.clock.tick(self.fps) / 1000
            self.update_state(pressed, dt)
            self.render_state()
        
        pygame.quit()


if __name__ == "__main__":
    field = GameField(0, 0, 800, 600)
    player = Player(400, 300)
    graph_engine = GraphicsEngine(800, 600)
    input_controller = InputController()
    game = GameEngine(graph_engine, input_controller, field, player)
    game.run_game()
