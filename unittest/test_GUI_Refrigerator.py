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

    