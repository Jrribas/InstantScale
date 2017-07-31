from tkinter import filedialog
from tkinter import Tk
import cv2
import pytesseract
from PIL import Image
import processImage as pI
import sys, ctypes
import os
import shutil
import getpass

#Tkinter parameters
root = Tk()
root.withdraw()
root.iconbitmap(default='icon.ico')

#Get *.exe path and username
exePath = os.getcwd()
user = getpass.getuser()

#Tesseract parameters
tess_path = exePath + '\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tess_path
TESSDATA_PREFIX = os.path.dirname(tess_path)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#Check if program is running with administrator priviligies and if not restarts with it
if is_admin():
    while True:
        #Asks to select images
        print("Selecting Images")
        files = filedialog.askopenfilenames(initialdir = "C:/Users/" + user + "/Desktop",title = "InstantScale - Please select the images to process", filetypes = [("Image files", "*.tif *.jpg *.png"), ("Tiff images", "*.tif"), ("Jpg images", "*.jpg"), ("Png images", "*.png")])
        file_path = list(files)

        if not file_path == []:

            #Aks to choose the location of the new scale
            position = None
            while position not in list(range(4)):
                try:
                    position =  int(input("Where do you want to place the scale? (Bottom Left - 0, Bottom Right - 1, Top Left - 2, Top Right - 3)"))
                except:
                    pass
            sizeOfScale = None
            while sizeOfScale not in list(range(1,11)):
                try:
                    sizeOfScale = int(input("Select scale size from 1 to 10: "))
                except:
                    pass
            #----------------------------------------------------
            #MAIN PART
            #----------------------------------------------------

            #Copies images to a temporary folde in C:\Temp and cleans weird characters in their names
            file_path1 = pI.cleanPathFiles(file_path)
            print("Looping Images...")

            #Loops through all images
            for x in range(len(file_path1)):

                print("-> Reading Image: " + file_path1[x][8::])
                img = cv2.imread(file_path1[x])

                try:
                    height, width, channels = img.shape
                except:
                    print("Image couldn't be loaded! Check name for special characters pls...")
                    continue

                crop_img, bar_img = pI.getBar(img)

                height1, width1, channels1 = bar_img.shape
                cv2.imwrite(exePath + "\\images\\HoldImages\\bar.tif", bar_img)

                img = Image.open(exePath + "\\images\\HoldImages\\bar.tif")
                img1 = img.resize((width1*3, height1*3), Image.ANTIALIAS)
                img1.save(exePath + "\\images\\HoldImages\\resize_im.tif", dpi=(600,600), quality = 100)

                bar_img_res = cv2.imread(exePath + "\\images\\HoldImages\\resize_im.tif")

                print("Geting scale bar size...")
                scale = len(pI.getScale(bar_img))

                print("Geting scale number...")

                scaleNumb, units = pI.getNumber(bar_img, bar_img_res, exePath)

                try:
                    print("Drawing new scale...")
                    pI.drawScale(crop_img,scale,int(scaleNumb),units,file_path[x],exePath,position, file_path1[x],sizeOfScale)
                except:
                    print("Couldn''t get the scale number... Continuing to the next images" )
                    continue

            shutil.rmtree('C:\\Temp')
            print("All done! Images saved on the folder, Images with new scale, where the original images are located.")
            input("Press Enter to restart...")

        else:
            print("No Image Selected")
            input("Press Enter to restart...")

else:
     #Re-run the program with admin rights
     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
