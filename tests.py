"""Read-only Ttk.Combobox style demo module.

The style of the second combobox has been slightly modified to
make text background match with combobox background when out of
focus.

In read-only state (which is default) you can notice that text
background gets white in the first (original styled) combobox
when focus moves towards. Second combobox looks nice then.

With the button you can test that the two works exactly the same
in writeable state.
"""

from random import randint
from tkinter import Button, Frame, StringVar, Tk
from tkinter.ttk import Combobox, Style

class App(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.state = None
        self.style = Style()
        self.style.map("Alt.TCombobox",
            selectbackground=[
                ('!readonly', '!focus', 'SystemWindow'),
                ('readonly', '!focus', 'SystemButtonFace'),
                ],
            )
        self.button = Button(self, text="Change state!",
            command=self.switch)
        self.cbox1var, self.cbox2var = StringVar(), StringVar()
        self.cbox1 = Combobox(self,
            exportselection=0,
            values=["sex", "sleep", "eat", "drink", "dream",],
            textvariable=self.cbox1var,
            )
        self.cbox1.bind('<<ComboboxSelected>>', self.bfocus)
        self.cbox1.current(1)
        self.cbox2 = Combobox(self,
            exportselection=0,
            values=["fear", "clarity", "power", "old age",],
            style="Alt.TCombobox",
            textvariable=self.cbox2var,
            )
        self.cbox2.bind('<<ComboboxSelected>>', self.bfocus)
        self.cbox2.current(3)
        self.cbox1.pack()
        self.cbox2.pack()
        self.button.pack()
        self.switch()

    def bfocus(self, *args):
        if randint(0,1):
            self.button.focus()
            print('Focus moved!')
        else:
            print('Focus stayed.')

    def switch(self):
        if self.state == ['readonly']:
            self.state = ['!readonly']
            print('State is writeable!')
        else:
            self.state = ['readonly']
            print('State is read-only!')
        self.cbox1.state(self.state)
        self.cbox2.state(self.state)

if __name__ == "__main__":
    root = Tk()
    root.title('ttk.Combobox styling')
    App(root).pack()
    root.mainloop()