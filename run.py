import main
from config import ROOT_PATH, DEFAULT_BLOCK_WIDTH, DEFAULT_BLOCK_CHAR

import json
import os
import random


def GetRandomName():
    files = os.listdir(ROOT_PATH + "/Images")

    file = random.choice(files)

    if not os.path.exists(ROOT_PATH + "/ASCII/" + file + ".json"):
        import regenerate

    return os.path.splitext(file)[0]


config_name = GetRandomName()

config_file = open(ROOT_PATH + "/ASCII/" + config_name + ".json")

config = json.load(config_file)
config_file.close()

command = "neofetch --ascii " + \
    config["path"] + " --gap " + str(config["offset"])

os.system(command)
