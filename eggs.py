import pygame, logging, urllib.request, io
from time import sleep

def r9k(window):
    logging.warn("Look, you found a pepe!")
    raw_image = urllib.request.urlopen("http://img.ifcdn.com/images/620f230fad2806fe5305fac45dd673b8fc005b98c1e3b8584abc9c439b050950_1.jpg").read()
    image_file =  io.BytesIO(raw_image)
    image = pygame.transform.scale(pygame.image.load(image_file), window.get_size())
    window.blit(image, (0,0))
    font = pygame.font.SysFont(None, 30, bold=False)
    window.blit(font.render("A rare pepe has been found. Alert R9k", True, (0,0,0)), (window.get_width()/2-175, window.get_height()/2))
    pygame.display.update()
    sleep(9)