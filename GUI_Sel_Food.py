import tkinter as tk
from tkinter import messagebox
import os
import userInfo

class FoodSelectionFrame(tk.Frame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback
        self.create_widgets()  # 위젯 생성

    def create_widgets(self):  # 음식 리스트 및 위젯 생성
        food_list = {
            "빵": {"image": "img/Bread.png", "duration": "2개월", "price": "20000원", "detail_name": "뚜레쥬르 2만원권"},
            "햄버거": {"image": "img/Burger.png", "duration": "2개월", "price": "20000원", "detail_name": "맥도날드 2만원권"},
            "치킨": {"image": "img/Chicken.png", "duration": "2개월", "price": "20000원", "detail_name": "교촌치킨 반반 오리지날"},
            "커피": {"image": "img/Coffee.png", "duration": "2개월", "price": "19000원", "detail_name": "스타벅스 피스타치오 크림 콜드 브루 T\n라이트 핑크 자몽 피지오 T\n치킨 & 머쉬룸 멜팅 치즈 샌드위치"},
            "편의점음식": {"image": "img/CU.png", "duration": "2개월", "price": "20000원", "detail_name": "CU 모바일 상품권 2만원권"},
            "아이스크림": {"image": "img/Icecream.png", "duration": "2개월", "price": "18000원", "detail_name": "베스킨라빈스 쿼터(네가지 맛)"},
            "피자": {"image": "img/Pizza.png", "duration": "2개월", "price": "19000원", "detail_name": "반올림피자R + 콜라500ml"}
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

    def select_food(self, food, info):
        success, user_info = userInfo.read_user_info()  # 사용자 정보 읽기
        if not success:
            messagebox.showinfo("Error", "사용자 정보를 불러오는데 실패했습니다.")
            return
        
        user_info['selected_food'] = { # 선택한 음식 정보 추가
            'food': food,
            'details': info
        }
        userInfo.save_user_info(user_info)  # 정보 저장
        self.switch_frame_callback(FoodDetailFrame, info["detail_name"], info)  # 상세 정보 화면으로 전환

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
            messagebox.showinfo("다음 단계", "다음 단계로 진행합니다.")
            self.master.destroy()  # 현재 창 닫기
            os.system('python GUI_Main.py')  # 메인 GUI 실행
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
