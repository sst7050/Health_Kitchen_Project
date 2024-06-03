import tkinter as tk
from tkinter import messagebox
import userInfo
import subprocess

class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, message, buttons):
        super().__init__(parent)
        self.result = None
        self.title("알림")
        self.geometry("400x200")
        self.resizable(False, False)
        
        tk.Label(self, text=message, wraplength=300).pack(pady=20)
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        for button_text, button_value in buttons.items():
            tk.Button(button_frame, text=button_text, command=lambda value=button_value: self.on_button_click(value)).pack(side=tk.LEFT, padx=5)
        
    def on_button_click(self, value):
        self.result = value
        self.destroy()
    
def show_custom_message(message, buttons):
    root = tk.Tk()
    root.withdraw()
    dialog = CustomMessageBox(root, message, buttons)
    root.wait_window(dialog)
    return dialog.result

def check_user_info_and_launch():
    exists, user_info = userInfo.read_user_info()
    if not exists:
        step = 0
        while True:
            if step == 0:
                result = show_custom_message(
                    "이 프로그램은 당신의 인바디 '분석 평가'(결과지의 우측 부분)의 일부 항목값을 입력받아\n그 값을 토대로 적정 체중이 되도록 돕거나 유지시켜주는 프로그램 입니다.",
                    {"다음": "next"}
                )
                if result == "next":
                    step += 1
            elif step == 1:
                result = show_custom_message(
                    "따라서 다음 질문에 답 하기 전에 먼저 인바디 검사를 받고, 해당 검사지를 출력하여 준비해 주시기 바랍니다.",
                    {"이전": "prev", "다음": "next"}
                )
                if result == "next":
                    step += 1
                elif result == "prev":
                    step -= 1
            elif step == 2:
                result = show_custom_message(
                    "만약 인바디 검사지가 준비되셨다면, 질문에 솔직하게 답변 해 주세요.",
                    {"이전": "prev", "확인": "confirm", "취소": "cancel"}
                )
                if result == "confirm":
                    subprocess.run('python GUI_basic_info.py')
                    break
                elif result == "prev":
                    step -= 1
                elif result == "cancel":
                    exit()
    else:
        subprocess.run('python GUI_MainScreen.py')

if __name__ == "__main__":
    check_user_info_and_launch()
