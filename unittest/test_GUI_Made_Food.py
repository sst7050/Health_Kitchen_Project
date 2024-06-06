import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import tkinter as tk
from GUI_Made_Food import MadeFoodScreen
import json


class TestMadeFoodScreen(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary user_info.json file for testing
        cls.user_info = {
            "made_food": [
                "path/to/food1.jpg",
                "path/to/food2.jpg"
            ]
        }
        with open('user_info.json', 'w', encoding='utf-8') as f:
            json.dump(cls.user_info, f)

    @classmethod
    def tearDownClass(cls):
        # Remove the temporary user_info.json file after testing
        if os.path.exists('user_info.json'):
            os.remove('user_info.json')

    def setUp(self):
        self.root = tk.Tk()
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        self.app = MadeFoodScreen(master=self.root)

    def tearDown(self):
        self.app.destroy()
        self.root.destroy()

    def test_read_user_info(self):
        user_info = self.app.read_user_info()
        self.assertEqual(user_info, self.user_info)

    def test_create_widgets(self):
        self.app.create_widgets()
        # Check if the title is set correctly
        self.assertEqual(self.root.title(), "만든 음식 목록")
        # Check if food items are loaded correctly
        self.assertEqual(len(self.app.food_items), len(self.user_info['made_food']))
        self.assertEqual(self.app.food_items, self.user_info['made_food'])

    def test_display_food_items(self):
        self.app.create_widgets()
        self.app.display_food_items()
        # Check if the images and labels are created
        for i, image_path in enumerate(self.user_info['made_food']):
            frame = self.app.grid_slaves(row=i // 4, column=i % 4)[0]
            labels = frame.winfo_children()
            self.assertEqual(len(labels), 2)  # Each frame should contain an image label and a text label
            self.assertIn(image_path.split('/')[-1].split('.')[0], labels[1].cget("text"))

if __name__ == "__main__":
    unittest.main()
