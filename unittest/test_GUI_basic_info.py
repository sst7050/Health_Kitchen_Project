import sys
import os
import unittest
from unittest.mock import patch
import tkinter as tk

# 현재 파일의 디렉토리 경로를 가져와 상위 디렉토리로 설정합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
os.chdir(parent_dir)

from GUI_basic_info import User_input

class TestUserInput(unittest.TestCase):
    
    def setUp(self):
        self.root = tk.Tk()
        self.app = User_input(master=self.root)

    def tearDown(self):
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def test_create_widgets(self):
        self.app.create_widgets()
        self.assertIsInstance(self.app.bmi_label, tk.Label)
        self.assertIsInstance(self.app.bmi_entry, tk.OptionMenu)
        self.assertIsInstance(self.app.body_fat_label, tk.Label)
        self.assertIsInstance(self.app.body_fat_entry, tk.OptionMenu)
        self.assertIsInstance(self.app.inbody_label, tk.Label)
        self.assertIsInstance(self.app.inbody_entry, tk.Entry)
        self.assertIsInstance(self.app.fat_control_label, tk.Label)
        self.assertIsInstance(self.app.fat_control_entry, tk.Entry)
        self.assertIsInstance(self.app.muscle_control_label, tk.Label)
        self.assertIsInstance(self.app.muscle_control_entry, tk.Entry)
        self.assertIsInstance(self.app.save_button, tk.Button)

    @patch('tkinter.messagebox.showwarning')
    def test_save_and_show_info_invalid_input(self, mock_showwarning):
        self.app.bmi_var.set('')
        self.app.body_fat_var.set('')
        self.app.inbody_entry.insert(0, 'not a digit')
        self.app.fat_control_entry.insert(0, 'not a float')
        self.app.muscle_control_entry.insert(0, 'not a float')
        self.app.save_and_show_info()
        mock_showwarning.assert_called_with("에러", "모든 정보를 올바르게 입력해주세요.")

    @patch('tkinter.messagebox.askyesno', return_value=True)
    @patch('tkinter.messagebox.showinfo')
    @patch('userInfo.save_user_info')
    @patch('userInfo.update_inbody_status', return_value=(0, {
        '추천 무산소 운동': {'종류': '스쿼트', '시간': 30},
        '추천 유산소 운동': {'종류': '달리기', '시간': 20}
    }))
    @patch('subprocess.run')
    def test_save_and_show_info_valid_input(self, mock_run, mock_update_status, mock_save_info, mock_showinfo, mock_askyesno):
        self.app.bmi_var.set('표준')
        self.app.body_fat_var.set('표준')
        self.app.inbody_entry.insert(0, '80')
        self.app.fat_control_entry.insert(0, '5.5')
        self.app.muscle_control_entry.insert(0, '3.2')
        self.app.save_and_show_info()
        mock_askyesno.assert_called()
        mock_save_info.assert_called()
        mock_update_status.assert_called()
        mock_showinfo.assert_any_call("성공", "정보가 성공적으로 저장되었습니다.")
        mock_showinfo.assert_any_call("분석결과", "스쿼트 30분, \n달리기 20분이 당신에게 적합한 운동량입니다.")
        mock_run.assert_called_with('python GUI_Sel_Food.py')

    def test_is_float(self):
        self.assertTrue(self.app.is_float('123.45'))
        self.assertFalse(self.app.is_float('abc'))

if __name__ == '__main__':
    unittest.main()

