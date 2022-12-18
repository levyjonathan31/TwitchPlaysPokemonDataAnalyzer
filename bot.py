import os
from random import random
import pyperclip
import pyautogui
import numpy as np
import re
import time
import keyboard


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
    pyautogui.moveTo(1580, 950)
    # press crtl + c
    pyautogui.hotkey('ctrl', 'c')
    # get text from clipboard with pyperclip
    text = pyperclip.paste()
    time.sleep(0.1)
    pyautogui.click(button='left')
    pyautogui.click(button='left')
    return text

def get_bets(text, list_red, list_blue):

    match = re.findall(
        r'[@][A-Za-z0-9_]+ \bplaced a \b[P][0-9,]+ \bbet on\b (?:red|blue)', text)
    for i in match:
        # get name of user
        name = i[1:i.find(' ')]
        val = i[i.find('placed a P') + 10: i.find(' bet on')]
        val = re.sub(",","", val)
        if 'red' in i:
            list_red[name] = int(val)
        else:
            list_blue[name] = int(val)


def sum_bets(list_of_bets):
    total = 0
    for i in list_of_bets:
        total += list_of_bets[i]
    return total


def determine_bet(list_of_bets_red, list_of_bets_blue):
    # get ratio of red to blue bets
    if sum_bets(list_of_bets_blue) == 0:
        return
    ratio = sum_bets(list_of_bets_red) / sum_bets(list_of_bets_blue)
    # accounts for number of people betting and modifies ratio.
    ratio = ratio * len(list_of_bets_red) / len(list_of_bets_blue)
    team = ""
    if ratio > 1.11:
        print("red " + str(ratio))
        make_bet(ratio, "red")
    elif ratio < 0.9:
        print("blue " + str(ratio))
        ratio = 1/ratio
        make_bet(ratio, "blue")
    else:
        print("hold " + str(ratio))
def make_bet(ratio, team):
    pyautogui.moveTo(1670, 950)
    pyautogui.mouseDown(button='left')
    bet = round(10*ratio)
    if (bet > 50):
        bet = 50
    pyautogui.write("!bet " + str(bet) + "% " + team)
    pyautogui.press('Enter')


def wait_for_match():
    while True:
        if keyboard.is_pressed('0'):
            return True
        text = get_text()
        time.sleep(0.5)
        if text.find("A new match is about to begin!") != -1:
            print("Match started!")
            return False
# MAIN
# ----------------------------------------
def main():
    list_of_bets_red = {}
    list_of_bets_blue = {}
    kill = False
    while not kill:
        if keyboard.is_pressed('0'):
            kill = True
            break
        text = get_text()
        get_bets(text, list_of_bets_red, list_of_bets_blue)
        print("Sum of blue bets: ", sum_bets(list_of_bets_blue))
        print("Sum of red bets: ", sum_bets(list_of_bets_red))
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(text)
        if text.find("The match starts in 5 seconds") != -1:
            time.sleep((3*random()))
            determine_bet(list_of_bets_red, list_of_bets_blue)
            list_of_bets_red = {}
            list_of_bets_blue = {}
            kill = wait_for_match()
        time.sleep(0.5)
   
main()