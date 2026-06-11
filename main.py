# main.py

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.style = ttk.Style()
        self.style.configure(
            "Button.TButton",
            font=("Arial", 10),
            padding=6
        )

        self.title("Phase-Mismatch Calculator")
        self.geometry("800x600")

        self.create_widgtes()

    def create_widgtes(self):

        # Files Frame
        files_frame = ttk.Frame(self)
        files_frame.grid(row=0,column=0)

        choose_files_bt = ttk.Button(
            files_frame,
            text="Choose data files",
            style="Button.TButton"
            )
        choose_files_bt.grid(row=0,column=0)

        self.files_read_box = scrolledtext.ScrolledText(files_frame, height=10)
        self.files_read_box.grid(row=1,column=0)
        self.files_read_box.config(state="disabled")

        # Parameters Frame
        params_frame = ttk.Frame(self)
        params_frame.grid(row=1,column=0)

        ttk.Label()


if __name__ == "__main__":
    app = App()
    app.mainloop()

