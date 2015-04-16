import os, pygame, glob
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
			targets = glob.glob(self.path+packName+"\\target*.png")
			for file in files:
				fileName = file.split("\\")[-1]
				if 
			self.pack = packName

	def getTexture(self, objectName):
		filename = self.path + self.pack + "\\{0}.png".format(self.images[objectName.upper()])
		return pygame.image.load(filename)

