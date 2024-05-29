import tkinter as tk
from tkinter import messagebox
import subprocess
from datetime import datetime, timedelta
import userInfo


class FoodSelectionFrame(tk.Frame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback
        self.create_widgets()  # 위젯 생성

    def create_widgets(self):  # 음식 리스트 및 위젯 생성
        food_list = {
            "햄버거": {"image": "img/food/Burger/Burger.png", "duration": "2개월", "price": "20000원", "detail_name": "햄버거", "ingredient_path" : "img/food/Burger/ingredient/"},
            "치킨": {"image": "img/food/Chicken/Chicken.png", "duration": "2개월", "price": "20000원", "detail_name": "치킨", "ingredient_path" : "img/food/Chicken/ingredient/"},
            "파스타": {"image": "img/food/Pasta/Pasta.png", "duration": "2개월", "price": "20000원", "detail_name": "파스타", "ingredient_path" : "img/food/Pasta/ingredient/"},
            "필라프": {"image": "img/food/Pilaf/Pilaf.png", "duration": "2개월", "price": "19000원", "detail_name": "필라프", "ingredient_path" : "img/food/Pilaf/ingredient/"},
            "피자": {"image": "img/food/Pizza/Pizza.png", "duration": "2개월", "price": "20000원", "detail_name": "피자", "ingredient_path" : "img/food/Pizza/ingredient/"},
            "스테이크": {"image": "img/food/Steak/Steak.png", "duration": "2개월", "price": "18000원", "detail_name": "스테이크", "ingredient_path" : "img/food/Steak/ingredient/"},
            "스튜": {"image": "img/food/Stew/Stew.png", "duration": "2개월", "price": "19000원", "detail_name": "스튜", "ingredient_path" : "img/food/Stew/ingredient/"}
        }

        row = 0
        col = 0
        for food, info in food_list.items():
            img = tk.PhotoImage(file=info["image"])  # 이미지 로드
            button = tk.Button(self, image=img, command=lambda f=food, i=info: self.select_food(f, i))  # 버튼에 음식 선택 명령 연결
            button.image = img  # 이미지 참조 유지
            button.grid(row=row, column=col, padx=10, pady=10)  # 버튼 위치 설정
            label = tk.Label(self, text=food)  # 음식 이름 레이블
            label.grid(row=row+1, column=col, sticky=tk.N)  # 레이블 위치 설정
            
            col += 1  # 열 위치 조정
            if col > 3:  # 열이 3을 초과하면 다음 행으로
                col = 0
                row += 2
                
    def relaunch_Main(self):
            self.master.destroy()
            subprocess.run(['python', 'GUI_Main.py'])
            
    def select_food(self, food, info):
        success, user_info = userInfo.read_user_info()
        if not success:
            messagebox.showinfo("Error", "올바르지 않은 경로입니다. 처음부터 다시 시작해 주세요.")
            self.master.after(100, self.relaunch_Main)
            return

        user_info['selected_food'] = {
            'food': food,
            'details': info
        }
    # 제한시간 추가
        timelimit = datetime.now() + timedelta(weeks=1)
        timelimit = timelimit.strftime("%Y-%m-%d %H:%M:%S")
        user_info['limit_time'] = timelimit
        user_info['ingredient'] = []  # 재료 초기화
        userInfo.save_user_info(user_info)
        self.switch_frame_callback(FoodDetailFrame, info["detail_name"], info) # 상세 정보 화면으로 전환

class FoodDetailFrame(tk.Frame):
    def __init__(self, master, go_back_callback):
        super().__init__(master)
        self.go_back_callback = go_back_callback

    def display_food(self, detail_name, details):
        self.pack_forget()  # 이전 내용 지우기
        self.master.title(f"{detail_name} 상세 정보")  # 창 제목 설정

        img = tk.PhotoImage(file=details["image"])  # 이미지 로드
        img_label = tk.Label(self, image=img)  # 이미지 레이블
        img_label.image = img  # 이미지 참조 유지
        img_label.pack(side=tk.TOP, pady=20)  # 이미지 레이블 위치 설정

        info_text = f"이름: {detail_name}\n예상 기간: {details['duration']}\n가격: {details['price']}"  # 상세 정보 텍스트
        info_label = tk.Label(self, text=info_text)  # 정보 레이블
        info_label.pack(side=tk.TOP, pady=20)  # 정보 레이블 위치 설정

        prev_button = tk.Button(self, text="이전", command=self.go_back)  # '이전' 버튼
        prev_button.pack(side=tk.LEFT, padx=20, pady=20)  # 버튼 위치 설정

        next_button = tk.Button(self, text="다음", command=self.go_next)  # '다음' 버튼
        next_button.pack(side=tk.RIGHT, padx=20, pady=20)  # 버튼 위치 설정

    def go_back(self):
        # 이전 화면으로 돌아가기
        self.go_back_callback(FoodSelectionFrame)

    def go_next(self):
        # 선택 확인받기
        response = messagebox.askyesno("확인", "선택한 음식으로 진행하시겠습니까?")
        if response:
            self.master.destroy()  # 현재 창 닫기
            subprocess.run('python GUI_MainScreen.py') # 메인 GUI 실행
        else:
            self.go_back() # 선택을 취소하고 음식 리스트 화면으로 돌아가기

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # 창 크기 설정
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