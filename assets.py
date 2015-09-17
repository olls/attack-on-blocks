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
        self.path = os.path.join(os.getcwd(), "resources", "texture_packs")
        self.pack = "default"

    def load_texture_pack(self, pack_name):
        if os.path.exists(os.path.join(self.path, pack_name)):
            self.images["TARGETS"] = []

            targets = glob.glob(os.path.join(self.path, pack_name, "target*.png"))
            logging.debug("Found {0} target files.".format(len(targets)))
            for file_ in targets:
                filename = file_.split(os.sep)[-1].replace(".png", "")
                self.images["TARGETS"].append(filename)

            self.pack = pack_name
        else: logging.warn("Cannot find texture pack '{}'".format(pack_name))

    def get_texture(self, objectName):
        filename = os.path.join(self.path, self.pack, "{0}.png".format(self.images[objectName.upper()]))
        return pygame.image.load(filename)

    def get_target_texture(self, ID=False):
        if not ID:
            index = randint(0,len(self.images["TARGETS"])-1) if len(self.images["TARGETS"]) >=1 else 0
            filename = os.path.join(self.path, self.pack, "{}.png".format(self.images["TARGETS"][index]))
            return [pygame.image.load(filename), index]
        else:
            filename = os.path.join(self.path, self.pack, "target{}.png".format(int(ID)))
            return [pygame.image.load(filename), ID]

    def list_packs(self):
        return [os.path.relpath(x[0], self.path) for x in os.walk(self.path) if os.path.samefile(x[0], self.path)]



Level_Template = namedtuple('Level_Template', ("rows", "padding", "firebacks", "powerups"))
Levels = [
    Level_Template(2, 20, 0, 0),
    Level_Template(3, 15, 1, 0),
    Level_Template(4, 15, 3, 1),
    Level_Template(3, 7, 2, 2),
    Level_Template(5, 15, 2, 1),
    Level_Template(2, 20, 100, 2), #All the enemies!
    Level_Template(3, 15, 2, 1),
    Level_Template(3, 7, 2, 4),
    Level_Template(4, 15, 4, 3),
    Level_Template(5, 35, 4, 6),
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
    music_files = ["main.ogg", "OP.ogg", "shot.ogg"]
    for file_ in music_files:
        path = os.path.join(os.getcwd(), "resources", "sounds", file_)
        if file_ == "main.ogg":
            mixer = pygame.mixer.music
            mixer.load(path)
        else: mixer = pygame.mixer.Sound(path)
        mixer.set_volume(1.0)
        Sounds[file_.replace(".ogg", "")] = mixer
