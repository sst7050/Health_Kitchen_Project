import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import tkinter.font as font
import json

class MainScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")  # 부모 컨테이너를 채우도록 프레임 확장
        self.create_main_menu()

    def read_user_info(self):
        try:
            with open('user_info.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("오류", "사용자 정보 파일을 찾을 수 없습니다.")
            return None
        
    def create_main_menu(self):
        # 버튼 이미지 로드
        self.about_image = ImageTk.PhotoImage(Image.open("img/about_btn.png"))
        # 배경 이미지 로드
        self.background_image = Image.open("img/Main_background.png")
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # 창 크기 설정
        self.master.geometry(f"{self.bg_image.width()}x{self.bg_image.height()}")
        
        # 창 크기 조정 불가능하게 설정
        self.master.resizable(False, False)
        
        # 전체 화면 비활성화
        self.master.attributes("-fullscreen", False)
        
        # 캔버스 생성 및 배경 이미지 추가
        self.canvas = tk.Canvas(self, width=self.bg_image.width(), height=self.bg_image.height())
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.canvas.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")
        root.wm_attributes("-transparentcolor", "white")
        _font = font.Font(family="Ubuntu", weight='bold')
        # 버튼 추가
        self.start_button = tk.Button(self, text="냉장고", command=self.start_info_input, bg="#DDDCDA", bd=0,font=_font)
        self.canvas.create_window(100, 100, anchor="nw", window=self.start_button)
        self.start_button.place(x=1200, y = 350, width=100, height=250)

        self.progress_button = tk.Button(self, text="운동진행상황", command=self.progress_info, bg="#333333", fg="blue",bd=0,font=_font)
        self.canvas.create_window(300, 100, anchor="nw", window=self.progress_button)
        self.progress_button.place(x=566, y = 473, width=315, height=175)

        self.about_button = tk.Button(self, text="사용자 정보", command=self.show_about, fg = "yellow", image=self.about_image, bd=0, compound='center',font=_font)
        self.canvas.create_window(500, 100, anchor="nw", window=self.about_button)
        self.about_button.place(x=1015, y = 620)


        self.quit_button = tk.Button(self, text="종료", command=self.master.quit, width=10, height=3, bg="SystemButtonFace", bd=0)
        self.canvas.create_window(700, 100, anchor="nw", window=self.quit_button)

    def start_info_input(self):
        messagebox.showinfo("알림", "이 프로그램은 당신의 인바디 '분석 평가'(결과지의 우측 부분)의 일부 항목값을 입력받아 그 값을 토대로 적정 체중이 되도록 돕거나 유지시켜주는 프로그램 입니다. 따라서 다음 질문에 답 하기 전에 먼저 인바디 검사를 받고, 해당 검사지를 출력하여 준비해 주시기 바랍니다. 만약 인바디 검사지가 준비되셨다면, 질문에 솔직하게 답변 해 주세요.")

    def progress_info(self):
        subprocess.run(["python", "GUI_Progress_info.py"]) # 버튼 클릭 시 GUI_Progress_info 실행

    def show_about(self):
        user_info = self.read_user_info()
        if user_info:
            info_str = (f"성별: {user_info['gender']}\n"
                        f"인바디 점수: {user_info['inbody_score']}\n"
                        f"적정 체중: {user_info['ideal_weight']} kg\n"
                        f"지방 조절 수치: {user_info['fat_control']} kg\n"
                        f"근육 조절 수치: {user_info['muscle_control']} kg\n"
                        f"나이: {user_info['age']} 세\n"
                        f"BMI: {user_info['bmi']}\n"
                        f"체지방률: {user_info['body_fat']}\n"
                        f"현재상태: {user_info['status']}\n"
                        f"선택한 음식: {user_info['selected_food']['food']}")
            messagebox.showinfo("사용자 정보", info_str)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.main_menu = MainScreen(self.master) # 메인 화면 인스턴스 생성
        self.main_menu.grid(sticky="nsew") # 메인 화면을 그리드에 배치하여 확장
