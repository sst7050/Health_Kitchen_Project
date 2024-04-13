import tkinter as tk
from tkinter import messagebox

class MainScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")  # Make sure the frame expands to fill the parent
        self.create_main_menu()

    def create_main_menu(self):
        # Configure the grid to expand the last row and all columns
        self.master.grid_rowconfigure(0, weight=1)  # Makes the row above the buttons expand
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)

        # Adding buttons in the last row, ensuring they align at the bottom
        self.start_button = tk.Button(self, text="버튼1", command=self.start_info_input, width=10, height=3)
        self.start_button.grid(row=1, column=0, padx=10, pady=10, ipadx=50, ipady=30, sticky="S")

        self.query_button = tk.Button(self, text="버튼2", command=self.query_info, width=10, height=3)
        self.query_button.grid(row=1, column=1, padx=10, pady=10, ipadx=50, ipady=30, sticky="S")

        self.about_button = tk.Button(self, text="정보", command=self.show_about, width=10, height=3)
        self.about_button.grid(row=1, column=2, padx=10, pady=10, ipadx=50, ipady=30, sticky="S")

        self.quit_button = tk.Button(self, text="종료", command=self.master.quit, width=10, height=3)
        self.quit_button.grid(row=1, column=3, padx=10, pady=10, ipadx=50, ipady=30, sticky="S")

    def start_info_input(self):
        messagebox.showinfo("버튼1", "버튼1")

    def query_info(self):
        messagebox.showinfo("버튼2", "버튼2")

    def show_about(self):
        messagebox.showinfo("About", "Health Kitchen\n\n개발자: 현규동")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")  # Ensure the frame expands to fill the parent
        self.create_widgets()

    def create_widgets(self):
        self.main_menu = MainScreen(self.master)
        self.main_menu.grid(sticky="nsew")  # Align the main menu frame to expand

root = tk.Tk()
root.geometry("800x600")
root.title("Health Kitchen")
app = Application(master=root)
root.mainloop()