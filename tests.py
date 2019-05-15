
scale = 444
units = "µm"
targetValue = 500
targetUnits = "mm"
width = 1280
scaleNumb = 1

conv_dict = {"mmµm": 1000, "mmnm": 1000000, "µmmm": 0.001, "µmnm": 1000, "nmmm": 0.000001, "nmµm": 0.001,
             "µmµm": 1, "nmnm": 1, "mmmm": 1}

key = units + targetUnits
print(key)
check = (((1 / conv_dict[key]) * scale) / scaleNumb)
print(check)

if conv_dict[key] < 1 or (conv_dict[key] == 1 and scaleNumb < targetValue):
    print(check * targetValue, 0.8 * width)
    if check * targetValue > 0.8 * width:
        message = "max"
        maxValue = (0.8 * width) / scale * scaleNumb
        print(0.8 * width / scale, width, scaleNumb, scale)
        print((0.8 * width) / scale * scaleNumb, scaleNumb)
        print(message + " value is : " + str(round(maxValue - maxValue*0.005)) + " " + units)
elif conv_dict[key] > 1 or (conv_dict[key] == 1 and scaleNumb > targetValue):
    if check * targetValue < 30:
        message = "min"
        print(message + " value is : " + str(round(30 / check) + 1) + " " + targetUnits)

newScaleNumb = targetValue
units = targetUnits
newScale = check * targetValue




