from webbrowser import open
from tkinter import END
from tkinter import Toplevel
from tkinter import Frame
from tkinter import Canvas
from tkinter import Label
from tkinter.ttk import Sizegrip
from tkinter.ttk import Combobox
from tkinter.ttk import Entry
from tkinter.ttk import Button
from PIL import Image, ImageTk
from cv2 import imread, imwrite
import os

exePath = os.getcwd()


class About(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.parent = parent

        self.resizable(0, 0)
        self.wm_title("About Instant Scale")

        self.grid_rowconfigure((0, 5), weight=1)
        self.grid_columnconfigure((0, 2), weight=1)

        la = Label(self, text="Instant Scale v2.0", font="Verdana 16 bold")
        la.grid(row=0, column=1)

        stringAbout = "Reads SEM images scale, crops the white bar, and creates\n a new smaller scale on a " \
                      "corner of your choice.\n\nCopyright"
        unicodeCopyright = u"\u00A9"
        stringAbout2 = "Instant Scale Projects Contributors\nLicensed under the terms of the MIT License\n\n" \
                       "Created by João Ribas and Ricardo Farinha.\n"
        stringAbout3 = "For bugs reports and feature requests, please go to our Github website: \n"

        lwiki = Label(self, text="https://github.com/Jrribas/InstantScale/Issues", fg="blue", cursor="hand2")
        lwiki.grid(row=2, column=1, padx=5, columnspan=1)

        lwiki.bind("<Button-1>", lambda event: open(lwiki.cget("text")))

        stringAbout4 = "\nCreated on Python 3.6.4, Tkinter 8.6 on Windows\n"

        aboutText = stringAbout + unicodeCopyright + stringAbout2 + stringAbout3

        lb = Label(self, text=aboutText)
        lb.grid(row=1, column=1)

        lb1 = Label(self, text=stringAbout4)
        lb1.grid(row=3, column=1)

        b = Button(self, text="Okay", command=self.destroy)
        b.grid(row=4, column=1)

        self.center()

    def center(self):
        # Center About window in any display resolution
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class Error(Toplevel):
    def __init__(self, parent, errorMessage, method, choice):
        Toplevel.__init__(self, parent)
        self.parent = parent

        self.resizable(0, 0)
        self.attributes('-topmost', 'true')

        self.grid_rowconfigure((0, 8), weight=1)
        self.grid_columnconfigure((0, 3), weight=1)

        # method: warning or error
        # choice: warning can be ignored?

        if method == "error":
            self.wm_title("Error!")
            stringAbout = "The error returned the following message:"
            l1 = Label(self, text="Instant Scale v2.0 found an error :(\n", font="Verdana 16 bold")

        elif method == "warning":
            self.wm_title("Warning!")
            stringAbout = "Warning message:"
            l1 = Label(self, text="Instant Scale v2.0 has a warning:(\n", font="Verdana 16 bold")
        else:
            self.wm_title("Message")
            stringAbout = "Message:"
            l1 = Label(self, text="Instant Scale v2.0 has a message :)\n", font="Verdana 16 bold")

        l1.grid(row=0, column=1, padx=5, columnspan=2)

        stringAbout2 = "If you can't understand this error first check the github wiki for more information."

        stringAbout3 = "If you still couldn't find a solution, please submit and issue in the projects page :)"

        errorMessage = errorMessage + "\n"

        l2 = Label(self, text=stringAbout)
        l2.grid(row=1, column=1, padx=5, columnspan=2)

        l2 = Label(self, text=errorMessage, fg="RED")
        l2.grid(row=2, column=1, padx=5, columnspan=2)

        l2 = Label(self, text=stringAbout2)
        l2.grid(row=3, column=1, padx=5, columnspan=2)

        lwiki = Label(self, text="https://github.com/Jrribas/InstantScale/wiki", fg="blue", cursor="hand2")
        lwiki.grid(row=4, column=1, padx=5, columnspan=2)

        lwiki.bind("<Button-1>", lambda event: open(lwiki.cget("text")))

        l3 = Label(self, text=stringAbout3)
        l3.grid(row=5, column=1, padx=5, columnspan=2)

        lissue = Label(self, text="https://github.com/Jrribas/InstantScale/issues", fg="blue", cursor="hand2")
        lissue.grid(row=6, column=1, padx=5, columnspan=2)

        lissue.bind("<Button-1>", lambda event: open(lissue.cget("text")))

        if choice == "yes":
            b1 = Button(self, text="Okay", command=self.on_ok)
            b1.grid(row=7, column=2, pady=5)
            b2 = Button(self, text="Ignore", command=self.on_ok_1)
            b2.grid(row=7, column=1, pady=5)

        else:
            b = Button(self, text="Okay", command=self.on_ok)
            b.grid(row=7, column=1, pady=5, columnspan=2)

        self.center()

    def on_ok(self, event=None):
        self.parent.choice = 0
        self.destroy()

    def on_ok_1(self, event=None):
        self.parent.choice = 1
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return False

    def center(self):
        # Center About window in any display resolution
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class RullerWindow(Toplevel):

    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.parent = parent

        # Variables
        # Zoom value from combobox (self.e5)
        self.zoom_value = None

        self.img_open = Image.open(exePath + "\\images\\HoldImages\\ruller_crop.tif")
        self.img = ImageTk.PhotoImage(self.img_open)

        # Define frame for image
        self.image = Frame(self)
        self.image.grid(row=3, column=1, sticky="ns")

        # Define frame for buttons
        self.buttons = Frame(self)
        # self.buttons.grid_propagate(False)
        self.buttons.grid(row=1, column=1, sticky="nw")

        # Frame configuration (center frames)
        self.grid_rowconfigure((2, 4), weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Frame buttons configuration (center frames)
        self.buttons.grid_rowconfigure((0, 3), weight=1)

        # self.buttons.grid_columnconfigure((0, 8), weight=1)

        # Frame image configuration (center frames)
        self.image.grid_rowconfigure((0, 2), weight=1)
        self.image.grid_columnconfigure((0, 2), weight=1)

        self.c1 = Combobox(self.buttons)
        self.c1['values'] = ("Top Left", "Top Right", "Bottom Left", "Bottom Right")
        self.c1.current(3)  # set the selected item
        self.c1.grid(row=1, column=4, padx=2.5)
        self.c1.bind('<<ComboboxSelected>>', lambda _: self.crop())

        self.c3 = Combobox(self.buttons)
        self.c3['values'] = ("35", "45", "55", "65", "75")
        self.c3.current(2)  # set the selected item
        self.c3.grid(row=1, column=7, padx=2.5)
        self.c3.bind('<<ComboboxSelected>>', lambda _: self.crop())

        self.panel = Label(self.image, image=self.img, anchor="center")
        self.panel.grid(row=2, column=1, padx=2)

        self.c2 = Combobox(self.buttons)
        self.c2['values'] = ("1x", "2x", "3x")
        self.c2.current(0)  # set the selected item
        self.c2.grid(row=1, column=5, padx=2.5)
        self.c2.bind('<<ComboboxSelected>>', lambda _: self.zoom())

        self.crop()

        self.b1 = Button(self.buttons, text="Ruler", command=lambda: Ruler(self))
        self.b1.grid(row=1, column=3, padx=2.5)

        self.l1 = Label(self.buttons, text="Pixel value")
        self.l1.grid(row=1, column=1)

        self.e5 = Entry(self.buttons)
        self.e5.grid(row=1, column=2, padx=2.5)
        self.e5.configure(state='disable')

        self.l2 = Label(self.buttons, text="Width %")
        self.l2.grid(row=1, column=6)

        instruct = "1 - Click button Ruller; 2 - Move the ruler by clicking/dragging the left gray icon; 3 - " \
                   "Increase the scale size by clicking/dragging the right gray icon; 4 - Left click inside the" \
                   " ruller to insert the pixel count; 5 - Right click inside the ruller to exit. "

        self.l3 = Label(self.buttons, wraplength=750, text=instruct, anchor="w", justify="left")
        self.l3.grid(row=2, column=1, columnspan=7, sticky="w")

    def crop(self):

        crop_img = None

        img_read = imread(self.parent.files[self.parent.i - 1])
        height, width, channels = img_read.shape

        if self.c1.get() == "Bottom Right":
            crop_img = img_read[int(height/1.4)::, int(width * int(self.c3.get())/100)::]
        elif self.c1.get() == "Bottom Left":
            crop_img = img_read[int(height / 1.4)::, 0:int(width - (width * int(self.c3.get())/100))]
        elif self.c1.get() == "Top Left":
            crop_img = img_read[0:int(height - (height / 1.4)), 0:int(width - (width * int(self.c3.get())/100))]
        elif self.c1.get() == "Top Right":
            crop_img = img_read[0:int(height - (height / 1.4)), int(width * int(self.c3.get())/100)::]

        imwrite(exePath + "\\images\\HoldImages\\ruller_crop.tif", crop_img)

        self.img_open = Image.open(exePath + "\\images\\HoldImages\\ruller_crop.tif")

        self.zoom()

    def zoom(self):

        width, height = self.img_open.size
        zoom = self.c2.get()
        zoom = int(zoom[0:1])

        self.img = ImageTk.PhotoImage(self.img_open.resize((width*zoom, height*zoom), Image.ANTIALIAS))

        self.panel.configure(image=self.img)

        self.zoom_value = zoom


class Ruler(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.parent = parent

        self.x = None
        self.y = None

        self.txt_ticks = []
        self.big_ticks = 0
        self.small_ticks = 0
        self.pixel = 0
        self.refline = None
        self.reftxt = None

        self.overrideredirect(True)
        self.attributes('-topmost', 'true')
        self.wm_geometry("200x50")
        self.wm_minsize(25, 60)
        self.wm_maxsize(2000, 60)
        self.canvas = Canvas(self, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas['background'] = 'yellow2'

        self.grip = Sizegrip(self)
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        self.grip.bind("<B1-Motion>", self.OnMotion)

        self.label = Label(self, text="Click on the grip to move")
        self.grip = Label(self, bitmap="gray25")
        self.grip.place(relx=0.0, rely=1.0, anchor="sw")

        self.grip.bind("<ButtonPress-1>", self.start_window_move)
        self.grip.bind("<ButtonRelease-1>", self.stop_window_move)
        self.grip.bind("<B1-Motion>", self.on_window_move)

        self.canvas.bind("<ButtonPress-1>", lambda e: self.send_number(self.pixel))
        self.canvas.bind("<ButtonRelease-3>", self.exit)

        self.center()

        self.after(100, self.updates)

    def exit(self, event):
        self.destroy()

    def updates(self):

        if self.small_ticks != int((self.winfo_width() / 10) - self.big_ticks + 1):
            self.update_ticks()
            self.canvas.delete('all')
            self.draw_ticks()

        self.canvas.delete(self.refline)
        self.canvas.delete(self.reftxt)
        self.draw_reference_line()
        self.after(50, self.updates)

    def draw_ticks(self):

        for i in range(self.big_ticks):
            self.canvas.create_line(self.txt_ticks[i], 0, self.txt_ticks[i], 20)
            self.canvas.create_text([self.txt_ticks[i], 25], text=str(self.txt_ticks[i]))

        small_ticks_coord = [x * 10 for x in range(1, self.small_ticks + self.big_ticks) if not x % 5 == 0]

        for i in small_ticks_coord:

            self.canvas.create_line(i, 0, i, 10)

    def draw_reference_line(self):

        x = self.winfo_pointerx() - self.winfo_rootx()

        self.pixel = x

        self.refline = self.canvas.create_line(x, 0, x, 32)
        self.reftxt = self.canvas.create_text([x, 35], text=str(x) + "px")

    def update_ticks(self):

        self.txt_ticks = []

        self.big_ticks = int((self.winfo_width() / 50) + 1)
        self.small_ticks = int((self.winfo_width() / 10) - self.big_ticks + 1)

        j = 0

        for i in range(self.big_ticks):

            self.txt_ticks.append(0 + j)
            j = j + 50

    def OnMotion(self, event):
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()

        # Avoid bad geometry error
        if y1-y0 < 0:
            y1 = y0
        if x1-x0 < 0:
            x1 = x0

        self.geometry("%sx%s" % ((x1-x0), (y1-y0)))
        return

    def start_window_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_window_move(self, event):
        self.x = None
        self.y = None

    def on_window_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))

    def send_number(self, pixel):

        self.parent.e5.configure(state='normal')
        self.parent.e5.delete(0, END)
        self.parent.e5.insert(END, str(int(pixel / self.parent.zoom_value)))
        self.parent.e5.configure(state='disable')

        self.parent.parent.e2.configure(state='normal')
        self.parent.parent.e2.delete(0, END)
        self.parent.parent.e2.insert(END, str(int(pixel/self.parent.zoom_value)))
        self.parent.parent.e2.configure(state='disable')

    def center(self):
        # Center About window in any display resolution
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
