import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import Label
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
from tkinter import Spinbox
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import getpass #get username
import cv2
import pytesseract
import os
import processImage as pI



user = getpass.getuser()
#Get *.exe path and username
exePath = os.getcwd()
user = getpass.getuser()

#Tesseract parameters
tess_path = exePath + '\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tess_path
TESSDATA_PREFIX = os.path.dirname(tess_path)

################################################

NORM_FONT = ("Verdana", 10)
E = tk.E
W = tk.W
N = tk.N
S = tk.S

################################################

def popupmsg(msg):

    popup = tk.Tk()

    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.grid(row=1, column=1, padx=2, pady=2)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy())
    B1.grid(row=2, column=1, padx=2, pady=2)

    popup.grid_rowconfigure(0, weight=1)
    popup.grid_rowconfigure(3, weight=1)
    popup.grid_columnconfigure(0, weight=1)
    popup.grid_columnconfigure(2, weight=1)

    popup.mainloop()


################################################



class InstantScale(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Instant Scale")
        tk.Tk.iconbitmap(self, default="icon.ico")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(tk.Frame(self))
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_command(label="Open", command=lambda: popupmsg("Not supported just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Export Data", command=lambda: popupmsg("Not supported just yet!"))
        menubar.add_cascade(label="File", menu=filemenu)

        menubar = tk.Menu(tk.Frame(self))
        file_menu = tk.Menu(menubar, tearoff=0)

        file_menu.add_command(label='Import Image', command=lambda: self.selectImages())
        file_menu.add_command(label='Save As', command=lambda: self.saveFile())
        file_menu.add_command(label='Exit', command=exit)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='version')
        menubar.add_cascade(label='File', menu=file_menu)
        menubar.add_cascade(label='About', menu=help_menu)

        tk.Tk.config(self, menu=menubar)

        img1 = ImageTk.PhotoImage(Image.open("images/file_import_image.png"))
        img2 = ImageTk.PhotoImage(Image.open("images/file_import_image2.png"))

        self.panel = ttk.Label(self, image=img1)
        self.panel.image = img1
        self.panel2 = ttk.Label(self, image=img2)
        self.panel2.image = img2
        self.panel.grid(row=1, column=1, rowspan=18, padx=10, pady=10)
        self.panel2.grid(row=1, column=2, rowspan=18, padx=10, pady=10)

        self.l1 = Label(self, text="Original Image", padx=5, pady=5)
        self.l1.grid(row=19, column=1)
        self.l2 = Label(self, text="Preview", padx=5, pady=5)
        self.l2.grid(row=19, column=2)

        ##SETIINGS BOX
        self.b1 = ttk.Button(self, text="ReadScale", command=self.readScale)
        self.b1.grid(row=1, column=3, columnspan=2, pady=5)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        self.bar = Progressbar(self, length=200, style='black.Horizontal.TProgressbar')
        self.bar['value'] = 0
        self.bar.grid(row=2, column=3, columnspan=2)

        self.l3 = Label(self, text="Value")
        self.l3.grid(row=3, column=3)

        self.l3 = Label(self, text="Unit (mm, um, nm)")
        self.l3.grid(row=3, column=4)

        self.e1 = ttk.Entry(self, state='disabled')
        self.e1.grid(row=4, column=3, padx=5)

        self.e2 = ttk.Entry(self, state='disabled')
        self.e2.grid(row=4, column=4, padx=5)

        self.l4 = Label(self, text="Scale Size (Pixels)")
        self.l4.grid(row=5, column=3, columnspan=2)

        self.e3 = ttk.Entry(self, state='disabled')
        self.e3.grid(row=6, column=3, columnspan=2)

        self.l5 = Label(self, text="White Bar (%)")
        self.l5.grid(row=7, column=3, columnspan=2)

        self.e4 = ttk.Entry(self, state='disabled')
        self.e4.grid(row=8, column=3, columnspan=2)

        self.l6 = Label(self, text="Target Value")
        self.l6.grid(row=9, column=3)

        self.l7 = Label(self, text="Target Unit")
        self.l7.grid(row=9, column=4)

        self.e5 = ttk.Entry(self, state='disabled')
        self.e5.grid(row=10, column=3, padx=5)

        self.e6 = ttk.Entry(self, state='disabled')
        self.e6.grid(row=10, column=4, padx=5)

        self.l8 = Label(self, text="Scale Position")
        self.l8.grid(row=11, column=3, columnspan=2)

        self.c1 = Combobox(self)
        self.c1['values'] = ("Top Left", "Top Right", "Bottom Left", "Bottom Right")
        self.c1.current(1)  # set the selected item
        self.c1.grid(row=12, column=3, columnspan=2)

        self.l9 = Label(self, text="Size of Scale")
        self.l9.grid(row=13, column=3, columnspan=2)

        self.spin = Spinbox(self, from_=1, to=20, width=5)
        self.spin.grid(column=3, row=14, columnspan=2)

        self.l10 = Label(self, text="Background Color")
        self.l10.grid(row=15, column=3, columnspan=1)

        self.e7 = ttk.Entry(self)
        self.e7.grid(row=16, column=3, columnspan=1)

        self.b7 = ttk.Button(self, text="Pick", command=self.colour)
        self.b7.grid(row=16, column=4)

        self.l11 = Label(self, text="Font Color")
        self.l11.grid(row=17, column=3, columnspan=1)

        self.e8 = ttk.Entry(self)
        self.e8.grid(row=18, column=3, columnspan=1)

        self.b8 = ttk.Button(self, text="Pick", command=self.colour)
        self.b8.grid(row=18, column=4)

        self.b2 = ttk.Button(self, text="Preview", command=self.preview)
        self.b2.grid(row=19, column=3, columnspan=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(6, weight=1)

    def colour(self):

        color = askcolor()
        print(color)

    def selectImages(self):
        print("Selecting Images")
        self.files = filedialog.askopenfilenames(initialdir="C:/Users/" + user + "/Desktop",
                                            title="InstantScale - Please select the images to process",
                                            filetypes=[("Image files", "*.tif *.jpg *.png"),
                                                       ("Tiff images", "*.tif"),
                                                       ("Jpg images", "*.jpg"),
                                                       ("Png images", "*.png")])

        img = Image.open(self.files[0])
        img2 = img.resize((500, 500), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(img2)
        self.panel.configure(image=img2)
        self.panel.image = img2

    def readScale(self):
        self.bar['value'] = 0
        self.update_idletasks()
        img = cv2.imread(self.files[0])
        height, width, channels = img.shape
        self.bar['value'] = 25
        self.update_idletasks()

        #GET BAR
        self.crop_img, self.bar_img, barSize = pI.getBar(img)
        print('bar Size: ' + str(barSize))
        barSizeRound = round(barSize)
        self.bar['value'] = 50
        self.update_idletasks()
        self.e4.configure(state='normal')
        self.e4.insert(tk.END,  barSizeRound)
        self.e4.configure(state='disabled')

        #things
        
        height1, width1, channels1 = self.bar_img.shape
        cv2.imwrite(exePath + "\\images\\HoldImages\\bar.tif", self.bar_img)
        
        img = Image.open(exePath + "\\images\\HoldImages\\bar.tif")
        img1 = img.resize((width1*3, height1*3), Image.ANTIALIAS)
        img1.save(exePath + "\\images\\HoldImages\\resize_im.tif", dpi=(600, 600), quality=100)

        self.bar_img_res = cv2.imread(exePath + "\\images\\HoldImages\\resize_im.tif")

        #READ SCALE

        self.scale = len(pI.getScale(self.bar_img))
        print('scale: ' + str(self.scale))
        self.bar['value'] = 75
        self.update_idletasks()
        self.e3.configure(state='normal')
        self.e3.insert(tk.END, self.scale)
        self.e3.configure(state='disabled')
        # GET SCALE NUMBER and unit
        self.scaleNumb, self.units = pI.getNumber(self.bar_img, self.bar_img_res, exePath)
        self.e1.configure(state='normal')
        self.e1.insert(tk.END, self.scaleNumb)
        self.e1.configure(state='disabled')
        self.e2.configure(state='normal')
        self.e2.insert(tk.END, self.units)
        self.e2.configure(state='disabled')
        self.bar['value'] = 100
        self.update_idletasks()
    
    def preview(self):
        #Bottom Left - 0, Bottom Right - 1, Top Left - 2, Top Right - 3)"
        #"Top Left", "Top Right", "Bottom Left", "Bottom Right"
        print("c1 get value: " + self.c1.get())
        if self.c1.get() == "Top Left":
            self.position = 2
        elif self.c1.get() == "Top Right":
            self.position = 3
        elif self.c1.get() == "Bottom Left":
            self.position = 0            
        elif self.c1.get() == "Bottom Right":
            self.position = 1
            
        self.sizeOfScale = int(self.spin.get())
        
        self.imageReturn= pI.drawScale(self.crop_img,self.scale,int(self.scaleNumb),self.units,self.files[0],exePath,self.position, exePath,self.sizeOfScale)
        self.finalImage = self.imageReturn
        img3 = self.finalImage.resize((500, 500), Image.ANTIALIAS)

        img3 = ImageTk.PhotoImage(img3)
        self.panel2.configure(image=img3)
        self.panel2.image = img3
    
    def saveFile(self):
        file = filedialog.asksaveasfile(mode='wb', defaultextension=".png", filetypes=(("PNG file", "*.png"),("All Files", "*.*") ))
        if file:
            print(self.imageReturn.mode)
            self.imageReturn.save(file)
        
if __name__ == "__main__":

    app = InstantScale()
    app.geometry("1360x700")
    app.mainloop()

