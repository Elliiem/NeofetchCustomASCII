from PIL import Image

import json
import os

from typing import TextIO
from typing import List, Dict

from config import *

if not os.path.exists(IMAGE_PATH):
    os.makedirs(IMAGE_PATH, exist_ok=True)

if not os.path.exists(ASCII_PATH):
    os.makedirs(ASCII_PATH, exist_ok=True)


def GetFilesRecurse(root_path: str, name_rel_path: str = "", ignore: list = []):
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


def FindExt(rel_name_path: str) -> str:
    search_path = os.path.dirname(IMAGE_PATH + rel_name_path)

    name = os.path.basename(rel_name_path)

    files = os.listdir(search_path)

    canidates = []

    for file in files:
        if file.find(name) != -1:
            canidates.append(file)

    if len(canidates) == 1:
        return os.path.splitext(canidates[0])[1]
    else:
        raise Exception("Extention is ambigous!")


def OpenFile(file_path: str, mode: str) -> TextIO:
    dir = os.path.dirname(file_path)

    if mode == "r" or mode == "r+":
        if not os.path.exists(file_path):
            raise Exception("Trying to read from imaginary file")
    else:
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

    return open(file_path, mode)


def GetASCIIPath(rel_name_path: str, root_path: str, ext: str) -> str:
    return root_path + rel_name_path + ext + ".ascii"


def OpenASCII(rel_name_path: str, root_path: str, ext: str, mode: str) -> TextIO:
    return OpenFile(GetASCIIPath(rel_name_path, root_path, ext), mode)


def GetImagePath(rel_name_path: str, ext: str) -> str:
    return IMAGE_PATH + rel_name_path + ext


def OpenImage(rel_name_path: str, ext: str) -> Image:
    image_path = GetImagePath(rel_name_path, ext)

    if not os.path.exists(image_path):
        raise Exception("Image does not exist!")

    return Image.open(image_path)


def GetConfigPath(rel_name_path: str, ext: str) -> str:
    return ASCII_PATH + rel_name_path + ext + ".json"


def HasConfig(rel_name_path: str, ext: str) -> bool:
    return os.path.exists(GetConfigPath(rel_name_path, ext))


def OpenConfig(rel_name_path: str, ext: str, mode: str) -> Dict[str, any]:
    config_path = GetConfigPath(rel_name_path, ext)

    return OpenFile(config_path, mode)


def HasSrcASCII(rel_name_path: str) -> bool:
    ascii_path = GetASCIIPath(rel_name_path, IMAGE_PATH, "")

    return os.path.exists(ascii_path)


def GetASCIIWidth(ascii: TextIO) -> int:
    lines = ascii.readlines()

    longest = 0

    for line in lines:
        if len(line) > longest:
            longest = len(line)

    return longest


def GetConfig(rel_name_path: str, ext: str) -> Dict[str, any]:
    if not HasConfig(rel_name_path, ext):
        return {}

    config_fd = OpenConfig(rel_name_path, ext, "r")
    config = json.load(config_fd)

    config_fd.close()

    return config


def SaveConfig(rel_name_path: str, ext: str, config: Dict[str, any]) -> None:
    config_fd = OpenConfig(rel_name_path, ext, "w")

    json.dump(config, config_fd)

    config_fd.close()


def GetPNGPixelString(px: (int, int, int, int), prev_px: (int, int, int, int), block_width: int, block_char: str) -> None:
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


def GeneratePNGASCII(image: Image, ascii: TextIO, block_width: int, block_char: str) -> None:
    line = " "
    prev = None

    for y in range(0, image.height):
        for x in range(0, image.width):
            px = image.getpixel([x, y])

            line += GetPNGPixelString(px, prev, block_width, block_char)

            prev = px

        ascii.write(line + "\n")

        line = " "


def GenerateJPGASCII(rel_name_path: str, image: Image, ascii: TextIO) -> None:
    pass


def GenerateImageASCII(image: Image, ascii: TextIO, config: Dict[str, any], ext: str) -> None:
    if "block_width" in config:
        block_width = config["block_width"]
    else:
        block_width = DEFAULT_BLOCK_WIDTH

    if "block_char" in config:
        block_char = config["block_char"]
    else:
        block_char = DEFAULT_BLOCK_CHAR

    match ext:
        case ".png":
            GeneratePNGASCII(image, ascii, block_width, block_char)
        case _:
            raise Exception("Invalid image type")


def GenerateImageConfig(rel_name_path: str, image: Image, ascii: TextIO, ext: str) -> None:
    config = GetConfig(rel_name_path, ext)

    config["path"] = GetASCIIPath(rel_name_path, ASCII_PATH, ext)

    if "block_width" in config:
        block_width = config["block_width"]
    else:
        block_width = DEFAULT_BLOCK_WIDTH

    if not "offset" in config:
        ascii_width = GetASCIIWidth(ascii)

        config["offset"] = -(ascii_width - image.width * block_width) + 3

    SaveConfig(rel_name_path, ext, config)


def GenerateSrcASCIIConfig(rel_name_path: str) -> None:
    config = GetConfig(rel_name_path, ".ascii")

    if not "path" in config:
        config["path"] = GetASCIIPath(rel_name_path, IMAGE_PATH, "")

    if not "offset" in config:
        config["offset"] = 0

    SaveConfig(rel_name_path, ".ascii", config)


def Generate(rel_name_path: str, ext: str = "") -> None:
    if HasSrcASCII(rel_name_path) and (ext == "" or ext == ".ascii"):
        GenerateSrcASCIIConfig(rel_name_path)
    else:
        image = OpenImage(rel_name_path, ext)
        ascii = OpenASCII(rel_name_path, ASCII_PATH, ext, "w+")

        config = GetConfig(rel_name_path, ext)

        GenerateImageASCII(image, ascii, config, ext)

        ascii.seek(0)

        GenerateImageConfig(rel_name_path, image, ascii, ext)

        ascii.close()
