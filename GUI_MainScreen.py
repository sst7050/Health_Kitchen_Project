import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import json
from datetime import datetime
from GUI_Progress_info import ExerciseTracker
from GUI_Refrigerator import RefrigeratorScreen
from GUI_Made_Food import MadeFoodScreen
import userInfo

class MainScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")  # 부모 컨테이너를 채우도록 프레임 확장
        self.create_main_menu()
        self.check_time_limit()

    def read_user_info(self):
        try:
            with open('user_info.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except UnicodeDecodeError:
            try:
                with open('user_info.json', 'r', encoding='cp949') as file: 
                    return json.load(file)
            except Exception as e:
                print(f"Failed to read the user info file: {e}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def check_time_limit(self):
        user_info = self.read_user_info()
        if user_info and 'limit_time' in user_info:
            limit_time = datetime.strptime(user_info['limit_time'], "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            if current_time >= limit_time:
                messagebox.showinfo("알림", "재료의 유통기한이 만료되었습니다.\n냉장고의 재료가 모두 사라집니다. 음식을 다시 선택해 주세요.")
                user_info["유산소"] = 0
                user_info["무산소"] = 0
                userInfo.save_user_info(user_info)
                self.master.after(100, self.relaunch_food_selection)

    def relaunch_food_selection(self):
        self.master.destroy()
        subprocess.run(['python', 'GUI_Sel_Food.py'])

    def create_main_menu(self):
        # 버튼 이미지 로드
        self.about_image = ImageTk.PhotoImage(Image.open("img/about_btn.png"))
        self.fridge_image = ImageTk.PhotoImage(Image.open("img/fridge_btn.png"))
        self.progress_image = ImageTk.PhotoImage(Image.open("img/progress_btn.png"))
        self.made_food_image = ImageTk.PhotoImage(Image.open("img/made_food_btn.png"))
        
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
        _font = font.Font(family="Ubuntu", weight='bold')
        
        # 냉장고 버튼 추가
        self.start_button = tk.Button(self, command=self.open_fridge, image=self.fridge_image, compound='center', bd=0, highlightthickness = 0, font=_font)
        self.canvas.create_window(100, 100, anchor="nw", window=self.start_button)
        self.start_button.place(x=1189, y=349)

        # 운동 진행 상황 버튼 추가
        self.progress_button = tk.Button(self, command=self.progress_info, image=self.progress_image, compound='center', bd=0, highlightthickness = 0, font=_font)
        self.canvas.create_window(300, 100, anchor="nw", window=self.progress_button)
        self.progress_button.place(x=566, y=473)

        # 사용자 정보 버튼 추가
        self.about_button = tk.Button(self, command=self.show_about, fg="yellow", image=self.about_image, compound='center', bd=0, highlightthickness = 0, font=_font)
        self.canvas.create_window(500, 100, anchor="nw", window=self.about_button)
        self.about_button.place(x=1013, y=619)
        
        # 만든 음식 버튼 추가
        self.made_food_button = tk.Button(self, command=self.made_food, image=self.made_food_image, compound='center', bd=0, highlightthickness = 0, font=_font)
        self.canvas.create_window(700, 100, anchor="nw", window=self.made_food_button)
        self.made_food_button.place(x=120, y=420)

        # 종료 버튼 추가
        self.quit_button = tk.Button(self, text="종료", command=self.master.quit, width=10, height=3, bg="SystemButtonFace", bd=0)
        self.canvas.create_window(700, 100, anchor="nw", window=self.quit_button)

    def open_fridge(self):
        # 재료 상황을 보여주기 위한 새 창 열기
        fridge_window = tk.Toplevel(self.master)
        RefrigeratorScreen(master=fridge_window, main_screen=self).grid(sticky="nsew")

    def start_info_input(self):
        messagebox.showinfo("알림", "이 프로그램은 당신의 인바디 '분석 평가'(결과지의 우측 부분)의 일부 항목값을 입력받아 그 값을 토대로 적정 체중이 되도록 돕거나 유지시켜주는 프로그램 입니다. 따라서 다음 질문에 답 하기 전에 먼저 인바디 검사를 받고, 해당 검사지를 출력하여 준비해 주시기 바랍니다. 만약 인바디 검사지가 준비되셨다면, 질문에 솔직하게 답변 해 주세요.")

    def progress_info(self):
        # 운동진행상황을 보여주기 위한 새 창 열기
        progress_window = tk.Toplevel(self.master)
        ExerciseTracker(master=progress_window, main_screen=self).grid(sticky="nsew")

    def show_about(self):
        user_info = self.read_user_info()
        if user_info:
            info_str = (
                        f"인바디 점수: {user_info['inbody_score']}\n"
                        f"지방 조절 수치: {user_info['fat_control']} kg\n"
                        f"근육 조절 수치: {user_info['muscle_control']} kg\n"
                        f"BMI: {user_info['bmi']}\n"
                        f"체지방률: {user_info['body_fat']}\n"
                        f"현재상태: {user_info['status']}\n"
                        f"선택한 음식: {user_info['selected_food']['food']}\n"
                        f"유통기한: {user_info['limit_time']}\n"
                        f"레벨: {user_info['level']}\n"
                        f"만든 음식 수: {user_info['made_food_count']}")
            messagebox.showinfo("사용자 정보", info_str)
    
    def made_food(self):
        # 만든 음식을 보여주기 위한 새 창 열기
        made_food_window = tk.Toplevel(self.master)
        made_food_window.title("만든 음식 목록")
        MadeFoodScreen(master=made_food_window).grid(sticky="nsew")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.main_menu = MainScreen(self.master)
        self.main_menu.grid(sticky="nsew")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    root.mainloop()
