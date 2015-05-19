import os, pygame, glob, logging
from collections import namedtuple
from random import randint

class Textures():
    def __init__(self):
        self.images = {
            "PLAYER":"player",
            "BULLET":"bullet",
            "TARGETS":[],
            "SHOOTER":"shooter",
            "TARGET_BULLET":"bullet_target",
            "POWERUP": "powerup"
        }
        self.path=os.path.dirname(os.path.realpath(__file__)) + "\\resources\\texture_packs\\"
        self.pack = "default"

    def load_texture_pack(self, pack_name):
        if os.path.exists(self.path + pack_name):
            self.images["TARGETS"] = []

            targets = glob.glob(self.path+pack_name+"\\target*.png")
            logging.debug("Found {0} target files.".format(len(targets)))
            for file in targets:
                filename = file.split("\\")[-1].replace(".png", "")
                self.images["TARGETS"].append(filename)

            self.pack = pack_name
        else: logging.warn("Cannot find texture pack '{}'".format(ppack_name))

    def get_texture(self, objectName):
        filename = self.path + self.pack + "\\{0}.png".format(self.images[objectName.upper()])
        return pygame.image.load(filename)

    def get_target_texture(self):
        index = randint(0,len(self.images["TARGETS"])-1) if len(self.images["TARGETS"]) >=1 else 0
        filename = self.path + self.pack + "\\{}.png".format(self.images["TARGETS"][randint(0,len(self.images["TARGETS"])-1)])
        return pygame.image.load(filename)

    def list_packs(self):
        return [x[0].replace(self.path, "") for x in os.walk(self.path)]



Level_Template = namedtuple('Level_Template', ("rows", "padding", "firebacks", "powerups"))
Levels = [
    Level_Template(2, 20, 0, 0),
    Level_Template(3, 15, 1, 0),
    Level_Template(4, 15, 3, 1),
    Level_Template(3, 7, 2, 2),
    Level_Template(5, 15, 2, 1),
    Level_Template(1, 20, 100, 0), #All the enemies!
    Level_Template(3, 15, 2, 1),
]


def generate_random_level():
    logging.info("Generating a random level!")
    rows = randint(1, 12)
    padding = randint(5, 30)
    firebacks = randint(0, 15)
    powerups = randint(0, 15)
    return Level_Template(rows, padding, firebacks, powerups)


Sounds = {}
def init_sounds():
    music_files = ["main.wav", "OP.wav", "shot.wav"]
    for file in music_files:
        path = os.path.dirname(os.path.realpath(__file__)) + "\\resources\\sounds\\" + file
        if file == "main.wav":
            mixer = pygame.mixer.music
            mixer.load(path)
        else: mixer = pygame.mixer.Sound(path)
        mixer.set_volume(1.0)
        Sounds[file.replace(".wav", "")] = mixer