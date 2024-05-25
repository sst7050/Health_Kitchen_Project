import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import PhotoImage

class ExerciseTracker(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()
        self.configure_grid()

    def create_widgets(self):
        # 유산소 운동량 입력 필드
        self.entry_aerobic = tk.Entry(self, width=40)
        self.entry_aerobic.insert(0, "유산소 운동량을 입력하세요")
        self.entry_aerobic.bind("<FocusIn>", lambda event: self.on_entry_click(event, "유산소 운동량을 입력하세요"))
        self.entry_aerobic.bind("<FocusOut>", lambda event: self.on_focusout(event, "유산소 운동량을 입력하세요"))
        self.entry_aerobic.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        # 유산소 운동량 추가 버튼
        self.add_button_aerobic = tk.Button(self, text="유산소 추가", command=lambda: self.update_progress("유산소"))
        self.add_button_aerobic.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # 무산소 운동량 입력 필드
        self.entry_anaerobic = tk.Entry(self, width=40)
        self.entry_anaerobic.insert(0, "무산소 운동량을 입력하세요")
        self.entry_anaerobic.bind("<FocusIn>", lambda event: self.on_entry_click(event, "무산소 운동량을 입력하세요"))
        self.entry_anaerobic.bind("<FocusOut>", lambda event: self.on_focusout(event, "무산소 운동량을 입력하세요"))
        self.entry_anaerobic.grid(row=1, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        # 무산소 운동량 추가 버튼
        self.add_button_anaerobic = tk.Button(self, text="무산소 추가", command=lambda: self.update_progress("무산소"))
        self.add_button_anaerobic.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # 유산소 진척도 게이지 바
        self.progress_aerobic = ttk.Progressbar(self, length=700, mode='determinate')
        self.progress_aerobic.grid(row=2, column=0, columnspan=3, pady=20, sticky="ew")
        self.progress_label_aerobic = tk.Label(self, text=f"유산소: {self.user_info['유산소']}/100")
        self.progress_label_aerobic.grid(row=2, column=3, padx=10, sticky="w")

        # 무산소 진척도 게이지 바
        self.progress_anaerobic = ttk.Progressbar(self, length=700, mode='determinate')
        self.progress_anaerobic.grid(row=3, column=0, columnspan=3, pady=20, sticky="ew")
        self.progress_label_anaerobic = tk.Label(self, text=f"무산소: {self.user_info['무산소']}/100")
        self.progress_label_anaerobic.grid(row=3, column=3, padx=10, sticky="w")

        # 이미지 표시 (하단에 위치 조정)
        self.image = PhotoImage(file="img/chicken.png")  # 적절한 이미지 파일 경로로 변경하세요
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.grid(row=4, column=0, columnspan=4, pady=20, sticky="nsew")  # 위치를 row=4으로 변경

    def configure_grid(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)  # 중간에 추가 공간을 만들기 위한 행
        self.master.grid_rowconfigure(3, weight=1)  # 이미지를 보여줄 행
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=0)

    def on_entry_click(self, event):
        if self.entry.get() == "운동량을 입력하세요":
            self.entry.delete(0, tk.END)  # delete all the text in the entry

    def on_focusout(self, event):
        if not self.entry.get():
            self.entry.insert(0, "운동량을 입력하세요")

    def update_progress(self):
        try:
            # 입력된 운동량을 정수로 변환하고 게이지 바 업데이트
            new_amount = int(self.entry.get())
            current_value = self.progress['value']
            new_value = min(current_value + new_amount, 100)  # 최대 100으로 제한
            self.progress['value'] = new_value
            self.progress_label.config(text=f"{new_value}/100")  # 레이블 업데이트
            self.entry.delete(0, tk.END)  # 입력 필드 클리어
        except ValueError:
            messagebox.showinfo("오류", "유효한 정수를 입력하세요.")

root = tk.Tk()
root.geometry("800x600")
root.title("운동진행상황")
app = ExerciseTracker(master=root)
root.mainloop()
