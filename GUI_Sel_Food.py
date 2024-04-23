import tkinter as tk
from tkinter import messagebox

class FoodSelectionFrame(tk.Frame):
    def __init__(self, master, switch_frame_callback):
        super().__init__(master)
        self.switch_frame_callback = switch_frame_callback
        self.create_widgets()

    def create_widgets(self):
        food_list = {
            "빵": {"image": "img/Bread.png", "duration": "2개월", "price": "20000원", "detail_name": "뚜레쥬르 2만원권"},
            "햄버거": {"image": "img/Burger.png", "duration": "2개월", "price": "20000원", "detail_name": "맥도날드 2만원권"},
            "치킨": {"image": "img/Chicken.png", "duration": "2개월", "price": "20000원", "detail_name": "교촌치킨 반반 오리지날"},
            "커피": {"image": "img/Coffee.png", "duration": "2개월", "price": "19000원", "detail_name": "스타벅스 피스타치오 크림 콜드 브루 T\n라이트 핑크 자몽 피지오 T\n치킨 & 머쉬룸 멜팅 치즈 샌드위치"},
            "편의점음식": {"image": "img/CU.png", "duration": "2개월", "price": "20000원", "detail_name": "CU 모바일 상품권 2만원권"},
            "아이스크림": {"image": "img/Icecream.png", "duration": "2개월", "price": "18000원", "detail_name": "베스킨라빈스 쿼터(네가지 맛)"},
            "피자": {"image": "img/Pizza.png", "duration": "2개월", "price": "19000원", "detail_name": "반올림피자R + 콜라500ml"}
        }

        row = 0
        col = 0
        for food, info in food_list.items():
            img = tk.PhotoImage(file=info["image"])
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
        self.switch_frame_callback(FoodDetailFrame, info["detail_name"], info)

class FoodDetailFrame(tk.Frame):
    def __init__(self, master, go_back_callback):
        super().__init__(master)
        self.go_back_callback = go_back_callback

    def display_food(self, detail_name, details):
        self.pack_forget()  # Clear any previous frame contents
        self.master.title(f"{detail_name} 상세 정보")

        img = tk.PhotoImage(file=details["image"])
        img_label = tk.Label(self, image=img)
        img_label.image = img  # Keep a reference.
        img_label.pack(side=tk.TOP, pady=20)

        info_text = f"이름: {detail_name}\n예상 기간: {details['duration']}\n가격: {details['price']}"
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
