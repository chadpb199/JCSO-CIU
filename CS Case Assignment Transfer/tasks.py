from pynput import mouse as m, keyboard as k
from time import sleep

mouse = m.Controller()
keyboard = k.Controller()

finish_task_link = (1820, 680)
terminal = (-1000, 1000)

for i in range(141):
    mouse.position = finish_task_link
    mouse.click(m.Button.left)
    sleep(1)
    keyboard.type("Case Assigned.")
    keyboard.press(k.Key.tab)
    keyboard.release(k.Key.tab)
    keyboard.press(k.Key.enter)
    keyboard.release(k.Key.enter)

    mouse.position = terminal
    mouse.click(m.Button.left)

    sleep(1)

    # if input("Continue? (y/n) ") == "n":
    #     break

