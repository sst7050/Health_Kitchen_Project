import tkinter as tk
from tkinter import messagebox


class RankImageFrame(tk.Frame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback
        self.create_Rank_widgets()  # 위젯 생성

def create_Rank_widgets(self):  # 음식 리스트 및 위젯 생성
        Rank_list = {
            "주방 견습생": {"image": "img/food/Burger/Burger.png", "duration": "2개월", "price": "20000원", "detail_name": "햄버거"},
            "초급 요리사": {"image": "img/food/Chicken/Chicken.png", "duration": "2개월", "price": "20000원", "detail_name": "치킨"},
            "중급 요리사": {"image": "img/food/Pasta/Pasta.png", "duration": "2개월", "price": "20000원", "detail_name": "파스타"},
            "주방장": {"image": "img/food/Pilaf/Pilaf.png", "duration": "2개월", "price": "19000원", "detail_name": "필라프"},
            "요리의 달인": {"image": "img/food/Pizza/Pizza.png", "duration": "2개월", "price": "20000원", "detail_name": "피자"},
            "요리왕 비룡": {"image": "img/food/Steak/Steak.png", "duration": "2개월", "price": "18000원", "detail_name": "스테이크"},
            "고든 램지": {"image": "img/food/Stew/Stew.png", "duration": "2개월", "price": "19000원", "detail_name": "스튜"}
        }




def show_rank_up_message(level):
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우 숨기기
    messagebox.showinfo("축하합니다", f"축하합니다, 당신은 {level} 레벨로 승급하셨습니다!")
    root.destroy()  # 메시지 박스 닫기


