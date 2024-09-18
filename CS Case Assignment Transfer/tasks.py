from pynput import mouse as m, keyboard as k
from time import sleep
import argparse

# declare sys arguments
parser = argparse.ArgumentParser(
    prog="Task Finisher",
    description="Finishes Investigative Assignment tasks in CentralSquare.",
    )
    
parser.add_argument("-c", "--check",
    action="store_true",
    dest="check",
    help="Print the cursor location on a loop to find the link locations."
    )
    
args = parser.parse_args()

# create mouse and keyboard controllers
mouse = m.Controller()
keyboard = k.Controller()

# declare locations to put the mouse cursor
finish_task_link = (1810, 683)
terminal = (2600, 700)

def find_links():
    """
    Print the mouse cursor location every 0.5secs in a permanent loop.
    """
    print("""
        WARNING: ENTERING PERMANENT LOOP
        """)
        
    while True:
        print(mouse.position,
        "To exit, press Ctrl + C or close this window.",
        sep="\t\t")
        sleep(0.5)
        
def finish_task(tasks:int = 1):
    """
    Finish the selected Investigative Assignment task.
    
    Args:
        range [int]:    number of tasks to finish in a row (default: 1)
    """
    
    for i in range(tasks):
        # move the mouse cursor to the "finish task" link and click it
        mouse.position = finish_task_link
        mouse.click(m.Button.left)
        
        # wait a second for loading
        sleep(1)
        
        # type the task completion comment and finish the task
        keyboard.type("Case Assigned.")
        keyboard.press(k.Key.tab)
        keyboard.release(k.Key.tab)
        keyboard.press(k.Key.enter)
        keyboard.release(k.Key.enter)
        
        # wait a second for loading
        sleep(1)

        # return focus to the terminal for user input
        mouse.position = terminal
        mouse.click(m.Button.left)
        
        if tasks == 1:
        # prompt user to continue if going task-by-task
            if input("Continue? (y/n) ") != "n":
                finish_task()
            else:
                return
        
if __name__ == "__main__":
    
    
    if args.check:
    # Print the cursor location to find the link locations if -c flag is True.
        find_links()
    else:
        # make sure user set the proper link locations
        checked = input("Did you check the link locations? (y/n) ")
        if checked != "n":
            try:
                # get the number of tasks to finish
                tasks = int(input(
                    "Enter number of tasks to finish (leave blank to go one-by-one): "
                    ))
            except ValueError:
                tasks = None
        # finish tasks either one-by-one or all in a row
            if tasks == None:
                finish_task()
            
            else:
                finish_task(tasks)
        else:
            find_links()

