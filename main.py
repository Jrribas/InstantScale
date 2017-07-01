import easygui
import cv2
import pytesseract

from processImage import *

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\Tesseract.exe"
TESSDATA_PREFIX = "C:\\Program Files (x86)\\Tesseract-OCR"

print("Selecting Images")
file_path = easygui.fileopenbox("Please select the images to process", "Instantscale", filetypes= "*.tif", multiple=True)
print('Cleaning File Types')
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
    scaleNumb, units = getNumber(bar_img)
    print("Scale Text: " + scaleNumb + units)
    print("Drawing new scale...")
    drawScale(crop_img,scale,int(scaleNumb),units,path)


######BUGS######

#ele cria pasta iamgens dentro de images_with_new_scale
#imagem 5.tif
