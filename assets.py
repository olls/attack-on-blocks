import os, pygame, glob, logging
from collections import namedtuple
from random import randint

class Textures():
	def __init__(self):
		self.images = {
			"PLAYER":"player.png",
			"BULLET":"bullet.png",
			"TARGETS":[]
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


Level_Template = namedtuple('Level_Template', ("rows", "padding", "firebacks", "powerups"))
Levels = [
	Level_Template(4, 30, 3, 0),
	Level_Template(3, 15, 0, 1),
	Level_Template(3, 20, 2, 1)
]

def generate_random_level():
	logging.info("Generating a random level!")
	rows = randint(0, 12)
	padding = randint(5, 75)
	firebacks = randint(0, 15)
	powerups = randint(0, 15)
	return Level_Template(rows, padding, firebacks, powerups)