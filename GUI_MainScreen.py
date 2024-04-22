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
        messagebox.showinfo("알림", "이 프로그램은 당신의 인바디 '분석 평가'(결과지의 우측 부분)의 일부 항목값을 입력받아 그 값을 토대로 적정 체중이 되도록 돕거나 유지시켜주는 프로그램 입니다. 따라서 다음 질문에 답 하기 전에 먼저 인바디 검사를 받고, 해당 검사지를 출력하여 준비해 주시기 바랍니다. 만약 인바디 검사지가 준비되셨다면, 질문에 솔직하게 답변 해 주세요.")

    def query_info(self):
        messagebox.showinfo("버튼2", "버튼2")

    def show_about(self):
        user_info = self.read_user_info()
        if user_info:
            info_str = f"성별: {user_info['gender']}\n인바디 점수: {user_info['inbody_score']}\n적정 체중: {user_info['ideal_weight']} kg\n지방 조절 수치: {user_info['fat_control']} kg\n근육 조절 수치: {user_info['muscle_control']} kg\n나이: {user_info['age']} 세"
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