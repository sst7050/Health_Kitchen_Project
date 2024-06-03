import tkinter as tk
from tkinter import messagebox
from tkinter.font import Font
import userInfo
import subprocess

class User_input(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
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

        self.bmi_label = tk.Label(self, text="당신의 BMI는 어떻게 되십니까?", font=self.customFont)
        self.bmi_label.pack()
        self.bmi_var = tk.StringVar()
        self.bmi_entry = tk.OptionMenu(self, self.bmi_var, "표준", "저체중", "과체중", "심한과체중")
        self.bmi_entry.pack()

        self.body_fat_label = tk.Label(self, text="당신의 체지방률은 어떻게 되십니까?", font=self.customFont)
        self.body_fat_label.pack()
        self.body_fat_var = tk.StringVar()
        self.body_fat_entry = tk.OptionMenu(self, self.body_fat_var, "표준", "경도비만", "비만", "해당없음")
        self.body_fat_entry.pack()

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
        if not self.gender_var.get() or not self.inbody_entry.get().isdigit() or not self.is_float(self.ideal_weight_entry.get()) or not self.is_float(self.fat_control_entry.get()) or not self.is_float(self.muscle_control_entry.get()) or not self.age_entry.get().isdigit() or not self.bmi_var.get() or not self.body_fat_var.get():
            messagebox.showinfo("에러", "모든 정보를 올바르게 입력해주세요.")
            return
        self.gender = self.gender_var.get()
        self.inbody_score = self.inbody_entry.get()
        self.ideal_weight = self.ideal_weight_entry.get()
        self.fat_control = self.fat_control_entry.get()
        self.muscle_control = self.muscle_control_entry.get()
        self.age = self.age_entry.get()
        self.bmi = self.bmi_var.get()
        self.body_fat = self.body_fat_var.get()
        for widget in self.winfo_children():
            widget.destroy()
        result = messagebox.askyesno("입력 정보", f"성별: {self.gender}\n인바디 점수: {self.inbody_score}\n적정 체중: {self.ideal_weight}\n지방 조절 수치: {self.fat_control}\n근육 조절 수치: {self.muscle_control}\n나이: {self.age}\nBMI: {self.bmi}\n체지방률: {self.body_fat}\n해당 정보가 맞습니까?")
        if result:
            user_info = {
                "gender": self.gender,
                "inbody_score": self.inbody_score,
                "ideal_weight": self.ideal_weight,
                "fat_control": self.fat_control,
                "muscle_control": self.muscle_control,
                "age": self.age,
                "bmi": self.bmi,
                "body_fat": self.body_fat
            }
            # 저장하는 함수
            userInfo.save_user_info(user_info)
            messagebox.showinfo("성공", "정보가 성공적으로 저장되었습니다.")
            #분석하여 status를 json파일에 저장 후 출력
            status, exercise_recommendation = userInfo.update_inbody_status()
            if status == -1 or exercise_recommendation is None:
                messagebox.showinfo("에러", "유효하지 않은 정보가 입력되었습니다. 다시 입력해주세요.")
                self.create_widgets()
            else:
                messagebox.showinfo("분석결과", f"{exercise_recommendation['추천 무산소 운동']['종류']} {exercise_recommendation['추천 무산소 운동']['시간']}분, \n{exercise_recommendation['추천 유산소 운동']['종류']} {exercise_recommendation['추천 유산소 운동']['시간']}분이 당신에게 적합한 운동량입니다.")

                # 최근의 창 닫기
                self.master.destroy()
                # 메인메뉴 열기
                subprocess.run('python GUI_Sel_Food.py')
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
app = User_input(master=root)
app.mainloop()