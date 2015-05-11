import os, pygame, glob, logging
from collections import namedtuple
from random import randint

class Textures():
	def __init__(self):
		self.images = {
			"PLAYER":"player.png",
			"BULLET":"bullet.png",
			"TARGETS":[],
			"SHOOTER":"shooter.png",
			"TARGET_BULLET":"target_bullet.png"
		}
		self.path=os.path.dirname(os.path.realpath(__file__)) + "\\resources\\texture_packs\\"
		self.pack = "default"

	def loadTexturePack(self, packName):
		if os.path.exists(self.path + packName):
			self.images["TARGETS"] = []

			targets = glob.glob(self.path+packName+"\\target*.png")
			logging.debug("Found {0} target files.".format(len(targets)))
			for file in targets:
				fileName = file.split("\\")[-1]
				self.images["TARGETS"].append(filename)

			self.pack = packName

	def getTexture(self, objectName):
		filename = self.path + self.pack + "\\{0}.png".format(self.images[objectName.upper()])
		return pygame.image.load(filename)

	def get_target_texture(self):
		filename = self.path + self.pack + "\\{}.png".format(self.images["TARGETS"][randint(0,len(self.images["TARGETS"]))])
		return pygame.image.load(filename)


Level_Template = namedtuple('Level_Template', ("rows", "padding", "firebacks", "powerups"))
Levels = [
	Level_Template(2, 20, 0, 0),
	Level_Template(3, 15, 2, 1),
	Level_Template(4, 25, 7, 1)
]


def generate_random_level():
	logging.info("Generating a random level!")
	rows = randint(0, 12)
	padding = randint(0, 30)
	firebacks = randint(0, 15)
	powerups = randint(0, 15)
	return Level_Template(rows, padding, firebacks, powerups)

Sounds = {}
def init_sounds():
	music_files = ["main.mp3", "fire.mp3"]
	for file in music_files:
		path = os.path.dirname(os.path.realpath(__file__)) + "\\resources\\sounds\\" + file
		if file == "main.mp3": mixer = pygame.mixer.music.load(path)
		else: mixer = pygame.mixer.Sound(file)
		Sounds.update(file.split(".")[0], mixer)
