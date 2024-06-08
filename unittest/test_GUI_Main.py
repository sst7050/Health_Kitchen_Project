import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tkinter as tk
import GUI_Main


# Ensure the correct directory is in the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
os.chdir(parent_dir)


class TestCustomMessageBox(unittest.TestCase):
    
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
    
    def tearDown(self):
        self.root.destroy()
    
    def test_initialization(self):
        message = "Test Message"
        buttons = {"OK": "ok", "Cancel": "cancel"}
        dialog = GUI_Main.CustomMessageBox(self.root, message, buttons)
        self.assertEqual(dialog.result, None)
        self.assertEqual(dialog.title(), "알림")
        self.assertEqual(len(dialog.children['!frame'].children), len(buttons))
    
    def test_button_click(self):
        message = "Test Message"
        buttons = {"OK": "ok", "Cancel": "cancel"}
        dialog = GUI_Main.CustomMessageBox(self.root, message, buttons)
        
        ok_button = dialog.children['!frame'].children['!button']
        ok_button.invoke()
        self.assertEqual(dialog.result, "ok")
        
    def test_show_custom_message(self):
        # Mocking Tkinter root window and CustomMessageBox
        root_mock = MagicMock()
        CustomMessageBox_mock = MagicMock()

        # Setting up mock return values and side effects
        CustomMessageBox_mock.return_value.result = "Test Result"

        # Patching Tkinter and CustomMessageBox classes
        with unittest.mock.patch('{}.tk.Tk'.format(GUI_Main.__name__), return_value=root_mock):
            with unittest.mock.patch('{}.CustomMessageBox'.format(GUI_Main.__name__), CustomMessageBox_mock):
                # Call the function
                result = GUI_Main.show_custom_message("Test Message", {"Button1": "Value1", "Button2": "Value2"})

        # Assertions
        CustomMessageBox_mock.assert_called_once_with(root_mock, "Test Message", {"Button1": "Value1", "Button2": "Value2"})
        root_mock.wait_window.assert_called_once_with(CustomMessageBox_mock.return_value)
        self.assertEqual(result, "Test Result")


class TestGUIMainFunctions(unittest.TestCase):

    @patch('userInfo.read_user_info')
    @patch('subprocess.run')
    @patch('GUI_Main.show_custom_message')
    def test_check_user_info_and_launch(self, mock_show_custom_message, mock_subprocess_run, mock_read_user_info):
        mock_read_user_info.return_value = (False, None)
        mock_show_custom_message.side_effect = ["next", "next", "confirm"]

        GUI_Main.check_user_info_and_launch()
        
        self.assertEqual(mock_show_custom_message.call_count, 3)
        mock_subprocess_run.assert_called_with('python GUI_basic_info.py')

        mock_read_user_info.return_value = (True, None)
        GUI_Main.check_user_info_and_launch()
        mock_subprocess_run.assert_called_with('python GUI_MainScreen.py')

if __name__ == '__main__':
    unittest.main()