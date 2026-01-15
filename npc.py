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