import pygame
from random import randint


class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, textures, color=(30,0,150), width=16, height=16):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(textures.get_target_texture(), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.speed = 7
        self.rect.x, self.rect.y = (x+(self.width/2)),(y+(self.width/2)) # centres co-ordinates
        self.type = "NORMAL"
        
    def move(self):
        self.rect.x += self.speed

    def drop(self):
        self.rect.y += 17
        self.speed *= -1

    def set_position(self, x, y, center=False):
        if center:
            self.rect.x, self.rect.y = (x+(self.width/2)),(y+(self.width/2))
        else:
            self.rect.x, self.rect.y = x, y


