import cv2
import os
#import pytesseract


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

    def getNumber(TesseractPath, img):
        pytesseract.pytesseract.tesseract_cmd = TesseractPath + "\\Tesseract.exe"
        TESSDATA_PREFIX = TesseractPath

    def cleanPathFiles(path):
        for x in range(len(path)):
            intab = "êéèíìîáàãâõñúùóòôç?!ÇÓÒÚÙÑÕÔÂÃÁÀÎÍÌÉÉÊ"
            outtab = "eeeiiiaaaaonuuoooc__COOUUNOOAAAAIIIEEE"
            trantab = str.maketrans(intab, outtab)

            newfile_path = path[x].translate(trantab)
            os.rename(path[x], newfile_path)
            path[x] = newfile_path
            return path
