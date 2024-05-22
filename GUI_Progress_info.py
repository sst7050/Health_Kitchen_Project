import tkinter as tk
from tkinter import messagebox

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
        self.entry.grid(row=0, column=0, columnspan=3, padx=10, pady=20, sticky="ew")

        # 운동량 추가 버튼 (중앙 정렬)
        self.add_button = tk.Button(self, text="운동량 추가", command=self.update_progress)
        self.add_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

    def configure_grid(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=1)

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
            messagebox.showinfo("진행", f"추가된 운동량: {new_amount}")
            self.entry.delete(0, tk.END)  # 입력 필드 클리어
        except ValueError:
            messagebox.showinfo("오류", "유효한 정수를 입력하세요.")

root = tk.Tk()
root.geometry("800x600")
root.title("운동량 트래커")
app = ExerciseTracker(master=root)
root.mainloop()
