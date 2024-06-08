import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, mock_open
import userInfo
import json


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

    @patch("builtins.open", new_callable=mock_open, read_data='{"level": "중급 요리사", "made_food_count": 5, "limit_time": "2024-06-06T14:00:00"}')
    @patch("userInfo.json.load", return_value={"level": "중급 요리사", "made_food_count": 5, "limit_time": "2024-06-06T14:00:00"})
    def test_read_user_info_complete(self, mock_json_load, mock_file):
        success, user_info = userInfo.read_user_info()
        self.assertTrue(success)
        self.assertEqual(user_info["level"], "중급 요리사")
        self.assertEqual(user_info["made_food_count"], 5)
        self.assertEqual(user_info["limit_time"], "2024-06-06T14:00:00")

    @patch("builtins.open", side_effect=UnicodeDecodeError("codec", b"", 0, 1, "reason"))
    def test_read_user_info_unicode_error(self, mock_file):
        with patch("userInfo.json.load", return_value={"name": "John", "age": 30}):
            success, user_info = userInfo.read_user_info()
            self.assertFalse(success)

    @patch("builtins.open", side_effect=Exception("Some error"))
    def test_read_user_info_general_exception(self, mock_file):
        success, user_info = userInfo.read_user_info()
        self.assertFalse(success)
        self.assertIsNone(user_info)
        
    @patch("builtins.open", side_effect=[UnicodeDecodeError("codec", b"", 0, 1, "reason"), mock_open(read_data='{"name": "John", "age": 30}').return_value])
    def test_read_user_info_unicode_error_with_cp949(self, mock_file):
        success, user_info = userInfo.read_user_info()
        self.assertTrue(success)
        self.assertIn("level", user_info)
        self.assertIn("made_food_count", user_info)
        self.assertIn("limit_time", user_info)
        self.assertEqual(user_info["level"], '주방 견습생')
        self.assertEqual(user_info["made_food_count"], 0)
        self.assertIsNone(user_info["limit_time"])

    @patch("builtins.open", new_callable=mock_open)
    @patch("userInfo.json.dump")
    def test_save_user_info_success(self, mock_json_dump, mock_file):
        user_info = {"name": "John", "age": 30}
        success = userInfo.save_user_info(user_info)
        self.assertTrue(success)
        mock_json_dump.assert_called_once_with(user_info, mock_file().__enter__(), ensure_ascii=False, indent=4)
 
    @patch("builtins.open", side_effect=Exception("Some error"))
    def test_save_user_info_failure(self, mock_file):
        user_info = {"name": "John", "age": 30}
        success = userInfo.save_user_info(user_info)
        self.assertFalse(success)
        
    def test_update_level(self):
        user_info_1 = {"level": "주방 견습생", "made_food_count": 0}
        updated_level_1 = userInfo.update_level(user_info_1)
        self.assertEqual(updated_level_1, "주방 견습생")

        user_info_2 = {"level": "주방 견습생", "made_food_count": 1}
        updated_level_2 = userInfo.update_level(user_info_2)
        self.assertEqual(updated_level_2, "초급 요리사")

        user_info_3 = {"level": "초급 요리사", "made_food_count": 3}
        updated_level_3 = userInfo.update_level(user_info_3)
        self.assertEqual(updated_level_3, "중급 요리사")
        
        user_info_4 = {"level": "중급 요리사", "made_food_count": 5}
        updated_level_4 = userInfo.update_level(user_info_4)
        self.assertEqual(updated_level_4, "주방장")
        
        user_info_5 = {"level": "주방장", "made_food_count": 8}
        updated_level_5 = userInfo.update_level(user_info_5)
        self.assertEqual(updated_level_5, "요리의 달인")
        
        user_info_6 = {"level": "요리의 달인", "made_food_count": 12}
        updated_level_6 = userInfo.update_level(user_info_6)
        self.assertEqual(updated_level_6, "요리왕 비룡")

        user_info_7 = {"level": "요리왕 비룡", "made_food_count": 17}
        updated_level_7 = userInfo.update_level(user_info_7)
        self.assertEqual(updated_level_7, "고든 램지")


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "inbody_score": 70,
        "fat_control": -1,
        "muscle_control": 1,
        "bmi": "과체중",
        "body_fat": "경도비만"
    }))
    @patch("userInfo.json.dump")
    def test_update_inbody_status_case1(self, mock_json_dump, mock_file):
        status, exercise_recommendation = userInfo.update_inbody_status()
        self.assertEqual(status, 2)
        self.assertEqual(exercise_recommendation, {
            '현재 상태': '과체중, 경도비만',
            '추천 목표': '지방 감량 및 근육 증량',
            '추천 유산소 운동': {'종류': '러닝', '시간': 30},
            '추천 무산소 운동': {'종류': '고강도 무산소 운동', '시간': 30}
        })
        mock_json_dump.assert_called_once()


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "inbody_score": 90,
        "fat_control": 0,
        "muscle_control": 0,
        "bmi": "표준",
        "body_fat": "표준"
    }))
    @patch("userInfo.json.dump")
    def test_update_inbody_status_case2(self, mock_json_dump, mock_file):
        status, exercise_recommendation = userInfo.update_inbody_status()
        self.assertEqual(status, 5)
        self.assertEqual(exercise_recommendation, {
            '현재 상태': '표준',
            '추천 목표': '지방 유지, 근육 유지',
            '추천 유산소 운동': {'종류': '걷기', '시간': 30},
            '추천 무산소 운동': {'종류': '저강도 무산소 운동', '시간': 45}
        })
        mock_json_dump.assert_called_once()


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "inbody_score": 60,
        "fat_control": -1,
        "muscle_control": 1,
        "bmi": "심한과체중",
        "body_fat": "비만"
    }))
    @patch("userInfo.json.dump")
    def test_update_inbody_status_case3(self, mock_json_dump, mock_file):
        status, exercise_recommendation = userInfo.update_inbody_status()
        self.assertEqual(status, 2)
        self.assertEqual(exercise_recommendation, {
            '현재 상태': '심한과체중, 비만',
            '추천 목표': '지방 감량 및 근육 증량',
            '추천 유산소 운동': {'종류': '걷기', '시간': 60},
            '추천 무산소 운동': {'종류': '고강도 무산소 운동', '시간': 30}
        })
        mock_json_dump.assert_called_once()


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "inbody_score": 60,
        "fat_control": -1,
        "muscle_control": 0,
        "bmi": "심한과체중",
        "body_fat": "비만"
    }))
    @patch("userInfo.json.dump")
    def test_update_inbody_status_case4(self, mock_json_dump, mock_file):
        status, exercise_recommendation = userInfo.update_inbody_status()
        self.assertEqual(status, 6)
        self.assertEqual(exercise_recommendation, {
            '현재 상태': '심한과체중, 비만',
            '추천 목표': '지방 감량, 근육 유지',
            '추천 유산소 운동': {'종류': '걷기', '시간': 60},
            '추천 무산소 운동': {'종류': '저강도 무산소 운동', '시간': 45}
        })
        mock_json_dump.assert_called_once()


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "inbody_score": 75,
        "fat_control": 1,
        "muscle_control": 1,
        "bmi": "저체중",
        "body_fat": "해당없음"
    }))
    @patch("userInfo.json.dump")
    def test_update_inbody_status_case5(self, mock_json_dump, mock_file):
        status, exercise_recommendation = userInfo.update_inbody_status()
        self.assertEqual(status, 4)
        self.assertEqual(exercise_recommendation, {
            '현재 상태': '저체중',
            '추천 목표': '지방 증량, 근육 증량',
            '추천 유산소 운동': {'종류': '계단 오르기', '시간': 30},
            '추천 무산소 운동': {'종류': '고강도 무산소 운동', '시간': 30}
        })
        mock_json_dump.assert_called_once()


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "inbody_score": 60,
        "fat_control": -1,
        "muscle_control": 0,
        "bmi": "과체중",
        "body_fat": "경도비만"
    }))
    @patch("userInfo.json.dump")
    def test_update_inbody_status_case6(self, mock_json_dump, mock_file):
        status, exercise_recommendation = userInfo.update_inbody_status()
        self.assertEqual(status, 6)
        self.assertEqual(exercise_recommendation, {
            '현재 상태': '과체중, 경도비만',
            '추천 목표': '지방 감량, 근육 유지',
            '추천 유산소 운동': {'종류': '러닝', '시간': 30},
            '추천 무산소 운동': {'종류': '중강도 무산소 운동', '시간': 45}
        })
        mock_json_dump.assert_called_once()
        
    @patch("builtins.open", side_effect=Exception("File read error"))
    def test_update_inbody_status_file_read_error(self, mock_file):
        status, exercise_recommendation = userInfo.update_inbody_status()
        self.assertIsNone(status)
        self.assertIsNone(exercise_recommendation)
     
     
        
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        "inbody_score": 70,
        "fat_control": -1,
        "muscle_control": 0,
        "bmi": "과체중",
        "body_fat": "경도비만"
    }))
    @patch("userInfo.json.dump", side_effect=Exception("JSON dump error"))
    def test_update_inbody_status_file_write_error(self, mock_json_dump, mock_open):
        with patch("userInfo.print") as mock_print:
            status, exercise_recommendation = userInfo.update_inbody_status()
            self.assertEqual(status, 6)
            self.assertEqual(exercise_recommendation, {
                '현재 상태': '과체중, 경도비만',
                '추천 목표': '지방 감량, 근육 유지',
                '추천 유산소 운동': {'종류': '러닝', '시간': 30},
                '추천 무산소 운동': {'종류': '중강도 무산소 운동', '시간': 45}
            })
            mock_print.assert_called_once_with("Failed to save the inbody data file: JSON dump error")

    
        
if __name__ == "__main__":
    unittest.main()
