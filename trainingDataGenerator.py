import random
import string
import time
import math
from pynput import keyboard, mouse
from pynput.mouse import Button, Controller
from PIL import Image, ImageGrab


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    # round to nearest decimal
    print("{0}:{1}:{2}".format(int(hours), int(mins), round(sec, 2)))


TRAIN_ON_ITALICS = True
NUMBER_OF_ITERATIONS = 10000
# Speed multiplier
# Speed = 1 is around 100 message per 430 seconds
# Speed = 10 is around 100 message per 43 seconds
start_time = time.time()
SPEED = 8
print("You are sending about 100 messages every " +
      str(round(430/SPEED, 2)) + " seconds")
print("Estimated time to complete: ")
time_convert((1/SPEED)*(NUMBER_OF_ITERATIONS * 4.3))
print("Starting in 5 seconds...")
time.sleep(5)
print("Generating training data...")

# letters and numbers and characters of my choosing
letters = f'{string.ascii_letters}{string.digits}!@:,'
buffer = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopq'
mouse = mouse.Controller()
# twitch chat box
mouse.position = (1200, 700)
time.sleep(0.2)
mouse.click(Button.left)
keyboard = keyboard.Controller()
for k in range(0, NUMBER_OF_ITERATIONS):
    sentence = ''
    # Resets random seed every iteration
    keyboard.press('/')
    # random sleep times due to paranoia
    if (TRAIN_ON_ITALICS):
        time.sleep((1/SPEED)*random.randint(500, 2000)/48000)
        keyboard.press('m')
        time.sleep((1/SPEED)*random.randint(500, 2000)/48000)
        keyboard.press('e')
        time.sleep((1/SPEED)*random.randint(500, 2000)/48000)
        keyboard.press(' ')
    random.seed(round(time.time()*1000))
    for i in range(random.randint(1, 3)):
        for j in range(random.randint(1, 10)):
            sentence += random.choice(letters)
        sentence += ' '
    for i in buffer:
        keyboard.press(i)
        time.sleep((1/SPEED)*random.randint(500, 2000)/48000)
        keyboard.release(i)
    for i in sentence:
        keyboard.press(i)
        time.sleep((1/SPEED)*random.randint(500, 2000)/48000)
        keyboard.release(i)
    keyboard.press(keyboard._Key.enter)
    time.sleep((1/SPEED)*random.randint(50, 100)/100)
    ss_region = (2000, 1150, 2550, 1180)
    ss_img = ImageGrab.grab(ss_region)
    imgIdentifier = str(round(time.time()*1000))
    ss_img.save("GeneratedTestData/data_" + imgIdentifier + ".png")
    f = open("GeneratedTestData/data_" + imgIdentifier + ".gt.txt", "w")
    f.write(sentence)
    time.sleep((1/SPEED)*random.randint(50, 200)/400)
print("Training data generated!")
end_time = time.time()
time_lapsed = end_time - start_time
time_convert(time_lapsed)
