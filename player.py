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