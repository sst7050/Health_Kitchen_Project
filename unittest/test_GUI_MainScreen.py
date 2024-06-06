import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from tkinter import Tk
from GUI_MainScreen import MainScreen

class TestGUIMainScreen(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        self.app = MainScreen(master=self.root)

    def tearDown(self):
        self.app.master.destroy()

    def test_read_user_info(self):
        user_info = self.app.read_user_info()
        self.assertIsNotNone(user_info)

    def test_check_time_limit(self):
        self.app.check_time_limit()
        # 테스트에서 직접 확인하기 어려우므로, 예외가 발생하지 않음을 확인합니다.

    def test_create_main_menu(self):
        self.app.create_main_menu()
        self.assertIsNotNone(self.app.canvas)

    def test_open_fridge(self):
        self.app.open_fridge()
        self.assertEqual(len(self.app.master.winfo_children()), 2)  # 새로운 Toplevel 창이 생성되었는지 확인

    def test_progress_info(self):
        self.app.progress_info()
        self.assertEqual(len(self.app.master.winfo_children()), 2)  # 새로운 Toplevel 창이 생성되었는지 확인

if __name__ == "__main__":
    unittest.main()