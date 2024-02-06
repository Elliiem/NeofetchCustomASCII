import json
import os
import random

import main


def GetRandomRelNamePath():
    images = main.GetFilesRecurse(main.IMAGE_PATH)

    if len(images) == 0:
        raise Exception("No Images Provided!")

    return os.path.splitext(random.choice(images))[0]


rel_name_path = GetRandomRelNamePath()

if not main.HasConfig(rel_name_path):
    main.GenerateImage(rel_name_path)

config_file = main.OpenConf(rel_name_path, "r")
config = json.load(config_file)
config_file.close()

out_path = main.GetOutPath(rel_name_path)
offset = config["offset"]

command = "neofetch --ascii " + out_path + " --gap " + str(offset)

os.system(command)
