# main.py
import utils
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog

# Main file of the program, handles the gui.

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.style = ttk.Style()
        self.style.configure(
            "Button.TButton",
            font=("Arial", 10),
            padding=10
        )
        self.style.configure(
            "Label.TLabel",
            font=("Arial", 10),
            padding=6
        )
        self.style.configure(
            "Entry.TEntry",
            font=("Arial", 10),
            padding=8
        )

        self.files_paths = []

        self.title("Phase-Mismatch Calculator")
        self.geometry("950x600")

        self.create_widgtes()

    def create_widgtes(self):

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # Files frame

        files_frame = ttk.Frame(self)
        files_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=(15, 5))

        files_frame.rowconfigure(1, weight=1)
        files_frame.columnconfigure(0, weight=1)

        choose_files_bt = ttk.Button(
            files_frame,
            text="Choose data files",
            style="Button.TButton",
            command=self.choose_files_btn_click
            )
        
        choose_files_bt.grid(row=0,column=0)

        self.files_read_box = scrolledtext.ScrolledText(files_frame)
        self.files_read_box.grid(row=1,column=0, sticky="nsew")
        self.files_read_box.config(state="disabled")

        # Params frame  

        params_frame = ttk.Frame(self)
        params_frame.grid(row=1,column=0,sticky="nsew",padx=15, pady=(5, 15))

        ttk.Label(params_frame, text="Frequencies (separated by comma):", style="Label.TLabel").grid(row=0,column=0)
        self.frequencies_entry = ttk.Entry(params_frame,width=30,style="Entry.TEntry")
        self.frequencies_entry.grid(row=0,column=1)

        ttk.Label(params_frame, text="Minimum poling:", style="Label.TLabel").grid(row=1,column=0,sticky="e")
        self.min_poling_entry = ttk.Entry(params_frame,width=10,style="Entry.TEntry")
        self.min_poling_entry.grid(row=1,column=1, sticky="w")

        ttk.Label(params_frame, text="Number of sweep points:", style="Label.TLabel").grid(row=2,column=0,sticky="e")
        self.sweep_points_entry = ttk.Entry(params_frame,width=10,style="Entry.TEntry")
        self.sweep_points_entry.grid(row=2,column=1, sticky="w")

        # Calculate button frame

        calculate_frame = ttk.Frame(self)
        calculate_frame.grid(row=2,column=0,sticky="nsew",padx=15, pady=(5, 15))

        self.calculate_button = ttk.Button(
            calculate_frame,
            text="Calculate",
            style="Button.TButton",
            command=self.calculate_btn_click
            )
        self.calculate_button.grid(row=0,column=0)
        self.calculate_button.config(state="disabled")

        # Results Frame
        
        results_frame = ttk.Frame(self)
        results_frame.grid(row=0,column=1, rowspan=3 ,sticky="nsew",padx=15, pady=(5, 15))

        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=0)
        results_frame.rowconfigure(1,weight=1)

        ttk.Label(results_frame, text="Results", style="Label.TLabel").grid(row=0,column=0)
        self.results_box = scrolledtext.ScrolledText(results_frame)
        self.results_box.grid(row=1,column=0,sticky="nsew",padx=5, pady=5)
        self.results_box.config(state="disabled")

    def choose_files_btn_click(self):
        self.files_paths = filedialog.askopenfilenames()
        self.bases, self.betas = utils.files_handling.read_data_txt(self.files_paths)
        self.print_files_read_box()
    
    def print_files_read_box(self):
        self.files_read_box.config(state="normal")
        self.files_read_box.delete('1.0', tk.END)
        for i in range(len(self.files_paths)):
            self.files_read_box.insert(tk.END, f"Data {i}: {self.files_paths[i]}\n")
        self.files_read_box.config(state="disabled")
        self.calculate_button.config(state="normal")

    def calculate_btn_click(self):
        frequencies = [int(x) for x in self.frequencies_entry.get().split(',')]
        min_poling = float(self.min_poling_entry.get())
        sweep_points = int(self.sweep_points_entry.get())
        calcs = utils.Calcs(self.bases, self.betas, frequencies, min_poling, sweep_points, len(self.files_paths))
        self.results = calcs.results
        self.print_results_box() 
    
    def print_results_box(self):
        self.results_box.config(state="normal")
        self.results_box.delete('1.0', tk.END)
        for i in range(len(self.results["parameter_value"])):
            self.results_box.insert(tk.END, f"For parameter {self.results["parameter_value"][i]}: curve {self.results["triplet_sum"][i][0]} + curve {self.results["triplet_sum"][i][1]} ≈ curve {self.results["triplet_sum"][i][2]}\n")
            self.results_box.insert(tk.END, f"Values: {self.results["values"][i][0]} + {self.results["values"][i][1]} ≈ {self.results["values"][i][2]}\n")
            self.results_box.insert(tk.END, f"Mismatch: {self.results["mismatch"][i]}\n")
            self.results_box.insert(tk.END, f"Poling: {self.results["poling"][i]}\n\n")
        self.results_box.config(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()

