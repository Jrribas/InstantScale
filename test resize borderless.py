import tkinter as tk
from tkinter import ttk


class Ruler(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.txt_ticks = []
        self.big_ticks = 0
        self.small_ticks = 0
        self.pixel = 0
        self.refline = None
        self.reftxt = None

        self.overrideredirect(True)
        self.wm_geometry("200x50")
        self.wm_minsize(25, 60)
        self.wm_maxsize(800, 100)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas['background'] = 'yellow2'

        self.grip = ttk.Sizegrip(self)
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        self.grip.bind("<B1-Motion>", self.OnMotion)

        self.label = tk.Label(self, text="Click on the grip to move")
        self.grip = tk.Label(self, bitmap="gray25")
        self.grip.place(relx=0.0, rely=1.0, anchor="sw")

        self.grip.bind("<ButtonPress-1>", self.start_window_move)
        self.grip.bind("<ButtonRelease-1>", self.stop_window_move)
        self.grip.bind("<B1-Motion>", self.on_window_move)

        self.bind("<ButtonPress-1>", self.send_number)
        self.bind("<ButtonRelease-3>", self.exit)

        self.center(self)

        self.after(100, self.updates)

    def exit(self, event):
        self.destroy()

    def send_number(self, event):
        print(self.pixel)

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

        self.small_ticks_coord = [x * 10 for x in range(1, self.small_ticks + self.big_ticks) if not x % 5 == 0]

        for i in self.small_ticks_coord:

            self.canvas.create_line(i, 0, i, 10)

    def draw_reference_line(self):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()

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

        #Avoid bad geometry error
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

    @staticmethod
    def center(win):
        # Center About window in any display resolution
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


app=Ruler()
app.mainloop()