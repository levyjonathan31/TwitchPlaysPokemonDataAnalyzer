import os
from random import random
import pyperclip
import pyautogui
import numpy as np
import re
import time
import cv2
# SETUP
# # ----------------------------------------
# # Define path to tessaract.exe
# path_to_tesseract = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# # Point tessaract_cmd to tessaract.exe
# pytesseract.tesseract_cmd = path_to_tesseract

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


def get_text():
    pyautogui.moveTo(1580, 350)
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(1580, 900)
    # press crtl + c
    pyautogui.hotkey('ctrl', 'c')
    # get text from clipboard with pyperclip
    text = pyperclip.paste()
    time.sleep(0.1)
    pyautogui.click(button='left')
    pyautogui.click(button='left')
    return text

def get_bets(text):

    match = re.findall(
        r'[@][A-Za-z0-9_]+ \bplaced a \b[P][0-9,]+ \bbet on\b (?:red|blue)', text)
    for i in match:
        # get name of user
        name = i[1:i.find(' ')]
        val = i[i.find('placed a P') + 10: i.find(' bet on')]
        val = re.sub(",","", val)
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
    if ratio > 1.25:
        print("red " + str(ratio))
        make_bet(ratio, "red")
    elif ratio < 0.75:
        print("blue " + str(ratio))
        ratio = 1/ratio
        make_bet(ratio, "blue")
    else:
        print("hold " + str(ratio))
def make_bet(ratio, team):
    pyautogui.moveTo(1670, 900)
    pyautogui.mouseDown(button='left')
    bet = round(10*ratio, 0)
    if (bet > 25):
        bet = 25
    pyautogui.write("!bet " + str(bet) + "% " + team)
    pyautogui.press('Enter')



# MAIN
# ----------------------------------------
def main():
    while True:
        text = get_text()
        get_bets(text)
        print(list_of_bets_blue)
        print(list_of_bets_red)
        print("Sum of blue bets: ", sum_bets(list_of_bets_blue))
        print("Sum of red bets: ", sum_bets(list_of_bets_red))
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(text)
        if text.find("The match starts in 10 seconds") != -1:
            time.sleep(2+(3*random()))
            determine_bet(list_of_bets_red, list_of_bets_blue)
            break
        time.sleep(0.5)
main()