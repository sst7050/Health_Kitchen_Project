import tkinter as tk
from PIL import Image, ImageTk

class RefrigeratorScreen(tk.Frame):
    def __init__(self, master=None, main_screen=None):
        super().__init__(master)
        self.master = master
        self.main_screen = main_screen
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.master.title("냉장고")
        self.master.geometry("800x600")  # 창 크기 설정
        self.master.resizable(False, False)

        # 배경 이미지 로드
        self.background_image = Image.open("img/refrigerator.png")
        self.background_image = self.background_image.resize((800, 600), Image.LANCZOS)  # 창 크기에 맞게 이미지 크기 조정
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # 캔버스 생성 및 배경 이미지 추가
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.canvas.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")

        # 재료 이미지 로드 및 배치
        self.ingredient_images_paths = [
            "img/food/Burger/ingredient/1.png", 
            "img/food/Burger/ingredient/2.png", 
            "img/food/Burger/ingredient/3.png", 
            "img/food/Burger/ingredient/4.png"
        ]
        self.ingredient_images = []  # 이미지를 저장할 리스트
        
        for idx, img_path in enumerate(self.ingredient_images_paths):
            img = Image.open(img_path)
            img = img.resize((150, 150), Image.LANCZOS)  # 이미지 크기를 150x150으로 조정
            photo_img = ImageTk.PhotoImage(img)
            # 각 이미지의 x, y 좌표 설정
            x_offset = 200 if idx % 2 == 0 else 500
            y_offset = 200 if idx // 2 == 0 else 400
            self.canvas.create_image(x_offset, y_offset, anchor="nw", image=photo_img)
            self.ingredient_images.append(photo_img)  # 이미지 리스트에 추가하여 참조 유지

if __name__ == "__main__":
    root = tk.Tk()
    app = RefrigeratorScreen(master=root)
    root.mainloop()
