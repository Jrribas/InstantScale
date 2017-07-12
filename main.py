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

Tk().withdraw()
exePath = os.getcwd()
user = getpass.getuser()
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
        #----------------------------------------------------
        #MAIN PART
        #----------------------------------------------------
        
        #Copies images to a temporary folde in C:\Temp and cleans weird characters in their names
        file_path1 = pI.cleanPathFiles(file_path)
        print("Looping Images...")
        
        #Loops through all images 
        for x in range(len(file_path1)):
            
            
            print("Reading Image...")
            img = cv2.imread(file_path1[x])
            height, width, channels = img.shape

            
            crop_img, bar_img = pI.getBar(img)
            print("Geting scale bar size...")
            scale = len(pI.getScale(bar_img))

            print("Geting scale number...")
            original_bar_img = bar_img
            
            for i in range(0,len(bar_img[0]),50):
                try:
                    scaleNumb, units = pI.getNumber(bar_img, exePath)
                    break
                except:
                    print("Failed - croping image bar")
                    bar_img = original_bar_img[::,i:i+100]
                    
            print("Drawing new scale...")
            pI.drawScale(crop_img,scale,int(scaleNumb),units,file_path[x],exePath,position, file_path1[x])
            
        shutil.rmtree('C:\\Temp')
        print("All done! Images saved on the folder, Images with new scale, where the original images are located.")
        input("Press Enter to exit...")
        
    else:
        print("No Image Selected")
        input("Press Enter to exit...")
    
else:
     #Re-run the program with admin rights
     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
