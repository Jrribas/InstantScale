from tkinter.colorchooser import askcolor

def colour():
    color = askcolor()
    return color


def contrasting_text_color(rgb):

    for i in range(0, 3):
        d = rgb[i] / 255.0

        print(d)

        if d <= 0.03928:
            rgb[i] = d / 12.92
        else:
            rgb[i] = ((d + 0.055) / 1.055) ** 2.4

    L = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

    return L

rgbList = list(colour()[0])

cenas = contrasting_text_color(rgbList)

print(cenas)


