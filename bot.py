from PIL import Image, ImageGrab
from pytesseract import pytesseract
from pytesseract import image_to_string
import os
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


def get_text(img_path, num_of_lines):
    combined_text = ""
    for img in os.listdir(img_path):
        filePath = os.path.join(img_path, img)
        img = Image.open(filePath)
        # Extract text from image
        text = image_to_string(img,
                               lang='eng_best_tpp')
        # Remove end of line characters
        text = text.replace('\n', ' ')

        # Remove all commas (from numbers)
        text = text.replace(',', '')

        combined_text += text
    return combined_text


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


def get_images(num):
    start = 750
    spacing = 28
    for i in range(num):
        ss_img = ImageGrab.grab(bbox=(start, 0, start + 28, 28))
        ss_img.save("TestData/Line" + str(i) + ".png")
        ss_img = cv2.imread("TestData/Line" + str(i) + ".png")
        ss_img = cv2.inRange(ss_img, (0, 0, 0), (28, 28, 28))
        ss_img = cv2.bitwise_not(ss_img)
        start += spacing
        cv2.imwrite("TestData/Line" + str(i) + ".png", ss_img)

# MAIN
# ----------------------------------------


while True:

    # save img
    time.sleep(0.2)
    num_of_lines = 4
    img_path = "TestData"
    get_images(num_of_lines)
    text = get_text(img_path, num_of_lines)
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
