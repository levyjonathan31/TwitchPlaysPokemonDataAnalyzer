from PIL import Image, ImageGrab
from pytesseract import pytesseract
from pytesseract import image_to_string
import numpy as np
import re
import time
import cv2
# SETUP
# ----------------------------------------
# Define path to tessaract.exe
path_to_tesseract = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

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


def get_text(img):

    # Extract text from image
    text = image_to_string(img,
                           lang='tpp_roo')
    # Remove end of line characters
    text = text.replace('\n', ' ')

    # Remove all commas (from numbers)
    text = text.replace(',', '')
    return text


def get_bets(text):
    # Combine all text into 1 line

    match = re.findall(
        r'[@][A-Za-z0-9_]+ \bplaced a \b[P][0-9,]+ \bbet on\b (?:red|blue)', text)
    for i in match:
        # get name of user
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


def determine_bet(list_of_bets_red, list_of_bets_blue):
    # get ratio of red to blue bets
    ratio = sum_bets(list_of_bets_red) / sum_bets(list_of_bets_blue)
    team = ""
    if ratio > 1.5:
        return "red " + str(ratio)
    elif ratio < 0.5:
        return "blue " + str(ratio)
    else:
        return "hold " + str(ratio)
# MAIN
# ----------------------------------------


while True:
    ss_region = (2000, 450, 2550, 850)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("chat.png")
    ss_img = cv2.imread("chat.png")
    # only show black
    ss_img = cv2.inRange(ss_img, (0, 0, 0), (20, 20, 20))
    # invert black and white
    ss_img = cv2.bitwise_not(ss_img)
    cv2.imwrite("chat.png", ss_img)
    # save img
    time.sleep(0.2)
    text = get_text(ss_img)
    get_bets(text)
    print(list_of_bets_blue)
    print(list_of_bets_red)
    print("Sum of blue bets: ", sum_bets(list_of_bets_blue))
    print("Sum of red bets: ", sum_bets(list_of_bets_red))
    with open("output.txt", "w") as f:
        f.write(get_text("chat.png"))
    if text.find("The match starts in 5 seconds") != -1:
        break

# Determine bet
print(determine_bet(list_of_bets_red, list_of_bets_blue))
