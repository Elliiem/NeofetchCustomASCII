from PIL import Image

import json
import os

from config import *

if not os.path.exists(IMAGE_PATH):
    os.makedirs(IMAGE_PATH, exist_ok=True)

if not os.path.exists(ASCII_PATH):
    os.makedirs(ASCII_PATH, exist_ok=True)


def OpenFile(file_path, mode):
    dir = os.path.dirname(file_path)

    if mode == "r" or mode == "r+":
        if not os.path.exists(file_path):
            raise Exception("Trying to read from imaginary file")
    else:
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

    return open(file_path, mode)


def GetOutPath(rel_name_path):
    return ASCII_PATH + rel_name_path + ".out"


def OpenOut(rel_name_path, mode):
    out_path = GetOutPath(rel_name_path)

    return OpenFile(out_path, mode)


def GetImagePath(rel_name_path):
    return IMAGE_PATH + rel_name_path + ".png"


def OpenImg(rel_name_path):
    image_path = GetImagePath(rel_name_path)

    if not os.path.exists(image_path):
        raise Exception("Image does not exist!")

    return Image.open(image_path)


def GetConfigPath(rel_name_path):
    return ASCII_PATH + rel_name_path + ".json"


def OpenConf(rel_name_path, mode):
    config_path = GetConfigPath(rel_name_path)

    return OpenFile(config_path, mode)


def HasConfig(rel_name_path):
    return os.path.exists(GetConfigPath(rel_name_path))


def GetPixelString(px, prev_px, block_width, block_char):
    r = px[0]
    g = px[1]
    b = px[2]
    a = px[3]

    escape = "\033[38;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"
    block = block_char * block_width

    if a == 0:
        return " " * block_width
    elif prev_px == px:
        return block

    return escape + block


def GenerateASCII(rel_name_path, block_width, block_char):
    # Open Image
    img = OpenImg(rel_name_path)

    # Open Output file
    out = OpenOut(rel_name_path, "w")

    # Create ASCII
    line = " "
    prev = None

    for y in range(0, img.height):
        for x in range(0, img.width):
            px = img.getpixel([x, y])

            line += GetPixelString(px, prev, block_width, block_char)

            prev = px

        out.write(line + "\n")

        line = " "

    # Close Image and Out
    img.close()
    out.close()


def GenerateImage(rel_name_path, block_width=DEFAULT_BLOCK_WIDTH, block_char=DEFAULT_BLOCK_CHAR):
    # Load config
    if HasConfig(rel_name_path):
        config_file = OpenConf(rel_name_path, "r")
        config = json.load(config_file)
        config_file.close()
    else:
        config = {}

    # Overwrite defaults with config
    if "block_width" in config:
        block_width = config["block_width"]

    if "block_char" in config:
        block_char = config["block_char"]

    # Generate .out file
    GenerateASCII(rel_name_path, block_width, block_char)

    # Calculate offset
    img = OpenImg(rel_name_path)
    out = OpenOut(rel_name_path, "r")

    lines = out.readlines()
    longest = 0

    for line in lines:
        if len(line) > longest:
            longest = len(line)

    config["offset"] = -(longest - img.width * block_width) + 3

    out.close()
    img.close()

    # Write new config to json
    config_file = OpenConf(rel_name_path, "w")
    json.dump(config, config_file)
    config_file.close()


def GetFilesRecurse(root_path, name_rel_path="", ignore=[]):
    if name_rel_path in ignore:
        return []

    files = os.listdir(root_path + name_rel_path)

    dirs = []

    i = 0
    while i < len(files):
        if os.path.isdir(root_path + name_rel_path + "/" + files[i]):
            dirs.append(name_rel_path + "/" + files[i])
            files.pop(i)
        else:
            files[i] = name_rel_path + "/" + files[i]
            i += 1

    for dir in dirs:
        files += GetFilesRecurse(root_path, dir, ignore)

    return files
