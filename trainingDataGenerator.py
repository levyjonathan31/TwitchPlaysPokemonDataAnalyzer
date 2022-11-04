import random
import string
import time
from pynput import keyboard, mouse
from pynput.mouse import Button, Controller
from PIL import Image, ImageGrab

TRAIN_ON_ITALICS = True
# letters and numbers and characters of my choosing
letters = f'{string.ascii_letters}{string.digits}!@:,'
buffer = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopq'
mouse = mouse.Controller()
# twitch chat box
mouse.position = (1200, 700)
time.sleep(0.2)
mouse.click(Button.left)
keyboard = keyboard.Controller()
for i in range(0, 1):
    sentence = ''
    # Resets random seed every iteration
    keyboard.press('/')
    # random sleep times due to paranoia
    if (TRAIN_ON_ITALICS):
        time.sleep(random.randint(1000, 3000)/48000)
        keyboard.press('m')
        time.sleep(random.randint(1000, 3000)/48000)
        keyboard.press('e')
        time.sleep(random.randint(1000, 3000)/48000)
        keyboard.press(' ')

    for i in range(random.randint(1, 4)):
        random.seed(round(time.time()*1000))
        for j in range(random.randint(1, 12)):
            time.sleep(0.01)
            sentence += random.choice(letters)
        sentence += ' '
    for i in buffer:
        keyboard.press(i)
        time.sleep(random.randint(1000, 2000)/48000)
        keyboard.release(i)
    for i in sentence:
        keyboard.press(i)
        time.sleep(random.randint(1000, 2000)/48000)
        keyboard.release(i)
    keyboard.press(keyboard._Key.enter)
    time.sleep(random.randint(100, 200)/100)
    ss_region = (2000, 1150, 2550, 1180)
    ss_img = ImageGrab.grab(ss_region)
    imgIdentifier = str(round(time.time()*1000))
    ss_img.save("GeneratedTestData/data_" + imgIdentifier + ".png")
    f = open("GeneratedTestData/data_" + imgIdentifier + ".txt", "w")
    f.write(sentence)

    time.sleep(random.randint(100, 200)/100)
