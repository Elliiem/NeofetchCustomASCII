# NeofetchCustomASCII
NeofetchCustomASCII changes your neofetch ASCII art to pixel art

## Usage
First add a images directory, this can be anything but by default it is "*/NeofetchCustomASCII/Images" 
change the path in cofig.py if you want it in a different place

```
mkdir Images
```

Then add some images (currently only png's with RGBA colors are supported) and you should be good to go

run run.py to run neofetch

```
python run.py
```

This should automatically create the ASCII directory here the raw text (.out files) for your image is stored aswell as the corresponding config (the JSON files)
you can change this path aswell in config.py (make shure this path is actually the path you want as the script runs rm -rf on ASCII_PATH/* when regenerating)

Run regenerate.py to regenerate your output this removes everything in your out path and regenerates every image

```
python regenerate.py
```

If you dont want to add the images in some subdirectories of your images path add these to your IMAGE_IGNORE in config.py