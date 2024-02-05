import main
from config import ROOT_PATH

import json
import os
import random


def GetRandomName():
    files = os.listdir(ROOT_PATH + "/Images")

    file_name = os.path.splitext(random.choice(files))[0]

    if not os.path.exists(ROOT_PATH + "/ASCII/" + file_name + ".json"):
        main.GenerateImage(file_name)

    return file_name


config_name = GetRandomName()

config_file = open(ROOT_PATH + "/ASCII/" + config_name + ".json")

config = json.load(config_file)
config_file.close()

path = config["path"]
offset = config["offset"]

command = "neofetch --ascii " + path + " --gap " + str(offset)

os.system(command)
