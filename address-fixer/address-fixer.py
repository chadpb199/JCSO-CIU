import csv
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from tkinter.simpledialog import Dialog
from tkinter import messagebox
from ttkbootstrap.scrolled import ScrolledText
import openai
from dotenv import load_dotenv

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        
        self.title("CS Address Fixer")
        
        self.generate_gui()
        
        self.mainloop()
        
    def generate_gui(self):
    
        # create widgets
        
        self.file_select = FileSelect(
            self,
            label="Choose a .csv file..."
            )
            
        self.action_btns = ActionButtons(self)
        
        self.log = ProcessLog(self)
        
        # place widgets
        self.file_select.pack(fill=BOTH, expand=YES, pady=5)
        self.log.pack(fill=BOTH, expand=YES, pady=10, padx=5)
        self.action_btns.pack(fill=BOTH, expand=YES, pady=5)
        
        # initialize .csv handler
        self.handler = CSVHandler(self)
        

class FileSelect(ttk.Frame):
    """
    Custom frame widget containing a label, entry(for file path), and
    button(to open file dialog).
    
    Args:
        parent: Any = parent object for the frame widget
        label: str = text for the label widget
        dir: bool = whether the user should choose a file or a directory.
    """
    def __init__(self, parent, label:str, dir:bool=False):
        super().__init__(parent)
        
        # StringVar so the browse_button can update the path_entry widget.
        self.path = ttk.StringVar()
        
        # Add dir flag for file_browse func
        self.dir = dir
        
        # Root reference to access other classes in the App
        self.root = parent
        
        # Configure grid layout
        self.columnconfigure((0,2), weight=0)
        self.columnconfigure(1, weight=1)
        
        # Generate widgets
        lbl = ttk.Label(
            self,
            text=label
            )
        path_entry = ttk.Entry(
            self,
            textvariable=self.path
            )
        browse_button = ttk.Button(
            self,
            text="Browse...",
            command=self.file_browse
            )
        
        # Place widgets
        lbl.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10
            )
        path_entry.grid(
            row=1,
            column=0,
            columnspan=2, 
            sticky="nsew",
            padx=10
           )
        browse_button.grid(
            row=1,
            column=2,
            sticky="nsew",
            padx=10
            )
        
            
    def file_browse(self):
        """
        Open a file dialog to choose a .csv file to extract and update the
        entry widget.
        """
        if self.dir:
            f = filedialog.askdirectory()
            self.path.set(f)
        else:
            f = filedialog.askopenfilename()
            
            # Check if the target file is a .csv file                        
            if f.endswith(".csv"):
                self.path.set(f)
            else:
                messagebox.showerror(
                    "Error",
                    "Please select a .csv file."
                    )
        
        
class ActionButtons(ttk.Frame):
    """
    Custom frame widget containing two buttons: go_btn and cancel_btn.
    
    Args:
        parent: Any = parent object for the frame widget
    """        
    def __init__(self, parent):
        super().__init__(parent, bootstyle=SECONDARY)
        self.root = parent
        
        # go_btn to start the process
        self.go_btn = ttk.Button(
            self,
            text="Go",
            command=lambda: self.root.handler.fix_addresses(
                self.root.file_select.path.get()
                )
            )
        
        # cancel_btn to stop the process
        self.cancel_btn = ttk.Button(
            self,
            text="Cancel",
            command=self.root.destroy
            )
            
        # Place the buttons
        self.cancel_btn.pack(side=tk.RIGHT, pady=5, padx=10)
        self.go_btn.pack(side=tk.RIGHT, pady=5)
        
        
class ProcessLog(ttk.Frame):
    """
    Custom frame widget containing a canvas to show what the program is doing.
    
    Args:
        parent: Any = parent object for the frame widget
    """
    def __init__(self, parent):
        super().__init__(parent, borderwidth=2, relief=SUNKEN)
        self.root = parent
        
        # scrolled frame to display the log
        self.log_txt = ScrolledText(
            self,
            autohide=True,
            hbar=True,
            width=100
            )
        self.log_txt.text.config(state=DISABLED)
        self.log_txt.pack(fill=BOTH, expand=YES)
    
    def add_line(self, text):
        # add a line to the log, but keep it disabled so the user can't type
        self.log_txt.text.config(state=NORMAL)
        self.log_txt.insert(END, text)
        self.log_txt.insert(END, "\n")
        self.log_txt.text.config(state=DISABLED)
        self.root.update_idletasks()


class CSVHandler():
    def __init__(self, parent):
        self.root = parent
        
    def fix_addresses(self, path) -> None:
        self.root.log.add_line("Starting...")
        
        # get the listed address and ask ChatGPT what the actual address is.
        self.cols = self.get_cols(path)
        
        for r in rows:
            address = self.get_address(r)
            
            
            

    def get_cols(self, path) -> list:
        self.root.log.add_line("Getting relevant column numbers...")
        
        # open the selected .csv file
        with open(path, newline="") as f:
            reader = csv.reader(f, dialect="excel")
            
            # list comp to get all the items in the .csv
            self.rows = [r.split(",") for r in f]
            
        # check the column headers for the columns we need
        address_col = self.rows[0].index("Address")
        city_col = self.rows[0].index("City")
        state_col = self.rows[0].index("State")
        lat_col = self.rows[0].index("Latitude")
        long_col = self.rows[0].index("Longitude")
        # have to treat the zip_col special because it changes b/t .csv files
        try:
            zip_col = self.rows[0].index("ZIP Code")
        except ValueError:
            zip_col = self.rows[0].index("ZIP")

        cols = [address_col,
            city_col,
            state_col,
            zip_col,
            lat_col,
            long_col]
            
        self.root.log.add_line(f"Relevant columns: {cols}.")   
        
        return cols
    
    def get_address(self, row):
        self.root.log.add_line(f"Getting address for row {self.rows[row]}")
        
        address_lst = []
        for col in self.cols:
            address_lst.append(self.rows[row][col])
            
        self.root.log.add_line(f"Row {row}: {", ".join(address_lst)}")
        
        return address_lst
        
    def ai_request(self, address):
        instructions = """
    You are an AI tool that receives input from a python script and
    provides an output. The input will be in the form of a list of 6 items
    separated by commas. All 5 commas will always be included in the input.
    If the input received does not match that format, your output should
    merely be "INVALID INPUT". The output should also be a comma separated
    list, but an additional item should be included, that being an integer
    between 0-100 indicating certainty percentage (no % should be
    included). In all cases, your output should consist of a list of 7
    items separated by commas. All 6 commas should always be included in
    the output. Some of the input list items may be empty, and your task
    will be to use the other items in the list to determine some of the
    missing items. The output should be formatted in all caps.

    Your response should contain the output and nothing else.

    The input will be a partial address or intersection corresponding to a
    call for service at the Jackson County Sheriff's Office. The list will
    be in the order of: STREET ADDRESS, CITY, STATE, ZIP CODE, LATITUDE,
    LONGITUDE. As stated before, one or more of those items may be missing
    from the input. The latitude and longitude will not normally be
    provided.

    Input formatting of the street address for intersections may vary, but
    the output should always be the two intersecting roadways separated by
    a backslash (e.g. "EXAMPLE ST/SAMPLE AVE").  The roadway type (St, Ave,
    Blvd, etc.) and direction should always be determined and included.
    Some of the CITY items provided in the input will be "UNINCORPORATED"
    or "JACKSON COUNTY". In such cases, you should determine the city
    associated with the mailing address. You do not need to attempt to find
    the ZIP CODE, LATITUDE, or LONGITUDE items. If these items were
    provided, merely pass them through to your output. If those items were
    left empty, then pass an empty item through to your output.

    Most, but not all, of the input addresses will be located within
    Jackson County, MO. If no CITY, STATE, or ZIP CODE is specified, assume
    the location is in Jackson County, MO, and attempt to determine the
    CITY.

    When a STREET ADDRESS is an intersection and one of the roadways is
    merely a number, that roadway is likely a state or US highway. If no
    such highway exists in that CITY or STATE, then assume it is a numbered
    street. If an input STREET ADDRESS contains an unabbreviated roadway
    type or direction, your output should use the appropriate
    abbreviations.

    You should attempt to find as complete an address as possible and check
    each list item against the others for accuracy. You should not fully
    trust the information provided in the input. The STREET ADDRESS item
    will likely be the most complicated and least trustworthy part. These
    addresses were entered by Dispatchers and Deputies, and each individual
    may have a slightly different method for notating certain information.
    The street type and direction may have also been entered incorrectly
    when recorded. Some calls for service are located some distance in some
    direction from the given address, and that information is normally
    notated in the STREET ADDRESS item as an abbreviation (e.g. "JN" for
    "Just North," etc.). There may also be erroneous or accidental characters
    in the STREET ADDRESS.

    You should make 3 separate attempts to find the correct address, and
    the attempts should not influence nor refer to each other.  Each check
    should be performed as though you were starting from the beginning, and
    you should attempt to locate all of the requested information during
    each. Then you will determine the most likely address from the 3
    attempts and output it. The certainty percentage should reflect the
    similarity between the 3 attempts. Identical findings in the 3 attempts
    would give 100% output certainty, and completely dissimilar findings
    would give 0% output certainty. The certainty percentage should also be
    influenced by how many items were provided in the INPUT. An input with
    all items provided would be 100% output certainty, and one with all
    items empty would be 0% output certainty. Multiplying the two output
    certainties will give you the total output certainty.
    """
        
        input = address
        
if __name__ == "__main__":
    root = App()