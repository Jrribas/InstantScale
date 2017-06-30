import easygui
import processImage
import cv2

pi = processImage.ProcessImage

print("Selecting Images")
file_path = easygui.fileopenbox("Please select the images to process", "Instantscale", filetypes= "*.tif", multiple=True)
print('Cleaning File Types')
file_path = pi.cleanPathFiles(file_path)

print("Looping Images...")
for path in file_path:
    print("Read Image...")
    img = cv2.imread(path)
    height, width, channels = img.shape
    print("Crop Image...")
    crop_img,bar_img = pi.getBar(img)
    print("Get scale bar size...")
    scale = len(pi.getScale(bar_img))
    print("scale: ", str(scale))
    print("Get scale number...")
    scaleNumb, units = pi.getNumber("C:\\Program Files (x86)\\Tesseract-OCR",bar_img)
    print("Scale Text: " + scaleNumb + units)
