import pygame, logging
from time import time, sleep
from random import randint
import eggs
from bullet import Bullet
from player import Shooter
from assets import *
from target import Target


PLAYING_GAME = False
WINDOW_SIZE = (640,480)
FPS = 120


def update_score(window, score):
    font = pygame.font.SysFont(None, 30, bold=False)
    window.blit(font.render("Score: {}".format(int(score)), True, (255,0,0)), (25, WINDOW_SIZE[1] - 30))

def update_level(window, level):
    font = pygame.font.SysFont(None, 25, bold=True)
    window.blit(font.render("Level: {}".format(int(level)+1), True, (0,255,0)), (8.7*WINDOW_SIZE[0]/10, WINDOW_SIZE[1] - 30))

def update_lives(window, lives):
    font = pygame.font.SysFont(None, 30, bold=False)
    window.blit(font.render("Lives Remaining: {}".format(int(lives)), True, (0,0,255)), (4.5*WINDOW_SIZE[0]/10, WINDOW_SIZE[1] - 30))

def initialise(menu, options):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    init_sounds()
    options["Difficulty"] = FPS
    window = pygame.display.set_mode(WINDOW_SIZE)

    exit_code = play(window, options) # Run main game loop
    for key, value in Sounds.items():
        value.stop()

    logging.debug("Game Exited with code {}".format(exit_code))
    if exit_code != "QUIT": sleep(1)

    pygame.quit()
    menu.deiconify()
    return exit_code


def generate_targets(player):
    sprite_list = []
    group = pygame.sprite.Group()
    if player.level > len(Levels)-1:
        level = generate_random_level()
    else: level = Levels[player.level]
    logging.debug("Generating Level: " + str(level))

    for i in range(level.rows):
        i *= level.padding + 8
        for j in range(40, WINDOW_SIZE[0] - 40, level.padding + 10):
            temp = Target(x=j,y=i, textures=player.options["Textures"])
            sprite_list.append(temp)
            del temp
    if len(sprite_list) > level.firebacks:
        level.firebacks = len(sprite_list)
    for i in range(level.firebacks):
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
        

def play(window, options):
    window_rect = window.get_rect()
    options["Textures"].load_texture_pack(options["Textures"].pack)
    player = Shooter(window=window, texture=options["Textures"])
    player.set_position(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]*0.83)
    player.options = options
    player_group = pygame.sprite.Group()
    player_group.add(player)

    target_group = generate_targets(player)
    bullet_group = pygame.sprite.Group()

    clock = pygame.time.Clock()

    timeouts = {
        "Target Movement":[FPS*0.5,FPS*0.5], 
        "Powerup":[FPS*100, FPS*100]
    }
    init_sounds()
    Sounds["main"].play(loops=-1) #Start background music

    logging.info("Game Started.")
    PLAYING_GAME = True
    while PLAYING_GAME:
        window.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.critical("Exiting Game...")
                PLAYING_GAME = False
                return "QUIT"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                temp = Bullet(player, player.options["Textures"])
                Sounds["shot"].play()
                bullet_group.add(temp)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_PLUS:
                player.OP = True
                Sounds["main"].stop()
                Sounds["OP"].play(loops=-1)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if player.powerup == "SPEED": player.move(player.speed * 1.5)
            else: player.move(player.speed)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if player.powerup == "SPEED": player.move(-player.speed*1.5)
            else: player.move(-player.speed)

        if keys[pygame.K_KP4] and keys[pygame.K_KP5] and keys[pygame.K_KP6] and player.OP:
            temp = Bullet(player, player.options["Textures"])
            bullet_group.add(temp)

        if keys[pygame.K_r] and [pygame.K_9] and [pygame.K_k] and player.OP:
            eggs.r9k(window)

        for sprite in bullet_group:
            sprite.update()
            if sprite.rect.y < 0 or (sprite.rect.y > player.rect.y and sprite.type == "TARGET"):
                bullet_group.remove(sprite)

        for bullet in bullet_group:
            hit_list = pygame.sprite.spritecollide(bullet, target_group, False)
            for target in hit_list:
                if bullet.type != "TARGET":
                    target_group.remove(target)
                    bullet_group.remove(bullet)
                    player.score += 1

            hit_list = pygame.sprite.spritecollide(bullet, player_group, False)
            for player in hit_list:
                if bullet.type == "TARGET":
                    bullet_group.remove(bullet)
                    logging.info("You were hit by a target's bullet!")
                    if not player.OP: player.lives -= 1
                    if player.lives <= 0:
                        return "LIVES"

        if timeouts["Target Movement"][0] <=0:
            drop_targets = False
            for target in target_group:
                target.move()
                if target.rect.x <= 30 or target.rect.x >=WINDOW_SIZE[0] - 30:
                    drop_targets = True

                if target.rect.y >= player.rect.y + 35:
                    PLAYING_GAME = False
                    return "PLAYER COLLISION"

            if drop_targets:
                logging.debug("The targets are moving down a level!")
                for target in target_group:
                    target.drop()

            timeouts["Target Movement"][0] = timeouts["Target Movement"][1]

        for target in target_group:
            if target.type == "SHOOTER":
                if randint(0,375) > 1: continue
                temp = Bullet(target, player.options["Textures"])
                temp.type="TARGET"
                temp.image = pygame.transform.scale(player.options["Textures"].get_texture("TARGET_BULLET"), (temp.width, temp.height))
                x,y = temp.rect.x, temp.rect.y
                temp.rect = temp.image.get_rect()
                temp.set_position(x,y)
                temp.speed = -3 #So it shoots down!
                bullet_group.add(temp)

        if len(target_group) == 0: #If all current players are gone.
            player.level += 1
            target_group = generate_targets(player)
            target_group.draw(window)
            bullet_group.empty()
            pygame.display.update()
            sleep(1.5)

        if player.OP:
            player.change_colour((255,96,0)) #override colour change if changed before

        update_score(window, player.score)
        update_level(window, player.level)
        update_lives(window, player.lives)

        bullet_group.draw(window)
        target_group.draw(window)
        player_group.draw(window)

        for key, value in timeouts.items():
            value[0] -= 1

        pygame.display.update()
        clock.tick(FPS)