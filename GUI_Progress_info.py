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
        # 운동량 입력 필드 (확장된 크기)
        self.entry = tk.Entry(self, width=40)
        self.entry.insert(0, "운동량을 입력하세요")  # 초기 텍스트 설정
        self.entry.bind("<FocusIn>", self.on_entry_click)
        self.entry.bind("<FocusOut>", self.on_focusout)
        self.entry.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        # 운동량 추가 버튼 (중앙 정렬)
        self.add_button = tk.Button(self, text="운동량 추가", command=self.update_progress)
        self.add_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # 진척도 게이지 바 (길이 조절)
        self.progress = ttk.Progressbar(self, length=700, mode='determinate')
        self.progress.grid(row=1, column=0, columnspan=3, pady=20, sticky="ew")

        # 진척도 표시 레이블
        self.progress_label = tk.Label(self, text="0/100")
        self.progress_label.grid(row=1, column=3, padx=10, sticky="w")

        # 이미지 표시 (하단에 위치 조정)
        self.image = PhotoImage(file="img/chicken.png")  # 적절한 이미지 파일 경로로 변경하세요
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.grid(row=3, column=0, columnspan=4, pady=20, sticky="nsew")  # 위치를 row=3으로 변경

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
        """Clear the entry field on focus if it contains the default text."""
        if self.entry.get() == "운동량을 입력하세요":
            self.entry.delete(0, tk.END)  # delete all the text in the entry

    def on_focusout(self, event):
        """Put the default text if the field is empty."""
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
root.title("운동량 트래커")
app = ExerciseTracker(master=root)
root.mainloop()
