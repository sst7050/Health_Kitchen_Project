import tkinter as tk
from tkinter import messagebox


class RankImageFrame(tk.Frame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback
        self.create_Rank_widgets()  # 위젯 생성

def create_Rank_widgets(self):  # 음식 리스트 및 위젯 생성
        Rank_list = {
            "주방 견습생": {"image": "img/chef/kitchen_apprentice.png", "foods": "default", "detail_explanation": "요리를 해 본적이 없는 초보 견습생"},
            "초급 요리사": {"image": "img/chef/beginner_chef.png", "foods": "1개", "detail_explanation": "좀 치기 시작한 요리사"},
            "중급 요리사": {"image": "img/chef/intermediate_chef.png", "foods": "3개", "detail_explanation": "짬이 차서 부점장까지 오른 요리사"},
            "주방장": {"image": "img/food/chef/head_chef.png", "foods": "6개","detail_explanation": "점장으로부터 식당을 승계받은 요리사"},
            "요리의 달인": {"image": "img/chef/master_of_cooking.png", "foods": "10개", "detail_explanation": "식당을 미슐랭 가이드에 등재시킨 요리사"},
            "요리왕 비룡": {"image": "img/chef/Cooking_King_Biryong.png", "foods": "15개", "detail_explanation": "TV 맛집탐방 프로그램에 출연하게 된 요리사"},
            "고든 램지": {"image": "img/chef/gordon_ramsey.png", "foods": "21개","detail_explanation": "전설의 요리사"}
        }




def show_rank_up_message(level):
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우 숨기기
    messagebox.showinfo("축하합니다", f"축하합니다, 당신은 {level} 레벨로 승급하셨습니다!")
    root.destroy()  # 메시지 박스 닫기


