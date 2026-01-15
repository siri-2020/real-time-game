import pygame

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