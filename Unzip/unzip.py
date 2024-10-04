import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from tkinter.simpledialog import Dialog
from tkinter import messagebox
from threading import Thread
import zipfile
        

class App(ttk.Window):
    """
    Custom app to extract .ZIP archives because Windows 11 won't play nice for
    the Detectives, for some unknown and apparently unsolvable reason.
    
    Only necessary because 7zip is blocked and "obsolete," according to IT.
    """
    def __init__(self):
        super().__init__(
            title="Extract .ZIP Folders",
            minsize=(500, 300)
            )
         
        self.resizable(False, False)
        
        self.generate_gui()
        
        self.mainloop()        
        
    def generate_gui(self) -> None:
        """
        Generate the program gui. Create widgets and place them in the window.
        """
        # First, generate widgets
        
        # Window title label
        title = ttk.Label(
            self,
            text="Extract .ZIP Folders",
            font=("", 12)
            )
            
        
        # Target FileSelect widget
        self.target_file = FileSelect(
            self,
            label="Select a .ZIP archive to extract:"
            )
            
        # Destination FileSelect widget
        self.destination_path = FileSelect(
            self,
            label="Select a destination for the extracted files:",
            dir = True
            )
        
        # ActionButtons widget
        self.action_btns = ActionButtons(self)

        # Second, place the widgets
        title.pack(
            side=tk.TOP,
            fill=tk.X,
            pady=10,
            padx=10
            )
        self.target_file.pack(
            side=tk.TOP,
            fill=tk.X,
            pady=25
            )
        self.destination_path.pack(
            side=tk.TOP,
            fill=tk.X
            )
        self.action_btns.pack(
            side=tk.BOTTOM,
            fill=tk.X
            )
        
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
        Open a file dialog to choose a .ZIP file to extract and update the
        entry widget.
        """
        if self.dir:
            f = filedialog.askdirectory()
            self.path.set(f)
        else:
            f = filedialog.askopenfilename()
            
            # Check if the target file is a .ZIP archive                        
            if zipfile.is_zipfile(f):
                self.path.set(f)
                self.path_update()
            else:
                messagebox.showerror(
                    "Error",
                    "Selected file must be a valid .ZIP archive."
                    )
            
    def path_update(self) -> None:
        """Update the destination path entry when a target .ZIP archive is
        selected.
        """
        # Get the selected target file
        f = self.root.target_file.path.get()
        # Remove the file extension
        f = f.rsplit(".", 1)[0]
        # Set the destination path as a new directory of the same name as the
        # target file
        self.root.destination_path.path.set(f)
        

class ActionButtons(ttk.Frame):
    """
    Custom frame widget containing two buttons: extract_btn and cancel_btn.
    
    Args:
        parent: Any = parent object for the frame widget
    """
    def __init__(self, parent):
        super().__init__(parent, bootstyle=SECONDARY)
        self.root = parent
        
        # Extract button to proceed with file extraction.
        self.extract_btn = ttk.Button(
            self,
            text="Extract",
            command=lambda: self.extract_file(
                self.root.target_file.path.get(),
                self.root.destination_path.path.get()
                )
            )
        
        # Cancel button to close window.
        self.cancel_btn = ttk.Button(
            self,
            text="Cancel",
            command=self.root.destroy
            )
            
        # Place the widgets
        self.cancel_btn.pack(side=tk.RIGHT, pady=5, padx=10)
        self.extract_btn.pack(side=tk.RIGHT, pady=5)
     
    def extract_file(self, target:str, destination:str) -> None:
        """
        Extract the selected .ZIP archive to the selected destination.
        
        Args:
            target: str = Path for target file to be extracted.
            destination: str = Destination path for extracted files.
        """
        print(target, destination, sep="\n")
        
        if target == "" or destination == "":
            messagebox.showerror(
                "Error",
                "Please choose a target file and a destination path."
                )
        else:
            self.progress = WorkingThrobber(self.root)
            self.progress.pack(
                side=tk.BOTTOM,
                fill=tk.X
                )
                
            self.progress.progress.start(25)
            self.root.update()
            
            # Extract the .ZIP archive
            extract = Thread(
                target=self.unzip,
                args=(target, destination),
                daemon=True
                )
            extract.start()
    
    def unzip(self, target:str, destination:str):
        with zipfile.ZipFile(target) as f:
            f.extractall(path=destination)
            
        self.root.destroy()
        


class WorkingThrobber(ttk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            
            self.root = parent
            
            lbl = ttk.Label(
                self,
                text="""Extracting...
This process may take several minutes, and the program may stop responding.
This window will close when finished.""",
                )
            lbl.pack(
                fill=tk.X,
                padx=10,
                pady=25,
                )
            
            self.progress = ttk.Progressbar(
                self,
                mode="indeterminate",
                maximum=25,
                style="success"
                )
            self.progress.pack(
                fill=tk.X,
                padx=10,
                pady=10
                )
                
        
if __name__ == "__main__":
    root = App()