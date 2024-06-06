import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, mock_open
import userInfo



class TestUserInfo(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"name": "John", "age": 30}')
    @patch("userInfo.json.load", return_value={"name": "John", "age": 30})
    def test_read_user_info_missing_keys(self, mock_json_load, mock_file):
        success, user_info = userInfo.read_user_info()
        self.assertTrue(success)
        self.assertIn("level", user_info)
        self.assertIn("made_food_count", user_info)
        self.assertIn("limit_time", user_info)
        self.assertEqual(user_info["level"], '주방 견습생')
        self.assertEqual(user_info["made_food_count"], 0)
        self.assertIsNone(user_info["limit_time"])
