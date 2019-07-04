from cx_Freeze import setup, Executable
import os
import sys

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

os.environ['TCL_LIBRARY'] = r'C:\Users\joaor\Anaconda3\envs\setup\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\joaor\Anaconda3\envs\setup\tcl\tk8.6'

includes = []
include_files = [r"C:\Users\joaor\Anaconda3\DLLs\tcl86t.dll",
                 r"C:\Users\joaor\Anaconda3\DLLs\tk86t.dll",
                 'Tesseract-OCR/',
                 'images/',
                 r"icon.ico"]

packages = ["numpy", "tkinter"]

setup(name='InstantScale',
      version='3.0',
      description='Parse stuff',
      options={"build_exe": {"includes": includes, "include_files": include_files, "packages": packages}},
      executables=[Executable("main.py", base=base, targetName="InstantScale.exe", shortcutName="InstantScale",
                              shortcutDir="DesktopFolder", icon="icon.ico")])
