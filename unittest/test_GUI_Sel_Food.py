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
    def test_widgets_creation(self):
        food_buttons = self.food_frame.grid_slaves()  # Retrieving all widgets in the grid
        self.assertTrue(len(food_buttons) > 0, "Widgets were not created correctly")
        
    @patch('userInfo.save_user_info')
    @patch('userInfo.read_user_info')
    @patch('tkinter.messagebox.askyesno')
    @patch('subprocess.run')
    def test_select_food_yes(self, mock_subprocess_run, mock_askyesno, mock_read_user_info, mock_save_user_info):
        mock_askyesno.return_value = True  # Simulate user clicking 'Yes'
        mock_read_user_info.return_value = (True, {'name': 'test_user'})
        
        food_info = {
            "image": "img/food/Burger/Burger.png",  
            "detail_name": "햄버거", 
            "ingredient_path": "img/food/Burger/ingredient/"
        }
        
        self.food_frame.select_food("햄버거", food_info)
        
        mock_save_user_info.assert_called_once()
        saved_info = mock_save_user_info.call_args[0][0]
        self.assertIn('selected_food', saved_info)
        self.assertEqual(saved_info['selected_food']['food'], "햄버거")
        self.assertIn('limit_time', saved_info)
        
        expected_time = datetime.now() + timedelta(weeks=1)
        limit_time = datetime.strptime(saved_info['limit_time'], "%Y-%m-%d %H:%M:%S")
        self.assertAlmostEqual(expected_time, limit_time, delta=timedelta(seconds=20))
        
    
    