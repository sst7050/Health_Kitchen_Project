import tkinter as tk
from tkinter import messagebox

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.gender_label = tk.Label(self, text="당신의 성별은 무엇입니까?")
        self.gender_label.pack()
        self.gender_var = tk.StringVar()
        self.gender_entry = tk.OptionMenu(self, self.gender_var, "남성", "여성")
        self.gender_entry.pack()
        self.next_button = tk.Button(self, text="다음", command=self.next_height)
        self.next_button.pack()

    def next_height(self):
        if not self.gender_var.get():
            messagebox.showinfo("에러", "성별을 선택해주세요.")
            return
        self.gender = self.gender_var.get()
        for widget in self.winfo_children():
            widget.destroy()
        self.height_label = tk.Label(self, text="당신의 키는 몇 cm입니까? 소수점을 제외하고 입력해 주세요.")
        self.height_label.pack()
        self.height_entry = tk.Entry(self)
        self.height_entry.pack()
        self.prev_button = tk.Button(self, text="이전", command=self.create_widgets)
        self.prev_button.pack()
        self.next_button = tk.Button(self, text="다음", command=self.next_weight)
        self.next_button.pack()

    def next_weight(self):
        if not self.height_entry.get().isdigit():
            messagebox.showinfo("에러", "키를 올바르게 입력해주세요.")
            return
        self.height = self.height_entry.get()
        for widget in self.winfo_children():
            widget.destroy()
        self.weight_label = tk.Label(self, text="당신의 몸무게는 몇 kg입니까? 소수점을 제외하고 입력해 주세요.")
        self.weight_label.pack()
        self.weight_entry = tk.Entry(self)
        self.weight_entry.pack()
        self.prev_button = tk.Button(self, text="이전", command=self.next_height)
        self.prev_button.pack()
        self.next_button = tk.Button(self, text="다음", command=self.next_age)
        self.next_button.pack()

    def next_age(self):
        if not self.weight_entry.get().isdigit():
            messagebox.showinfo("에러", "몸무게를 올바르게 입력해주세요.")
            return
        self.weight = self.weight_entry.get()
        for widget in self.winfo_children():
            widget.destroy()
        self.age_label = tk.Label(self, text="당신의 연령은 어떻게 되십니까? 만 나이를 입력해 주세요")
        self.age_label.pack()
        self.age_entry = tk.Entry(self)
        self.age_entry.pack()
        self.prev_button = tk.Button(self, text="이전", command=self.next_weight)
        self.prev_button.pack()
        self.next_button = tk.Button(self, text="다음", command=self.show_info)
        self.next_button.pack()

    def show_info(self):
        if not self.age_entry.get().isdigit():
            messagebox.showinfo("에러", "나이를 올바르게 입력해주세요.")
            return
        self.age = self.age_entry.get()
        for widget in self.winfo_children():
            widget.destroy()
        result = messagebox.askyesno("입력 정보", f"성별: {self.gender}\n키: {self.height}\n몸무게: {self.weight}\n나이: {self.age}\n해당 정보가 맞습니까?")
        if result:
            messagebox.showinfo("성공", "정보가 성공적으로 저장되었습니다.")
            self.master.after(self.master.quit)
        else:
            self.create_widgets()

root = tk.Tk()
root.geometry("800x600")  # 화면 크기를 조정하는 코드를 추가합니다.
root.title("Health Kitchen")
app = Application(master=root)
app.mainloop()