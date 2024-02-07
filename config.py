import os

# The default width of a pixel if for example this value is 2 each pixel will be '██' or two characters long
DEFAULT_BLOCK_WIDTH = 2
# The default character that will be used for the pixels
DEFAULT_BLOCK_CHAR = "█"

# Paths to your images and output directories these use absolute paths
ROOT_PATH = os.path.dirname(__file__)
IMAGE_PATH = ROOT_PATH + "/Images"
ASCII_PATH = ROOT_PATH + "/ASCII"

# Ignores a directories in the image path this uses rel_name_paths which are the ending of a path for example
# if you have a directory called Test in your image path and want to ignore it you add "/Test" in the image ignore
IMAGE_IGNORE = []
