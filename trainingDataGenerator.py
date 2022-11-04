import random
import string
import time
from pynput import keyboard, mouse
from pynput.mouse import Button, Controller
from PIL import Image, ImageGrab
# letters and numbers and characters of my choosing
letters = string.ascii_letters + string.digits + '!' + '@' + ':' + ','
sentence = ''
mouse = mouse.Controller()
# twitch chat box
mouse.position = (1200, 700)
time.sleep(0.2)
mouse.click(Button.left)
keyboard = keyboard.Controller()
for i in range(0, 100):
    keyboard.press('/')
    # random sleep times due to paranoia
    time.sleep(random.randint(1, 2)/48)
    keyboard.press('m')
    time.sleep(random.randint(1, 2)/48)
    keyboard.press('e')
    time.sleep(random.randint(1, 2)/48)
    keyboard.press(' ')
    for i in range(random.randint(1, 7)):
        for i in range(random.randint(1, 15)):
            sentence += random.choice(letters)
        sentence += ' '
    for i in sentence:
        keyboard.press(i)
        time.sleep(random.randint(1, 2)/48)
        keyboard.release(i)
    keyboard.press(keyboard._Key.enter)

    ss_region1 = (2000, 770, 2550, 800)
    ss_region2 = (2000, 800, 2550, 830)
    ss_region3 = (2000, 830, 2550, 860)
    ss_region4 = (2000, 860, 2550, 890)
    ss_img1 = ImageGrab.grab(ss_region1)
    ss_img2 = ImageGrab.grab(ss_region2)
    ss_img3 = ImageGrab.grab(ss_region3)
    ss_img4 = ImageGrab.grab(ss_region4)
    ss_img1.save("GeneratedTestData/data" + str(i) + ".1" + ".png")
    ss_img2.save("GeneratedTestData/data" + str(i) + ".2" + ".png")
    ss_img3.save("GeneratedTestData/data" + str(i) + ".3" + ".png")
    ss_img4.save("GeneratedTestData/data" + str(i) + ".4" + ".png")
    time.sleep(random.randint(1, 2))

# Grab Image
