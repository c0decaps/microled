#!/usr/bin/python3
import sys, os, math
from PIL import Image

# set this according to your needs
# needs to be divisible by 8 (for now)
DISPLAY_IMAGE_WIDTH  = 128
DISPLAY_IMAGE_HEIGHT = 32
debug = False

if len(sys.argv) < 2:
    print("no image passed")
    quit()

def avg_color(img, x, y, width, height):
    r=0
    g=0
    b=0
    for current_y in range(height):
        for current_x in range(width):
            r += img[x+current_x, y+current_y][0]
            g += img[x+current_x, y+current_y][1]
            b += img[x+current_x, y+current_y][2]
    area_size = width*height
    r = r/area_size
    g = g/area_size
    b = b/area_size
    return (r,g,b)
            
def is_pixel_active_in_oled(img, x, y, width, height, threshhold):
    rgb_val = avg_color(img, x, y, width, height)
    brightness = (rgb_val[0] + rgb_val[1] + rgb_val[2])/3
    if brightness < threshhold:
        if debug:
            print("Brightness "+str(brightness)+" should be too low")
        return False
    if debug:
        print("Brightness "+str(brightness)+" should be above threshhold")
    return True

im = Image.open(sys.argv[1])
pixels = im.load()
img_height = im.size[1]
img_width = im.size[0]
# the input image wont be the same size as the wanted size so there needs to be a transformation
# this is done by summarizing an area of pixels into a single pixel in the oled, realized by the functions defined above
area_width = math.floor(DISPLAY_IMAGE_WIDTH/img_width)
area_height= math.floor(DISPLAY_IMAGE_HEIGHT/img_height)
amount_areas_x = DISPLAY_IMAGE_WIDTH
amount_areas_y = DISPLAY_IMAGE_HEIGHT
amount_bytes_per_row = math.floor(DISPLAY_IMAGE_HEIGHT/8)
rows = []
for row_index in range(amount_areas_y):
    row = []
    for in_row_index in range(amount_areas_x):
        result = is_pixel_active_in_oled(pixels, in_row_index, row_index, area_width, area_height, 40)
        if result and debug:
            print(result)
        if result:
            row.append(1)
        else:
            row.append(0)
    rows.append(row)

decimal_rows = []
for y in range(len(rows)):
    row_value = 0
    for x in range(len(rows[y])):
        if rows[y][len(rows[y])-1-x] == 1:
            row_value += 2**x
    decimal_rows.append(row_value)

print(decimal_rows)

with open('main.py', 'w') as file:
    file.write("import ssd1306\n")
    file.write("from machine import I2C, Pin\n\n")
    file.write("i2c = I2C(-1, scl=Pin(5), sda=Pin(4))\n")
    file.write("display = ssd1306.SSD1306_I2C(128, 32, i2c)\n")
    file.write("lines = [")
    rows_strings = []
    for decimal_row_number in range(len(decimal_rows)):
        file.write(str(decimal_rows[decimal_row_number]))
        if decimal_row_number != len(decimal_rows)-1:    
            file.write(",")
    file.write("]\n")
    file.write("def draw_img(img, x, y, display):\n")
    file.write("    display.fill(0)\n")
    file.write("    line_bits = []\n")
    file.write("    for line in lines:\n")
    file.write("        raw_line_bits = bin(line)[2:]\n")
    file.write("        diff = 128 - len(raw_line_bits)\n")
    file.write("        prefix = ''\n")
    file.write("        for i in range(diff):\n")
    file.write("            prefix += '0'\n")
    file.write("        true_line_bits = prefix + raw_line_bits\n")
    file.write("        line_bits.append(true_line_bits)\n")
    file.write("    for line in range(len(line_bits)):\n")
    file.write("        for bit in range(len(line_bits[line])):\n")
    file.write("            if line_bits[line][bit] == '1':\n")
    file.write("                display.pixel(bit, line, 1)\n")
    file.write("    display.show()\n\n")
    file.write("draw_img(lines, 0, 0, display)\n")
    file.close()
if debug:
    print(rows_strings)
