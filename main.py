import easygui
import cv2
import pytesseract
from PIL import Image
from processImage import *

exePath = os.getcwd()

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
                scaleNumb, units = getNumber(bar_img, exePath)
                break
            except:
                print("Failed - croping image bar")
                bar_img = original_bar_img[::,i:i+100]
        print("Scale Text: " + scaleNumb + units)
        print("Drawing new scale...")
        drawScale(crop_img,scale,int(scaleNumb),units,path,exePath,position)
except TypeError:
    print("No Image Selected")

print("All done")
input("Press Enter to exit...")
