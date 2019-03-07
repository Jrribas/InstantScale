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

user = getpass.getuser()

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
        tk.Tk.wm_title(self, "Smart Plug Monitoring")
        # tk.Tk.iconbitmap(self, default="clienticon.ico")

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
        file_menu.add_command(label='Exit', command=exit)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='version')
        menubar.add_cascade(label='File', menu=file_menu)
        menubar.add_cascade(label='About', menu=help_menu)

        tk.Tk.config(self, menu=menubar)

        img1 = ImageTk.PhotoImage(Image.open("images/file_import_image.png"))
        img2 = ImageTk.PhotoImage(Image.open("images/file_import_image2.png"))

        self.panel = tk.Label(self, image=img1)
        self.panel.image = img1
        self.panel2 = tk.Label(self, image=img2)
        self.panel2.image = img2
        self.panel.grid(row=1, column=1, rowspan=18, padx=10, pady=10)
        self.panel2.grid(row=1, column=2, rowspan=18, padx=10, pady=10)

        self.l1 = Label(self, text="Original Image", padx=5, pady=5)
        self.l1.grid(row=19, column=1)
        self.l2 = Label(self, text="Preview", padx=5, pady=5)
        self.l2.grid(row=19, column=2)

        ##SETIINGS BOX
        self.b1 = tk.Button(self, text="ReadScale", command=self.readScale)
        self.b1.grid(row=1, column=3, columnspan=2, pady=5)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        bar = Progressbar(self, length=200, style='black.Horizontal.TProgressbar')
        bar['value'] = 0
        bar.grid(row=2, column=3, columnspan=2)

        self.l3 = Label(self, text="Value")
        self.l3.grid(row=3, column=3)

        self.l3 = Label(self, text="Unit (mm, um, nm)")
        self.l3.grid(row=3, column=4)

        self.e1 = tk.Entry(self, state='disabled')
        self.e1.grid(row=4, column=3, padx=5)

        self.e2 = tk.Entry(self, state='disabled')
        self.e2.grid(row=4, column=4, padx=5)

        self.l4 = Label(self, text="Scale Size (Pixels)")
        self.l4.grid(row=5, column=3, columnspan=2)

        self.e3 = tk.Entry(self, state='disabled')
        self.e3.grid(row=6, column=3, columnspan=2)

        self.l5 = Label(self, text="White Bar (%)")
        self.l5.grid(row=7, column=3, columnspan=2)

        self.e4 = tk.Entry(self, state='disabled')
        self.e4.grid(row=8, column=3, columnspan=2)

        self.l6 = Label(self, text="Target Value")
        self.l6.grid(row=9, column=3)

        self.l7 = Label(self, text="Target Unit")
        self.l7.grid(row=9, column=4)

        self.e5 = tk.Entry(self, state='disabled')
        self.e5.grid(row=10, column=3, padx=5)

        self.e6 = tk.Entry(self, state='disabled')
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
        self.l10.grid(row=15, column=3, columnspan=2)

        self.e4 = tk.Entry(self)
        self.e4.grid(row=16, column=3, columnspan=2)

        self.l11 = Label(self, text="Font Color")
        self.l11.grid(row=17, column=3, columnspan=2)

        self.e4 = tk.Entry(self)
        self.e4.grid(row=18, column=3, columnspan=2)

        self.b2 = tk.Button(self, text="Preview", command=quit)
        self.b2.grid(row=19, column=3, columnspan=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(20, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

    def selectImages(self):
        print("Selecting Images")
        files = filedialog.askopenfilenames(initialdir="C:/Users/" + user + "/Desktop",
                                            title="InstantScale - Please select the images to process",
                                            filetypes=[("Image files", "*.tif *.jpg *.png"),
                                                       ("Tiff images", "*.tif"),
                                                       ("Jpg images", "*.jpg"),
                                                       ("Png images", "*.png")])

        img = Image.open(files[0])
        img2 = img.resize((500, 500), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(img2)
        self.panel.configure(image=img2)
        self.panel.image = img2

    def readScale(self):
        print("sad")


if __name__ == "__main__":

    app = InstantScale()
    app.geometry("1024x512")
    app.mainloop()

