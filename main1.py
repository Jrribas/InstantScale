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
import getpass  # get username
import cv2
import pytesseract
import os
import processImage as pI

################################################

# Get *.exe path and username
exePath = os.getcwd()
user = getpass.getuser()

# Tesseract parameters
tess_path = exePath + '\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tess_path
TESSDATA_PREFIX = os.path.dirname(tess_path)

################################################

# TODO
# remover Save automatico
# adicionar if's de controlo
# bloquear manual during readscale


class Menubar(Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent, tearoff=False)
        self.parent = parent
        self.images = self.parent.images

        # We don't like tear off xD
        menubar = Menu(self, tearoff=0)
        file_menu = Menu(self, tearoff=0)
        help_menu = Menu(menubar, tearoff=0)

        # Define itens in menus
        file_menu.add_command(label='Import Image', command=lambda: self.selectImages())
        file_menu.add_command(label='Save As', command= self.saveFile)
        file_menu.add_command(label='Exit', command=exit)
        help_menu.add_command(label='Version', command=lambda: About())

        # Assign menus
        self.add_cascade(label='File', menu=file_menu)
        self.add_cascade(label='About', menu=help_menu)
        self.parent.config(menu=self)

    def selectImages(self):
        # Select file window
        # print("Selecting Images")

        self.parent.files = filedialog.askopenfilenames(initialdir="C:/Users/" + user + "/Desktop",
                                                        title="InstantScale - Please select the images to process",
                                                        filetypes=[("Image files", "*.tif *.jpg *.png"),
                                                                   ("Tiff images", "*.tif"),
                                                                   ("Jpg images", "*.jpg"),
                                                                   ("Png images", "*.png")])

        self.parent.img3open = Image.open(self.parent.files[0])
        self.parent.img3 = ImageTk.PhotoImage(self.parent.img3open.resize(
            (int(self.parent.panel2.winfo_width()) - 5, int(self.parent.panel2.winfo_height()) - 5), Image.ANTIALIAS))

        self.parent.panel.itemconfig(self.parent.image_on_panel, image=self.parent.img3)

    def saveFile(self):
        # Save file window
        self.image = self.parent.img4open
        file = filedialog.asksaveasfile(mode='wb', defaultextension=".tiff",
                                        filetypes=(("Tiff file", "*.tiff"), ("All Files", "*.*")))
        if file:
            # print(self.image.mode)
            self.image.save(file)


class TopFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Frame assignment
        self.readscale = tk.Frame(self.parent, height=190, width=800)
        self.readscale.grid_propagate(False)
        self.readscale.grid(row=1, column=1, sticky="nw")

        # Frame configuration
        self.readscale.grid_rowconfigure((0, 7), weight=1)
        self.readscale.grid_columnconfigure((0, 7), weight=1)

        # Widgets assignment
        self.b1 = ttk.Button(self.readscale, text="ReadScale", command=self.readScale)
        self.b1.grid(row=1, column=1, columnspan=2, pady=5)

        # Progress bar assignment
        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        self.bar = Progressbar(self.readscale, length=200, style='black.Horizontal.TProgressbar')
        self.bar['value'] = 0
        self.bar.grid(row=2, column=1, columnspan=2, sticky="nswe", padx=2)

        # All widgets
        self.l3 = Label(self.readscale, text="Value")
        self.l3.grid(row=3, column=1, pady=5)

        self.l3 = Label(self.readscale, text="Unit (mm, um, nm)")
        self.l3.grid(row=3, column=2, pady=5)

        self.e1 = ttk.Entry(self.readscale, state='disabled')
        self.e1.grid(row=4, column=1, padx=2, sticky="we")

        self.e2 = ttk.Entry(self.readscale, state='disabled')
        self.e2.grid(row=4, column=2, padx=2, sticky="we")

        self.l4 = Label(self.readscale, text="Scale Size (Pixels)")
        self.l4.grid(row=5, column=1, pady=5)

        self.l5 = Label(self.readscale, text="White Bar (%)")
        self.l5.grid(row=5, column=2, pady=5)

        self.e3 = ttk.Entry(self.readscale, state='disabled')
        self.e3.grid(row=6, column=1, sticky="we", padx=2)

        self.e4 = ttk.Entry(self.readscale, state='disabled')
        self.e4.grid(row=6, column=2, sticky="we", padx=2)

        self.l7 = Label(self.readscale, text="Target Value")
        self.l7.grid(row=3, column=3, pady=5)

        self.l8 = Label(self.readscale, text="Target Unit")
        self.l8.grid(row=3, column=4, pady=5)

        self.e5 = ttk.Entry(self.readscale, state='disabled')
        self.e5.grid(row=4, column=3, sticky="we", padx=2)

        self.e6 = ttk.Entry(self.readscale, state='disabled')
        self.e6.grid(row=4, column=4, sticky="we", padx=2)

        self.l8 = Label(self.readscale, text="Scale Position")
        self.l8.grid(row=5, column=3)

        self.l9 = Label(self.readscale, text="Size of Scale")
        self.l9.grid(row=5, column=4)

        self.c1 = Combobox(self.readscale)
        self.c1['values'] = ("Top Left", "Top Right", "Bottom Left", "Bottom Right")
        self.c1.current(1)  # set the selected item
        self.c1.grid(row=6, column=3)

        self.spin = Spinbox(self.readscale, from_=1, to=20, width=5, textvariable=tk.StringVar(value="4"))
        self.spin.grid(row=6, column=4)

        self.l10 = Label(self.readscale, text="Font Color", bg="#ffffff", fg="#000000")
        self.l10.grid(row=3, column=5, rowspan=2, sticky="nsew", padx=5)

        self.bgcolour_rgb = [255.0, 255.0, 255.0]
        self.ftcolour_rgb = [0.0, 0.0, 0.0]

        self.b3 = ttk.Button(self.readscale, text="Pick background color", command=lambda: self.chooseColour(0))
        self.b3.grid(row=3, column=6, sticky="ew")

        contrast_ratio = 21
        self.text = tk.StringVar()
        self.text.set("Contrast = %.2f" % contrast_ratio)

        self.l11 = Label(self.readscale, textvariable=self.text, bg="#008000")
        self.l11.grid(row=5, column=5, rowspan=2, sticky="ew", padx=5)

        self.b4 = ttk.Button(self.readscale, text="Pick font color", command=lambda: self.chooseColour(1))
        self.b4.grid(row=4, column=6, sticky="ew")

        self.var = tk.IntVar()
        self.c2 = tk.Checkbutton(self.readscale, text="Manual", variable=self.var, command=self.manual)
        self.c2.grid(row=2, column=3, sticky="ew")
        self.b2 = ttk.Button(self.readscale, text="Preview", command=self.preview)
        self.b2.grid(row=6, column=6)

    def manual(self):

        # Change widgets from disabled to normal

        if self.var.get() == 1:
            self.e1.configure(state='normal')
            self.e2.configure(state='normal')
            self.e3.configure(state='normal')
            self.e4.configure(state='normal')
            self.e5.configure(state='normal')
            self.e6.configure(state='normal')
        else:
            self.e1.configure(state='disabled')
            self.e2.configure(state='disabled')
            self.e3.configure(state='disabled')
            self.e4.configure(state='disabled')
            self.e5.configure(state='disabled')
            self.e6.configure(state='disabled')

    def contrast(self, rgb, rgb1):

        # Calculates the constrast between the font and background color chosen
        # For more infomation: https://www.w3.org/TR/WCAG20-TECHS/G17#G17-procedure

        lumi = [0, 0]

        rgb_list = [rgb, rgb1]
        rgb_math = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

        for j in range(0, 2):

            for i in range(0, 3):

                temp = rgb_list[j][i] / 255.0

                if temp <= 0.03928:
                    rgb_math[j][i] = temp / 12.92
                else:
                    rgb_math[j][i] = ((temp + 0.055) / 1.055) ** 2.4

            lumi[j] = 0.2126 * rgb_math[j][0] + 0.7152 * rgb_math[j][1] + 0.0722 * rgb_math[j][2]

        if lumi[0] > lumi[1]:
            contrast = (lumi[0] + 0.05) / (lumi[1] + 0.05)

        else:
            contrast = (lumi[1] + 0.05) / (lumi[0] + 0.05)

        self.text.set("Contrast = %.2f" % contrast)

        if contrast >= 7:
            self.l11.config(bg="#008000")

        else:
            self.l11.config(bg="#FF0000")

    def chooseColour(self, label):
        # Window to choose color

        if label == 0:
            # Window to choose color
            bgcolour = askcolor()
            # askcolor returns a list with the color rgb and hex codes [[rgb], hex]
            self.bgcolour_rgb = list(bgcolour[0])
            # Change label background color
            self.l10.config(bg=bgcolour[1])
            # Calculate constrast
            self.contrast(self.bgcolour_rgb, self.ftcolour_rgb)
        else:
            ftcolour = askcolor()
            self.ftcolour_rgb = list(ftcolour[0])
            self.l10.config(fg=ftcolour[1])
            self.contrast(self.bgcolour_rgb, self.ftcolour_rgb)

    def readScale(self):

        # Update progress bar to 0
        self.bar['value'] = 0
        self.update_idletasks()

        #Open image
        self.img = cv2.imread(self.parent.files[0])

        # Update progress bar to 25 and update GUI
        self.bar['value'] = 25
        self.update_idletasks()

        # Send image to function getBar and obtain information about the "white bar in SEM images.
        self.crop_img, self.bar_img, barSize = pI.getBar(self.img)
        # print('bar Size: ' + str(barSize))
        barSizeRound = round(barSize)

        # Update entry widgets with values obtaines
        self.e4.configure(state='normal')
        self.e4.delete(0, tk.END)
        self.e4.insert(tk.END, barSizeRound)
        self.e4.configure(state='disabled')

        # Update progress bar to 50 and update GUI
        self.bar['value'] = 50
        self.update_idletasks()

        # Save white bar image, resize it (for better tesseract readability), and calling it again
        height, width, channels = self.bar_img.shape
        cv2.imwrite(exePath + "\\images\\HoldImages\\bar.tif", self.bar_img)

        img = Image.open(exePath + "\\images\\HoldImages\\bar.tif")
        img1 = img.resize((width * 3, height * 3), Image.ANTIALIAS)
        img1.save(exePath + "\\images\\HoldImages\\resize_im.tif", dpi=(600, 600), quality=100)

        self.bar_img_res = cv2.imread(exePath + "\\images\\HoldImages\\resize_im.tif")

        # Measures scale bar (in pixels) from resized white bar image
        self.scale = len(pI.getScale(self.bar_img))
        # print('scale: ' + str(self.scale))

        # Update entry widgets with values obtained
        self.e3.configure(state='normal')
        self.e3.delete(0, tk.END)
        self.e3.insert(tk.END, self.scale)
        self.e3.configure(state='disabled')

        # Update progress bar to 75 and update GUI
        self.bar['value'] = 75
        self.update_idletasks()

        # Get scale number and it's units
        self.scaleNumb, self.units = pI.getNumber(self.bar_img, self.bar_img_res, exePath)

        # Update entry widgets with values obtained
        self.e1.configure(state='normal')
        self.e1.delete(0, tk.END)
        self.e1.insert(tk.END, self.scaleNumb)
        self.e1.configure(state='disabled')

        self.e2.configure(state='normal')
        self.e2.delete(0, tk.END)
        self.e2.insert(tk.END, self.units)
        self.e2.configure(state='disabled')

        # Update progress bar to 100 and update GUI
        self.bar['value'] = 100
        self.update_idletasks()

    def preview(self):

        # print("c1 get value: " + self.c1.get())

        # Obtain
        if self.c1.get() == "Top Left":
            self.position = 2
        elif self.c1.get() == "Top Right":
            self.position = 3
        elif self.c1.get() == "Bottom Left":
            self.position = 0
        elif self.c1.get() == "Bottom Right":
            self.position = 1

        self.scale = int(self.e3.get())
        self.sizeOfScale = int(self.spin.get())
        self.scaleNumb = int(self.e1.get())
        self.units = self.e2.get()

        # Change variable of scale colors from list of floats to tupple of integrers
        self.bgColor = self.bgcolour_rgb
        self.bgColor[0] = int(self.bgColor[0])
        self.bgColor[1] = int(self.bgColor[1])
        self.bgColor[2] = int(self.bgColor[2])
        self.bgColor_tupple = tuple(self.bgColor)

        self.fontColor = self.ftcolour_rgb
        self.fontColor[0] = int(self.fontColor[0])
        self.fontColor[1] = int(self.fontColor[1])
        self.fontColor[2] = int(self.fontColor[2])
        self.fontColor_tupple = tuple(self.fontColor)

        # Check if target values are inserted manualy
        if self.e5.index("end") == 0:
            self.targetValue = 0
        else:
            self.targetValue = int(self.e5.get())

        if self.e6.index("end") == 0:
            self.targetUnit = ''
        else:
            self.targetUnit = self.e6.get()

        # Obtain image without white bar
        self.crop_img = pI.cropImage(self.img, int(self.e4.get()))

        # Draw scale in cropped image
        self.finalImage = pI.drawScale(self.crop_img, self.scale, int(self.scaleNumb), self.units, self.parent.files[0],
                                        exePath, self.position, exePath, self.sizeOfScale, self.fontColor_tupple, self.bgColor_tupple,
                                        self.targetValue, self.targetUnit)

        self.parent.img4open = self.finalImage

        # Resize image
        self.parent.img4 = ImageTk.PhotoImage(
            self.parent.img4open.resize((int(self.parent.panel2.winfo_width()) - 5, int(self.parent.panel2.winfo_height()) - 5),
                                        Image.ANTIALIAS))
        # Put image on canvas
        self.parent.panel2.itemconfig(self.parent.image_on_panel2, image=self.parent.img4)


class Images(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Resizing window event id
        self.drag_id = ""

        # Define frame for canvas
        self.images = tk.Frame(self.parent)
        self.images.grid(row=3, column=1, sticky="nwes")

        # Frame configuration
        self.images.grid_rowconfigure((0, 2), weight=1)
        self.images.grid_columnconfigure((0, 3), weight=1)
        self.images.grid_columnconfigure((1, 2), weight=10)

        # Canvas 1
        # Default image
        self.parent.img1open = Image.open("images/file_import_image.png")
        self.parent.img1 = ImageTk.PhotoImage(self.parent.img1open)

        self.parent.panel = tk.Canvas(self.images)
        self.parent.panel.grid(row=1, column=1, sticky="nswe")

        self.parent.image_on_panel = self.parent.panel.create_image(0, 0, anchor='nw', image=self.parent.img1,
                                                                    tags="IMG1")
        # Canvas 2
        # Default image
        self.parent.img2open = Image.open("images/file_import_image2.png")
        self.parent.img2 = ImageTk.PhotoImage(self.parent.img2open)

        self.parent.panel2 = tk.Canvas(self.images)
        self.parent.panel2.grid(row=1, column=2, sticky="nswe")

        self.parent.image_on_panel2 = self.parent.panel2.create_image(0, 0, anchor='nw', image=self.parent.img2,
                                                                      tags="IMG2")

        # Resizing event
        # Resizes canvas and images depending windows size, keeping image ratio
        self.parent.bind("<Configure>", self.dragging)

    def dragging(self, event):

        root = self.parent

        if event.widget is root:  # do nothing if the event is triggered by one of root's children
            if self.drag_id != "":
                # cancel scheduled call to stop_drag
                # print('dragging')
                root.after_cancel(self.drag_id)

            # schedule stop_drag
            self.drag_id = root.after(100, self.stopDrag)

    def stopDrag(self):

        # print('stop drag')
        # reset drag_id to be able to detect the start of next dragging
        self.drag_id = ""

        width_canvas = (self.parent.winfo_width() / 2)
        height_canvas = self.parent.winfo_height() - 190

        if hasattr(self.parent, 'files'):
            height = self.parent.img3.height()
            width = self.parent.img3.width()
            ratio_img = width / height

        else:
            height = self.parent.img1.height()
            width = self.parent.img1.width()
            ratio_img = width / height

        new_width = height_canvas * ratio_img
        new_height = height_canvas

        if new_width > width_canvas:
            new_width = width_canvas
            new_height = new_width / ratio_img

        self.parent.panel.config(width=int(new_width) - 5, height=int(new_height) - 5)
        self.parent.panel2.config(width=int(new_width) - 5, height=int(new_height) - 5)

        if hasattr(self.parent, 'img3'):
            self.parent.img1res = ImageTk.PhotoImage(
                self.parent.img3open.resize((int(new_width) - 5, int(new_height) - 5), Image.ANTIALIAS))
        else:
            self.parent.img1res = ImageTk.PhotoImage(
                self.parent.img1open.resize((int(new_width) - 5, int(new_height) - 5), Image.ANTIALIAS))

        if hasattr(self.parent, 'img4'):
            self.parent.img2res = ImageTk.PhotoImage(
                self.parent.img4open.resize((int(new_width) - 5, int(new_height) - 5), Image.ANTIALIAS))
        else:
            self.parent.img2res = ImageTk.PhotoImage(
                self.parent.img2open.resize((int(new_width) - 5, int(new_height) - 5), Image.ANTIALIAS))

        self.parent.panel.delete("IMG1")
        self.parent.panel2.delete("IMG2")

        self.parent.image_on_panel = self.parent.panel.create_image(0, 0, anchor='nw', image=self.parent.img1res,
                                                                    tags="IMG1")
        self.parent.image_on_panel2 = self.parent.panel2.create_image(0, 0, anchor='nw', image=self.parent.img2res,
                                                                      tags="IMG2")

# =============================================================================
# Main application
# =============================================================================

class InstantScale(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Main app windows definitions
        self.wm_title("Instant Scale")
        self.iconbitmap(default="icon.ico")
        self.wm_minsize(800, 600)
        self.geometry("1024x600")
        self.grid_rowconfigure((2, 4), weight=1)

        # Call of other classes (menubar,
        self.images = Images(self)
        self.menu = Menubar(self)
        self.topframe = TopFrame(self)



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

        stringAbout = "Reads SEM images scale, crops the white bar, and creates\n a new smaller scale on a " \
                      "corner of your choice.\n\nCopyright"
        unicodeCopyright = u"\u00A9"
        stringAbout2 = "Instant Scale Projects Contributors\nLicensed under the terms of the MIT License\n\n" \
                       "Created by João Ribas and Ricardo Farinha.\n"
        stringAbout3 = "For bugs reports and feature requests, please go to our Github website: \n" \
                       "https://github.com/Jrribas/InstantScale\n\n"
        stringAbout4 = "Created on Python 3.6.4, Tkinter 8.6 on Windows\n"
        aboutText = stringAbout + unicodeCopyright + stringAbout2 + stringAbout3 + stringAbout4

        lb = tk.Label(win, text=aboutText)
        lb.grid(row=1, column=1)

        b = ttk.Button(win, text="Okay", command=win.destroy)
        b.grid(row=2, column=1)
        self.center(win)

    def center(self, win):
        # Center About window in any display resolution
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


if __name__ == "__main__":
    app = InstantScale()
    app.mainloop()
