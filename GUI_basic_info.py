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
        # self.check_and_display_user_info()

    # def check_and_display_user_info(self):
    #     exists, user_info = userInfo.read_user_info()
    #     if exists:
    #         messagebox.showinfo("정보 확인", "사용자 정보가 이미 존재합니다.")
    #         messagebox.showinfo("사용자 정보\n", f"성별: {user_info['gender']}\n인바디 점수: {user_info['inbody_score']}\n적정 체중: {user_info['ideal_weight']}\n지방 조절 수치: {user_info['fat_control']}\n근육 조절 수치: {user_info['muscle_control']}\n나이: {user_info['age']}\n")
    #         self.master.destroy()  # Close the current window
    #         os.system('python GUI_Main.py')  # Open the main menu
    #     else:
    #         messagebox.showinfo("알림", "이 프로그램은 당신의 인바디 '분석 평가'(결과지의 우측 부분)의 일부 항목값을 입력받아 그 값을 토대로 적정 체중이 되도록 돕거나 유지시켜주는 프로그램 입니다. 따라서 다음 질문에 답 하기 전에 먼저 인바디 검사를 받고, 해당 검사지를 출력하여 준비해 주시기 바랍니다. 만약 인바디 검사지가 준비되셨다면, 질문에 솔직하게 답변 해 주세요.")
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

        self.inbody_label = tk.Label(self, text="당신의 인바디 점수는 몇 점입니까?", font=self.customFont)
        self.inbody_label.pack()
        self.inbody_entry = tk.Entry(self, width=20)  # 엔트리 너비 설정
        self.inbody_entry.pack()

        self.ideal_weight_label = tk.Label(self, text="당신의 적정 체중은 몇 kg 입니까? 소수점을 포함하여 입력해 주세요.", font=self.customFont)
        self.ideal_weight_label.pack()
        self.ideal_weight_entry = tk.Entry(self, width=20)  # 엔트리 너비 설정
        self.ideal_weight_entry.pack()

        self.fat_control_label = tk.Label(self, text="당신의 지방 조절 수치는 몇 kg 입니까? 소수점을 포함하여 입력해 주세요.", font=self.customFont)
        self.fat_control_label.pack()
        self.fat_control_entry = tk.Entry(self, width=20)  # 엔트리 너비 설정
        self.fat_control_entry.pack()

        self.muscle_control_label = tk.Label(self, text="당신의 근육 조절 수치는 몇 kg 입니까? 소수점을 포함하여 입력해 주세요.", font=self.customFont)
        self.muscle_control_label.pack()
        self.muscle_control_entry = tk.Entry(self, width=20)  # 엔트리 너비 설정
        self.muscle_control_entry.pack()

        self.age_label = tk.Label(self, text="당신의 연령은 어떻게 되십니까? 만 나이를 입력해 주세요", font=self.customFont)
        self.age_label.pack()
        self.age_entry = tk.Entry(self, width=20)  # 엔트리 너비 설정
        self.age_entry.pack()

        self.save_button = tk.Button(self, text="저장", command=self.save_and_show_info, bg="lightblue", fg="black")  # 버튼 색상 변경
        self.save_button.pack()

    def save_and_show_info(self):
        if not self.gender_var.get() or not self.inbody_entry.get().isdigit() or not self.is_float(self.ideal_weight_entry.get()) or not self.is_float(self.fat_control_entry.get()) or not self.is_float(self.muscle_control_entry.get()) or not self.age_entry.get().isdigit():
            messagebox.showinfo("에러", "모든 정보를 올바르게 입력해주세요.")
            return
        self.gender = self.gender_var.get()
        self.inbody_score = self.inbody_entry.get()
        self.ideal_weight = self.ideal_weight_entry.get()
        self.fat_control = self.fat_control_entry.get()
        self.muscle_control = self.muscle_control_entry.get()
        self.age = self.age_entry.get()
        for widget in self.winfo_children():
            widget.destroy()
        result = messagebox.askyesno("입력 정보", f"성별: {self.gender}\n인바디 점수: {self.inbody_score}\n적정 체중: {self.ideal_weight}\n지방 조절 수치: {self.fat_control}\n근육 조절 수치: {self.muscle_control}\n나이: {self.age}\n해당 정보가 맞습니까?")
        if result:
            user_info = {
            "gender": self.gender,
            "inbody_score": self.inbody_score,
            "ideal_weight": self.ideal_weight,
            "fat_control": self.fat_control,
            "muscle_control": self.muscle_control,
            "age": self.age
            }
            userInfo.save_user_info(user_info)
            messagebox.showinfo("성공", "정보가 성공적으로 저장되었습니다.")
            self.master.destroy()  # Close the current window
            os.system('python GUI_Main.py')  # Open the main menu
        else:
            self.create_widgets()

    def is_float(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

root = tk.Tk()
root.geometry("800x600")  # 화면 크기를 조정하는 코드를 추가합니다.
root.title("Health Kitchen")
app = Application(master=root)
app.mainloop()

