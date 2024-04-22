import tkinter as tk
from tkinter import messagebox
import userInfo
import os
import GUI_MainScreen

def check_user_info_and_launch():
    exists, user_info = userInfo.read_user_info()  # Call function from userInfo module
    if not exists:
        messagebox.showinfo("알림", "이 프로그램은 당신의 인바디 '분석 평가'(결과지의 우측 부분)의 일부 항목값을 입력받아 그 값을 토대로 적정 체중이 되도록 돕거나 유지시켜주는 프로그램 입니다. 따라서 다음 질문에 답 하기 전에 먼저 인바디 검사를 받고, 해당 검사지를 출력하여 준비해 주시기 바랍니다. 만약 인바디 검사지가 준비되셨다면, 질문에 솔직하게 답변 해 주세요.")
        os.system('python GUI_basic_info.py')  # Launch user info input window
    else:
        root = tk.Tk()
        root.geometry("800x600")
        root.title("Health Kitchen")
        app = GUI_MainScreen.Application(master=root)
        root.mainloop()

if __name__ == "__main__":
    check_user_info_and_launch()    

