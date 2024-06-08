import unittest
import os
import sys
from PIL import Image, ImageTk
from unittest.mock import patch, MagicMock

# GUI_Made_Food.py 파일이 있는 상위 디렉토리를 path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# 현재 작업 디렉토리를 GUI_Made_Food.py 파일이 있는 디렉토리로 변경
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GUI_Made_Food import MadeFoodScreen
import tkinter as tk
from unittest.mock import patch, mock_open

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

    @patch('builtins.open')
    def test_read_user_info_unicode_decode_error(self, mock_open):
        # Configure mock to raise UnicodeDecodeError
        mock_open.side_effect = UnicodeDecodeError("utf-8", b'\x80', 1, 2, "mock reason")

        # Call the function and check if it returns the default value
        result = self.app.read_user_info()
        self.assertEqual(result, {"made_food": []})

    @patch('builtins.open')
    def test_read_user_info_file_not_found_error(self, mock_open):
        # Configure mock to raise FileNotFoundError
        mock_open.side_effect = FileNotFoundError

        # Call the function and check if it returns the default value
        result = self.app.read_user_info()
        self.assertEqual(result, {"made_food": []})

    @patch('builtins.open')
    def test_read_user_info_other_exception(self, mock_open):
        # Configure mock to raise a generic Exception
        mock_open.side_effect = Exception("mock exception")

        # Call the function and check if it returns the default value
        result = self.app.read_user_info()
        self.assertEqual(result, {"made_food": []})
    
    @patch("builtins.print")
    def test_display_food_items_with_no_items(self, mock_print):
        # 만든 음식 목록이 없을 때 적절한 처리가 되는지 테스트
        self.app.food_items = []
        self.app.display_food_items()
        # 이미지가 없는 경우 출력되는 메시지를 확인
        mock_print.assert_not_called()
        
    @patch("builtins.print")
    def test_display_food_items_load_image_success(self, mock_print):
        # 이미지를 성공적으로 로드하는 경우를 테스트합니다.
        self.app.food_items = ["path/to/image1.jpg"]
        with patch.object(Image, 'open') as mock_open:
            mock_image = MagicMock()
            mock_open.return_value = mock_image
            self.app.display_food_items()
            # 이미지를 성공적으로 로드하고 GUI에 표시하는지 확인합니다.
            mock_open.assert_called_with("path/to/image1.jpg")
            mock_image.resize.assert_called_with((150, 150), Image.LANCZOS)
            self.assertTrue(mock_image.resize.called)
            self.assertEqual(len(self.app.grid_slaves()), 1)  # 두 개의 위젯이 그리드에 배치되었는지 확인합니다.

    @patch("builtins.print")
    def test_display_food_items_load_image_failure(self, mock_print):
        # 이미지를 로드하지 못하는 경우를 테스트합니다.
        self.app.food_items = ["path/to/image1.jpg"]
        with patch.object(Image, 'open') as mock_open:
            mock_open.side_effect = FileNotFoundError("Image not found")
            self.app.display_food_items()
            # 이미지 로드 실패 시 적절한 메시지를 출력하는지 확인합니다.
            mock_print.assert_called_once_with("Failed to load image from path/to/image1.jpg: Image not found")
            self.assertEqual(len(self.app.grid_slaves()), 1)  # 두 개의 위젯이 그리드에 배치되었는지 확인합니다.
            
if __name__ == "__main__":
    unittest.main()