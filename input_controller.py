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
