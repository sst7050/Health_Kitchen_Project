import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import userInfo
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.check_and_display_user_info()

    def check_and_display_user_info(self):
        exists, user_info = userInfo.read_user_info()
        if exists:
            messagebox.showinfo("정보 확인", "사용자 정보가 이미 존재합니다.")
            messagebox.showinfo("사용자 정보\n", f"성별: {user_info['gender']}\n키: {user_info['height']}\n몸무게: {user_info['weight']}\n나이: {user_info['age']}\n")
            self.master.destroy()  # Close the current window
            os.system('python GUI_Main.py')  # Open the main menu
        else:
            self.create_widgets()  # 사용자 정보 입력 위젯 생성
            
            
    def create_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.customFont = Font(family="Helvetica", size=12)  # 폰트 설정
        self.gender_label = tk.Label(self, text="당신의 성별은 무엇입니까?", font=self.customFont)
        self.gender_label.pack()
        self.gender_var = tk.StringVar()
        self.gender_entry = tk.OptionMenu(self, self.gender_var, "남성", "여성")
        self.gender_entry.pack()
        self.next_button = tk.Button(self, text="다음", command=self.next_height, bg="lightblue", fg="black")  # 버튼 색상 변경
        self.next_button.pack()

    def next_height(self):
        if not self.gender_var.get():
            messagebox.showinfo("에러", "성별을 선택해주세요.")
            return
        self.gender = self.gender_var.get()
        for widget in self.winfo_children():
            widget.destroy()
        self.height_label = tk.Label(self, text="당신의 키는 몇 cm입니까? 소수점을 제외하고 입력해 주세요.", font=self.customFont)
        self.height_label.pack()
        self.height_entry = tk.Entry(self, width=20)  # 엔트리 너비 설정
        self.height_entry.pack()
        self.prev_button = tk.Button(self, text="이전", command=self.create_widgets, bg="lightgray", fg="black")  # 버튼 색상 변경
        self.prev_button.pack()
        self.next_button = tk.Button(self, text="다음", command=self.next_weight, bg="lightblue", fg="black")  # 버튼 색상 변경
        self.next_button.pack()

    def next_weight(self):
        if not self.height_entry.get().isdigit():
            messagebox.showinfo("에러", "키를 올바르게 입력해주세요.")
            return
        self.height = self.height_entry.get()
        for widget in self.winfo_children():
            widget.destroy()
        self.next_weight_again()
    
    def next_weight_again(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.weight_label = tk.Label(self, text="당신의 몸무게는 몇 kg입니까? 소수점을 제외하고 입력해 주세요.", font=self.customFont)
        self.weight_label.pack()
        self.weight_entry = tk.Entry(self, width=20)  # 엔트리 너비 설정
        self.weight_entry.pack()
        self.prev_button = tk.Button(self, text="이전", command=self.next_height, bg="lightgray", fg="black")  # 버튼 색상 변경
        self.prev_button.pack()
        self.next_button = tk.Button(self, text="다음", command=self.next_age, bg="lightblue", fg="black")  # 버튼 색상 변경
        self.next_button.pack()

    def next_age(self):
        if not self.weight_entry.get().isdigit():
            messagebox.showinfo("에러", "몸무게를 올바르게 입력해주세요.")
            return
        self.weight = self.weight_entry.get()
        for widget in self.winfo_children():
            widget.destroy()
        self.age_label = tk.Label(self, text="당신의 연령은 어떻게 되십니까? 만 나이를 입력해 주세요", font=self.customFont)
        self.age_label.pack()
        self.age_entry = tk.Entry(self, width=20)  # 엔트리 너비 설정
        self.age_entry.pack()
        self.prev_button = tk.Button(self, text="이전", command=self.next_weight_again, bg="lightgray", fg="black")  # 버튼 색상 변경
        self.prev_button.pack()
        self.next_button = tk.Button(self, text="다음", command=self.save_and_show_info, bg="lightblue", fg="black")  # 버튼 색상 변경
        self.next_button.pack()

    def save_and_show_info(self):
        if not self.age_entry.get().isdigit():
            messagebox.showinfo("에러", "나이를 올바르게 입력해주세요.")
            return
        self.age = self.age_entry.get()
        for widget in self.winfo_children():
            widget.destroy()
        result = messagebox.askyesno("입력 정보", f"성별: {self.gender}\n키: {self.height}\n몸무게: {self.weight}\n나이: {self.age}\n해당 정보가 맞습니까?")
        if result:
            user_info = {
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "age": self.age
            }
            userInfo.save_user_info(user_info)
            messagebox.showinfo("성공", "정보가 성공적으로 저장되었습니다.")
            self.master.destroy()  # Close the current window
            os.system('python GUI_Main.py')  # Open the main menu
        else:
            self.create_widgets()

root = tk.Tk()
root.geometry("800x600")  # 화면 크기를 조정하는 코드를 추가합니다.
root.title("Health Kitchen")
app = Application(master=root)
app.mainloop()
