# ExiWrite

An open-source graphical image steganography tool written in Python.

(Full & more detailed documentation coming soon.)

## Usage

Exiwrite is capable of encoding messages within a JPEG image's exif data. This is done by re-ordering the images pixels and inserting pixels that contain a series of data used to cipher the message pixel-by-pixel. For now, Exiwrite only supports the following characters:
```ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890~!@#$%^&*()_+`{}|[]\:";'<>?,./```

### Encoding messages

Exiwrite requires **at least 2** files to start any image encoding process. First, a valid ```.JPG``` or ```.JPEG``` file to write messages to, and Second, a valid ```.TXT``` file that contains the message. After two of those files are chosen, the encoding process can initiate. After the encoding process is completed, you will be prompted where to save the new image in which contains your encoded message. This new image will be a ```.PNG``` file. The ```.JPG```/```.JPEG``` file you chose will ***not*** hold any encoded data, only the ```.PNG``` file will, while appearing *completely identical* to the ```.JPG``` file when opened in any photo viewer application.

( Image examples coming soon )

### Decoding messages

Exiwrite requires **atleast *1*** file to start any image decoding process. First and foremost, a ```.PNG``` image containing any encoded messages written by **Exiwrite itself only**. An optional ```.TXT``` file can also be chosen alongside the ```.PNG``` image, acting as a destination in which will contain any encoded messages found in the image. If no ```.TXT``` file is chosen, you will be prompted where to save a new ```.TXT``` file that will contain the decoded messages. Upon a successful decoding process, the message that was encoded within the ```.PNG``` file will appear in the ```.TXT``` file. The ```.PNG``` image will not be altered during the process, thus meaning that the encoded message will remain inside of the image even after the decoding process.  
(Image examples coming soon) 

## Requirements

### Unix
Python 3 (should be pre-installed)

Pillow (https://pillow.readthedocs.io/en/stable/installation.html#basic-installation)

Tkinter (sudo apt-get install python3-tk)

### Windows
None other than the executable itself.

## Installation
See releases page (https://github.com/tre-x/ExiWrite/releases)
