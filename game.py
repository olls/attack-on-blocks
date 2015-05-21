import pygame, logging
from time import time, sleep
from random import randint
import eggs
from bullet import Bullet
from player import Shooter
from assets import *
from target import Target, generate_targets

POWERUPS = ["SPEED", "DOUBLE", "LIVES", "SCORE", "BIGGER"]
PLAYING_GAME = False
WINDOW_SIZE = (680, 790)
HUD_COLOUR = (255,168,72)


def update_score(window, score, colour=HUD_COLOUR):
    font = pygame.font.SysFont(None, 30, bold=False)
    window.blit(font.render("Score: {}".format(int(score)), True, colour), (25, WINDOW_SIZE[1] - 30))

def update_level(window, level, colour=HUD_COLOUR):
    font = pygame.font.SysFont(None, 30, bold=False)
    window.blit(font.render("Level: {}".format(int(level)+1), True, colour), (8.5*WINDOW_SIZE[0]/10, WINDOW_SIZE[1] - 30))

def update_lives(window, lives, colour=HUD_COLOUR):
    font = pygame.font.SysFont(None, 30, bold=False)
    window.blit(font.render("Lives Remaining: {}".format(int(lives)), True, colour if lives != 1 else (255,50,0)), (3.8*WINDOW_SIZE[0]/10, WINDOW_SIZE[1] - 30))

def initialise(menu, options):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Attack on Blocks")
    exit_code = play(window, options) # Run main game loop
    for key, value in Sounds.items():
        value.fadeout(500)

    logging.debug("Game Exited with code {}".format(exit_code))
    if exit_code != "QUIT": sleep(1)

    pygame.quit()
    menu.deiconify()
    return exit_code

def play(window, options):
    window_rect = window.get_rect()
    options["Textures"].load_texture_pack(options["Textures"].pack)
    player = Shooter(window=window, texture=options["Textures"])
    player.set_position(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]*0.90)
    player.options = options
    player_group = pygame.sprite.Group()
    player_group.add(player)

    target_group = generate_targets(player, WINDOW_SIZE, Levels)
    bullet_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    FPS = player.options["Difficulty"]

    timeouts = {
        "Target Movement":[FPS*0.65,FPS*0.65], 
        "Powerup":[FPS*15, FPS*15]
    }
    init_sounds()
    Sounds["main"].play(loops=-1) #Start background music

    logging.info("Game Started.")
    PLAYING_GAME = True
    while PLAYING_GAME:
        window.fill((0,0,0))
        
        fired = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.critical("Exiting Game...")
                PLAYING_GAME = False
                return "QUIT"

            if event.type == pygame.KEYDOWN and event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP] and not fired:
                if player.options["Sounds"]: Sounds["shot"].play()
                temp = Bullet(player, player.options["Textures"], player.powerup == "BIGGER")
                bullet_group.add(temp)
                if player.powerup == "DOUBLE":
                    temp = Bullet(player, player.options["Textures"], player.powerup == "BIGGER")
                    temp.rect.y += 20
                    bullet_group.add(temp)
                fired = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_PLUS:
                if not player.options["Sounds"] or not player.OP: 
                    Sounds["main"].stop()
                    #Sounds["OP"].play(loops=-1)
                    player.OP = True
                    player.change_colour((255,96,0))
                elif player.OP:
                    Sounds["OP"].stop()
                    Sounds["main"].play(loops=-1)
                    player.OP = False
                    player.reset_image()

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
                    target.lives -= 1
                    if target.lives <= 0:           
                        target_group.remove(target)
                        player.score += 1
                    bullet_group.remove(bullet)
                if target.lives <= 0 and target.type == "POWERUP":
                    player.powerup = POWERUPS[randint(0,len(POWERUPS)-1)]
                    logging.info("Powerup set to {}".format(player.powerup))

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
                if target.rect.x <= 30 or target.rect.x >=WINDOW_SIZE[0] - target.width/2 - 30:
                    drop_targets = True

                if target.rect.y >= player.rect.y + target.height/2:
                    PLAYING_GAME = False
                    return "PLAYER COLLISION"

            if drop_targets:
                logging.debug("The targets are moving down a level!")
                for target in target_group:
                    target.drop()

            timeouts["Target Movement"][0] = timeouts["Target Movement"][1]

        if timeouts["Powerup"][0] <= 0:
            timeouts["Powerup"][0] = timeouts["Powerup"][1]

        if player.powerup == "SCORE":
            player.score += 10
            player.powerup = ""
        elif player.powerup == "LIVES":
            player.lives += 1
            player.powerup = ""

        for target in target_group:
            if target.type == "SHOOTER":
                if randint(0,600) > 1: continue
                temp = Bullet(target, player.options["Textures"], False)
                temp.type="TARGET"
                temp.image = pygame.transform.scale(player.options["Textures"].get_texture("TARGET_BULLET"), (temp.width, temp.height))
                x,y = temp.rect.x, temp.rect.y
                temp.rect = temp.image.get_rect()
                temp.set_position(x,y)
                temp.speed = -1 #So it shoots down!
                bullet_group.add(temp)

        if len(target_group) == 0: #If all current players are gone.
            player.level += 1
            Sounds["main"].set_volume(0.5)
            target_group = generate_targets(player, WINDOW_SIZE, Levels)
            target_group.draw(window)
            bullet_group.empty()
            pygame.display.update()
            sleep(0.75)
            Sounds["main"].set_volume(1.0)

        update_score(window, player.score)
        update_level(window, player.level)
        update_lives(window, player.lives)

        target_group.draw(window)
        bullet_group.draw(window)
        player_group.draw(window)

        for key, value in timeouts.items():
            value[0] -= 1

        pygame.display.update()
        clock.tick(FPS)