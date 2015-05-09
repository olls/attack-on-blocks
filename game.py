import pygame, logging
from time import time
from random import randint
from bullet import Bullet
from player import Shooter
from assets import Textures, Levels, generate_random_level
from target import Target


PLAYING_GAME = False
WINDOW_SIZE = (640,480)
FPS = 120


def update_score(window, score):
	font = pygame.font.SysFont(None, 30, bold=False)
	window.blit(font.render("Score: {}".format(int(score)), True, (255,0,0)), (25, WINDOW_SIZE[1] - 30))

def update_level(window, level):
	font = pygame.font.SysFont(None, 20, bold=True)
	window.blit(font.render("Level: {}".format(int(level)+1), True, (0,255,0)), (8.7*WINDOW_SIZE[0]/10, WINDOW_SIZE[1] - 30))

def update_lives(window, lives):
	font = pygame.font.SysFont(None, 30, bold=False)
	window.blit(font.render("Lives Remaining: {}".format(int(lives)), True, (0,0,255)), (4.5*WINDOW_SIZE[0]/10, WINDOW_SIZE[1] - 30))

def initialise(menu, options):
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	window = pygame.display.set_mode(WINDOW_SIZE)

	exit_code = play(window) # Run main game loop

	pygame.quit()
	menu.deiconify()
	return exit_code


def generate_targets(player):
	sprite_list = []
	group = pygame.sprite.Group()
	if player.level > len(Levels)-1:
		level = generate_random_level()
	else: level = Levels[player.level]

	for i in range(level.rows):
		i *= level.padding
		for j in range(50, WINDOW_SIZE[0] - 70, level.padding):
			temp = Target(x=j,y=i)
			sprite_list.append(temp)
			del temp

	for i in range(level.firebacks):
		changed = False
		while not changed:
			index = randint(0, len(sprite_list)-1)
			if sprite_list[index].type != "SHOOTER":
				sprite_list[index].type = "SHOOTER"
				sprite_list[index].image.fill((0,255,0))
				x,y = sprite_list[index].rect.x, sprite_list[index].rect.y
				sprite_list[index].rect = sprite_list[index].image.get_rect()
				sprite_list[index].set_position(x,y, center=False)
				logging.debug("There's a shooter in the map!")
				changed = True

	for sprite in sprite_list: #Because sprite groups dont support indexing!
		group.add(sprite)
	return group
		

def play(window):
	window_rect = window.get_rect()

	player = Shooter(window=window)
	player.set_position(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]*0.83)
	player_group = pygame.sprite.Group()
	player_group.add(player)

	target_group = generate_targets(player)
	bullet_group = pygame.sprite.Group()

	clock = pygame.time.Clock()

	timeouts = {
		"Target Movement":[FPS*0.5,FPS*0.5]
	}

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
				temp = Bullet(player)
				bullet_group.add(temp)

			if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_PLUS:
				player.OP = not player.OP

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			if player.powerup == "SPEED": player.move(player.speed * 1.5)
			else: player.move(player.speed)

		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			if player.powerup == "SPEED": player.move(-player.speed*1.5)
			else: player.move(-player.speed)

		if keys[pygame.K_KP4] and keys[pygame.K_KP5] and keys[pygame.K_KP6] and player.OP:
			temp = Bullet(player)
			bullet_group.add(temp)

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
					logging.debug("Hit Target!")
					player.score += 1

			hit_list = pygame.sprite.spritecollide(bullet, player_group, False)
			for player in hit_list:
				if bullet.type == "TARGET":
					bullet_group.remove(bullet)
					logging.info("")
					player.lives -= 1
					if player.lives <= 0:
						return "LIVES"
		print(timeouts["Target Movement"][0])
		if timeouts["Target Movement"][0] <=0:
			drop_targets = False
			for target in target_group:
				target.move()
				if target.rect.x <= 30 or target.rect.x >=WINDOW_SIZE[0] - 30:
					drop_targets = True

				if target.rect.y >= player.rect.y + 20:
					PLAYING_GAME = False
					return "PLAYER COLLISION"

			if drop_targets:
				logging.debug("The targets are moving down a level!")
				for target in target_group:
					target.drop()

			timeouts["Target Movement"][0] = timeouts["Target Movement"][1]

		for target in target_group:
			if target.type == "SHOOTER":
				if randint(0,350) > 1: continue
				temp = Bullet(target)
				temp.type="TARGET"
				temp.speed = -3 #So it shoots down!
				bullet_group.add(temp)
				logging.info("A shot was fired by an enemy.")

		update_score(window, player.score)
		update_level(window, player.level)
		update_lives(window, player.lives)

		player_group.draw(window)
		bullet_group.draw(window)
		target_group.draw(window)
		pygame.display.update()

		for i in range(len(timeouts)):
			timeouts[i][0] -= 1
			print("subtract")

		clock.tick(FPS)


if __name__ == "__main__":
	logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
	initialise(None, None)
