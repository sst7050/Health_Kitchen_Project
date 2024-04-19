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
