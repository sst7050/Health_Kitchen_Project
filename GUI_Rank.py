import tkinter as tk
from tkinter import messagebox


class RankImageFrame(tk.Frame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback
        self.create_Rank_widgets()  # 위젯 생성





def show_rank_up_message(level):
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우 숨기기
    messagebox.showinfo("축하합니다", f"축하합니다, 당신은 {level} 레벨로 승급하셨습니다!")
    root.destroy()  # 메시지 박스 닫기


