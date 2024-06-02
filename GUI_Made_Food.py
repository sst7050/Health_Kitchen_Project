import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

class MadeFoodScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.master.title("만든 음식 목록")
        self.pack(fill="both", expand=True)
        
        user_info = self.read_user_info()
        
        if user_info and 'made_food' in user_info:
            self.food_items = user_info['made_food']
            self.display_food_items()
        else:
            tk.Label(self, text="만든 음식 목록이 없습니다.", anchor="center", justify="left").pack(padx=10, pady=10, fill="both", expand=True)

        self.close_button = tk.Button(self, text="닫기", command=self.master.destroy)
        self.close_button.pack(pady=10)

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
        for image_path in self.food_items:
            frame = tk.Frame(self)
            frame.pack(padx=10, pady=10, fill="x", expand=True)

            try:
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                img_label = tk.Label(frame, image=photo)
                img_label.image = photo  # keep a reference to avoid garbage collection
                img_label.pack(side="left", padx=10, pady=10)
            except Exception as e:
                print(f"Failed to load image from {image_path}: {e}")
                tk.Label(frame, text=f"이미지를 불러올 수 없습니다: {image_path}").pack(side="left", padx=10, pady=10)

            food_name = image_path.split('/')[-1].split('.')[0]  # 이미지 경로에서 음식 이름 추출
            tk.Label(frame, text=food_name, anchor="w", justify="left").pack(side="left", padx=10, pady=10, fill="x", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = MadeFoodScreen(master=root)
    root.mainloop()
