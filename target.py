import pygame, logging
from random import randint


class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, textures, color=(30,0,150), width=23, height=23):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(textures.get_target_texture(), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.speed = 5
        self.rect.x, self.rect.y = (x+(self.width/2)),(y+(self.width/2)) # centres co-ordinates
        self.type = "NORMAL"
        
    def move(self):
        self.rect.x += self.speed

    def drop(self):
        self.rect.y += 13
        self.speed *= -1

    def set_position(self, x, y, center=False):
        if center:
            self.rect.x, self.rect.y = (x+(self.width/2)),(y+(self.width/2))
        else:
            self.rect.x, self.rect.y = x, y


def generate_targets(player, window_size, Levels):
    sprite_list = []
    group = pygame.sprite.Group()
    if player.level > len(Levels)-1:
        level = generate_random_level()
    else: level = Levels[player.level]
    logging.debug("Generating Level: " + str(level))

    for i in range(level.rows):
        i *= level.padding + 8
        for j in range(75, window_size[0] - 75, level.padding + 10):
            temp = Target(x=j,y=i, textures=player.options["Textures"])
            sprite_list.append(temp)
            del temp

    if len(sprite_list) < level.firebacks:
        firebacks = len(sprite_list)
    else: firebacks = level.firebacks
    for i in range(firebacks):
        changed = False
        while not changed:
            index = randint(0, len(sprite_list)-1) if (len(sprite_list) - 1 != 0) else 0
            if sprite_list[index].type != "SHOOTER":
                sprite_list[index].type = "SHOOTER"
                sprite_list[index].image = pygame.transform.scale(player.options["Textures"].get_texture("SHOOTER"), (sprite_list[index].width, sprite_list[index].height))
                x,y = sprite_list[index].rect.x, sprite_list[index].rect.y
                sprite_list[index].rect = sprite_list[index].image.get_rect()
                sprite_list[index].set_position(x,y, center=False) #Already Centered!
                changed = True

    for sprite in sprite_list: #Because sprite groups dont support indexing!
        group.add(sprite)
    return group
        