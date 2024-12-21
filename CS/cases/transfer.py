from pynput import mouse as m, keyboard as k
from time import sleep

mouse = m.Controller()
keyboard = k.Controller()

# # testing to find all of the relevant mouse positions
# while True:
#     print("Current pointer position: {0}".format(mouse.position))

# relevant mouse positions
case_num_search_entry = (830, 128)
search_button = (242, 417)
case_record = (242, 468)
# approval_link = (1433, 98)
# kick_back_link = (1087, 285)
edit_case_info_link = (1019, 105)
edit_anyway_link = (560,64)
investigator_dd = (400, 205)
save_close_button = (225, 64)
approve_link = (1128, 190)
close_record = (1900,35)
terminal = (-1000, 1000)

comment = "Transfer case assignment from Omnigo."

# get cases to transfer
with open("cases.txt", "r") as f:
    cases = [line.split() for line in f]

finished_cases = []

print(cases)

def tab(tabs: int):
    for i in range(tabs):
        keyboard.press(k.Key.tab)
        keyboard.release(k.Key.tab)

def transfer():
    """Transfer a case investigator assignment from Omnigo to CentralSquare.
    """

    for i in cases:
        # get case # to transfer
        case = i[1]
        investigator = i[0]
        input(f"Confirm:\nCase #: {i[1]}\tInvestigator: {i[0]}")

        # remove case from the list
        finished_cases.append(i)

        # search for the case #
        mouse.position = case_num_search_entry
        mouse.click(m.Button.left, 3)

        keyboard.type(case)
        keyboard.press(k.Key.enter)
        keyboard.release(k.Key.enter)
        sleep(1)

        # open the searched case record and wait for loading
        mouse.position = case_record
        mouse.click(m.Button.left, 2)
        sleep(3)

        # # kick back the case and wait
        # mouse.position = approval_link
        # mouse.click(m.Button.left)
        # sleep(1)

        # mouse.position = kick_back_link
        # mouse.click(m.Button.left)
        # sleep(2)

        # keyboard.type("51")
        # sleep(1)
        # tab(1)
        # keyboard.type(comment)
        # sleep(1)
        # tab(1)
        # keyboard.press(k.Key.enter)
        # keyboard.release(k.Key.enter)

        # sleep(3)

        # edit the case info
        mouse.position = edit_case_info_link
        mouse.click(m.Button.left)
        sleep(3)

        mouse.position = edit_anyway_link
        mouse.click(m.Button.left)
        sleep(2)

        mouse.position = investigator_dd
        mouse.click(m.Button.left, 2)
        keyboard.type(investigator)
        tab(2)
        keyboard.type("A")
        tab(3)
        keyboard.type(comment)
        sleep(1)
        tab(5)
        keyboard.type("J")
        tab(1)


        # prompt the user to change the case incident code manually
        mouse.position = terminal
        mouse.click(m.Button.left)
        input("Change incident code manually. Press enter to continue.")

        mouse.position = save_close_button
        mouse.click(m.Button.left)
        sleep(3)

        # # reapprove case
        # mouse.position = approve_link
        # mouse.click(m.Button.left)
        # sleep(2)
        # keyboard.type(comment)
        # tab(6)
        # keyboard.press(k.Key.enter)
        # keyboard.release(k.Key.enter)
        # sleep (5)

        #close case record
        mouse.position = close_record
        mouse.click(m.Button.left)

        # return focus to terminal and prompt to continue
        mouse.position = terminal
        mouse.click(m.Button.left)
        if input("Continue? (y/n) ") == "n":
            break

if __name__ == "__main__":
    input("Begin?")
    transfer()

    with open("cases.txt", "w"):
        pass

    with open("cases.txt", "a") as f:
        cases = [i for i in cases if i not in finished_cases]
        for i in cases:
            f.write(f"{i[0]}\t{i[1]}\n")