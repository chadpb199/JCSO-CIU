from pynput import mouse as m, keyboard as k
from time import sleep
import argparse

# declare sys arguments
parser = argparse.ArgumentParser(
    prog="File Tag Remover",
    description="Removes erroneous file tags in Autopsy.",
    )
    
parser.add_argument("-c", "--check",
    action="store_true",
    dest="check",
    help="Print the cursor location on a loop to find the link locations."
    )
    
parser.add_argument("-i", "--initial", nargs=2)
    
parser.add_argument("-t", "--terminal", nargs=2)
    
args = parser.parse_args()
    
# create mouse and keyboard controllers
mouse = m.Controller()
keyboard = k.Controller()

# declare locations to put the mouse cursor
try:
    initial_location = tuple(args.initial)
    terminal_location = tuple(args.terminal)
except TypeError:
    print("\nWARNING: Pixel locations not provided.\n\nPrinting current cursor location.")

def print_cursor_location():
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

def remove_tags(tasks:int=1):
    """
    Remove the tags from the selected file.
    
    Args:
        range [int]:    number of iterations to perform before continue prompt
                        (default: 1)
    """
    
    for i in range(tasks):
        # move the mouse cursor to the top file location and right click it
        mouse.position = initial_location
        mouse.click(m.Button.right)
        
        # wait for loading
        sleep(0.1)
        
        # use the arrow keys to navigate the context menu
        for i in range(8):
            keyboard.tap(k.Key.down)
            sleep(0.1)
        keyboard.tap(k.Key.right)
        sleep(0.1)
        keyboard.tap(k.Key.enter)
        sleep(0.1)
    
    # return focus to terminal for user input
    mouse.position = terminal_location
    mouse.click(m.Button.left)
    
    # prompt user to continue after the specified number of iterations
    if input("Continue? (Y/n): ") == "Y":
        remove_tags(int(input("Specify number of iterations: ")))
    else:
        return
        
if __name__ == "__main__":
    
    if args.check or not (args.initial and args.terminal):
    # Print the cursor location to find the link locations if -c flag is True.
        print_cursor_location()
    else:
        # check for location args, and prompt for them if None
        if not (args.initial and args.terminal):
            initial_location = input("Initial file pixel location (# #): ")
            terminal_location = input("Terminal pixel location (# #): ")
        
        # get user input for initial number of iterations
        try:
            iterations = int(input("Specify number of iterations: "))
        except ValueError:
            iterations = 1
            
        remove_tags(iterations)