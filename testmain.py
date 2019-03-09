import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import Label
from tkinter import Scrollbar
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
from tkinter import Spinbox
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import getpass # get username
import cv2
import pytesseract
import os
import processImage as pI

#######TODO########
#manual target scale


# Get *.exe path and username
exePath = os.getcwd()
user = getpass.getuser()

# Tesseract parameters
tess_path = exePath + '\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tess_path
TESSDATA_PREFIX = os.path.dirname(tess_path)

################################################

#TODO LIST
#Segunda imagem está com a resolução errada, se meter escala bottom nao aparece, mas grava a imagem de maneira certa
#Manual white bar
#Manual Scale Size
#remover Save automatico


class Menubar(Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent, tearoff=False)
        self.parent = parent

        menubar = Menu(self, tearoff=0)
        file_menu = Menu(self, tearoff=0)

        file_menu.add_command(label='Import Image')
        file_menu.add_command(label='Save As')
        file_menu.add_command(label='Exit', command=exit)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='version')
        self.add_cascade(label='File', menu=file_menu)
        self.add_cascade(label='About', menu=help_menu)

        parent.config(menu=self)


class ReadScale(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.readscale = tk.Frame(parent, bg="#ffffff", width=400, height=200, borderwidth=3, relief="ridge")

        self.readscale.grid(row=1, column=1)
        self.readscale.grid_propagate(False)

        self.readscale.grid_rowconfigure(0, weight=1)
        self.readscale.grid_rowconfigure(2, weight=1)
        self.readscale.grid_columnconfigure(0, weight=1)
        self.readscale.grid_columnconfigure(2, weight=1)

        self.b1 = ttk.Button(self.readscale, text="ReadScale")
        self.b1.grid(row=1, column=1, sticky="nsew")




class InstantScale(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("Instant Scale")
        self.iconbitmap(default="icon.ico")
        self.wm_minsize(800, 600)
        self.geometry("1360x700")

        # MENUBAR

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


        menu = Menubar(self)
        readscale1 = ReadScale(self)

        # SETIINGS BOX



        # self.b1 = ttk.Button(self, text="ReadScale")
        # self.b1.grid(row=1, column=3, columnspan=2, pady=5)
        #
        # style = ttk.Style()
        # style.theme_use('default')
        # style.configure("black.Horizontal.TProgressbar", background='black')
        # self.bar = Progressbar(self, length=200, style='black.Horizontal.TProgressbar')
        # self.bar['value'] = 0
        # self.bar.grid(row=2, column=3, columnspan=2)
        #
        # self.l3 = Label(self, text="Value")
        # self.l3.grid(row=3, column=3)
        #
        # self.l3 = Label(self, text="Unit (mm, um, nm)")
        # self.l3.grid(row=3, column=4)
        #
        # self.e1 = ttk.Entry(self, state='disabled')
        # self.e1.grid(row=4, column=3, padx=5)
        #
        # self.e2 = ttk.Entry(self, state='disabled')
        # self.e2.grid(row=4, column=4, padx=5)
        #
        # self.l4 = Label(self, text="Scale Size (Pixels)")
        # self.l4.grid(row=5, column=3, columnspan=2)
        #
        # self.e3 = ttk.Entry(self, state='disabled')
        # self.e3.grid(row=6, column=3, columnspan=2)
        #
        # self.l5 = Label(self, text="White Bar (%)")
        # self.l5.grid(row=7, column=3, columnspan=2)
        #
        # self.e4 = ttk.Entry(self, state='disabled')
        # self.e4.grid(row=8, column=3, columnspan=2)
        #
        # self.l6 = Label(self, text="Target Value")
        # self.l6.grid(row=9, column=3)
        #
        # self.l7 = Label(self, text="Target Unit")
        # self.l7.grid(row=9, column=4)
        #
        # self.e5 = ttk.Entry(self, state='disabled')
        # self.e5.grid(row=10, column=3, padx=5)
        #
        # self.e6 = ttk.Entry(self, state='disabled')
        # self.e6.grid(row=10, column=4, padx=5)
        #
        # self.l8 = Label(self, text="Scale Position")
        # self.l8.grid(row=11, column=3, columnspan=2)
        #
        # self.c1 = Combobox(self)
        # self.c1['values'] = ("Top Left", "Top Right", "Bottom Left", "Bottom Right")
        # self.c1.current(1)  # set the selected item
        # self.c1.grid(row=12, column=3, columnspan=2)
        #
        # self.l9 = Label(self, text="Size of Scale")
        # self.l9.grid(row=13, column=3, columnspan=2)
        #
        # self.spin = Spinbox(self, from_=1, to=20, width=5)
        # self.spin.grid(column=3, row=14, columnspan=2)
        #
        # self.l10 = Label(self, text="Font Color", bg="#ffffff", fg="#000000")
        # self.l10.grid(row=16, column=3, rowspan=1, sticky="nsew", padx=5)
        #
        # self.bgcolour_rgb = [255.0, 255.0, 255.0]
        # self.ftcolour_rgb = [0.0, 0.0, 0.0]
        #
        # self.b3 = ttk.Button(self, text="Pick background color")
        # self.b3.grid(row=16, column=4, sticky="ew")
        #
        # contrast_ratio = 21
        # self.text = tk.StringVar()
        # self.text.set("Contrast = %.2f" % contrast_ratio)
        #
        # self.l11 = Label(self, textvariable=self.text, bg="#008000")
        # self.l11.grid(row=17, column=3, rowspan=1, sticky="nsew", padx=5)
        #
        # self.b4 = ttk.Button(self, text="Pick font color")
        # self.b4.grid(row=17, column=4, sticky="ew")
        #
        # self.var = tk.IntVar()
        # self.c2 = tk.Checkbutton(self, text="Manual", variable=self.var)
        # self.c2.grid(row=19, column=4, sticky="ew")
        # self.b2 = ttk.Button(self, text="Preview")
        # self.b2.grid(row=19, column=3)
        #

        # self.grid_columnconfigure(1, weight=10)
        # self.grid_columnconfigure(2, weight=10)


if __name__ == "__main__":


    app = InstantScale()
    app.mainloop()
