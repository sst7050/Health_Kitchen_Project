import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import messagebox

# GUI_Rank.py 파일의 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GUI_Rank import RankImageFrame, show_rank_up_message

class TestRankImageFrame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 테스트 중에 메인 윈도우 숨기기
        self.switch_frame_callback = MagicMock()
        self.frame = RankImageFrame(self.root, self.switch_frame_callback)

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        self.assertEqual(self.frame.switch_frame_callback, self.switch_frame_callback)
        # 추가적인 속성이나 메서드 테스트가 필요하다면 여기에 추가

class TestShowRankUpMessage(unittest.TestCase):
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.Tk')
    def test_show_rank_up_message(self, mock_tk, mock_showinfo):
        level = 5
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance
        
        show_rank_up_message(level)
        
        mock_tk.assert_called_once()
        mock_showinfo.assert_called_once_with("축하합니다", f"축하합니다, 당신은 {level} 레벨로 승급하셨습니다!")
        mock_tk_instance.withdraw.assert_called_once()
        mock_tk_instance.destroy.assert_called_once()

if __name__ == '__main__':
    unittest.main()
