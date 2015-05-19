import pygame


class Shooter(pygame.sprite.Sprite):
    def __init__(self, window, texture, colour=(255,255,255), width=55, height=25):
        super().__init__()
        self.width = width
        self.height = height
        self.colour = colour
        self.texture = texture
        self.image = pygame.transform.scale(self.texture.get_texture("PLAYER"), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.speed = 3
        self.window_rect = window.get_rect()

        self.score = 0
        self.OP = False
        self.level = 0
        self.lives = 3
        self.powerup = "" 

    def set_position(self,x,y):
         self.rect.x, self.rect.y = x, y
         
    def move(self, value): 
        self.rect.x += value
        self.rect.clamp_ip(self.window_rect)

    def update(self):
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()

    def change_colour(self, colour):
        x,y = self.rect.x, self.rect.y
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.set_position(x,y)

    def reset_image(self):
    	x,y = self.rect.x, self.rect.y
    	self.image = pygame.transform.scale(self.texture.get_texture("PLAYER"), (self.width, self.height))
    	self.rect = self.image.get_rect()
    	self.set_position(x,y)