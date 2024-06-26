import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import tkinter as tk
import json
import os
from PIL import Image
from GUI_Refrigerator import RefrigeratorScreen

class TestRefrigeratorScreen(unittest.TestCase):
    def setUp(self):
        # 임시 JSON 데이터 생성
        self.user_info = {
            "selected_food": {
                "details": {
                    "ingredient_path": "temp_ingredients"
                }
            },
            "ingredient": ["test_img1.png", "test_img2.png"]
        }
        with open("user_info.json", "w", encoding="utf-8") as file:
            json.dump(self.user_info, file)
        
        # 임시 이미지 디렉토리 및 파일 생성
        os.makedirs("temp_ingredients", exist_ok=True)
        for img_name in self.user_info["ingredient"]:
            img = Image.new('RGB', (100, 100), color = 'red')
            img.save(os.path.join("temp_ingredients", img_name))

    def tearDown(self):
        # 생성한 파일 및 디렉토리 삭제
        if os.path.exists("user_info.json"):
            os.remove("user_info.json")
        
        for img_name in self.user_info["ingredient"]:
            img_path = os.path.join("temp_ingredients", img_name)
            if os.path.exists(img_path):
                os.remove(img_path)
        
        if os.path.exists("temp_ingredients"):
            os.rmdir("temp_ingredients")

    def test_load_selected_food_info(self):
        root = tk.Tk()
        app = RefrigeratorScreen(master=root)
        self.assertEqual(app.selected_food_info, self.user_info)

    def test_create_widgets_with_ingredients(self):
        root = tk.Tk()
        app = RefrigeratorScreen(master=root)
        app.create_widgets()
        self.assertTrue(hasattr(app, 'ingredient_images'))
        self.assertEqual(len(app.ingredient_images), 2)
        root.destroy()

if __name__ == "__main__":
    unittest.main()
