import cv2
import os
import pytesseract
from PIL import Image, ImageFont, ImageDraw
import re
import shutil

def getBar(img):
    height, width, channels = img.shape

    for i in reversed(range(len(img))):
        if img[i,3][0] > 254 and img[i,3][1] > 254 and img[i,3][2] > 254 and 'startRow' not in locals():
            startRow = i
        if img[i,3][0] < 250 and img[i,3][1] < 250 and img[i,3][2] < 250 and 'startRow' in locals():
            cropRow = i
            break
    crop_img = img[0:cropRow, 0::]
    bar_img = img[cropRow+1:startRow, 1:width]

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

def getNumber(bar_img,bar_img_res,exePath):
    path = 'images/HoldImages'

    bar_img = cv2.cvtColor(bar_img, cv2.COLOR_BGR2GRAY)


    for i in range(0, 100, 10):
        thresh = i
        max_Value = 255
        th, imga = cv2.threshold(bar_img, thresh, max_Value, cv2.THRESH_BINARY)

        os.chdir(exePath)

        if not os.path.exists(path):
            os.makedirs(path)

        cv2.imwrite(path + "/thres.tif", imga)
        scalenumb = pytesseract.image_to_string(Image.open(path + "/thres.tif"))

        findSize = re.compile(r'(?<!\.)(\d+)\s?(nm|mm|µm|um|pm)')
        mo = findSize.search(scalenumb)

        if mo is not None and mo.group(1) != '0':
            print(mo.group(1), mo.group(2))
            return mo.group(1), mo.group(2)

    bar_img_res = cv2.cvtColor(bar_img_res, cv2.COLOR_BGR2GRAY)

    original_bar_img = bar_img_res

    for j in range(0,len(bar_img_res[0]),100):


        x = [69, 71, 73, 75, 77, 79, 81, 83, 85]

        for w in x:
            bar_img_th = cv2.adaptiveThreshold(bar_img_res,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,w,4)
            os.chdir(exePath)

            if not os.path.exists(path):
                os.makedirs(path)

            cv2.imwrite(path + "\\thres.tif", bar_img_th)
            scalenumb = pytesseract.image_to_string(Image.open(path + "\\thres.tif"), lang='eng')

            findSize = re.compile(r'(?<!\.)(\d+)\s?(nm|mm|µm|um|pm)')
            mo = findSize.search(scalenumb)

            if mo is not None and mo.group(1) != '0':
                print(mo.group(1), mo.group(2))
                return mo.group(1), mo.group(2)

        print("Failed - croping image bar")
        bar_img_res = original_bar_img[1:200,j:j+250]

        cv2.imwrite(exePath + "\\images\\HoldImages\\resize_im1.tif", bar_img_res)
        temp = Image.open(exePath + "\\images\\HoldImages\\resize_im1.tif")

        temp = temp.resize((600, 750), Image.ANTIALIAS)

        temp.save(exePath + "\\images\\HoldImages\\resize_im1.tif", dpi=(600,600))
        bar_img_res = cv2.imread(exePath + "\\images\\HoldImages\\resize_im1.tif")
        bar_img_res = cv2.cvtColor(bar_img_res, cv2.COLOR_BGR2GRAY)


def cleanPathFiles(path):

    Cpath = [None] * len(path)

    if os.path.exists('C:\Temp'):
        shutil.rmtree('C:\\Temp')
        os.makedirs('C:\Temp')
    else:
        os.makedirs('C:\Temp')

    for x in path:
        x = x.replace('/', '\\')
        path1, file = os.path.split(x)
        os.system ('copy "%s" "%s"' % (x, 'C:\\Temp\\' + file))


    for x in range(len(path)):

        filename, fileExtension = os.path.splitext(os.path.basename(path[x]))

        intab = "êéèíìîáàãâõñúùóòôç?!ÇÓÒÚÙÑÕÔÂÃÁÀÎÍÌÉÉÊ"
        outtab = "eeeiiiaaaaonuuoooc__COOUUNOOAAAAIIIEEE"
        trantab = str.maketrans(intab, outtab)

        new_filename = filename.translate(trantab)

        Cpath[x] = 'C:\\Temp\\' + new_filename + fileExtension
        os.rename('C:\\Temp\\' + filename + fileExtension, Cpath[x])

    return Cpath

def drawScale(img,scale,scaleNumb,units,originalPath,exePath,position, Cpath):
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
        if 60 <= newScale <= 200:
            if val < 1:
                newScaleNumb = int(val * 1000)
                units = 'nm'
            elif val > 500:
                newScaleNumb = int(val / 1000)
                units = 'mm'
            else:
                newScaleNumb = val
                units = 'µm'
            break

    if position == 0:
        sD = [round(width*0.0235) , round(height*0.9636)-70, (round(width*0.0235) + newScale) + 20, round(height*0.9636)] # X0,Y0,X1,Y1
    elif position == 1:
        sD = [(round(width*0.9765) - newScale) - 20, round(height*0.9636)-70, round(width*0.9765), round(height*0.9636)] # X0,Y0,X1,Y1
    elif position == 2:
        sD = [round(width*0.0235) , round(height*0.0364), (round(width*0.0235) + newScale) + 20, round(height*0.0364) + 70] # X0,Y0,X1,Y1
    else:
        sD = [(round(width*0.9765) - newScale) - 20 , round(height*0.0364),round(width*0.9765), round(height*0.0364) + 70] # X0,Y0,X1,Y1


    os.chdir(exePath)
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
    if position == 0 or position == 2:
        textDimensions = [x + y for x, y in zip(sD, [0,0,-newScale +w,0])]
    else:
        textDimensions = [x + y for x, y in zip(sD, [+newScale-w,0,0,0])]


    if newScale > w:
        draw.rectangle(sD, fill="white", outline="white")
        draw.text(((((sD[2]-sD[0])/2) - w/2) + sD[0], sD[1] + 20), scaletext, font=font, fill='Black')
        draw.line([((sD[2]-sD[0])/2) - newScale/2 + sD[0], sD[1] + 15, sD[0] +  ((sD[2]-sD[0])/2) + newScale/2, sD[1] + 15], fill='Black', width=10)
    else:
        draw.rectangle(textDimensions, fill="white", outline="white")
        draw.text(((((textDimensions[2]-textDimensions[0])/2) - w/2) + textDimensions[0], textDimensions[1] + 20), scaletext, font=font, fill='Black')
        draw.line([((textDimensions[2]-textDimensions[0])/2) - newScale/2 + textDimensions[0], textDimensions[1] + 15, textDimensions[0] +  ((textDimensions[2]-textDimensions[0])/2) + newScale/2, textDimensions[1] + 15], fill='Black', width=10)


    del draw

    filename, fileExtension = os.path.splitext(os.path.basename(originalPath))
    dirName = os.path.dirname(originalPath)
    os.chdir(dirName)
    if not os.path.exists("images_with_new_scale"):
        os.makedirs("images_with_new_scale")
    os.chdir(dirName + "/images_with_new_scale")

    im.save(filename + '_scale' + fileExtension)
    print("ImageSaved with name: " + filename + '_scale' + fileExtension + "!")
