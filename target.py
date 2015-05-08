import pygame


class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(30,0,150), width=16, height=16):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = 7
        self.rect.x, self.rect.y = (x+(self.width/2)),(y+(self.width/2)) # centres co-ordinates
        self.type = "NORMAL"
        
    def move(self):
        self.rect.x += self.speed

    def drop(self):
        self.rect.y += 17
        self.speed *= -1


