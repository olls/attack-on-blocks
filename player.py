import pygame


class Shooter(pygame.sprite.Sprite):
    def __init__(self, window, color=(30,0,150), width=50, height=25):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = 3
        self.window_rect = window.get_rect()
        self.score = 0
        self.OP = True
        self.level = 0
        self.lives = 3
        self.powerup = ""
        
    def set_position(self,x,y):
         self.rect.x, self.rect.y = x,y
         
    def move(self, value): 
    	self.rect.x += value
    	self.rect.clamp_ip(self.window_rect)