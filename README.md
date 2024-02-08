# NeofetchCustomASCII
NeofetchCustomASCII changes your neofetch ASCII art to pixel art or some other ASCII

You can do what this does with built-in neofetch functionallity, I just wanted to implement this myself

## Usage
First add a images directory, this can be anything but by default it is "*/NeofetchCustomASCII/Images"
change the path in cofig.py if you want it in a different place

```
mkdir Images
```

Then add some images in this directory or in a subdirectory of this dir these can currently be pngs (with RGBA colors)
and files with the extention .ascii which are just plain text documents with the ascii art inside so for example cat.ascii would look like this

```
 _._     _,-'""`-._
(,-.`._,'(       |\`-/|
    `-.-' \ )-`( , o o)
          `-    \`_`"'-
```


run run.py to run neofetch

You can set the image you want by specifying the image you want with the first two arguments.
The first tells run.py where to find the image the second tells it the extention of said image if you have multiple images with the same name but a different extention for example you have cat.ascii and cat.png in the same subdirectory in your image directory. The first uses the rel_name_path which is just the path relative to the image folder; for example when you have a file at the path "*/NeofetchCustomASCII/Images/Art/cat.ascii" the relative name path would be "/Art/cat" the extention would be ".ascii"

```
python run.py
```

This should automatically create the ASCII directory here the raw text (.out files) for your image is stored aswell as the corresponding config (the JSON files)
you can change this path aswell in config.py (make shure this path is actually the path you want as the script runs rm -rf on ASCII_PATH/* when regenerating)

Run regenerate.py to regenerate your output this removes everything in your out path and regenerates every image and its config

```
python regenerate.py
```

If you dont want to add the images in some subdirectories of your images path add these to your IMAGE_IGNORE in config.py