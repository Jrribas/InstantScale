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

        file_menu.add_command(label='Import Image', command=lambda: self.selectImages())
        # file_menu.add_command(label='Save As', command=lambda: saveFile())
        file_menu.add_command(label='Exit', command=exit)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='Version', command=lambda: About())
        self.add_cascade(label='File', menu=file_menu)
        self.add_cascade(label='About', menu=help_menu)

        parent.config(menu=self)

    def selectImages(self):
        print("Selecting Images")
        self.files = filedialog.askopenfilenames(initialdir="C:/Users/" + user + "/Desktop",
                                                 title="InstantScale - Please select the images to process",
                                                 filetypes=[("Image files", "*.tif *.jpg *.png"),
                                                            ("Tiff images", "*.tif"),
                                                            ("Jpg images", "*.jpg"),
                                                            ("Png images", "*.png")])

        img = Image.open(self.files[0])
        img = img.resize((500, 375), Image.ANTIALIAS)
        self.img = img = ImageTk.PhotoImage(img)

        Img = Images(self.parent)
        Img.panel.itemconfig(Img.image_on_panel, image=self.img)

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


class Images(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.images = tk.Frame(self.parent, borderwidth=3, relief="ridge")
        self.images.grid(row=2, column=1)

        self.images.grid_rowconfigure(0, weight=1)
        self.images.grid_rowconfigure(3, weight=1)
        self.images.grid_columnconfigure(0, weight=1)
        self.images.grid_columnconfigure(3, weight=1)
        self.images.grid_columnconfigure(1, weight=10)
        self.images.grid_columnconfigure(2, weight=10)

        # Scrollbars

        self.scrollbar = Scrollbar(self.images, orient=tk.HORIZONTAL)
        self.scrollbar.grid(row=2, column=1, sticky="ew")

        self.scrollbar2 = Scrollbar(self.images, orient=tk.HORIZONTAL)
        self.scrollbar2.grid(row=2, column=2, sticky="ew")


        # Image 1
        self.img1 = img1 = ImageTk.PhotoImage(Image.open("images/file_import_image.png"))

        self.panel = tk.Canvas(self.images, width=self.img1.width(), height=self.img1.height(),
                               xscrollcommand=self.scrollbar.set)
        self.panel.grid(row=1, column=1, sticky="nswe")

        self.image_on_panel = self.panel.create_image(0, 0, anchor='nw', image=img1)

        self.scrollbar.config(command=self.panel.xview)

        # Image 2
        self.img3 = img3 = ImageTk.PhotoImage(Image.open("images/file_import_image2.png"))

        self.panel2 = tk.Canvas(self.images, width=self.img1.width(), height=self.img1.height(),
                                xscrollcommand=self.scrollbar2.set)
        self.panel2.grid(row=1, column=2, sticky="nswe")

        self.image_on_panel2 = self.panel2.create_image(0, 0, anchor='nw', image=img3, tags='image')

        self.scrollbar2.config(command=self.panel2.xview)

        self.parent.bind("<Configure>", self.update_scrollregion)

    def update_scrollregion(self, event):
        self.panel.configure(scrollregion=self.panel.bbox("all"))
        self.panel2.configure(scrollregion=self.panel2.bbox("all"))


class InstantScale(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)



        self.wm_title("Instant Scale")
        self.iconbitmap(default="icon.ico")
        self.wm_minsize(800, 600)
        self.geometry("1370x780")

        # MENUBAR

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=10)


        menu = Menubar(self)
        readscale1 = ReadScale(self)
        self.images = Images(self)


# =============================================================================
# About Window
# =============================================================================

class About():
    def __init__(self, *args, **kwargs):
        win = tk.Toplevel()
        win.geometry("380x270")
        win.wm_title("About Instant Scale")

        la = Label(win, text="Instant Scale v2.0", font="Verdana 16 bold")
        la.grid(row=0, column=1)

        stringAbout = "Reads SEM images scale, crops the white bar, and creates\n a new smaller scale on a corner of your choice.\n\nCopyright"
        unicodeCopyright = u"\u00A9"
        stringAbout2 = "Instant Scale Projects Contributors\nLicensed under the terms of the MIT License\n\nCreated by João Ribas and Ricardo Farinha.\n"
        stringAbout3 = "For bugs reports and feature requests, please go to our Github website: \nhttps://github.com/Jrribas/InstantScale\n\n"
        stringAbout4 = "Created on Python 3.6.4, Tkinter 8.6 on Windows\n"
        aboutText = stringAbout + unicodeCopyright + stringAbout2 + stringAbout3 + stringAbout4

        lb = tk.Label(win, text=aboutText)
        lb.grid(row=1, column=1)

        b = ttk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=2, column=1)
        self.center(win)

    def center(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


if __name__ == "__main__":
    app = InstantScale()
    app.mainloop()
