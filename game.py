import pygame, logging

import bullet, player, textures
from bullet import Bullet
from player import Shooter
from textures import Textures
from target import Target

PLAYING_GAME = False
WINDOW_SIZE = (640,480)
FPS = 120

def rounding(x, base): return int(base * round(float(x)/base))

def update_score(window, score):
	font = pygame.font.SysFont(None, 30, bold=False)
	window.blit(font.render("Score: {}".format(int(score)), True, (12,123,190)), (50, WINDOW_SIZE[1] - 30))

def initialise(menu, options):
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	window = pygame.display.set_mode(WINDOW_SIZE)

	exit_code = play(window) # Run main game loop

	if exit_code == "QUIT":
		pygame.quit()

	menu.deiconify()
	return exit_code


def generate_targets():
	group = pygame.sprite.Group()
	for i in range(5): # Number of rows
		i *= 25
		for j in range(50, WINDOW_SIZE[0] - 70, 30):
			#logging.debug("Target generated with position ({},{})".format(j,i))
			temp = Target(x=j,y=i)
			group.add(temp)
			del temp			
	return group
		

def play(window):
	window_rect = window.get_rect()

	player = Shooter(window=window)
	player.set_position(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]*0.83)
	player_group = pygame.sprite.Group()
	player_group.add(player)
	player_group.draw(window)

	target_group = generate_targets()
	bullet_group = pygame.sprite.Group()

	clock = pygame.time.Clock()
	PLAYING_GAME = True
	target_movement_timeout_default = FPS * 0.5
	target_movement_timeout = target_movement_timeout_default

	while PLAYING_GAME:
		window.fill((0,0,0))
		player_group.update()


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				logging.critical("Exiting Game...")
				PLAYING_GAME = False
				return "QUIT"

			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				temp = Bullet(player)
				bullet_group.add(temp)


		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			player.move(player.speed)

		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			player.move(-player.speed)

		if keys[pygame.K_KP4] and keys[pygame.K_KP5] and keys[pygame.K_KP6] and player.OP:
			temp = Bullet(player)
			bullet_group.add(temp)


		for sprite in bullet_group:
			if not sprite.at_top():
				sprite.update()
			if sprite.rect.y < 0:
				bullet_group.remove(sprite)


		for bullet in bullet_group:
			hit_list = pygame.sprite.spritecollide(bullet, target_group, True)
			for target in hit_list:
				target_group.remove(target)
				bullet_group.remove(bullet)
				logging.info("Hit Target!")
				player.score += 1


		if target_movement_timeout <=0:
			drop_targets = False
			for target in target_group:
				target.move()
				if target.rect.x <= 20 or target.rect.x >=WINDOW_SIZE[0] - 20 + target.width:
					drop_targets = True

				if target.rect.y >= player.rect.y + 10:
					PLAYING_GAME = False
					for target in target_group:
						target.image.fill((255,0,0))
					return "player collision"

			if drop_targets:
				logging.debug("drop")
				for target in target_group:
					target.drop()

			target_movement_timeout = target_movement_timeout_default




		update_score(window, player.score)
		player_group.update()
		bullet_group.draw(window)
		target_group.draw(window)
		player_group.draw(window)
		pygame.display.update()
		target_movement_timeout -= 1
		clock.tick(FPS)

if __name__ == "__main__":
	logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
	initialise(None, None)
