import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from datetime import datetime, timedelta
import userInfo
from GUI_Sel_Food import FoodSelectionFrame, MainApp


class TestFoodSelectionFrame(unittest.TestCase):
    @patch('userInfo.read_user_info')
    def setUp(self, mock_read_user_info):
        mock_read_user_info.return_value = (True, {'name': 'test_user'})  # Mocking userInfo read
        self.root = tk.Tk()
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        self.food_frame = FoodSelectionFrame(self.root, lambda x: None)
        
    def tearDown(self):
        if self.root:
            try:
                self.root.destroy()
            except tk.TclError:
                pass
        
    