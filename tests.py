# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:46:45 2017

@author: joaor
"""

import os
import pytesseract
from PIL import Image, ImageEnhance
import cv2

exePath = os.getcwd()
tess_path = exePath + '\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tess_path
TESSDATA_PREFIX = os.path.dirname(tess_path)

file_path1 = r'C:\Users\joaor\Desktop\05_07_2017\15\5.tif'
file_path2 = r'C:\Users\joaor\Desktop\05_07_2017\15'


img = cv2.imread(file_path1)
img =  img[683:753,4:1024]
cv2.imwrite(file_path2 + "\\teste.tif", img)


#img3 = Image.open(file_path2 + "\\teste.tif")
#img4 = img3.resize((3060, 210), Image.ANTIALIAS)
#img4.save(file_path2 + "/th0.tif", dpi=(600,600))
#
#img = cv2.imread(file_path2 + "/th0.tif")
#img5 = img[1:200, 1:250]
#cv2.imwrite(file_path2 + "\\th1.tif", img5)
#
#img3 = Image.open(file_path2 + "\\th1.tif")
#img = img3.resize((600, 750), Image.ANTIALIAS)
#img.save(file_path2 + "/th1.tif", dpi=(600,600))


img = cv2.imread(file_path2 + "/teste.tif")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

y= [0, 10, 20, 30, 40, 50, 60, 70,80, 90, 100]
x = [69, 71, 73, 75, 77, 79, 81, 83, 85]

for i in x:
#    thresh = i
#    max_Value = 255
#    th, img1 = cv2.threshold(img, thresh, max_Value, cv2.THRESH_BINARY)



    img1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,i,3)
    u = str(i)
 
    cv2.imwrite(file_path2 + "\\thres" + u + ".tif", img1)
    print(u)
    scalenumb = pytesseract.image_to_string(Image.open(file_path2 + "\\thres" + u + ".tif"), lang='eng')
    print(scalenumb)

#img6 = Image.open(file_path1)
#enhancer = ImageEnhance.Sharpness(img6)
#
#
#
#for i in range(8):
#    factor = i / 4.0
#    enhancer.enhance(factor).show("Sharpness %f" % factor)

#scalenumb = pytesseract.image_to_string(Image.open(file_path2 + "/thres1.tif"))
#print(scalenumb)
#
#thresh = 100
#max_Value = 255
#th, imga = cv2.threshold(img , thresh, max_Value, cv2.THRESH_BINARY)
#
#cv2.imwrite(file_path2 + "/thres2.tif", imga)
#scalenumb = pytesseract.image_to_string(Image.open(file_path2 + "/thres2.tif"))
#print(scalenumb)
#
#factor = 6 / 4.0
#imga = Image.open(file_path2 + "/th1.tif")
#img6 = ImageEnhance.Sharpness(imga)
#img7 = img6.enhance(factor)
#img7.save(file_path2 + "/thres2_enhance.tif")
#
#
#img7 = cv2.imread(file_path2 + "/thres2_enhance.tif")
#thresh = 100
#max_Value = 255
#th, imga = cv2.threshold(img7 , thresh, max_Value, cv2.THRESH_BINARY)
#
#cv2.imwrite(file_path2 + "/thres2_enhance_thresh.tif", imga)
#scalenumb = pytesseract.image_to_string(Image.open(file_path2 + "/thres2.tif"))
#print(scalenumb)
