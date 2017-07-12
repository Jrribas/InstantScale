from cx_Freeze import setup, Executable
import os

exePath = os.getcwd()


os.environ['TCL_LIBRARY'] = r'C:\Users\Farinha\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Farinha\Anaconda3\tcl\tk8.6'

includes      = []
include_files = [r"C:\Users\Farinha\Anaconda3\DLLs\tcl86t.dll", \
                 r"C:\Users\Farinha\Anaconda3\DLLs\tk86t.dll",
                 r"C:\Users\Farinha\Documents\GitHub\InstantScale\TesseractPath.txt"]

buildOptions = dict(include_files = [exePath + '\\Tesseract-OCR'])

packages = ["numpy","shutil"]

setup(name='InstantScale',
    version = '0.1',
    description='Parse stuff',
    options = {"build_exe": {"includes": includes, "include_files": include_files, "packages": packages}},
    executables = [Executable("main.py",targetName="InstantScale.exe", shortcutName="InstantScale", shortcutDir="DesktopFolder", icon="icon.ico")])
