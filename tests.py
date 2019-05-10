def ola(o=0):

    scale = 100 # pixeis
    sizeOfScale = 4
    scaleNumb = 3
    units = "nm"
    height = 675
    width = 1024
    targetValue = 10
    targetUnits = "um"

    scaleboxwidth = width * sizeOfScale * 0.01
    scaleboxheight = (height * sizeOfScale * 0.01)/2

    values = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100,
              200, 500, 1000, 2000, 5000, 10000]

    conv_dict = {"mmum": 1000, "mmnm": 1000000, "ummm": 0.001, "umnm": 1000, "nmmm": 0.000001, "nmum": 0.001}

    check = units + targetUnits

    if scaleNumb == 1 and (1/conv_dict[check]) * scale > 0.8 * width:
        return "ola"
    elif (1/conv_dict[check]) * (scale/scaleNumb) > 0.8 * width:
        return "ola1"
    print((1/conv_dict[check]) * scale, 0.8 * width)
    print((1/conv_dict[check]) * (scale / scaleNumb), 0.8 * width)

    if units == 'nm':
        scaleNumb *= 0.001
    elif units == 'mm':
        scaleNumb *= 1000

        units = 'um'

    # Limit scale number from 1 to 500
    for val in values:
        newScale = round((val * scale) / scaleNumb)
        print(val, scale, scaleNumb, 20 * sizeOfScale, newScale, 66 * sizeOfScale)
        if 20 * sizeOfScale <= newScale <= 66 * sizeOfScale:
            if val < 1:
                newScaleNumb = int(val * 1000)
                print(1, val, newScaleNumb, units)
            elif val > 500:
                newScaleNumb = int(val / 1000)
                print(2, val, newScaleNumb, units)
            else:
                newScaleNumb = val
                print(3, val, newScaleNumb, units)
            break

    # Convert scale number to the final units.
    if targetValue != 0:
        if targetUnits == 'nm':
            val = targetValue / 1000
        elif targetUnits == 'mm':
            val = targetValue * 1000
        else:
            targetUnits = 'um'
            val = targetValue

    print(val, units)


if __name__ == "__main__":

    a=ola(1)
    print(a)
