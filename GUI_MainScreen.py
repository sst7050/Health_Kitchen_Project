
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
        self.grid(sticky="nsew")
        self.load_images()
        self.create_main_menu()
        self.check_time_limit()

    def load_images(self):
        # 버튼 이미지 로드
        self.images = {
            "about": ImageTk.PhotoImage(Image.open("img/about_btn.png")),
            "fridge": ImageTk.PhotoImage(Image.open("img/fridge_btn.png")),
            "progress": ImageTk.PhotoImage(Image.open("img/progress_btn.png")),
            "made_food": ImageTk.PhotoImage(Image.open("img/made_food_btn.png")),
            "background": ImageTk.PhotoImage(Image.open("img/Main_background.png")),
            "kitchen_apprentice": ImageTk.PhotoImage(Image.open("img/chef/kitchen_apprentice-removebg-preview.png")),
            "beginner_chef": ImageTk.PhotoImage(Image.open("img/chef/beginner_chef-removebg-preview.png")),
            "intermediate_chef": ImageTk.PhotoImage(Image.open("img/chef/intermediate_chef-removebg-preview.png")),
            "head_chef": ImageTk.PhotoImage(Image.open("img/chef/head_chef-removebg-preview.png")),
            "master_of_cooking": ImageTk.PhotoImage(Image.open("img/chef/master_of_cooking-removebg-preview.png")),
            "cooking_king_birong": ImageTk.PhotoImage(Image.open("img/chef/Cooking_King_Biryong-removebg-preview.png")),
            "gordon_ramsey": ImageTk.PhotoImage(Image.open("img/chef/gordon_ramsey-removebg-preview.png")),
        }

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
        user_info = self.read_user_info()
        user_level = user_info.get('level', '주방 견습생') if user_info else '주방 견습생'
        # 창 크기 설정
        self.master.geometry(f"{self.images['background'].width()}x{self.images['background'].height()}")
        
        # 창 크기 조정 불가능하게 설정
        self.master.resizable(False, False)
        
        # 전체 화면 비활성화
        self.master.attributes("-fullscreen", False)
        
        # 캔버스 생성 및 배경 이미지 추가
        self.canvas = tk.Canvas(self, width=self.images['background'].width(), height=self.images['background'].height())
        self.canvas.create_image(0, 0, anchor="nw", image=self.images['background'])
        self.canvas.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")
        _font = font.Font(family="Ubuntu", weight='bold')
        
        # 버튼 추가
        buttons = {
            "fridge": (self.open_fridge, self.images['fridge'], 1189, 349),
            "progress": (self.progress_info, self.images['progress'], 566, 473),
            "about": (self.show_about, self.images['about'], 1013, 619),
            "made_food": (self.made_food, self.images['made_food'], 120, 420),
        }

        for key, (command, image, x, y) in buttons.items():
            button = tk.Button(self, command=command, image=image, compound='center', bd=0, highlightthickness=0, font=_font)
            self.canvas.create_window(x, y, anchor="nw", window=button)

        # 랭크 이미지 추가
        rank_images = {
           '주방 견습생': self.images['kitchen_apprentice'],
            '초급 요리사': self.images['beginner_chef'],
            '중급 요리사': self.images['intermediate_chef'],
            '주방장': self.images['head_chef'],
            '요리의 달인': self.images['master_of_cooking'],
            '요리왕 비룡': self.images['cooking_king_birong'],
            '고든 램지': self.images['gordon_ramsey'],
        }
        
        rank_image_positions = {
            '주방 견습생': (290, 380),
            '초급 요리사': (300, 330),
            '중급 요리사': (280, 350),
            '주방장': (280, 350),
            '요리의 달인': (270, 340),
            '요리왕 비룡': (270, 330),
            '고든 램지': (475, -15),
        }
        
        selected_rank_image = rank_images.get(user_level, self.images['kitchen_apprentice'])
        selected_rank_position = rank_image_positions.get(user_level, (220, 245))
        
        # 선택된 랭크 이미지 추가
        self.canvas.create_image(*selected_rank_position, anchor="nw", image=selected_rank_image)

    def open_fridge(self):
        # 재료 상황을 보여주기 위한 새 창 열기
        fridge_window = tk.Toplevel(self.master)
        RefrigeratorScreen(master=fridge_window, main_screen=self).grid(sticky="nsew")

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
