from PIL import Image
import json
import os

from config import ROOT_PATH, DEFAULT_BLOCK_WIDTH, DEFAULT_BLOCK_CHAR


def GetPixelString(px, prev_px, block_width, block_char):
    r = px[0]
    g = px[1]
    b = px[2]
    a = px[3]

    escape = "\033[38;2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"
    block = block_char * block_width

    if a != 255:
        return " " * block_width
    elif prev_px == None:
        return escape + block
    elif px != prev_px and prev_px[3] == 255:
        return escape + block
    else:
        return block


def GenerateASCII(name, block_width, block_char):
    img = Image.open(ROOT_PATH + "/Images/" + name + ".png")
    out = open(ROOT_PATH + "/ASCII/" + name + ".out", "w")

    line = " "
    prev = None

    for y in range(0, img.height):
        for x in range(0, img.width):
            px = img.getpixel([x, y])

            line += GetPixelString(px, prev, block_width, block_char)

            if px[3] == 255:
                prev = px

        out.write(line + "\n")

        line = " "

    img.close()
    out.close()


def GenerateImage(name, block_width=DEFAULT_BLOCK_WIDTH, block_char=DEFAULT_BLOCK_CHAR):
    json_exists = os.path.exists(ROOT_PATH + "/ASCII/" + name + ".json")

    if json_exists:
        config_file = open(ROOT_PATH + "/ASCII/" + name + ".json", "r")
        config = json.load(config_file)

        if "block_width" in config:
            block_width = config["block_width"]

        if "block_char" in config:
            block_char = config["block_char"]
    else:
        config = {}
        config_file = open(ROOT_PATH + "/ASCII/" + name + ".json", "w")

    GenerateASCII(name, block_width, block_char)

    if not "path" in config:
        config["path"] = ROOT_PATH + "/ASCII/" + name + ".out"

    if not "offset" in config:
        img = Image.open(ROOT_PATH + "/Images/" + name + ".png")
        out = open(ROOT_PATH + "/ASCII/" + name + ".out", "r")

        lines = out.readlines()

        longest = 0
        for line in lines:
            if len(line) > longest:
                longest = len(line)

        config["offset"] = (-(longest - img.width * block_width)) + 3

        out.close()
        img.close()

    if json_exists:
        config_file.close()
        config_file = open(ROOT_PATH + "/ASCII/" + name + ".json", "w")

    json.dump(config, config_file)

    config_file.close()
