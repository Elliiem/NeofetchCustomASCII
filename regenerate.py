import os

import main


def GenerateRecurse(images_path):
    files = main.GetFilesRecurse(images_path, ignore=main.IMAGE_IGNORE)

    for file in files:
        file = os.path.splitext(file)[0]

        main.GenerateImage(file)

        out = main.OpenOut(file, "r")
        print(out.read())
        print("\033[0m")
        out.close()


def Clean():
    if main.ASCII_PATH == "":
        return

    # Scary (I learned nothing from steam, pwease lemme delete your filesystem uwu)
    os.system("rm -rf " + main.ASCII_PATH + "/*")


Clean()

GenerateRecurse(
    "/home/elliem/Dev/Scripts/1st-Party/python/NeofetchCustomASCII/Images",
)
