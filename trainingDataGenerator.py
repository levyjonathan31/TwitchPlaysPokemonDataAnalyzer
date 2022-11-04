import random
import string
import time
from pynput import keyboard, mouse
from pynput.mouse import Button, Controller
# letters and numbers
letters = string.ascii_letters + string.digits + '!' + '@' + ':' + ','
sentence = ''
mouse = mouse.Controller()
mouse.position = (1200, 700)
time.sleep(0.2)
mouse.click(Button.left)
keyboard = keyboard.Controller()

for i in range(0, 100):
    keyboard.press('/')
    keyboard.press('m')
    keyboard.press('e')
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

    time.sleep(random.randint(1, 2))
  