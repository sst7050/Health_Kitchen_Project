import json
import os

def read_user_info():
    file_path = "user_info.json"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            user_info = json.load(file)
        return True, user_info
    else:
        return False, None

def save_user_info(user_info):
    file_path = "user_info.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(user_info, file, indent=4)


def update_inbody_status():
    # JSON 파일을 읽기
    file_path = "user_info.json"
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    inbody_score = float(data['inbody_score'])
    fat_control = float(data['fat_control'])
    muscle_control = float(data['muscle_control'])
    
    # inbody_score에 따른 조건 분기
    if inbody_score < 80:
        if fat_control < 0 and muscle_control <= 0:
            status = '지방감량'
        elif fat_control < 0 and muscle_control > 0:
            status = '지방감량 및 근육증량'
        elif fat_control > 0 and muscle_control <= 0:
            status = '지방증량'
        elif fat_control > 0 and muscle_control > 0:
            status = '지방증량 및 근육 증량'
    else:
        status = '유지'
    
    # status 업데이트
    data['status'] = status
    
    # 업데이트 된 데이터를 JSON 파일에 쓰기
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    return status

