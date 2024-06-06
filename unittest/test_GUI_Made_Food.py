"""import unittest
import tkinter as tk
from unittest.mock import patch, mock_open
import os
import sys

# GUI_Made_Food.py 파일이 있는 상위 디렉토리를 path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# 현재 작업 디렉토리를 GUI_Made_Food.py 파일이 있는 디렉토리로 변경
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GUI_Made_Food import MadeFoodScreen

class TestMadeFoodScreen(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = MadeFoodScreen(master=self.root)

    def tearDown(self):
        self.root.destroy()

    @patch("builtins.open", new_callable=mock_open, read_data='{"made_food": ["path/to/image.png"]}')
    def test_read_user_info(self, mock_file):
        # 사용자 정보 파일이 잘 읽혀지는지 테스트
        user_info = self.app.read_user_info()
        self.assertIsNotNone(user_info)
        self.assertIn("made_food", user_info)
        self.assertEqual(user_info["made_food"], ["path/to/image.png"])

    @patch("builtins.print")
    def test_display_food_items_with_no_items(self, mock_print):
        # 만든 음식 목록이 없을 때 적절한 처리가 되는지 테스트
        self.app.food_items = []
        self.app.display_food_items()
        mock_print.assert_called_with("Failed to load image from : open() argument 1 must be str, bytes or os.PathLike object, not None")

if __name__ == "__main__":
    unittest.main()"""

import unittest
import tkinter as tk
from unittest.mock import patch, mock_open
import os
import sys

# GUI_Made_Food.py 파일이 있는 상위 디렉토리를 path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# 현재 작업 디렉토리를 GUI_Made_Food.py 파일이 있는 디렉토리로 변경
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GUI_Made_Food import MadeFoodScreen

class TestMadeFoodScreen(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = MadeFoodScreen(master=self.root)

    def tearDown(self):
        self.root.destroy()

    @patch("builtins.open", new_callable=mock_open, read_data='{"made_food": ["path/to/image.png"]}')
    def test_read_user_info(self, mock_file):
        # 사용자 정보 파일이 잘 읽혀지는지 테스트
        user_info = self.app.read_user_info()
        self.assertIsNotNone(user_info)
        self.assertIn("made_food", user_info)
        self.assertEqual(user_info["made_food"], ["path/to/image.png"])

    @patch("os.path.exists", return_value=False)
    def test_read_user_info_file_not_exist(self, mock_exists):
    # 사용자 정보 파일이 없을 때 빈 딕셔너리를 반환하는지 테스트
        user_info = self.app.read_user_info()
        self.assertEqual(user_info, {"made_food":[]})

    @patch("builtins.print")
    def test_display_food_items_with_no_items(self, mock_print):
        # 만든 음식 목록이 없을 때 적절한 처리가 되는지 테스트
        self.app.food_items = []
        self.app.display_food_items()
        # 이미지가 없는 경우 출력되는 메시지를 확인
        mock_print.assert_not_called()

if __name__ == "__main__":
    unittest.main()