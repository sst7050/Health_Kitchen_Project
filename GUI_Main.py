import tkinter as tk
from tkinter import messagebox
import json

class MainScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")  # Make sure the frame expands to fill the parent
        self.create_main_menu()

    def read_user_info(self):
        try:
            with open('user_info.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("오류", "사용자 정보 파일을 찾을 수 없습니다.")
            return None
        
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

        self.about_button = tk.Button(self, text="사용자 정보", command=self.show_about, width=10, height=3)
        self.about_button.grid(row=1, column=2, padx=10, pady=10, ipadx=50, ipady=30, sticky="S")

        self.quit_button = tk.Button(self, text="종료", command=self.master.quit, width=10, height=3)
        self.quit_button.grid(row=1, column=3, padx=10, pady=10, ipadx=50, ipady=30, sticky="S")

    def start_info_input(self):
        messagebox.showinfo("버튼1", "버튼1")

    def query_info(self):
        messagebox.showinfo("버튼2", "버튼2")

    def show_about(self):
        user_info = self.read_user_info()
        if user_info:
            info_str = f"성별: {user_info['gender']}\n키: {user_info['height']} cm\n몸무게: {user_info['weight']} kg\n나이: {user_info['age']} 세"
            messagebox.showinfo("사용자 정보", info_str)

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