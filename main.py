from tkinter import IntVar
from tkinter import StringVar
from tkinter import Tk
from tkinter import Menu
from tkinter import Frame
from tkinter import Canvas
from tkinter import filedialog
from tkinter import Label
from tkinter import Checkbutton
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
from tkinter.ttk import Style
from tkinter.ttk import Entry
from tkinter.ttk import Button
from tkinter import Spinbox
from PIL import Image, ImageTk
from getpass import getuser
from webbrowser import open
import pytesseract
import os
import processImage as pI
import topFrame_functions as tF_f
import popupWindows as pW

# TODO: Check for bug with unit "nm"
# TODO: Check for more bugs
# TODO: Check if code can be more clean
# TODO: Check for more elegant solutions

################################################

# Get *.exe path and username
exePath = os.getcwd()
user = getuser()

# Tesseract parameters
tess_path = exePath + '\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tess_path
TESSDATA_PREFIX = os.path.dirname(tess_path)

################################################


class Menubar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent, tearoff=False)
        self.parent = parent

        # We don't like tear off xD
        menubar = Menu(self, tearoff=0)
        file_menu = Menu(self, tearoff=0)
        help_menu = Menu(menubar, tearoff=0)

        # Define items in menus
        file_menu.add_command(label='Import Image', command=lambda: self.selectImages())
        file_menu.add_command(label='Save As', command=self.saveFile)
        file_menu.add_command(label='Exit', command=lambda: InstantScale.exit(self.parent))
        help_menu.add_command(label='Information', command=lambda: pW.About(self.parent))
        help_menu.add_command(label='Help', command=lambda: open("https://github.com/Jrribas/InstantScale/wiki"))

        # Assign menus
        self.add_cascade(label='File', menu=file_menu)
        self.add_cascade(label='About', menu=help_menu)

    def selectImages(self):

        # Select file window
        files = filedialog.askopenfilenames(initialdir="C:/Users/" + user + "/Desktop",
                                            title="InstantScale - Please select the images to process",
                                            filetypes=[("Image files", "*.tif *.jpg *.png"),
                                                       ("Tiff images", "*.tif"),
                                                       ("Jpg images", "*.jpg"),
                                                       ("Png images", "*.png")])

        # Check if user selected at least an image
        if not isinstance(files, str):

            # Check if an image was already opened before.
            if hasattr(self.parent, 'img3open') and self.parent.img3open is not None:
                # Reset GUI for new image
                tF_f.reset(self.parent.topframe)

            # Clean path files of strange characters
            self.parent.files = pI.cleanPathFiles(files, exePath)

            # Open image
            self.parent.img3open = Image.open(self.parent.files[0])

            self.parent.img3 = ImageTk.PhotoImage(self.parent.img3open.resize(
                (int(self.parent.panel2.winfo_width()), int(self.parent.panel2.winfo_height())),
                Image.ANTIALIAS))

            # Put image in canvas 1
            self.parent.panel.itemconfig(self.parent.image_on_panel, image=self.parent.img3)

            # Define checkbox manual as "clickable"
            self.parent.ch1.config(state='normal')
            self.parent.b1.config(state='normal')

    def saveFile(self):
        # Save file window

        # Check if Preview was already performed
        if hasattr(self.parent, 'img4open'):

            message = "Not all images were saved! \n"
            self.parent.save = 0

            # Ask for a folder to save images
            folder = filedialog.askdirectory(initialdir="C:/Users/" + user + "/Desktop")

            # Check if a folder was selected
            if folder != "":

                # Checks if a folder named Images with new scale exist. If not it creates it.
                if not os.path.exists(folder + "\\Images with new scale"):
                    os.makedirs(folder + "\\Images with new scale")

                # Checks if several images were selected or just one
                if len(self.parent.files) > 1:

                    # Cycle through images and saves them
                    for self.parent.i in range(1, len(self.parent.files)+1):

                        filename, fileExtension = os.path.splitext(os.path.basename(self.parent.files[self.parent.i-1]))

                        self.parent.img3open = Image.open(self.parent.files[self.parent.i-1])
                        self.parent.img3 = ImageTk.PhotoImage(self.parent.img3open)

                        if self.parent.var.get() != 1:
                            tF_f.readScale(self.parent.topframe)

                            if self.parent.topframe.bar['value'] != 100:
                                message = message + self.parent.files[self.parent.i-1] + "\n"
                                continue

                        tF_f.preview(self)
                        self.parent.img4open.save(folder + "\\Images with new scale\\" + filename + fileExtension)
                        self.parent.save += 1

                else:

                    filename, fileExtension = os.path.splitext(os.path.basename(self.parent.files[0]))
                    self.parent.img4open.save(folder + "\\Images with new scale\\" + filename + fileExtension)
                    self.parent.save = 1

                # Check if images all images were saved
                if self.parent.save == len(self.parent.files):
                    pW.Error(self.parent, "All images saved!", "message", "no")
                    self.parent.save = 0
                else:
                    message = message + "Try using manual/Ruler for this images."
                    pW.Error(self.parent, message, "warning", "no")
                    self.parent.save = 0

                self.parent.i = 1

        else:
            pW.Error(self, "Please do Preview before saving.", "error", "no")


class TopFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        # Frame assignment
        self.TopFrame = Frame(self.parent, height=190, width=800)
        self.TopFrame.grid_propagate(False)
        self.TopFrame.grid(row=1, column=1, sticky="nw")

        # Frame configuration
        self.TopFrame.grid_rowconfigure((0, 7), weight=1)
        self.TopFrame.grid_columnconfigure((0, 8), weight=1)

        # Widgets assignment
        self.parent.b1 = Button(self.TopFrame, text="Read Scale", command=lambda: tF_f.readScale(self))
        self.parent.b1.grid(row=1, column=1, columnspan=2, pady=5)
        self.parent.b1.config(state='disabled')

        # Progress bar assignment
        style = Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        self.p_bar = Progressbar(self.TopFrame, length=200, style='black.Horizontal.TProgressbar')
        self.p_bar['value'] = 0
        self.p_bar.grid(row=2, column=1, columnspan=2, sticky="nswe", padx=2)

        # All widgets
        self.l3 = Label(self.TopFrame, text="Value")
        self.l3.grid(row=3, column=1, pady=5)

        self.l3 = Label(self.TopFrame, text="Unit (mm, µm, nm)")
        self.l3.grid(row=3, column=2, pady=5)

        self.vcmd = (self.register(self.checkInput), '%S', '%P')

        self.e1 = Entry(self.TopFrame, state='disabled', validate="key", validatecommand=self.vcmd)
        self.e1.grid(row=4, column=1, padx=2, sticky="we")

        self.c1 = Combobox(self.TopFrame, state='disabled')
        self.c1['values'] = ("mm", "µm", "nm")
        self.c1.grid(row=4, column=2, padx=2, sticky="we")
        self.c1.current(1)

        self.l4 = Label(self.TopFrame, text="Scale Size (Pixels)")
        self.l4.grid(row=5, column=1, pady=5)

        self.l5 = Label(self.TopFrame, text="White Bar (%)")
        self.l5.grid(row=5, column=2, pady=5)

        self.parent.e2 = Entry(self.TopFrame, state='disabled', validate="key", validatecommand=self.vcmd)
        self.parent.e2.grid(row=6, column=1, sticky="we", padx=2)

        self.vcmd1 = (self.register(self.checkInput1), '%S', "%P")

        self.e3 = Entry(self.TopFrame, state='disabled', validate="key", validatecommand=self.vcmd1)
        self.e3.grid(row=6, column=2, sticky="we", padx=2)

        self.l7 = Label(self.TopFrame, text="Target Value")
        self.l7.grid(row=3, column=3, pady=5)

        self.l8 = Label(self.TopFrame, text="Target Unit")
        self.l8.grid(row=3, column=4, pady=5)

        self.e4 = Entry(self.TopFrame, state='disabled', validate="key", validatecommand=self.vcmd)
        self.e4.grid(row=4, column=3, sticky="we", padx=2)

        self.c2 = Combobox(self.TopFrame, state='disabled')
        self.c2['values'] = ("mm", "µm", "nm")
        self.c2.grid(row=4, column=4, padx=2, sticky="we")
        self.c2.current(1)

        self.l8 = Label(self.TopFrame, text="Scale Position")
        self.l8.grid(row=5, column=3)

        self.l9 = Label(self.TopFrame, text="Scale Size")
        self.l9.grid(row=5, column=4)

        self.c3 = Combobox(self.TopFrame)
        self.c3['values'] = ("Top Left", "Top Right", "Bottom Left", "Bottom Right")
        self.c3.current(1)  # set the selected item
        self.c3.grid(row=6, column=3)

        self.spin = Spinbox(self.TopFrame, from_=1, to=10, width=5, textvariable=StringVar(value="4"))
        self.spin.grid(row=6, column=4)

        self.l10 = Label(self.TopFrame, text="Font Color", bg="#ffffff", fg="#000000")
        self.l10.grid(row=2, column=5, rowspan=2, sticky="nsew", padx=5)

        self.bgColour_rgb = [255.0, 255.0, 255.0]
        self.ftColour_rgb = [0.0, 0.0, 0.0]

        self.b3 = Button(self.TopFrame, text="Pick background color", command=lambda: tF_f.chooseColour(self, "bg"))
        self.b3.grid(row=2, column=6, sticky="ew")

        self.contrast = 21
        self.text = StringVar()
        self.text.set("Contrast = %.2f" % self.contrast)

        self.l11 = Label(self.TopFrame, textvariable=self.text, bg="#008000")
        self.l11.grid(row=4, column=5, sticky="ew", padx=5)

        self.b4 = Button(self.TopFrame, text="Pick font color", command=lambda: tF_f.chooseColour(self, "fg"))
        self.b4.grid(row=3, column=6, sticky="ew")

        self.parent.var = IntVar()
        self.parent.ch1 = Checkbutton(self.TopFrame, text="Manual", variable=self.parent.var,
                                      command=lambda: tF_f.manual(self), state="disable")
        self.parent.ch1.grid(row=2, column=3, sticky="ew")

        self.b5 = Button(self.TopFrame, text="Ruler window", command=lambda: pW.RullerWindow(self.parent))
        self.b5.grid(row=2, column=4, sticky="ew")
        self.b5.configure(state='disable')

        self.b2 = Button(self.TopFrame, text="Preview", command=lambda: tF_f.preview(self))
        self.b2.grid(row=6, column=6)

        self.l12 = Label(self.TopFrame, text="Crop Position")
        self.l12.grid(row=5, column=5, padx=5)

        self.c4 = Combobox(self.TopFrame, width=13)
        self.c4['values'] = ("Bottom", "Top")
        self.c4.current(0)  # set the selected item
        self.c4.grid(row=6, column=5, sticky="ew")

    def checkInput(self, S, P):
        # - Allow only numbers // - Disallow number zero when alone // - Max number of 3 digits

        if S.isnumeric() and int(len(P)) <= 3 and P != "0" and P != "00":
            return True
        else:
            self.bell()
            return False

    def checkInput1(self, S, P):
        # - Allow only numbers // - Disallow a number bigger than 50

        if S.isnumeric() and int(len(P)) <= 2:

            if P == "":
                return True
            elif int(P) > 50:
                self.bell()
                pW.Error(self.parent,
                         "White bar (where the scale normally is) can't be more than 50% of the image.",
                         "error", "no")
                return False
            else:
                return True
        else:
            self.bell()
            return False


class Images(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        # Resizing window event id
        self.drag_id = ""

        # Define frame for canvas
        self.images = Frame(self.parent)
        self.images.grid(row=3, column=1, sticky="nwes")

        # Frame configuration
        self.images.grid_rowconfigure((0, 2), weight=1)
        self.images.grid_columnconfigure((0, 3), weight=1)
        self.images.grid_columnconfigure((1, 2), weight=5)

        # Canvas 1
        # Default image
        self.parent.img1open = Image.open("images/file_import_image.png")
        self.parent.img1 = ImageTk.PhotoImage(self.parent.img1open)

        self.parent.panel = Canvas(self.images)
        self.parent.panel.grid(row=1, column=1, sticky="nswe", padx=2)

        self.parent.image_on_panel = self.parent.panel.create_image(0, 0, anchor='nw', image=self.parent.img1,
                                                                    tags="IMG1")
        # Canvas 2
        # Default image
        self.parent.img2open = Image.open("images/file_import_image2.png")
        self.parent.img2 = ImageTk.PhotoImage(self.parent.img2open)

        self.parent.panel2 = Canvas(self.images)
        self.parent.panel2.grid(row=1, column=2, sticky="nswe")

        self.parent.image_on_panel2 = self.parent.panel2.create_image(0, 0, anchor='nw', image=self.parent.img2,
                                                                      tags="IMG2")

        # Resizing event
        # Resize canvas and images depending windows size, keeping image ratio
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

        # reset drag_id to be able to detect the start of next dragging
        self.drag_id = ""

        width_canvas = (self.parent.winfo_width() / 2)
        height_canvas = self.parent.winfo_height() - 190

        # Check if an image was already opened so it doesn't get the ratio from default image
        if self.parent.files is not None:
            width, height = self.parent.img3open.size
            ratio_img = width / height

        else:
            height = self.parent.img1.height()
            width = self.parent.img1.width()
            ratio_img = width / height

        # Math to maintain ratio of canvas
        new_width = height_canvas * ratio_img
        new_height = height_canvas

        if new_width > width_canvas:
            new_width = width_canvas
            new_height = new_width / ratio_img

        self.parent.panel.config(width=int(new_width) - 5, height=int(new_height) - 5)
        self.parent.panel2.config(width=int(new_width) - 5, height=int(new_height) - 5)

        # Check if an image was already opened so it doesn't resize the default image
        if hasattr(self.parent, 'img3'):
            self.parent.img1res = ImageTk.PhotoImage(
                self.parent.img3open.resize((int(new_width) - 2, int(new_height) - 5), Image.ANTIALIAS))
        else:
            self.parent.img1res = ImageTk.PhotoImage(
                self.parent.img1open.resize((int(new_width) - 5, int(new_height) - 5), Image.ANTIALIAS))

        # Check if an image was already processed so it doesn't resize the default image
        if hasattr(self.parent, 'img4'):
            self.parent.img2res = ImageTk.PhotoImage(
                self.parent.img4open.resize((int(new_width) - 5, int(new_height) - 5), Image.ANTIALIAS))
        else:
            self.parent.img2res = ImageTk.PhotoImage(
                self.parent.img2open.resize((int(new_width) - 5, int(new_height) - 5), Image.ANTIALIAS))

        # Delete former images on canvas
        self.parent.panel.delete("IMG1")
        self.parent.panel2.delete("IMG2")

        # Redraw new resized images
        self.parent.image_on_panel = self.parent.panel.create_image(0, 0, anchor='nw', image=self.parent.img1res,
                                                                    tags="IMG1")
        self.parent.image_on_panel2 = self.parent.panel2.create_image(0, 0, anchor='nw', image=self.parent.img2res,
                                                                      tags="IMG2")

# =============================================================================
# Main application
# =============================================================================


class InstantScale(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.i = 1
        self.files = None
        self.save = 0

        self.protocol("WM_DELETE_WINDOW", lambda: InstantScale.exit(self))

        # Main app windows definitions
        self.wm_title("Instant Scale")
        self.iconbitmap(default="icon.ico")
        self.wm_minsize(800, 600)
        self.geometry("1024x600")
        self.grid_rowconfigure((2, 4), weight=1)
        self.grid_columnconfigure((0, 2), weight=1)

        # Call of other classes
        self.images = Images(self)
        self.topframe = TopFrame(self)
        self.menu = Menubar(self)
        self.config(menu=self.menu)

        self.center()
        
    def center(self):
        # Center About window in any display resolution
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def exit(self):

        self.i = 1

        if self.files is not None:

            for self.i in range(1, len(self.files)+1):

                self.img3open.close()
                os.remove(self.files[self.i - 1])

        self.destroy()


if __name__ == "__main__":

    app = InstantScale()
    app.mainloop()
