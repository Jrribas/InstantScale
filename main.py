import easygui
import cv2
import pytesseract
from PIL import Image
from processImage import *
import sys, ctypes 
import os
import shutil

exePath = os.getcwd()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    def tesseractPath(failed=False):
        #SELECT PATH TO TESSERACT FOLDER AND SAVE
        if not os.path.isfile('TesseractPath.txt'):
            f = open("TesseractPath.txt", "wb")
            f.close()

        f = open( 'TesseractPath.txt', 'r' )
        file_path = f.read()
        f.close()
        if file_path == '':
            print("Select path to tesseract exe, by default on Program Files (x86)\Tesseract-OCR")
            file_path = easygui.fileopenbox("Please select the Tesseract.exe file", "Instantscale", filetypes= "*.exe")
            f = open('TesseractPath.txt', 'w')
            f.write(file_path)
            f.close()

        elif failed == True:
            #Clean txt
            file_path = easygui.fileopenbox("Please select the Tesseract.exe file", "Instantscale", filetypes= "*.exe")
            with open('TesseractPath.txt', "w"):
                pass
            f = open('TesseractPath.txt', 'w')
            f.write(file_path)
            f.close()

        pytesseract.pytesseract.tesseract_cmd = file_path
        TESSDATA_PREFIX = os.path.dirname(file_path)




    file_path = tesseractPath()

    #TEST TESSERACT
    try:
        pytesseract.image_to_string(Image.open(r'pytesseract\test.png'))
    except:
        print("Tesseract failed to Load Try Again")
        tesseractPath(True)


    print("Selecting Images")
    file_path = easygui.fileopenbox("Please select the images to process", "Instantscale", filetypes= "*.tif", multiple=True)
    print('Cleaning File Types')

    position = None
    while position not in list(range(4)):
        try:
            position =  int(input("Where do you want to place the scale? (Bottom Left - 0, Bottom Right - 1, Top Left - 2, Top Right - 3)"))
        except:
            pass

    #MAIN PART
    try:
        file_path1 = cleanPathFiles(file_path)
        print("Looping Images...")

        if type(file_path1) is str:
            file_path1 = [file_path1]

        for x in range(len(file_path1)):
            print("Read Image...")
            img = cv2.imread(file_path1[x])
            height, width, channels = img.shape
            print("Crop Image...")
            crop_img,bar_img = getBar(img)
            print("Get scale bar size...")
            scale = len(getScale(bar_img))
            print("scale: ", str(scale))
            print("Get scale number...")
            original_bar_img = bar_img
            for i in range(0,len(bar_img[0]),50):
                try:
                    scaleNumb, units = getNumber(bar_img, exePath)
                    break
                except:
                    print("Failed - croping image bar")
                    bar_img = original_bar_img[::,i:i+100]
            print("Scale Text: " + scaleNumb + units)
            print("Drawing new scale...")
            drawScale(crop_img,scale,int(scaleNumb),units,file_path[x],exePath,position, file_path1[x])
    except TypeError:
        print("No Image Selected")
    print("Erasing temporary images...")
    shutil.rmtree('C:\\Temp')
    print("All done")
    input("Press Enter to exit...")
else:
     #Re-run the program with admin rights
     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
