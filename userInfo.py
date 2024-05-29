import json

def read_user_info():
    file_path = "user_info.json"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            user_info = json.load(file)
        return True, user_info
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='cp949') as file:
                user_info = json.load(file)
            return True, user_info
        except Exception as e:
            print(f"Failed to read the user info file: {e}")
            return False, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, None
    
def save_user_info(user_info):
    file_path = "user_info.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(user_info, file, ensure_ascii=False, indent=4)

def update_inbody_status():
    file_path = "user_info.json"
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
   
    inbody_score = float(data['inbody_score'])
    fat_control = float(data['fat_control'])
    muscle_control = float(data['muscle_control'])
    bmi = data['bmi']
    body_fat = data['body_fat']
    
    # inbody_score에 따른 조건 분기
    status = 0
    if inbody_score < 80:
        if fat_control < 0 and muscle_control <= 0:
            status = 1 # 지방 감량
        elif fat_control < 0 and muscle_control > 0:
            status = 2 # 지방 감량, 근육 증량
        elif fat_control > 0 and muscle_control <= 0:
            status = 3 # 지방 증량
        elif fat_control > 0 and muscle_control > 0:
            status = 4 # 지방 증량, 근육 증량
        elif fat_control < 0 and muscle_control == 0:
            status = 6 # 지방 감량, 근육 유지
    elif inbody_score >= 80:
        if fat_control == 0 and muscle_control == 0:
            status = 5 # 지방 유지, 근육 유지
        
   
    # BMI와 체지방률에 따른 조건 분기
    """def get_exercise_recommendation(status):
        if bmi == "과체중" and status == 2 and body_fat == "경도비만":
            return f'현재 상태: 과체중, 경도비만 \n 추천 목표: 지방 감량 및 근육 증량 \n 추천 유산소 운동: 러닝(하루에 {30}분) 추천 무산소 운동: 고강도(하루에 {30}분)'
        elif bmi == "심한과체중" and status == 2 and body_fat == "비만":
            return f'현재 상태: 심한과체중, 비만 \n 추천 목표: 지방 감량 및 근육 증량 \n 추천 유산소 운동: 걷기(하루에 {60}분) 추천 무산소 운동: 고강도(하루에 {30}분)'
        elif bmi == "과체중" and status == 6 and body_fat == "경도비만":
            return f'현재 상태: 과체중, 경도비만 \n 추천 목표: 지방 감량, 근육 유지 \n 추천 유산소 운동: 러닝(하루에 {30}분) 추천 무산소 운동: 중강도(하루에 {45}분)'
        elif bmi == "심한과체중" and status == 6 and body_fat == "비만":
            return f'현재 상태: 심한과체중, 비만 \n 추천 목표: 지방 감량, 근육 유지 \n 추천 유산소 운동: 걷기(하루에 {60}분) 추천 무산소 운동: 저강도(하루에 {45}분)'
        elif bmi == "표준" and status == 5 and body_fat == "표준":
            return f'현재 상태: 표준 \n 추천 목표: 지방 유지, 근육 유지 \n 추천 유산소 운동: 걷기(하루에 {30}분) 추천 무산소 운동: 저강도(하루에 {45}분)'
        elif bmi == "저체중" and status == 4 and body_fat == "해당없음":
            return f'현재 상태: 저체중 \n 추천 목표: 지방 증량, 근육 증량 \n 추천 유산소 운동: 계단 오르기(하루에 {30}분) 추천 무산소 운동: 고강도 (하루에 {30}분)'
        else:
            status = -1  # 조건에 맞지 않으면 status를 -1으로 설정"""
    def get_exercise_recommendation(status):
        if bmi == "과체중" and status == 2 and body_fat == "경도비만":
            return {
            '현재 상태': '과체중, 경도비만',
            '추천 목표': '지방 감량 및 근육 증량',
            '추천 유산소 운동': {'종류': '러닝', '시간': 30},
            '추천 무산소 운동': {'종류': '고강도', '시간': 30}
        }
        elif bmi == "심한과체중" and status == 2 and body_fat == "비만":
            return {
            '현재 상태': '심한과체중, 비만',
            '추천 목표': '지방 감량 및 근육 증량',
            '추천 유산소 운동': {'종류': '걷기', '시간': 60},
            '추천 무산소 운동': {'종류': '고강도', '시간': 30}
        }
        elif bmi == "과체중" and status == 6 and body_fat == "경도비만":
            return {
            '현재 상태': '과체중, 경도비만',
            '추천 목표': '지방 감량, 근육 유지',
            '추천 유산소 운동': {'종류': '러닝', '시간': 30},
            '추천 무산소 운동': {'종류': '중강도', '시간': 45}
        }
        elif bmi == "심한과체중" and status == 6 and body_fat == "비만":
            return {
            '현재 상태': '심한과체중, 비만',
            '추천 목표': '지방 감량, 근육 유지',
            '추천 유산소 운동': {'종류': '걷기', '시간': 60},
            '추천 무산소 운동': {'종류': '저강도', '시간': 45}
        }
        elif bmi == "표준" and status == 5 and body_fat == "표준":
            return {
            '현재 상태': '표준',
            '추천 목표': '지방 유지, 근육 유지',
            '추천 유산소 운동': {'종류': '걷기', '시간': 30},
            '추천 무산소 운동': {'종류': '저강도', '시간': 45}
        }
        elif bmi == "저체중" and status == 4 and body_fat == "해당없음":
            return {
            '현재 상태': '저체중',
            '추천 목표': '지방 증량, 근육 증량',
            '추천 유산소 운동': {'종류': '계단 오르기', '시간': 30},
            '추천 무산소 운동': {'종류': '고강도', '시간': 30}
        }
        else:
            return None  # 조건에 맞지 않으면 None 반환

   
    # status가 0이거나 else 값인 경우 JSON 파일에 저장하지 않음
    if status != -1:
        # status 업데이트
        data['status'] = status
       
        # 운동 추천
        exercise_recommendation = get_exercise_recommendation(status)
        data['exercise_recommendation'] = exercise_recommendation

        # 업데이트 된 데이터를 JSON 파일에 쓰기
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
       
        return status, exercise_recommendation
    else:
        return status, None
