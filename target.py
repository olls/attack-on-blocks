import pygame

class Target(pygame.sprite.Sprite):
    def __init__(self, color=(30,0,150), width=16, height=16):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = 4
        
    def set_position(self,x,y):
         self.rect.x, self.rect.y = (x+(self.width/2)),(x+(self.width/2)) # centres co-ordinates
         
    def move(self, x,y):
        if ((self.rect.y + self.width) > window_rect.y) or((self.rect.y - self.width < 0)):
            movement = self.speed
        else:
            movement = -self.speed
        self.rect.y += movement
