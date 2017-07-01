import cv2
import os
import pytesseract
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import re


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

def getNumber(bar_img):
    path = 'images/HoldImages'
    kernel = np.ones((1, 1), np.uint8)
    bar_img = cv2.dilate(bar_img, kernel, iterations=1)
    bar_img = cv2.erode(bar_img, kernel, iterations=1)

    for i in range(0, 100, 10):
        thresh = i
        max_Value = 255

        th, imga = cv2.threshold(bar_img , thresh, max_Value, cv2.THRESH_BINARY)

        if not os.path.exists(path):
            os.makedirs(path)
        cv2.imwrite(path + "/thres.png", imga)
        scalenumb = pytesseract.image_to_string(Image.open(path + "/thres.png"))
        print(scalenumb)
        findSize = re.compile(r'(?<!\.)(\d+)\s?(nm|mm|µm|um|pm)')
        mo = findSize.search(scalenumb)

        if mo is not None and mo.group(1) != '0':
            #print(mo.group(1), mo.group(2))
            return mo.group(1), mo.group(2)



def cleanPathFiles(path):
    for x in range(len(path)):
        intab = "êéèíìîáàãâõñúùóòôç?!ÇÓÒÚÙÑÕÔÂÃÁÀÎÍÌÉÉÊ"
        outtab = "eeeiiiaaaaonuuoooc__COOUUNOOAAAAIIIEEE"
        trantab = str.maketrans(intab, outtab)

        newfile_path = path[x].translate(trantab)
        os.rename(path[x], newfile_path)
        path[x] = newfile_path
        return path

def drawScale(img,scale,scaleNumb,units,originalPath):
    # Desenhar a escala nova
    height, width, channels = img.shape
    values = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    if units == 'nm':
        scaleNumb *= 0.001
    elif units == 'mm':
        scaleNumb *= 1000
    else:
        units = 'µm'

    for val in values:
        newScale = round((val * scale) / scaleNumb)
        #print("newScale: " + str(newScale))
        if 40 <= newScale <= 200:
            if val < 1:
                newScaleNumb = int(val * 1000)
                units = 'nm'
            elif val > 500:
                newScaleNumb = int(val / 1000)
                units = 'mm'
            else:
                newScaleNumb = val
            break

    squareDimensions = [(round(width*0.9765) - newScale) - 20 , round(height*0.0364),round(width*0.9765), round(height*0.0364) + 70] # X0,Y0,X1,Y1
    print(squareDimensions)

    path= "images/cropImages"
    if not os.path.exists(path):
        os.makedirs(path)
    cv2.imwrite(path + "/crop_rect.png", img)

    im = Image.open(path + "/crop_rect.png")
    draw = ImageDraw.Draw(im)

    fontsize = 40
    font = ImageFont.truetype("arial.ttf", fontsize)
    scaletext = str(newScaleNumb) + ' ' + units

    w, h = draw.textsize(scaletext, font)

    textDimensions = [x + y for x, y in zip(squareDimensions, [+newScale-w,0,0,0])]
    if newScale > w:
        draw.rectangle(squareDimensions, fill="white", outline="white")
        draw.text(((((squareDimensions[2]-squareDimensions[0])/2) - w/2) + squareDimensions[0], squareDimensions[1] + 20), scaletext, font=font, fill='Black')
        draw.line([((squareDimensions[2]-squareDimensions[0])/2) - newScale/2 + squareDimensions[0], squareDimensions[1] + 15, squareDimensions[0] +  ((squareDimensions[2]-squareDimensions[0])/2) + newScale/2, squareDimensions[1] + 15], fill='Black', width=10)
    else:
        draw.rectangle(textDimensions, fill="white", outline="white")
        draw.text(((((textDimensions[2]-textDimensions[0])/2) - w/2) + textDimensions[0], textDimensions[1] + 20), scaletext, font=font, fill='Black')
        draw.line([((textDimensions[2]-textDimensions[0])/2) - newScale/2 + textDimensions[0], textDimensions[1] + 15, textDimensions[0] +  ((textDimensions[2]-textDimensions[0])/2) + newScale/2, textDimensions[1] + 15], fill='Black', width=10)
    #lineDimensions = [x + y for x, y in zip(squareDimensions, [10,15,-10,-55])]


    del draw
    # print(path[:len(path)-4] + '_scale' + path[len(path)-4:])
    filename, fileExtension = os.path.splitext(os.path.basename(originalPath))
    dirName = os.path.dirname(originalPath)
    os.chdir(dirName)
    if not os.path.exists("images_with_new_scale"):
        os.makedirs("images_with_new_scale")
    os.chdir(dirName + "/images_with_new_scale")
    print(fileExtension)
    im.save(filename + '_scale' + fileExtension)
    print("ImageSaved")
    # cv2.imwrite(path[:len(path)-4] + '_scale' + path[len(path)-4:], im)
