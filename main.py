import easygui
import cv2
import pytesseract
from processImage import *


# Select Tesseract.exe path
# file_path = easygui.fileopenbox("Please select the Tesseract.exe file", "Instantscale", filetypes= "*.exe")

# pytesseract.pytesseract.tesseract_cmd = file_path
# TESSDATA_PREFIX = file_path[:len(file_path)-14]


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\Tesseract.exe"
TESSDATA_PREFIX = "C:\\Program Files (x86)\\Tesseract-OCR"

f = open( 'TesseractPath.py', 'w' )
f.write( 'path' )
f.close()


print("Selecting Images")
file_path = easygui.fileopenbox("Please select the images to process", "Instantscale", filetypes= "*.tif", multiple=True)
print('Cleaning File Types')

position = None
while position not in list(range(4)):
    try:
        position =  int(input("Where do you want to place the scale? (Bottom Left - 0, Bottom Right - 1, Top Left - 2, Top Right - 3)"))
    except:
        pass

try:
    file_path = cleanPathFiles(file_path)
    print("Looping Images...")
    for path in file_path:
        print("Read Image...")
        img = cv2.imread(path)
        height, width, channels = img.shape
        print("Crop Image...")
        crop_img,bar_img = getBar(img)
        print("Get scale bar size...")
        scale = len(getScale(bar_img))
        print("scale: ", str(scale))
        print("Get scale number...")
        original_bar_img = bar_img
        for i in range(0,len(bar_img[0]),50):
            #print(i)
            #cv2.imshow('image',bar_img)
            #cv2.waitKey(0)
            try:
                scaleNumb, units = getNumber(bar_img)
                break
            except:
                bar_img = original_bar_img[::,i:i+100]
        print("Scale Text: " + scaleNumb + units)
        print("Drawing new scale...")
        drawScale(crop_img,scale,int(scaleNumb),units,path,position)
except TypeError:
    print("No Image Selected")
