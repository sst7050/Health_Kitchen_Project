import tkinter as tk
from PIL import Image, ImageTk
import json

class MadeFoodScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.minsize(400, 400)  # Set the minimum window size
        self.grid(sticky="nsew")
        self.images = []  # List to hold image objects
        self.create_widgets()

    def create_widgets(self):
        self.master.title("List of Made Foods")
        
        user_info = self.read_user_info()
        
        if 'made_food' in user_info:
            self.food_items = user_info['made_food']
            self.display_food_items()

    def read_user_info(self):
        try:
            with open('user_info.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("The user_info.json file does not exist. Starting with an empty list.")
            return {"made_food": []}  # Provide a default value with the "made_food" key
        except UnicodeDecodeError as e:
                print(f"Failed to read the user info file: {e}")
                return {"made_food": []}  # Provide a default value in case of any other exception
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"made_food": []}  # Provide a default value in case of any other exception

    def display_food_items(self):
        row, col = 0, 0
        max_cols = 4

        for image_path in self.food_items:
            frame = tk.Frame(self)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            try:
                image = Image.open(image_path)
                image = image.resize((150, 150), Image.LANCZOS)  # Resize the image
                photo = ImageTk.PhotoImage(image)
                img_label = tk.Label(frame, image=photo)
                img_label.image = photo
                img_label.pack(padx=5, pady=5)
                self.images.append(photo)  # Keep a reference to the image
            except Exception as e:
                print(f"Failed to load image from {image_path}: {e}")
                tk.Label(frame, text=f"Cannot load image: {image_path}").pack(padx=5, pady=5)

            food_name = image_path.split('/')[-1].split('.')[0]  # Extract the food name from the image path
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