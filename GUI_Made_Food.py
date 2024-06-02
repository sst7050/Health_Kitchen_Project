import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

class MadeFoodScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.minsize(400, 400)  # 창 최소 크기 설정
        self.grid(sticky="nsew")
        self.images = []  # 이미지 객체를 참조하기 위한 리스트
        self.create_widgets()

    def create_widgets(self):
        self.master.title("만든 음식 목록")
        
        user_info = self.read_user_info()
        
        if user_info and 'made_food' in user_info:
            self.food_items = user_info['made_food']
            self.display_food_items()
        else:
            self.no_food_label = tk.Label(self, text="만든 음식이 없습니다.", anchor="center", justify="center")
            self.no_food_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)

    def read_user_info(self):
        try:
            with open('user_info.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except UnicodeDecodeError:
            try:
                with open('user_info.json', 'r', encoding='cp949') as file: 
                    return json.load(file)
            except Exception as e:
                print(f"Failed to read the user info file: {e}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def display_food_items(self):
        row, col = 0, 0
        max_cols = 4

        for image_path in self.food_items:
            frame = tk.Frame(self)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            try:
                image = Image.open(image_path)
                image = image.resize((100, 100), Image.LANCZOS)  # 이미지 크기 조정
                photo = ImageTk.PhotoImage(image)
                img_label = tk.Label(frame, image=photo)
                img_label.image = photo
                img_label.pack(padx=5, pady=5)
                self.images.append(photo)  # 참조 유지
            except Exception as e:
                print(f"Failed to load image from {image_path}: {e}")
                tk.Label(frame, text=f"이미지를 불러올 수 없습니다: {image_path}").pack(padx=5, pady=5)

            food_name = image_path.split('/')[-1].split('.')[0]  # 이미지 경로에서 음식 이름 추출
            tk.Label(frame, text=food_name, anchor="w", justify="left").pack(padx=5, pady=5)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        for i in range(row + 1):
            self.grid_rowconfigure(i, weight=1)
        for j in range(max_cols):
            self.grid_columnconfigure(j, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = MadeFoodScreen(master=root)
    app.grid(sticky="nsew")
    root.mainloop()
