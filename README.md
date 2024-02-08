# NeofetchCustomASCII
NeofetchCustomASCII changes your neofetch ASCII art to pixel art or some other ASCII

![](https://github.com/Elliiem/NeofetchCustomASCII/blob/master/Readme-Images/Trans.png)

![](https://github.com/Elliiem/NeofetchCustomASCII/blob/master/Readme-Images/cat.png)

You can do what this does with built-in neofetch functionallity, I just wanted to implement this myself

# Usage
The Images directory contains all your source images you can put images directly in this directory or add them to subdirectories like this
```
Images
|-- ASCII
|   `-- cat.ascii
`-- Image
    `-- cat.png
```
Images are identified by their extention so make sure these are correct; a .ascii file is just a plain text document. For example cat.ascii looks like this
```
 _._     _,-'""`-._
(,-.`._,'(       |\`-/|
    `-.-' \ )-`( , o o)
          `-    \`_`"'-
```

##

run run.py to run neofetch

```
python run.py
```

You can set the image you want by specifying the image you want with the first two arguments.
The first tells run.py where to find the image the second tells it the extention of said image; this is used to identify images with the same name but have different extention. For example you have cat.ascii and cat.png in the same directory in your image directory; like this.

```
Images
|-- cat.ascii
`-- cat.png
```

If you dont choose an image a random one is chosen. The IGNORE variable in `config.py` is used to ignore subdirectories from this selection

The first argument uses the relative path to the image which is just the path relative to the image folder; for example if you have a file-structure like the one above
this would be `/cat` to get one of the files named cat, note the / at the start. Since there is `cat.ascii` and `cat.png` you need to add the extention. If you want to point to `cat.ascii` you need to run

```
python run.py /cat .ascii
```

for `cat.png` it would be

```
python run.py /cat .png
```

If the filestructure is like the other one above and you want to select `cat.png` you run this command

```
python /Image/cat
```

You dont need to add the exention since it isnt ambiguous here

## Regenerating

`run.py` automatically generates the config for the source it uses if it isnt present, when it uses an Image it also generates the raw `.ascii file`. If you want to regenerate all ascii files you can run

```
python regenerate.py
```