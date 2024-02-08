import os
import random
import sys

import main


def GetRandomSource():
    sources = main.GetFilesRecurse(main.IMAGE_PATH, ignore=main.IMAGE_IGNORE)

    if len(sources) == 0:
        raise Exception(
            "No Images Provided! Add some images to your images path! (only png's)")

    split = os.path.splitext(random.choice(sources))

    return (split[0], split[1])


if len(sys.argv) > 1:
    if len(sys.argv) > 2:
        ext = sys.argv[2]
    else:
        ext = main.FindExt(sys.argv[1])

    source = (sys.argv[1], ext)
else:
    source = GetRandomSource()

rel_name_path = source[0]
ext = source[1]

if not main.HasConfig(rel_name_path, ext):
    main.Generate(rel_name_path, ext)

config = main.GetConfig(rel_name_path, ext)

out_path = config["path"]
offset = config["offset"]

command = "neofetch --ascii --source \"$(cat " + \
    out_path + ")\" --gap " + str(offset)

os.system(command)
