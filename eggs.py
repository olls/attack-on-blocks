import pygame, logging, urllib.request, io
from time import sleep

def r9k(window):
	logging.warn("Look, you found a pepe!")
	raw_image = urllib.request.urlopen("https://38.media.tumblr.com/avatar_2cd47bc1ad07_128.png").read()
	image_file =  io.BytesIO(raw_image)
	image = pygame.transform.scale(pygame.image.load(image_file), window.get_size())
	window.blit(image, (0,0))
	font = pygame.font.SysFont(None, 30, bold=False)
	window.blit(font.render("A rare pepe has been found. Alert R9k", True, (0,0,0)), (window.get_width()/2-175, window.get_height()/2))
	pygame.display.update()
	sleep(9)