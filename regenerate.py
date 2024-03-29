import os
import json

import main


def GenerateRecurse(images_path):
    files = main.GetFilesRecurse(images_path, ignore=main.IMAGE_IGNORE)

    for file in files:
        source = (os.path.splitext(file))

        main.Generate(source[0], source[1])

        config_file = main.OpenConfig(source[0], source[1], "r")
        config = json.load(config_file)

        out = main.OpenFile(config["path"], "r")

        print(out.read())
        print("\033[0m")

        out.close()
        config_file.close()


GenerateRecurse(
    "/home/elliem/Dev/Scripts/1st-Party/python/NeofetchCustomASCII/Images",
)
