from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import messagebox
import subprocess
from tkinter.font import Font
from datetime import datetime, timedelta
import userInfo


class FoodSelectionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.images={}
        self.create_widgets()  # 위젯 생성

    def create_widgets(self):  # 음식 리스트 및 위젯 생성
        self.images = {}  # 이미지 객체를 저장할 딕셔너리
        food_list = {
            "햄버거": {"image": "img/food/Burger/Burger.png",  "detail_name": "햄버거", "ingredient_path" : "img/food/Burger/ingredient/"},
            "치킨": {"image": "img/food/Chicken/Chicken.png",  "detail_name": "치킨", "ingredient_path" : "img/food/Chicken/ingredient/"},
            "파스타": {"image": "img/food/Pasta/Pasta.png",  "detail_name": "파스타", "ingredient_path" : "img/food/Pasta/ingredient/"},
            "필라프": {"image": "img/food/Pilaf/Pilaf.png", "detail_name": "필라프", "ingredient_path" : "img/food/Pilaf/ingredient/"},
            "피자": {"image": "img/food/Pizza/Pizza.png",  "detail_name": "피자", "ingredient_path" : "img/food/Pizza/ingredient/"},
            "스테이크": {"image": "img/food/Steak/Steak.png", "detail_name": "스테이크", "ingredient_path" : "img/food/Steak/ingredient/"},
            "스튜": {"image": "img/food/Stew/Stew.png", "detail_name": "스튜", "ingredient_path" : "img/food/Stew/ingredient/"}
        }
        self.pont = Font(family="Helvetica", size=12)
        row = 0
        col = 0
        for food, info in food_list.items():
            if os.path.exists(info["image"]):  # 이미지 파일이 존재하는지 확인
                pil_image = Image.open(info["image"])  # Pillow로 이미지 로드
                img = ImageTk.PhotoImage(pil_image)  # tk.PhotoImage로 변환
                self.images[food] = img  # 이미지 객체를 딕셔너리에 저장
                button = tk.Button(self, command=lambda f=food, i=info: self.select_food(f, i))  # 버튼에 음식 선택 명령 연결
                try:
                    button.config(image=img)
                except:
                    pass
            else:
                button = tk.Button(self, text=food, command=lambda f=food, i=info: self.select_food(f, i))  # 이미지가 없을 경우 텍스트만 표시
            button.grid(row=row, column=col, padx=30, pady=(10, 0))  # 버튼 위치 설정
            label = tk.Label(self, text=food, font=self.pont, padx=30, pady=10)  # 음식 이름 레이블
            label.grid(row=row+1, column=col, sticky=tk.N)  # 레이블 위치 설정

            col += 1  # 열 위치 조정
            if col > 3:  # 열이 3을 초과하면 다음 행으로
                col = 0
                row += 2

    def relaunch_Main(self):
        self.master.destroy()
        subprocess.run(['python', 'GUI_Main.py'])

    def select_food(self, food, info):
        success, user_info = userInfo.read_user_info()  # 사용자 정보 읽기
        if not success:
            messagebox.showerror("Error", "올바르지 않은 경로입니다. 처음부터 다시 시작해 주세요.")  # json파일이 없을 경우
            self.master.after(100, self.relaunch_Main)
            return
        response = messagebox.askyesno("확인", f"{food}을(를) 선택하시겠습니까?")
        if response:
            user_info['selected_food'] = { # 선택한 음식 정보 추가
                'food': food,
                'details': info
            }
            #제한시간 추가
            timelimit = datetime.now() + timedelta(weeks= 1)
            timelimit = timelimit.strftime("%Y-%m-%d %H:%M:%S")
            user_info['limit_time'] = timelimit
            user_info['ingredient'] = []
            userInfo.save_user_info(user_info)  # 정보 저장
            self.master.destroy()
            subprocess.run('python GUI_MainScreen.py')
        else:
            self.switch_frame_callback(FoodSelectionFrame)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.current_frame = None
        self.switch_frame(FoodSelectionFrame)  # 초기 프레임 설정

    def switch_frame(self, frame_class, food=None, info=None):
        new_frame = frame_class(self, self.switch_frame)  # 새 프레임 생성
        if self.current_frame is not None:
            self.current_frame.destroy()  # 현재 프레임 제거
        self.current_frame = new_frame  # 새 프레임 설정
        if food and info:
            self.current_frame.display_food(food, info)  # 음식 정보 표시
        self.current_frame.pack()  # 프레임 패킹

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()  # 애플리케이션 실행