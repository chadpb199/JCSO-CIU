from pynput import mouse as m, keyboard as k
from time import sleep

# create mouse and keyboard controllers
mouse = m.Controller()
keyboard = k.Controller()

# declare locations to put the mouse cursor
edit_link = (383, 441)
remove_link = (1055, 510)

while True:
	cycles = int(input("Cycles: "))
	
	for i in range(cycles):
		mouse.position = edit_link
		mouse.click()
	
		sleep(0.5)
	
		mouse.position = remove_link
		mouse.click()
		
	if input("Continue? (y/n): ") == "n":
		break