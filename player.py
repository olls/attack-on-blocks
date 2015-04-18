import pygame


class Shooter(pygame.sprite.Sprite):
    def __init__(self, color=(30,0,150), width=64, height=64):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = 4
        
    def set_position(self,x,y):
         self.rect.x, self.rect.y = x,y
         
    def move(self, value): self.rect.x += value