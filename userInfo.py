import json

def read_user_info():
    file_path = "user_info.json"
    user_info = {}

    def set_default_values(info):
        if 'level' not in info:
            info['level'] = '주방 견습생'
        if 'made_food_count' not in info:
            info['made_food_count'] = 0
        if 'limit_time' not in info:
            info['limit_time'] = None  # 유통기한 정보를 기본값으로 추가
        return info

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            user_info = json.load(file)
            user_info = set_default_values(user_info)
        return True, user_info
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='cp949') as file:
                user_info = json.load(file)
                user_info = set_default_values(user_info)
            return True, user_info
        except Exception as e:
            print(f"Failed to read the user info file: {e}")
            return False, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, None

def save_user_info(user_info):
    file_path = "user_info.json"
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(user_info, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Failed to save the user info file: {e}")
        return False

def update_level(user_info):
    level = user_info.get('level', '주방 견습생')
    made_food_count = user_info.get('made_food_count', 0)

    level_thresholds = [
        ('주방 견습생', 1, '초급 요리사'),
        ('초급 요리사', 3, '중급 요리사'),
        ('중급 요리사', 5, '주방장'),
        ('주방장', 8, '요리의 달인'),
        ('요리의 달인', 12, '요리왕 비룡'),
        ('요리왕 비룡', 17, '고든 램지')
    ]

    for current_level, threshold, new_level in level_thresholds:
        if level == current_level and made_food_count >= threshold:
            user_info['level'] = new_level
            break

    return user_info['level']

def update_inbody_status():
    file_path = "user_info.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Failed to read the inbody data file: {e}")
        return None, None

    inbody_score = float(data.get('inbody_score', 0))
    fat_control = float(data.get('fat_control', 0))
    muscle_control = float(data.get('muscle_control', 0))
    bmi = data.get('bmi', '')
    body_fat = data.get('body_fat', '')

    status = 0
    if inbody_score < 80:
        if fat_control < 0 and muscle_control > 0:
            status = 2  # 지방 감량, 근육 증량
        elif fat_control > 0 and muscle_control > 0:
            status = 4  # 지방 증량, 근육 증량
        elif fat_control < 0 and muscle_control == 0:
            status = 6  # 지방 감량, 근육 유지
    elif inbody_score >= 80:
        if fat_control == 0 and muscle_control == 0:
            status = 5  # 지방 유지, 근육 유지

    def get_exercise_recommendation(status):
        recommendations = {
            (bmi == "과체중" and status == 2 and body_fat == "경도비만"): {
                '현재 상태': '과체중, 경도비만',
                '추천 목표': '지방 감량 및 근육 증량',
                '추천 유산소 운동': {'종류': '러닝', '시간': 30},
                '추천 무산소 운동': {'종류': '고강도 무산소 운동', '시간': 30}
            },
            (bmi == "심한과체중" and status == 2 and body_fat == "비만"): {
                '현재 상태': '심한과체중, 비만',
                '추천 목표': '지방 감량 및 근육 증량',
                '추천 유산소 운동': {'종류': '걷기', '시간': 60},
                '추천 무산소 운동': {'종류': '고강도 무산소 운동', '시간': 30}
            },
            (bmi == "과체중" and status == 6 and body_fat == "경도비만"): {
                '현재 상태': '과체중, 경도비만',
                '추천 목표': '지방 감량, 근육 유지',
                '추천 유산소 운동': {'종류': '러닝', '시간': 30},
                '추천 무산소 운동': {'종류': '중강도 무산소 운동', '시간': 45}
            },
            (bmi == "심한과체중" and status == 6 and body_fat == "비만"): {
                '현재 상태': '심한과체중, 비만',
                '추천 목표': '지방 감량, 근육 유지',
                '추천 유산소 운동': {'종류': '걷기', '시간': 60},
                '추천 무산소 운동': {'종류': '저강도 무산소 운동', '시간': 45}
            },
            (bmi == "표준" and status == 5 and body_fat == "표준"): {
                '현재 상태': '표준',
                '추천 목표': '지방 유지, 근육 유지',
                '추천 유산소 운동': {'종류': '걷기', '시간': 30},
                '추천 무산소 운동': {'종류': '저강도 무산소 운동', '시간': 45}
            },
            (bmi == "저체중" and status == 4 and body_fat == "해당없음"): {
                '현재 상태': '저체중',
                '추천 목표': '지방 증량, 근육 증량',
                '추천 유산소 운동': {'종류': '계단 오르기', '시간': 30},
                '추천 무산소 운동': {'종류': '고강도 무산소 운동', '시간': 30}
            }
        }
        return recommendations.get(True)

    exercise_recommendation = get_exercise_recommendation(status)
    if status != 0:
        data['status'] = status
        data['exercise_recommendation'] = exercise_recommendation

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Failed to save the inbody data file: {e}")

    return status, exercise_recommendation

