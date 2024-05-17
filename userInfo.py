import json
import os

def read_user_info():
    file_path = "user_info.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            user_info = json.load(file)
        return True, user_info
    else:
        return False, None

def save_user_info(user_info):
    file_path = "user_info.json"
    with open(file_path, 'w') as file:
        json.dump(user_info, file, indent=4)

def update_inbody_status():
    file_path = "user_info.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    inbody_score = float(data['inbody_score'])
    fat_control = float(data['fat_control'])
    muscle_control = float(data['muscle_control'])
    bmi = data['bmi']
    body_fat = data['body_fat']
    
    # inbody_score에 따른 조건 분기
    if inbody_score < 80:
        if fat_control < 0 and muscle_control < 0:
            status = '지방 감량'
        elif fat_control < 0 and muscle_control > 0:
            status = '지방 감량, 근육 증량'
        elif fat_control > 0 and muscle_control < 0:
            status = '지방 증량'
        elif fat_control > 0 and muscle_control > 0:
            status = '지방 증량, 근육 증량'
        elif fat_control == 0 and muscle_control == 0:
            status = '지방 유지, 근육 유지'
        elif fat_control < 0 and muscle_control == 0:
            status = '지방 감량, 근육 유지'
    
    # BMI와 체지방률에 따른 조건 분기
    if bmi == "과체중" and status == '지방 감량, 근육 증량' and body_fat == "경도비만":
        status += 5
    elif bmi == "심한과체중" and status == '지방 감량, 근육 증량' and body_fat == "비만":
        status += 6
    elif bmi == "과체중" and status == '지방 감량, 근육 유지' and body_fat == "경도비만":
        status += 3
    elif bmi == "심한과체중" and status == '지방 감량, 근육 유지' and body_fat == "비만":
        status += 4
    elif bmi == "표준" and status == '지방 유지, 근육 유지' and body_fat == "표준":
        status += 6
    elif bmi == "저체중" and status == '지방 증량, 근육 증량' and body_fat == "해당없음":
        status += 8
    
    # status 업데이트
    data['status'] = status
    
    # 운동 추천
    exercise_recommendation = get_exercise_recommendation(status)
    data['exercise_recommendation'] = exercise_recommendation

    # 업데이트 된 데이터를 JSON 파일에 쓰기
    with open(file_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    return status, exercise_recommendation

def get_exercise_recommendation(status):
    if status == 7:      
        return '현재 상태: 과체중, 경도비만 \n 추천 목표: 지방 감량 및 근육 증량 \n 추천 유산소 운동: 러닝(하루에 30분) 추천 무산소 운동: 고강도(하루에 30분)'
    elif status == 8:
        return '현재 상태: 심한과체중, 비만 \n 추천 목표: 지방 감량 및 근육 증량 \n 추천 유산소 운동: 걷기(하루에 60분) 추천 무산소 운동: 고강도(하루에 30분)'
    elif status == 9:
        return '현재 상태: 과체중, 경도비만 \n 추천 목표: 지방 감량, 근육 유지 \n 추천 유산소 운동: 러닝(하루에 30분) 추천 무산소 운동: 중강도(하루에 45분)'
    elif status == 10:
        return '현재 상태: 심한과체중, 비만 \n 추천 목표: 지방 감량, 근육 유지 \n 추천 유산소 운동: 걷기(하루에 60분) 추천 무산소 운동: 저강도(하루에 45분)'
    elif status == 11:
        return '현재 상태: 표준 \n 추천 목표: 지방 유지, 근육 유지 \n 추천 유산소 운동: 걷기(하루에 30분) 추천 무산소 운동: 저강도(하루에 45분)'
    elif status == 12:
        return '현재 상태: 저체중 \n 추천 목표: 지방 증량, 근육 증량 \n 추천 유산소 운동: 계단 오르기(하루에 30분) 추천 무산소 운동: 고강도 (하루에 30분)'
    else:
        return '적절하지 않은 결과값입니다. 정보를 다시 입력해주세요.'
