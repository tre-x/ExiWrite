# EXIWRITE SCRIPT VERSION 1 (tre-x)
from PIL import Image
from PIL import ImageTk

from pathlib import Path
import os

import logging

from tkinter import Tk, Label, Button
from tkinter import N, W, E, S
from tkinter import filedialog as FileDialog
from tkinter import messagebox as MessageBox

# log
logger = logging.getLogger('exiwrite')
hdlr = logging.FileHandler('exiwrite.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)
logger.setLevel(logging.INFO)

# path functions
def getParentDir(path):
    return os.path.dirname(os.path.dirname(os.path.abspath(path)))

def getFileExt(path):
    return os.path.splitext(path)[1]

def getFileName(path, extension=True):
    if extension:
        return os.path.basename(path)
    else:
        return os.path.splitext(os.path.basename(path))[0]

# img functions
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd
    
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):
                if (pix[j] % 2 != 0):
                    pix[j] -= 1
            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
        
def writePix(newimg, data):
    with open(Path(data), 'r') as f:
        wdata = f.read()
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), wdata):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# main functions
def notify(title, txt):
    MessageBox.showinfo(title, txt)

def Encode(imgfilepath, datafilepath):

    imgfilename = getFileName(imgfilepath)
    imgfiledir = getParentDir(imgfilepath)
    logger.info('ENCODING %s (%s)'%(imgfilename, imgfiledir))
    newfile = FileDialog.asksaveasfilename(initialdir = imgfiledir,title = "Save new encoded file as...",filetypes = (("PNG files","*.png"),("all files","*.*")))
    # TODO: temporary fix for windows users where file extension went missing
    default_extension = '.png'
    if default_extension not in newfile:
        newfile = newfile + default_extension
    with open(Path(datafilepath), 'r') as f:
    
        if len(f.read()) == 0:
            notify(
                'Error', 
                '%s is empty! (error code 0.1)'%(datafilepath)
            )
            logger.error('[0.1] ENCODING %s (%s) FAILED, source %s is empty'%(imgfilename,
                                                                            imgfiledir,
                                                                            datafilepath))
            return 'disabled'

    try:
        image = Image.open(Path(imgfilepath), 'r')
    except Exception as e:
        notify(
            'PIL Error', 'Unable to open %s during encoding process. Please check exiwrite.log (error code 1.1)'%(imgfilename)
        )
        logger.error('[1.1] ENCODING %s (%s) FAILED, PIL could not open image\n%s'%(imgfilename,
                                                                            imgfiledir,
                                                                            str(e)))
        return 'disabled'

    try:
        copy = image.copy()
    except Exception as e:
        notify(
            'Error', 
            'Unable to copy %s during encoding process. Please check exiwrite.log (error code 2.1)'%(imgfilename)
        )
        logger.error('[2.1] ENCODING %s (%s) FAILED, PIL could not copy image\n%s'%(imgfilename,
                                                                            imgfiledir,
                                                                            str(e)))
        return 'disabled'
    
    try:
        writePix(copy, datafilepath)
    except Exception as e:
        notify(
            'Error', 
            'Unable to write pixels in %s. Please check exiwrite.log (error code 3.1)'%(imgfilename)
        )
        logger.error('[3.1] ENCODING %s (%s) FAILED, could not write pixels\n%s'%(imgfilename,
                                                                            imgfiledir,
                                                                            str(e)))
        return 'disabled'

    try:
        print(newfile)
        copy.save(Path(newfile))
    except Exception as e:
        notify(
            'Error', 
            'Unable to save newly created %s after a completed encoding process. Are you the owner of the containing folder? A detailed error was logged to output (error code 4.1)'%(getFileName(newfile), imgfilename)
        )
        logger.error('[4.1] ENCODING %s (%s) FAILED, could not save file %s\n%s'%(imgfilename,
                                                                            imgfiledir, 
                                                                            newfile,
                                                                            str(e)))
        return 'disabled'
    
    notify(
        'Success!', 
        '%s was encoded successfully into the new image file located at %s!'%(imgfilename, newfile)
    )
    logger.info('ENCODING %s (%s) COMPLETE'%(imgfilename,imgfiledir))
    return 'disabled'

def Decode(imgfilepath, existing=False):

    imgfilename_ext = getFileName(imgfilepath)
    imgfilename = getFileName(imgfilepath, extension=False)
    imgfiledir = getParentDir(imgfilepath)
    logger.info('DECODING %s (%s)'%(imgfilename_ext, imgfiledir))
    try:
        image = Image.open(imgfilepath, 'r')
    except Exception as e:
        notify(
            'PIL Error',
            'Unable to open %s . Please check exiwrite.log (error code 1.2)'%(imgfilename_ext)
        )
        logger.error('[1.2] DECODING %s (%s) FAILED, PIL could not open image\n%s'%(imgfilename_ext,
                                                                            imgfiledir,
                                                                            str(e)))
        return 'disabled'

    try:
        out = ''
        imgdata = iter(image.getdata())
        while True:
            pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
            binary = ''

            for i in pixels[:8]:
                if (i % 2 == 0):
                    binary += '0'
                else:
                    binary += '1'

            out += chr(int(binary, 2))

            if (pixels[-1] % 2 != 0):
                if 1 > len(out):
                    e = '(error 0.2) encoded data: %s'%(out)
                    notify(
                        'Error', 
                        '%s does not contain any encoded data (error code 0.2)'%(imgfilename_ext)
                    )
                    logger.error('[0.2] DECODING %s (%s) FAILED, image does not contain any encoded data\n%s'%(imgfilename_ext,
                                                                                                               imgfiledir,
                                                                                                               str(e)))
                    return 'disabled'
                if not existing:
                    newdatafile = FileDialog.asksaveasfilename(initialdir = imgfiledir,title = "Save decoded results as...",filetypes = (("TXT files","*.txt"),("all files","*.*")))
                    # TODO: temporary fix for windows users where file extension went missing
                    default_extension = '.txt'
                    if default_extension not in newdatafile:
                        newdatafile = newdatafile + default_extension
                    with open(Path(newdatafile), 'w+') as f:
                        f.write(out)
                    notify(
                        'Success!', 
                        '%s was decoded successfully! Contents have been written to %s'%(imgfilename_ext, newdatafile)
                    )
                    logger.info('DECODING %s (%s) COMPLETE'%(imgfilename_ext,imgfiledir))
                    return 'disabled'
                elif existing:
                    with open(Path(existing), 'w+') as ef:
                        ef.write(out)
                    notify(
                        'Success!', 
                        '%s was decoded successfully! Contents have been written to %s'%(imgfilename_ext, existing)
                    )
                    return 'disabled'

    except Exception as e:
        notify(
            'Error', 
            '%s does not contain any encoded data (error code 2.2)'%(imgfilename_ext)
        )
        logger.error('[2.2] DECODING %s (%s) FAILED, unable to read pixels on image, image contains no encoded data\n%s'%(imgfilename_ext,
                                                                                          imgfiledir,
                                                                                          str(e)))
        return 'disabled'

def main():

    window = Tk()
    window.geometry("300x108")
    window.title('ExiWrite 1')
    window.iconbitmap('imgs/icon.ico')
    window.resizable(0,0)

    class script:
        TargetFile = None # (type, path, name_with_extension)
        SourceFile = None
        def reset():
            script.TargetFile = None
            script.SourceFile = None
    
    def fileHandler():
        script.EncodeButton['state'] = 'disabled'
        script.DecodeButton['state'] = 'disabled'
        script.reset()

        files = FileDialog.askopenfiles(multiple=True)
        txt = (False,False,False)
        jpeg, png = (False,False,False), (False,False,False)

        if len(files) > 2:
            notify('Warning', 'Please select no more than 2 files to begin the encoding/decoding process. See the help page for more information')
            return None
        elif 2 >= len(files):
            for file in files:

                filepath = file.name
                filename = getFileName(filepath)
                filetype = getFileExt(filepath)
                print(filename, filepath)

                if filetype == '.txt':
                    txt = (True, filepath, filename)
                elif filetype == '.jpg' or filetype == '.jpeg':
                    jpeg = (True, filepath, filename)
                elif filetype == '.png':
                    png = (True, filepath, filename)

            if jpeg[0] and png[0]:
                notify('Warning', 'Please select either a JPG image to encode or a PNG image to decode instead of both. See the help page for more information')
                return None

            if len(files) == 2 and png[0] and not txt[0] and not jpeg[0]:
                notify('Warning', 'Please select only one PNG image to decode and one TXT file (optional) to write the decoded data to. See the help page for more information')
                return None

            if len(files) == 2 and jpeg[0] and not txt[0] and not png[0]:
                notify('Warning', 'Please select only one JPG image to encode and one TXT file as a source. See the help page for more information')
                return None

            if len(files) == 2 and txt[0] and not jpeg[0] and not png[0]:
                notify('Warning', 'Please select only one TXT file as a source/destination and one image (JPG/PNG) file. See the help page for more information')
                return None

            if len(files) == 1 and jpeg[0]:
                notify('Warning', 'Please also select a TXT file as a source file to encode data to %s. See the help page for more information'%(jpeg[2]))
                return None
            
            if len(files) == 1 and txt[0]:
                notify('Warning', 'Please also select a JPG/PNG image as a destination/source to encode data onto from %s. See the help page for more information'%(txt[2]))
                return None
                
            if txt[0] and jpeg[0]:
                script.SourceFile = (txt[1], txt[2])
                script.TargetFile = (jpeg[1], jpeg[2])
                script.EncodeButton['state'] = 'normal'
            elif txt[0] and png[0]:
                script.SourceFile = (txt[1], txt[2])
                script.TargetFile = (png[1], png[2])
                script.DecodeButton['state'] = 'normal'
            elif png[0]:
                script.TargetFile = (png[1], png[2])
                script.DecodeButton['state'] = 'normal'
            else:
                return None
    
    def encode():
        if script.SourceFile:
            if script.TargetFile:
                script.EncodeButton['state'] = Encode(script.TargetFile[0], script.SourceFile[0])
                script.reset()

    def decode():
        if script.TargetFile:
            if not script.SourceFile:
                script.DecodeButton['state'] = Decode(script.TargetFile[0])
                script.reset()
            elif script.SourceFile:
                script.DecodeButton['state'] = Decode(script.TargetFile[0], existing=script.SourceFile[0])
                script.reset()
    
    openf = Button(window, width=12, height=1, text='Choose file(s)', command=fileHandler)
    openf.grid(row=1, column=1, padx=10)
    
    img = ImageTk.PhotoImage(Image.open('imgs/banner-small.png'))
    banner = Label(window, image=img)
    banner.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=0, pady=5)

    script.EncodeButton = Button(window, width=9, height=1, text='Encode', command=encode)
    script.EncodeButton['state'] = 'disabled'
    script.EncodeButton.grid(row=2, column=2)

    script.DecodeButton = Button(window, width=9, height=1, text='Decode', command=decode)
    script.DecodeButton['state'] = 'disabled'
    script.DecodeButton.grid(row=2, column=3)

    window.mainloop()

if __name__ == '__main__':
    main()
