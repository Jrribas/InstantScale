from PIL import ImageTk
from tkinter import END
from PIL import Image
from cv2 import imread, imwrite
import processImage as pI
import os
import popupWindows as pW
from tkinter.colorchooser import askcolor

exePath = os.getcwd()


def readScale(self):

    # Disable manual checkbox
    self.parent.ch1.config(state='disable')

    # Update progress bar to 0
    valueStateChanger(self, self.p_bar, 0)

    # Open image
    self.img = imread(self.parent.files[self.parent.i - 1])

    # Update progress bar to 25 and update GUI
    valueStateChanger(self, self.p_bar, 25)

    # Send image to function getBar and obtain information about the "white bar in SEM images.
    self.crop_img, self.bar_img, barSize = pI.getBar(self.img)

    if barSize != 0:

        # Update entry widgets with values obtaines
        valueStateChanger(self, self.e3, round(barSize))

        # Update progress bar to 50 and update GUI
        valueStateChanger(self, self.p_bar, 50)

        # Save white bar image, resize it (for better tesseract readability), and calling it again
        height, width, channels = self.bar_img.shape
        imwrite(exePath + "\\images\\HoldImages\\bar.tif", self.bar_img)

        img = Image.open(exePath + "\\images\\HoldImages\\bar.tif")
        img1 = img.resize((width * 3, height * 3), Image.ANTIALIAS)
        img1.save(exePath + "\\images\\HoldImages\\resize_im.tif", dpi=(600, 600), quality=100)

        self.bar_img_res = imread(exePath + "\\images\\HoldImages\\resize_im.tif")

        # Measures scale bar (in pixels) from resized white bar image
        self.scale = len(pI.getScale(self.bar_img))

        # Update entry widgets with values obtained
        valueStateChanger(self, self.parent.e2, self.scale)

        # Update progress bar to 75 and update GUI
        valueStateChanger(self, self.p_bar, 75)

        # Get scale number and it's units
        self.scaleNumb, self.units = pI.getNumber(self.bar_img, self.bar_img_res, exePath)

        # Update entry widgets with values obtained
        valueStateChanger(self, self.e1, self.scaleNumb)

        # Update combobox widgets (units) with value obtained
        valueStateChanger(self, self.c1, self.units)

        # Update progress bar to 100 and update GUI
        valueStateChanger(self, self.p_bar, 100)

        # If manual checkbox is checked return widgets to normal state
        if self.parent.var.get() == 1:
            widgets = [self.e1, self.parent.e2, self.e3, self.c1, self.c2]
            for wg in widgets:
                wg.configure(state='normal')

        self.parent.ch1.config(state='normal')

    # If the program is processing several files don't show error window
    elif self.parent.save < 1:
        # If a whiter bar is not found, user must use manual
        self.parent.ch1.config(state='normal')
        pW.Error(self, "White Bar (usually where scale is) could not be determined. Use manual instead.", "error",
                 "no")
        valueStateChanger(self, self.p_bar, 0)


def preview(self):
    self.choice = 1

    # Check if an image was imported
    if hasattr(self.parent, 'img3open'):

        # Checks if all parameters are filled and if the user chose a contrast higher than 7 or chose to ignore the
        # warning the code continues to run
        if self.e1.get() == '' or self.parent.e2.get() == '' or self.e3.get() == '':
            pW.Error(self, "Please have all parameters with values, or click Read Scale.", "warning", "no")
            self.choice = 0
        elif self.contrast < 7:
            errormessage = "Contrast is less than 7. This means that visibility/readability can be compromised. \n " \
                           "We sugest a contrast higher than 7 for better scale color set :)"
            pW.Error(self, errormessage, "warning", "yes").show()

        if self.choice == 1:

            self.img = imread(self.parent.files[self.parent.i - 1])

            # Check if target value was specified
            if self.parent.var.get() == 0:
                self.targetValue = 0
                self.targetUnit = ''
            elif self.e4.get() != "":
                self.targetValue = int(self.e4.get())
                self.targetUnit = self.c2.get()
                if self.targetUnit == "":
                    pW.Error(self.parent, "If a target value is chosen, a target unit must be chosen too.", "error",
                             "no")
                    return False
            else:
                self.targetValue = 0
                self.targetUnit = ''

            # Check the new scale position
            position_dict = {"Bottom Left": 0, "Bottom Right": 1, "Top Left": 2, "Top Right": 3}
            self.position = position_dict[self.c3.get()]

            # Get parameters: Scale number, Scale units, Number of pixels, Size of the new scale.
            self.scale = int(self.parent.e2.get())
            self.sizeOfScale = int(self.spin.get())
            self.scaleNumb = int(self.e1.get())
            self.units = self.c1.get()

            # Change variable of scale colors from list of floats to tupple of integrers
            self.bgColour = tuple([int(i) for i in self.bgColour_rgb])
            self.ftColour = tuple([int(i) for i in self.ftColour_rgb])

            # Check if crop is from top or from bottom
            self.cropbeg = self.c4.get()

            # Obtain image without white bar
            self.crop_img = pI.cropImage(self.img, int(self.e3.get()), self.cropbeg)

            # Draw scale in cropped image
            self.finalImage = pI.drawScale(self.crop_img, self.scale, int(self.scaleNumb), self.units,
                                           exePath, self.position, self.sizeOfScale, self.ftColour,
                                           self.bgColour, self.targetValue, self.targetUnit)

            self.parent.img4open = self.finalImage

            # Resize image
            self.parent.img4 = ImageTk.PhotoImage(
                self.parent.img4open.resize((int(self.parent.panel2.winfo_width()) - 5,
                                             int(self.parent.panel2.winfo_height()) - 5), Image.ANTIALIAS))

            # Put image on canvas
            self.parent.panel2.itemconfig(self.parent.image_on_panel2, image=self.parent.img4)
    else:
        pW.Error(self, "Please import a image first.", "error", "no")


def manual(self):
    # Change widgets from disabled to normal

    widgets = [self.e1, self.parent.e2, self.e3, self.e4, self.c1, self.c2, self.b5]

    if self.parent.var.get() == 1:
        for wg in widgets:
            wg.configure(state='normal')
    else:
        for wg in widgets:
            wg.configure(state='disabled')


def contrastChecker(self, rgb, rgb1):
    # Calculates the contrast between the font and background color chosen
    # For more information: https://www.w3.org/TR/WCAG20-TECHS/G17#G17-procedure

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
        self.contrast = (lumi[0] + 0.05) / (lumi[1] + 0.05)

    else:
        self.contrast = (lumi[1] + 0.05) / (lumi[0] + 0.05)

    self.text.set("Contrast = %.2f" % self.contrast)

    if self.contrast >= 7:
        self.l11.config(bg="#008000")

    else:
        self.l11.config(bg="#FF0000")


def chooseColour(self, pick):
    # Check if font colour or background color is selected. label == 0 -> font colour
    if pick == "bg":
        # Window to choose color
        self.bgcolour = askcolor()

        # askcolor returns a list with the color rgb and hex codes [[rgb], hex]
        if self.bgcolour[0] is not None:
            self.bgcColour_rgb = list(self.bgcolour[0])
            # Change label background color
            self.l10.config(bg=self.bgcolour[1])
            # Calculate constrast
            contrastChecker(self, self.bgcColour_rgb, self.ftColour_rgb)
    else:
        self.ftcolour = askcolor()
        if self.ftcolour[0] is not None:
            self.ftColour_rgb = list(self.ftcolour[0])
            self.l10.config(fg=self.ftcolour[1])
            contrastChecker(self, self.bgcColour_rgb, self.ftColour_rgb)


def reset(self):
    # Resets GUI to original state

    self.parent.i = 1

    for j in range(1, len(self.parent.files) + 1):
        self.parent.img3open.close()
        os.remove(self.parent.files[j - 1])

    valueStateChanger(self, self.p_bar, 0)

    widgets = [self.e1, self.parent.e2, self.e3, self.e4]
    for wg in widgets:
        wg.configure(state='normal')
        wg.delete(0, END)
        wg.configure(state='disabled')

    self.c1.current(1)
    self.c2.current(1)

    self.parent.var.set(0)
    self.c1.configure(state='disabled')
    self.c2.configure(state='disabled')

    self.parent.img3open.close()

    if hasattr(self.parent, "img4open"):
        self.parent.img4open.close()
        del self.parent.img4open
        del self.parent.img4
        self.parent.panel2.delete("IMG2")

    del self.parent.img3open
    del self.parent.img3

    self.parent.panel.delete("IMG1")

    self.parent.image_on_panel = self.parent.panel.create_image(0, 0, anchor='nw', image=self.parent.img1,
                                                                tags="IMG1")
    self.parent.image_on_panel2 = self.parent.panel.create_image(0, 0, anchor='nw', image=self.parent.img2,
                                                                 tags="IMG2")
    self.update_idletasks()


def valueStateChanger(self, widget, value):

    str_widget = str(widget)

    if str_widget.find("entry") > -1:
        widget.configure(state='normal')
        widget.delete(0, END)
        widget.insert(END, value)
        widget.configure(state='disabled')
    elif str_widget.find("combobox") > -1:
        widget.configure(state='normal')
        widget.current(value)
        widget.configure(state='disabled')
    elif str_widget.find("progressbar") > -1:
        widget['value'] = value

    self.update_idletasks()
