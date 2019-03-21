from tkinter import filedialog
import os

ola = filedialog.askopenfilenames()

filename, fileExtension = os.path.splitext(os.path.basename(ola[0]))

print(ola, filename)
