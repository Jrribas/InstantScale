import cv2
import os
import pytesseract
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import re

class ProcessImage:
    def getBar(img):
        for i in reversed(range(len(img))):
            if img[i,3][0] > 254 and img[i,3][1] > 254 and img[i,3][2] > 254 and 'startRow' not in locals():
                startRow = i
            if img[i,3][0] < 250 and img[i,3][1] < 250 and img[i,3][2] < 250 and 'startRow' in locals():
                cropRow = i
                break
        crop_img = img[0:cropRow, 0::]
        bar_img = img[cropRow+1:startRow, 0::]
        return crop_img,bar_img

    def getScale(bar_img):
        scale = []
        k = []
        for i in range(len(bar_img)):
            for j in range(len(bar_img[i])):
                if bar_img[i,j][0] < 50 and bar_img[i,j][1] < 50 and bar_img[i,j][2] < 50:
                    k.append([i,j])
                else:
                    if len(k) > 30:
                        scale = k
                        return scale
                    k = []

    def getNumber(TesseractPath, bar_img):
        pytesseract.pytesseract.tesseract_cmd = TesseractPath + "\\Tesseract.exe"
        TESSDATA_PREFIX = TesseractPath
        path = 'images/threshHoldImages'
        for i in range(0, 100, 10):
            thresh = i
            max_Value = 255
            th, imga = cv2.threshold(bar_img, thresh, max_Value, cv2.THRESH_BINARY)
            #lol = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            #cv2.imshow("thresh test",imga)
            cv2.waitKey(0)
            if not os.path.exists(path):
                os.makedirs(path)
            cv2.imwrite(path + "/thres.png", imga)
            scalenumb = pytesseract.image_to_string(Image.open(path + "/thres.png"))
            print(scalenumb)
            findSize = re.compile(r'(?<!\.)(\d+)\s?(nm|mm|µm|um)')
            mo = findSize.search(scalenumb)

            if mo is not None:
                #print(mo.group(1), mo.group(2))
                return mo.group(1), mo.group(2)

        bar_img = cv2.cvtColor(bar_img, cv2.COLOR_BGR2GRAY)
        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        bar_img = cv2.dilate(bar_img, kernel, iterations=1)
        bar_img = cv2.erode(bar_img, kernel, iterations=1)
        # Write the image after apply opencv to do some ...
        path = 'images/threshHoldImages'
        if not os.path.exists(path):
            os.makedirs(path)
        cv2.imwrite("images/threshHoldImages/thres.png", bar_img)
        # Recognize text with tesseract for python
        scalenumb = pytesseract.image_to_string(Image.open("images/threshHoldImages/thres.png"))
        scalenumb = scalenumb.split()

        units = scalenumb[1]
        scalenumb = int(scalenumb[0])

        poss_units = ['nm', 'um', 'mm']
        real_units = ['nm', 'µm', 'mm']

        units = real_units[poss_units.index(units)]
        return scalenumb,units

    def cleanPathFiles(path):
        for x in range(len(path)):
            intab = "êéèíìîáàãâõñúùóòôç?!ÇÓÒÚÙÑÕÔÂÃÁÀÎÍÌÉÉÊ"
            outtab = "eeeiiiaaaaonuuoooc__COOUUNOOAAAAIIIEEE"
            trantab = str.maketrans(intab, outtab)

            newfile_path = path[x].translate(trantab)
            os.rename(path[x], newfile_path)
            path[x] = newfile_path
            return path

    def drawScale(img):
        pass
