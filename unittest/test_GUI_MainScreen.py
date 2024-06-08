import sys
import os
import unittest
import json
from tkinter import Tk
from datetime import datetime, timedelta
import shutil
from unittest.mock import patch

# 현재 파일의 부모 디렉토리를 경로에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GUI_MainScreen import MainScreen

class TestGUIMainScreen(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        # 현재 파일의 부모 디렉토리 설정
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.user_info_path = os.path.join(base_path, 'user_info.json')
        self.image_path = os.path.join(base_path, 'path/to/image.png')

        # 임시 user_info.json 파일 생성
        self.app = MainScreen(master=self.root)
        self.app.user_info = {
            "inbody_score": "80",
            "fat_control": "0",
            "muscle_control": "0",
            "bmi": "표준",
            "body_fat": "표준",
            "status": 5,
            "exercise_recommendation": {
                "현재 상태": "표준",
                "추천 목표": "지방 유지, 근육 유지",
                "추천 유산소 운동": {
                    "종류": "걷기",
                    "시간": 30
                },
                "추천 무산소 운동": {
                    "종류": "저강도 무산소 운동",
                    "시간": 45
                }
            },
            "level": "주방 견습생",
            "made_food_count": 0,
            "limit_time": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "selected_food": {
                "food": "치킨",
                "details": {
                    "image": self.image_path,
                    "detail_name": "치킨",
                    "ingredient_path": "path/to/ingredients/"
                }
            },
            "ingredient": [],
            "유산소": 0,
            "무산소": 0
        }
        self.save_user_info()
        self.app.read_user_info()  # Ensure the app loads the updated user_info

        # 임시 이미지 파일 생성
        self.create_temp_image(self.image_path)

    def tearDown(self):
        try:
            self.app.master.destroy()
        except:
            pass
        if os.path.exists(self.user_info_path):
            os.remove(self.user_info_path)
        if os.path.exists("path"):
            shutil.rmtree("path")

    def save_user_info(self):
        with open(self.user_info_path, "w", encoding='utf-8') as file:
            json.dump(self.app.user_info, file, ensure_ascii=False, indent=4)

    def create_temp_image(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path, 'w') as f:
            f.write('')  # 빈 파일 생성

    def test_read_user_info(self):
        self.app.read_user_info()
        self.assertIn("유산소", self.app.user_info)
        self.assertIn("무산소", self.app.user_info)
        self.assertIn("ingredient", self.app.user_info)

    def test_check_time_limit(self):
        self.app.read_user_info()
        try:
            self.app.check_time_limit()
        except Exception as e:
            self.fail(f"check_time_limit 실행 중 예외가 발생했습니다: {e}")

    def test_create_main_menu(self):
        self.app.create_main_menu()
        self.assertIsNotNone(self.app.canvas)

    def test_open_fridge(self):
        self.app.open_fridge()
        self.assertEqual(len(self.app.master.winfo_children()), 2)  # 새로운 Toplevel 창이 생성되었는지 확인

    def test_progress_info(self):
        self.app.progress_info()
        self.assertEqual(len(self.app.master.winfo_children()), 2)  # 새로운 Toplevel 창이 생성되었는지 확인
    
    @patch("GUI_MainScreen.MainScreen.read_user_info")
    def test_show_about(self, mock_read_user_info):
        # 가짜 사용자 정보 생성
        fake_user_info = {
            "inbody_score": "80",
            "fat_control": "0",
            "muscle_control": "0",
            "bmi": "표준",
            "body_fat": "표준",
            "exercise_recommendation": {
                "추천 유산소 운동": {"종류": "걷기", "시간": 30},
                "추천 무산소 운동": {"종류": "저강도 무산소 운동", "시간": 45}
            },
            "selected_food": {"food": "치킨"},
            "ingredient": [],
            "limit_time": "2024-06-08 12:00:00",
            "level": "주방 견습생",
            "made_food_count": 0
        }
        mock_read_user_info.return_value = fake_user_info

        # 테스트할 메서드 호출
        MainScreen(master=self.root).show_about()
        
if __name__ == "__main__":
    unittest.main()
