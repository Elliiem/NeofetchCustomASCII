import os

import main


def GenerateRecurse(images_path):
    files = main.GetFilesRecurse(images_path)

    for file in files:
        file = os.path.splitext(file)[0]

        main.GenerateImage(file)

        out = main.OpenOut(file, "r")
        print(out.read())
        print("\033[0m")
        out.close()


GenerateRecurse(
    "/home/elliem/Dev/Scripts/1st-Party/python/NeofetchCustomASCII/Images",
)
