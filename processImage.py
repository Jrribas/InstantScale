import os
import pytesseract
from re import compile
from cv2 import imread, imwrite, cvtColor, threshold, COLOR_BGR2GRAY, THRESH_BINARY, ADAPTIVE_THRESH_GAUSSIAN_C
from cv2 import adaptiveThreshold
from PIL import Image, ImageFont, ImageDraw
import shutil


def getBar(img):
    height, width, channels = img.shape
    startRow = None
    cropRow = None

    # Look pixel by pixel for the white bar

    try:
        for i in reversed(range(len(img))):
            if img[i, 3][0] >= 254 and img[i, 3][1] >= 254 and img[i, 3][2] >= 254 and startRow is None:
                startRow = i
            if img[i, 3][0] <= 250 and img[i, 3][1] <= 250 and img[i, 3][2] <= 250 and startRow is not None:
                cropRow = i
                break

        # Cropping image
        crop_img = img[0:cropRow, 0::]
        bar_img = img[cropRow + 1:startRow, 1:width]
        barSize = (len(img) - cropRow) * 100 / len(img)+1

    except TypeError:
        return 0, 0, 0

    return crop_img, bar_img, barSize


def cropImage(img, cropPercentage, position):
    # Cropping image function if manual is selected

    height, width, channels = img.shape

    if position == "Bottom":
        cropRow = int((height * (100-cropPercentage)) / 100)
        crop_image = img[0:cropRow, 0::]
    else:
        cropRow = int((height * (100-cropPercentage)) / 100)
        crop_image = img[height - cropRow::, 0::]

    return crop_image


def getScale(bar_img):
    # Function that count the scale bar pixels

    k = []
    for i in range(len(bar_img)):
        for j in range(len(bar_img[i])):
            if bar_img[i, j][0] < 50 and bar_img[i, j][1] < 50 and bar_img[i, j][2] < 50:
                k.append([i, j])
            else:
                if len(k) > 30:
                    scale = k
                    return scale
                k = []


def getNumber(bar_img, bar_img_res, exePath):

    units = None

    # Get path from copy of original image
    path = exePath + "\\images\\"

    # Transform image in gray "colour"
    bar_img = cvtColor(bar_img, COLOR_BGR2GRAY)

    units_dict = {"mm": 0, "um": 1, "nm": 2}

    for i in range(0, 100, 10):

        # Loops through thresh values in order to help tesseract read the scale number
        thresh = i
        max_Value = 255
        th, imga = threshold(bar_img, thresh, max_Value, THRESH_BINARY)

        os.chdir(exePath)

        if not os.path.exists(path):
            os.makedirs(path)

        imwrite(path + "/thres.tif", imga)

        # Tesseract
        scalenumb = pytesseract.image_to_string(Image.open(path + "/thres.tif"))

        # Find scale unit
        findSize = compile(r'(?<!\.)(\d+)\s?(nm|mm|µm|um|pm)')
        mo = findSize.search(scalenumb)

        if mo is not None and mo.group(1) != '0 ':

            return mo.group(1), units_dict[mo.group(2)]

    # If not scale number or unit was found till now an improved threshold is done
    bar_img_res = cvtColor(bar_img_res, COLOR_BGR2GRAY)

    original_bar_img = bar_img_res

    for j in range(0, len(bar_img_res[0]), 100):

        x = [69, 71, 73, 75, 77, 79, 81, 83, 85]

        for w in x:
            bar_img_th = adaptiveThreshold(bar_img_res, 255, ADAPTIVE_THRESH_GAUSSIAN_C,
                                           THRESH_BINARY, w, 4)
            os.chdir(exePath)

            if not os.path.exists(path):
                os.makedirs(path)

            imwrite(path + "\\thres.tif", bar_img_th)
            scalenumb = pytesseract.image_to_string(Image.open(path + "\\thres.tif"), lang='eng')

            findSize = compile(r'(?<!\.)(\d+)\s?(nm|mm|µm|um|pm)')
            mo = findSize.search(scalenumb)

            if mo is not None and mo.group(1) != '0 ':
                return mo.group(1), units_dict[mo.group(2)]

        bar_img_res = original_bar_img[1:200, j:j+250]

        imwrite(path + "HoldImages\\resize_im1.tif", bar_img_res)
        temp = Image.open(path + "HoldImages\\resize_im1.tif")

        temp = temp.resize((600, 750), Image.ANTIALIAS)

        temp.save(path + "HoldImages\\resize_im1.tif", dpi=(600, 600))
        bar_img_res = imread(path + "HoldImages\\resize_im1.tif")
        bar_img_res = cvtColor(bar_img_res, COLOR_BGR2GRAY)


def cleanPathFiles(path, exePath):

    Cpath = [""] * len(path)

    # Create temp directory

    exePath = exePath + "\\images\\"

    # Copy images to a more easy directory
    for x in path:
        x = x.replace('/', '\\')
        path1, file = os.path.split(x)
        shutil.copyfile(x, exePath + file)

    # Clean file name of strange characters
    for x in range(len(path)):

        filename, fileExtension = os.path.splitext(os.path.basename(path[x]))

        intab = "êéèíìîáàãâõñúùóòôç?!ÇÓÒÚÙÑÕÔÂÃÁÀÎÍÌÉÉÊ"
        outtab = "eeeiiiaaaaonuuoooc__COOUUNOOAAAAIIIEEE"
        trantab = str.maketrans(intab, outtab)

        new_filename = filename.translate(trantab)

        Cpath[x] = exePath + new_filename + fileExtension

        os.rename(exePath + filename + fileExtension, Cpath[x])

    return Cpath


def drawScale(img, scale, scaleNumb, units, exePath, position, sizeOfScale,
              fontColor=(0, 0, 0), bgColor=(255, 255, 255), targetValue=0, targetUnits=''):
    
    # Draw the new scale in the image
    height, width, channels = img.shape
    minpixels = 0.08 * width
    maxpixels = 0.20 * width
    newScale = None
    newScaleNumb = None

    if targetUnits != "":
        conv_dict = {"mmµm": 1000, "mmnm": 1000000, "µmmm": 0.001, "µmnm": 1000, "nmmm": 0.000001, "nmµm": 0.001,
                     "µmµm": 1, "nmnm": 1, "mmmm": 1}

        key = units + targetUnits
        check = (((1 / conv_dict[key]) * scale) / scaleNumb)

        if conv_dict[key] < 1 or (conv_dict[key] == 1 and scaleNumb < targetValue):
            if check * targetValue > 0.8 * width:
                message = "max"
                return message + " value is : " + str(round((0.8*width)/scale)-1) + " " + units
        elif conv_dict[key] > 1 or (conv_dict[key] == 1 and scaleNumb > targetValue):
            if check * targetValue < 30:
                message = "min"
                return message + " value is : " + str(round(30/check)+1) + " " + targetUnits

        newScaleNumb = targetValue
        units = targetUnits
        newScale = check * targetValue

    else:
        val = [500, 200, 100, 50, 20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
        unit_dict = {"mm": "µm", "µm": "nm"}
        conv = 1

        if scaleNumb == 1 and scale > maxpixels and units == "nm":
            newScale = scale
            newScaleNumb = scaleNumb
        else:
            for val in val:
                if minpixels < val * scale < maxpixels:
                    if val < 1:
                        conv = 1000
                        units = unit_dict[units]
                        break
                    else:
                        break

            newScale = round(val * scale)
            newScaleNumb = int(val * conv)

    os.chdir(exePath)
    path = "images/cropImages"
    if not os.path.exists(path):
        os.makedirs(path)
    imwrite(path + "/crop_rect.png", img)

    im = Image.open(path + "/crop_rect.png")
    draw = ImageDraw.Draw(im)

    fontsize = 13 * sizeOfScale
    font = ImageFont.truetype("arial.ttf", fontsize)
    scaletext = str(newScaleNumb) + ' ' + units

    # Draw scale in the cropped image
    w, h = draw.textsize(scaletext, font)

    if position == 0:
        sD = [round(width * 0.0235), round(height * 0.9636) - (20 * sizeOfScale / 3 + 3 * sizeOfScale + h),
              (round(width * 0.0235) + newScale) + (20 * sizeOfScale / 3), round(height * 0.9636)]  # X0,Y0,X1,Y1
    elif position == 1:
        sD = [(round(width * 0.9765) - newScale) - (20 * sizeOfScale / 3),
              round(height * 0.9636) - (20 * sizeOfScale / 3 + 3 * sizeOfScale + h), round(width * 0.9765),
              round(height * 0.9636)]  # X0,Y0,X1,Y1
    elif position == 2:
        sD = [round(width * 0.0235), round(height * 0.0364),
              (round(width * 0.0235) + newScale) + (20 * sizeOfScale / 3),
              round(height * 0.0364) + (20 * sizeOfScale / 3 + 3 * sizeOfScale + h)]  # X0,Y0,X1,Y1
    else:
        # print(str(round(width * 0.0235)) + "\n")
        # print(str(round(height * 0.9636) - (20 * sizeOfScale / 3 + 3 * sizeOfScale + h)) + "\n")
        # print(str((round(width * 0.0235) + newScale) + (20 * sizeOfScale / 3)))
        # print(width, newScale, sizeOfScale)
        # print(str(round(height * 0.9636)) + "\n")

        sD = [(round(width * 0.9765) - newScale) - (20 * sizeOfScale / 3), round(height * 0.0364),
              round(width * 0.9765),
              round(height * 0.0364) + (20 * sizeOfScale / 3 + 3 * sizeOfScale + h)]  # X0,Y0,X1,Y1

    if position == 0 or position == 2:
        textDimensions = [x + y for x, y in zip(sD, [0, 0, -newScale + w, 0])]
    else:
        textDimensions = [x + y for x, y in zip(sD, [+newScale-w, 0, 0, 0])]

    if newScale > w:
        draw.rectangle(sD, fill=bgColor, outline=bgColor)
        draw.text(((((sD[2]-sD[0])/2) - w/2) + sD[0], sD[1] + 7*sizeOfScale), scaletext, font=font, fill=fontColor)
        draw.line([((sD[2] - sD[0]) / 2) - newScale / 2 + sD[0], sD[1] + 5 * sizeOfScale,
                   sD[0] + ((sD[2] - sD[0]) / 2) + newScale / 2, sD[1] + 5 * sizeOfScale], fill=fontColor,
                  width=3 * sizeOfScale)
    else:
        draw.rectangle(textDimensions, fill=bgColor, outline=bgColor)
        draw.text(((((textDimensions[2] - textDimensions[0]) / 2) - w / 2) + textDimensions[0],
                   textDimensions[1] + 7 * sizeOfScale), scaletext, font=font, fill=fontColor)
        draw.line([((textDimensions[2] - textDimensions[0]) / 2) - newScale / 2 + textDimensions[0],
                   textDimensions[1] + 5 * sizeOfScale,
                   textDimensions[0] + ((textDimensions[2] - textDimensions[0]) / 2) + newScale / 2,
                   textDimensions[1] + 5 * sizeOfScale], fill=fontColor, width=3 * sizeOfScale)

    del draw

    return im
