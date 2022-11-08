import random
import string
import time
import math
import pyperclip
import cv2
from pynput import keyboard, mouse
from pynput.mouse import Button, Controller
from PIL import Image, ImageGrab
# Settings
# ----------------------------------------
TRAIN_ON_ITALICS = True
USE_WORDLIST = True
NUMBER_OF_ITERATIONS = 100
SPEED = 0.6

# Variables
# ----------------------------------------
letters = f'{string.ascii_letters}{string.digits}!@:,_'
buffer = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopq'


# Functions
# ----------------------------------------


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    # round to nearest decimal
    print("{0}:{1}:{2}".format(int(hours), int(mins), round(sec, 2)))


def italic_training():
    keyboard.press('/')
    time.sleep((1/SPEED)*random.randint(500, 2000)/48000)
    keyboard.press('m')
    time.sleep((1/SPEED)*random.randint(500, 2000)/48000)
    keyboard.press('e')
    time.sleep((1/SPEED)*random.randint(500, 2000)/48000)
    keyboard.press(' ')


def sentece_generator(trainOnItalics, useWordlist):
    sentence = ''
    random.seed(round(time.time()*1000))
    if trainOnItalics:
        italic_training()
    for i in range(random.randint(1, 3)):
        for j in range(random.randint(1, 10)):
            if useWordlist:
                # choose 5 random letters from buffer
                name = ''.join(random.choice(buffer)
                               for i in range(random.randint(5, 15)))
                word_bank = ['placed a P' +
                             str(random.randint(0, 20000)) +
                             ' ', 'bet on ', 'blue. ', 'red. ',
                             '@' + buffer[random.randint(0, 25)] + ' ']
                sentence += word_bank[random.randint(0, len(word_bank)-1)]
            else:
                sentence += random.choice(letters)
        sentence += ' '
    return sentence


def paste_to_chat(sentence):
    pyperclip.copy(sentence)
    keyboard.press(keyboard._Key.ctrl)
    keyboard.press('v')
    time.sleep((1/SPEED)*random.randint(1000, 2000)/2000)
    keyboard.release('v')
    keyboard.release(keyboard._Key.ctrl)
    time.sleep((1/SPEED)*random.randint(1000, 2000)/2000)
    keyboard.press(keyboard._Key.enter)


def get_image_and_text(s):
    ss_region = (2000, 1150, 2550, 1180)
    ss_img = ImageGrab.grab(ss_region)
    imgIdentifier = str(round(time.time()*1000))
    ss_img.save("TestData/data_" + imgIdentifier + ".png")
    ss_img = cv2.imread("TestData/data_" + imgIdentifier + ".png")
    # only show black
    ss_img = cv2.inRange(ss_img, (0, 0, 0), (28, 28, 28))
    # invert black and white
    ss_img = cv2.bitwise_not(ss_img)
    cv2.imwrite("TestData/data_" + imgIdentifier + ".png", ss_img)
    f = open("TestData/data_" + imgIdentifier + ".gt.txt", "w")
    f.write(s)
# MAIN


start_time = time.time()
print("Estimated time to complete: ")
time_convert((1/SPEED)*(NUMBER_OF_ITERATIONS*1.5))
print("Starting in 5 seconds...")
time.sleep(5)
print("Generating training data...")


mouse = mouse.Controller()
# twitch chat box
mouse.position = (1200, 700)
time.sleep(0.2)
mouse.click(Button.left)
keyboard = keyboard.Controller()
for k in range(0, NUMBER_OF_ITERATIONS):
    sentence = sentece_generator(TRAIN_ON_ITALICS, USE_WORDLIST)
    paste_to_chat(sentence)
    get_image_and_text(sentence)
    time.sleep((1/SPEED)*random.randint(100, 200)/500)
print("Training data generated!")
end_time = time.time()
time_lapsed = end_time - start_time
time_convert(time_lapsed)
