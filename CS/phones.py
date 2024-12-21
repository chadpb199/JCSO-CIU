from pynput import mouse as m, keyboard as k
from time import sleep

# create mouse and keyboard controllers
mouse = m.Controller()
keyboard = k.Controller()

def mouse_move_and_click(location:tuple, button=m.Button.left):
    mouse.position = location
    mouse.click(button)

# declare locations to put the mouse cursor
edit_link = (375, 440)
remove_link = (1055, 510)
terminal = (-900, 800)

while True:
    cycles = int(input("Cycles: "))
	
    for i in range(cycles):
        mouse_move_and_click(edit_link)
        
        sleep(0.5)
        
        mouse_move_and_click(remove_link)
        
        sleep(0.5)
        
    mouse_move_and_click(terminal)
		
    if input("Continue? (y/n): ") == "n":
        break