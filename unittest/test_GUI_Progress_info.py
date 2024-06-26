import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from tkinter import Tk, END
from datetime import datetime, timedelta
from GUI_Progress_info import ExerciseTracker
import shutil
from unittest.mock import patch

class TestExerciseTracker(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.root.withdraw()  # 테스트 중에는 Tkinter 윈도우가 표시되지 않도록 합니다
        self.app = ExerciseTracker(master=self.root, is_test=True)
        self.app.user_info = {
            "유산소": 0,
            "무산소": 0,
            "ingredient": [],
            "exercise_recommendation": {
                "추천 유산소 운동": {"시간": 30},
                "추천 무산소 운동": {"시간": 30}
            },
            "selected_food": {
                "details": {
                    "image": "path/to/image.png",
                    "ingredient_path": "path/to/ingredients/"
                }
            },
            "limit_time": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_user_info()
        self.app.load_user_info()  # Ensure the app loads the updated user_info

    def tearDown(self):
        self.app.master.destroy()
        if os.path.exists("user_info.json"):
            os.remove("user_info.json")
        # 폴더와 그 내용을 삭제합니다
        if os.path.exists("path"):
            shutil.rmtree("path")

    def save_user_info(self):
        with open("user_info.json", "w", encoding='utf-8') as file:
            json.dump(self.app.user_info, file, ensure_ascii=False, indent=4)

    def test_load_user_info(self):
        self.app.load_user_info()
        self.assertIn("유산소", self.app.user_info)
        self.assertIn("무산소", self.app.user_info)
        self.assertIn("ingredient", self.app.user_info)

    def test_save_user_info(self):
        self.app.user_info['유산소'] = 10
        self.app.save_user_info()
        with open("user_info.json", "r", encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(data['유산소'], 10)

    def test_update_progress_aerobic(self):
        self.app.entry_aerobic.delete(0, END)
        self.app.entry_aerobic.insert(0, "10")
        self.app.update_progress("유산소")
        self.assertEqual(self.app.user_info["유산소"], 10)

    def test_update_progress_anaerobic(self):
        self.app.entry_anaerobic.delete(0, END)
        self.app.entry_anaerobic.insert(0, "10")
        self.app.update_progress("무산소")
        self.assertEqual(self.app.user_info["무산소"], 10)

    def test_update_progress_bars(self):
        self.app.user_info["유산소"] = 10
        self.app.user_info["무산소"] = 10
        self.app.update_progress_bars()
        self.assertEqual(self.app.progress_aerobic['value'], 10)
        self.assertEqual(self.app.progress_anaerobic['value'], 10)

    def test_check_ingredient_collection(self):
        self.app.user_info["유산소"] = self.app.recommended_aerobic_time
        self.app.user_info["무산소"] = self.app.recommended_anaerobic_time
        self.save_user_info()  # Ensure the user_info.json reflects these changes
        self.app.check_ingredient_collection()
        self.assertEqual(len(self.app.user_info["ingredient"]), 1)

    def test_show_ingredient_notification(self):
        # Prepare a dummy image file path
        ingredient_image_path = "path/to/ingredients/1.png"
        # Ensure the path exists (you may need to adjust this for your test environment)
        if not os.path.exists(os.path.dirname(ingredient_image_path)):
            os.makedirs(os.path.dirname(ingredient_image_path))
        with open(ingredient_image_path, 'w') as f:
            f.write('')  # Create an empty file to simulate an image

        self.app.show_ingredient_notification(ingredient_image_path, "재료가 냉장고에 추가되었습니다.")
        self.assertEqual(len(self.root.winfo_children()), 2)  # 이미지와 메시지 확인

        # Clean up the dummy file
        os.remove(ingredient_image_path)

    @patch("GUI_Progress_info.messagebox.showinfo")
    @patch("GUI_Progress_info.update_level", return_value='초급 요리사')
    @patch("GUI_Progress_info.GUI_Rank.show_rank_up_message")
    @patch("GUI_Progress_info.tk.Tk.after")
    def test_check_ingredient_collection_completion(self, mock_after, mock_show_rank_up_message, mock_update_level, mock_showinfo):
        # Prepare the user_info for the test scenario
        self.app.user_info["유산소"] = self.app.recommended_aerobic_time
        self.app.user_info["무산소"] = self.app.recommended_anaerobic_time
        self.app.user_info["ingredient"] = ["1.png", "2.png", "3.png"]
        self.save_user_info()

        self.app.check_ingredient_collection()

        # Check that messagebox.showinfo was called
        mock_showinfo.assert_called_once_with("축하합니다!", "모든 재료를 모았습니다! 음식이 만들어집니다.")
        
        # Check that user_info['ingredient'] was reset
        self.assertEqual(self.app.user_info['ingredient'], [])

        # Check that 'made_food' was added to user_info
        self.assertIn('made_food', self.app.user_info)
        self.assertIn("path/to/image.png", self.app.user_info['made_food'])

        # Check that the made food count increased
        self.assertEqual(self.app.user_info['made_food_count'], 1)

        # Check that update_level was called
        mock_update_level.assert_called_once_with(self.app.user_info)

        # Check that show_rank_up_message was called
        mock_show_rank_up_message.assert_called_once_with('초급 요리사')

        # Check that self.master.after was called
        mock_after.assert_called_once_with(100, self.app.relaunch_food_selection)

if __name__ == "__main__":
    unittest.main()
