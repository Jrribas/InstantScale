# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 16:49:51 2019

@author: Farinha
"""
import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import Label
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
from tkinter import Spinbox
from tkinter import ttk
from PIL import Image, ImageTk
import getpass #get username
import cv2
import processImage as pI

user = getpass.getuser()
S = tk.S


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.frame = tk.Frame(self.parent)  
        self.frame.pack(fill=tk.BOTH,expand = 1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(21, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(6, weight=1)
        
        #self.frame.grid(sticky=tk.N+tk.E+tk.W+tk.S)
        
        # IMAGE BOX
        img1 = ImageTk.PhotoImage(Image.open("images/file_import_image.png"))
        img2 = ImageTk.PhotoImage(Image.open("images/file_import_image2.png"))
        
        panel = tk.Label(self, image=img1)
        panel.image = img1
        panel2 = tk.Label(self, image=img2)
        panel2.image = img2

        panel.grid(row=1, column=1, rowspan=18, padx=10, pady=10)
        panel2.grid(row=1, column=2, rowspan=18, padx=10, pady=10)
        
        l1 = Label(self.frame, text="Original Image",  padx=5, pady=5)
        l1.grid(row=19, column=1)
        l2 = Label(self.frame, text="Preview",  padx=5, pady=5)
        l2.grid(row=19, column=2)
        
        # SETTINGS BOX

        b1 = tk.Button(self.frame, text="ReadScale", command=self.readScale)
        b1.grid(row=1, column=3, columnspan=2, pady=5)
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        bar = Progressbar(self.frame, length=200, style='black.Horizontal.TProgressbar')
        bar['value'] = 0
        bar.grid(row=2, column=3, columnspan=2)
        
        l3 = Label(self.frame, text="Value")
        l3.grid(row=3, column=3)
        
        l3 = Label(self.frame, text="Unit (mm, um, nm)")
        l3.grid(row=3, column=4)
        
        e1 = tk.Entry(self.frame, state='disabled')
        e1.grid(row=4, column=3, padx=5)
        
        e2 = tk.Entry(self.frame, state='disabled')
        e2.grid(row=4, column=4, padx=5)
        
        l4 = Label(self.frame, text="Scale Size (Pixels)")
        l4.grid(row=5, column=3, columnspan=2)
        
        e3 = tk.Entry(self.frame, state='disabled')
        e3.grid(row=6, column=3, columnspan=2)
        
        l5 = Label(self.frame, text="White Bar (%)")
        l5.grid(row=7, column=3, columnspan=2)
        
        e4 = tk.Entry(self.frame, state='disabled')
        e4.grid(row=8, column=3, columnspan=2)
        
        l6 = Label(self.frame, text="Target Value")
        l6.grid(row=9, column=3)
        
        l7 = Label(self.frame, text="Target Unit")
        l7.grid(row=9, column=4)
        
        e5 = tk.Entry(self.frame,state='disabled')
        e5.grid(row=10, column=3, padx=5)
        
        e6 = tk.Entry(self.frame, state='disabled')
        e6.grid(row=10, column=4, padx=5)

        l8 = Label(self.frame, text="Scale Position")
        l8.grid(row=11, column=3, columnspan=2)
        
        c1 = Combobox(self.frame)
        c1['values'] = ("Top Left", "Top Right", "Bottom Left", "Bottom Right")
        c1.current(1) # set the selected item
        c1.grid(row=12, column=3, columnspan=2)
        
        l9 = Label(self.frame, text="Size of Scale")
        l9.grid(row=13, column=3, columnspan=2)
        
        spin = Spinbox(self.frame, from_=1, to=20, width=5)
        spin.grid(column=3, row=14, columnspan=2)
        
        l10 = Label(self.frame, text="Background Color")
        l10.grid(row=15, column=3, columnspan=2)
        
        e4 = tk.Entry(self.frame)
        e4.grid(row=16, column=3, columnspan=2)
        
        l11 = Label(self.frame, text="Font Color")
        l11.grid(row=17, column=3, columnspan=2)
        
        e4 = tk.Entry(self.frame)
        e4.grid(row=18, column=3, columnspan=2)

        b2 = tk.Button(self.frame, text="Preview", command=quit)
        b2.grid(row=19, column=3, columnspan=2)

        self.createMenu(panel)
        
    def createMenu(self, panel):
        menu = Menu(app)        
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label='Import Image', command=lambda: self.selectImages(panel))
        file_menu.add_command(label='Exit', command=app.destroy)
        help_menu = Menu(menu, tearoff=0)
        help_menu.add_command(label='version')
        menu.add_cascade(label='File', menu=file_menu)
        menu.add_cascade(label='About', menu=help_menu)
        app.config(menu=menu)
    
    def selectImages(self, panel):
        print("Selecting Images")
        self.files = filedialog.askopenfilenames(initialdir = "C:/Users/" + user + "/Desktop",title = "InstantScale - Please select the images to process", 
                                            filetypes = [("Image files", "*.tif *.jpg *.png"), 
                                                         ("Tiff images", "*.tif"), 
                                                         ("Jpg images", "*.jpg"), 
                                                         ("Png images", "*.png")])

        img = Image.open(self.files[0])
        img2 = img.resize((500, 500), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(img2)
        panel.configure(image=img2)
      
    def readScale(self,):
        img = cv2.imread(self.files[0])
        height, width, channels = img.shape
        print(height)
        crop_img, bar_img = pI.getBar(img)
        
    


if __name__ == "__main__":
    app = tk.Tk()
    app.geometry("1500x600")
    app.title("Instant Scale")
    app.iconbitmap('icon.ico')
    MainApplication(app)
    app.mainloop()



