import tkinter as tk
from tkinter import messagebox

class FoodSelectionFrame(tk.Frame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback
        self.create_widgets()

    def create_widgets(self):
        food_list = {
            "빵": ["img/Bread.png", 250, "한 달", "20000원"],
            "햄버거": ["img/Burger.png", 300, "한 달", "20000원"],
            "치킨": ["img/Chicken.png", 450, "한 달", "20000원"],
            "커피": ["img/Coffee.png", 800, "한 달", "19000원"],
            "편의점음식": ["img/CU.png", 550, "한 달", "20000원"],
            "아이스크림": ["img/Icecream.png", 500, "한 달", "18000원"],
            "피자": ["img/Pizza.png", 900, "한 달", "19000원"]
        }

        row = 0
        col = 0
        for food, info in food_list.items():
            img = tk.PhotoImage(file=info[0])
            button = tk.Button(self, image=img, command=lambda f=food, i=info: self.select_food(f, i))
            button.image = img  # Keep a reference to avoid garbage collection
            button.grid(row=row, column=col, padx=10, pady=10)
            label = tk.Label(self, text=food)
            label.grid(row=row+1, column=col, sticky=tk.N)
            
            col += 1
            if col > 3:
                col = 0
                row += 2

    def select_food(self, food, info):
        self.switch_frame_callback(FoodDetailFrame, food, info)

class FoodDetailFrame(tk.Frame):
    def __init__(self, master, go_back_callback):
        super().__init__(master)
        self.go_back_callback = go_back_callback

    def display_food(self, food, details):
        self.pack_forget()  # Clear any previous frame contents
        self.master.title(f"{food} 상세 정보")

        img = tk.PhotoImage(file=details[0])
        img_label = tk.Label(self, image=img)
        img_label.image = img  # Keep a reference.
        img_label.pack(side=tk.TOP, pady=20)

        info_text = f"이름: {food}\n칼로리: {details[1]} Kcal\n예상 기간: {details[2]}\n가격: {details[3]}"
        info_label = tk.Label(self, text=info_text)
        info_label.pack(side=tk.TOP, pady=20)

        prev_button = tk.Button(self, text="이전", command=self.go_back)
        prev_button.pack(side=tk.LEFT, padx=20, pady=20)

        next_button = tk.Button(self, text="다음", command=self.go_next)
        next_button.pack(side=tk.RIGHT, padx=20, pady=20)

    def go_back(self):
        self.go_back_callback(FoodSelectionFrame)

    def go_next(self):
        messagebox.showinfo("다음 단계", "다음 단계로 진행합니다.")

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.current_frame = None
        self.switch_frame(FoodSelectionFrame)

    def switch_frame(self, frame_class, food=None, info=None):
        new_frame = frame_class(self, self.switch_frame)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        if food and info:
            self.current_frame.display_food(food, info)
        self.current_frame.pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()