import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import filedialog
from tkinter.simpledialog import Dialog
from tkinter import messagebox
from threading import Thread
from pypdf import PdfWriter
import os

class App(ttk.Window):
    def __init__(self):
        super().__init__(
        title="MERGE .PDF FILES",
        minsize=(700, 250)
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
            text="MERGE .PDF FILES",
            font=("", 12)
            )
            
        
        # Target FileSelect widget
        self.target_file = FileSelect(
            self,
            label="Select .pdf files to merge:"
            )
            
        # Widget to display list of files to merge
        self.files_list = FilesList(self)
        
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
        self.files_list.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            padx=10,
            pady=10
            )
        self.action_btns.pack(
            side=tk.BOTTOM,
            fill=tk.X
            )
            
    def add_file(self, file):
        self.files_list.text_box.text["state"] = "normal"
        self.files_list.text_box.insert("end", "\n".join(file) + "\n")
        self.files_list.text_box.text["state"] = "disabled"
        
    def clear_list(self):
        self.files_list.text_box.text["state"] = "normal"
        self.files_list.text_box.delete(1.0, "end")
        self.files_list.text_box.text["state"] = "disabled"
        
    def merge_pdfs(self, files:list) -> None:
        print(files)
        # initialize PdfWriter to work with .pdf files
        merger = PdfWriter()
        
        # merge all selected .pdf files
        for file in files:
            merger.append(file)
        
        # write the new combined .pdf file to the selected destination_path
        merger.write(filedialog.asksaveasfilename(defaultextension=".pdf"))
        merger.close()


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
        
        # Root reference to access other classes in the App
        self.root = parent
        
        # Configure grid layout
        self.columnconfigure((0,1,3), weight=0)
        self.columnconfigure(2, weight=1)
        
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
            columnspan=2,
            sticky="nsew",
            padx=10
            )
        path_entry.grid(
            row=1,
            column=0,
            columnspan=3, 
            sticky="nsew",
            padx=10,
            pady=5
           )
        browse_button.grid(
            row=1,
            column=3,
            sticky="ew",
            padx=10
            )        
            
    def file_browse(self) -> tuple:
        """
        Open a file dialog to choose a .pdf file to extract and update the
        entry widget.
        """
        files = filedialog.askopenfilenames()
        
        # Check if the target file is a .pdf archive                        
        if self.file_check(files):
            # file is valid, coninue
            self.root.add_file(files)
        elif not files:
            # no file selected, do nothing
            pass
        else:
            # invalid file selected, present error popup
            messagebox.showerror(
                "Error",
                "All selected files must be valid .pdf files."
                )
                
    def file_check(self, files:tuple) -> bool:
        for f in files:
            if not f.endswith(".pdf"):
                return False
            else:
                return True


class FilesList(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.root = parent
        
        self.columnconfigure((0,1), weight=0)
        self.columnconfigure(2, weight=1)
        
        add_button = ttk.Button(
            self,
            text="Add",
            command=lambda: self.root.add_file((self.root.target_file.path.get(),))
            )
        clear_button = ttk.Button(
            self,
            text="Clear",
            command=self.root.clear_list
            )
        
        self.text_box = ScrolledText(self)
        self.text_box.text["state"] = "disabled"
        
        add_button.grid(
            row=0,
            column=0,
            sticky="nsew",
            )
        clear_button.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10
            )   
        self.text_box.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="nsew",
            pady=5
            )
        

class ActionButtons(ttk.Frame):
    """
    Custom frame widget containing two buttons: merge_btn and cancel_btn.
    
    Args:
        parent: Any = parent object for the frame widget
    """
    def __init__(self, parent):
        super().__init__(parent, bootstyle=SECONDARY)
        self.root = parent
        
        # Extract button to proceed with file extraction.
        self.merge_btn = ttk.Button(
            self,
            text="Merge",
            command=lambda: self.root.merge_pdfs(
                [f for f in
                self.root.files_list.text_box.text.get("1.0", "end").split("\n")
                if f != ""]
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
        self.merge_btn.pack(side=tk.RIGHT, pady=5)


if __name__ == "__main__":
    App()