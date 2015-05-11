import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, parent):
        super().__init__()
        self.width = 4
        self.height = 10
        self.image = pygame.transform.scale(textures.get_texture("BULLET"), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = parent.rect.x + parent.width/2 - self.width/2
        self.rect.y = parent.rect.y + parent.height/2
        self.speed = 5
        self.type = "PLAYER"
        self.parent = parent
        
    def set_position(self,x,y):
        self.rect.x, self.rect.y = x,y

    def update(self):
        self.rect.y -= self.speed #direction may need editing?