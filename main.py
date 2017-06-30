import easygui
import processImage
import cv2

pi = processImage.ProcessImage

file_path = easygui.fileopenbox("Please select the images to process", "Instantscale", filetypes= "*.tif", multiple=True)
file_path = pi.cleanPathFiles(file_path)
print(file_path)



for path in file_path:
    print(path)
    img = cv2.imread(path)
    height, width, channels = img.shape
    crop_img,bar_img = pi.getBar(img)
    scale = pi.getScale(bar_img)
    scaleSize = scale[-1][1]-scale[0][1]
    print(scaleSize)
