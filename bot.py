from PIL import Image
from pytesseract import pytesseract
from PIL import ImageGrab
import re
import time
# SETUP
# ----------------------------------------
# Define path to tessaract.exe
path_to_tesseract = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Define path to image
path_to_image = 'images/testing2.png'

# Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = path_to_tesseract


# DATA ANALYSIS
# ----------------------------------------
list_of_bets_red = {}
list_of_bets_blue = {}

# FUNCTIONS
# ----------------------------------------


def find_nth(string, substring, n):
    if (n == 1):
        return string.find(substring)
    else:
        return string.find(substring, find_nth(string, substring, n - 1) + 1)


def get_text(path_to_image):
    # Open image with PIL
    img = Image.open(path_to_image)

    # Extract text from image
    text = pytesseract.image_to_string(img)
    text = text.replace('\n', ' ')
    return text


def get_bets(text):
    # Combine all text into 1 line

    match = re.findall(
        r'[@][a-zA-Z0-9_]+ \bplaced a \b[P][0-9]+ \bbet on\b (?:red|blue)[.]', text)
    for i in match:
        # get name
        # remove all non-alphanumeric characters
        name = i[1:i.find(' ')]
        val = i[i.find('placed a P') + 10: i.find(' bet on')]
        if 'red' in i:
            list_of_bets_red[name] = int(val)
        else:
            list_of_bets_blue[name] = int(val)


def sum_bets(list_of_bets):
    total = 0
    for i in list_of_bets:
        total += list_of_bets[i]
    return total

# MAIN
# ----------------------------------------


while True:
    ss_region = (2075, 450, 2550, 1200)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("SS3.png")
    time.sleep(1)
    text = get_text("SS3.png")
    get_bets(text)
    print(list_of_bets_blue)
    print(list_of_bets_red)
    print(sum_bets(list_of_bets_blue))
    print(sum_bets(list_of_bets_red))
    f = open("output.txt", "w")
    f.write(text)
