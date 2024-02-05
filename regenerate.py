import main
from config import ROOT_PATH

import os

files = os.listdir(ROOT_PATH + "/Images")

for file in files:
    name = os.path.splitext(file)[0]

    main.GenerateImage(name)

    file = open(ROOT_PATH + "/ASCII/" + name + ".out")
    print(file.read())
    file.close()
