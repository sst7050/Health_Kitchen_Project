import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from datetime import datetime, timedelta
import subprocess
import time
import GUI_Rank


class ExerciseTracker(tk.Frame):
    def __init__(self, master=None, main_screen=None):
        super().__init__(master)
        self.master = master
        self.main_screen = main_screen
        self.grid(sticky="nsew")
        self.load_user_info()
        self.create_widgets()
        self.configure_grid()
        self.update_progress_bars()  # 초기 로드 시 진척도 게이지 업데이트

    def load_user_info(self):
        try:
            with open("user_info.json", "r", encoding='utf-8') as file:
                self.user_info = json.load(file)
                if '유산소' not in self.user_info:
                    self.user_info['유산소'] = 0
                if '무산소' not in self.user_info:
                    self.user_info['무산소'] = 0
                if 'ingredient' not in self.user_info:
                    self.user_info['ingredient'] = []
        except FileNotFoundError:
            self.user_info = {"유산소": 0, "무산소": 0, "ingredient": []}
        self.save_user_info()

    def save_user_info(self):
        with open("user_info.json", "w", encoding='utf-8') as file:
            json.dump(self.user_info, file, ensure_ascii=False, indent=4)

    def create_widgets(self):
        # 유산소 운동량 입력 필드
        self.entry_aerobic = tk.Entry(self, width=40)
        self.entry_aerobic.insert(0, "유산소 운동량을 입력하세요")
        self.entry_aerobic.bind("<FocusIn>", lambda event: self.on_entry_click(event, "유산소 운동량을 입력하세요"))
        self.entry_aerobic.bind("<FocusOut>", lambda event: self.on_focusout(event, "유산소 운동량을 입력하세요"))
        self.entry_aerobic.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        # 유산소 운동량 추가 버튼
        self.add_button_aerobic = tk.Button(self, text="유산소 추가", command=lambda: self.update_progress("유산소"))
        self.add_button_aerobic.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # 무산소 운동량 입력 필드
        self.entry_anaerobic = tk.Entry(self, width=40)
        self.entry_anaerobic.insert(0, "무산소 운동량을 입력하세요")
        self.entry_anaerobic.bind("<FocusIn>", lambda event: self.on_entry_click(event, "무산소 운동량을 입력하세요"))
        self.entry_anaerobic.bind("<FocusOut>", lambda event: self.on_focusout(event, "무산소 운동량을 입력하세요"))
        self.entry_anaerobic.grid(row=1, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        # 무산소 운동량 추가 버튼
        self.add_button_anaerobic = tk.Button(self, text="무산소 추가", command=lambda: self.update_progress("무산소"))
        self.add_button_anaerobic.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # 유산소 진척도 게이지 바
        self.recommended_aerobic_time = self.user_info['exercise_recommendation']['추천 유산소 운동']['시간'] * 7
        self.progress_aerobic = ttk.Progressbar(self, length=700, mode='determinate', maximum=self.recommended_aerobic_time)
        self.progress_aerobic.grid(row=2, column=0, columnspan=3, pady=20, sticky="ew")
        self.progress_label_aerobic = tk.Label(self, text=f"유산소: {self.user_info['유산소']}/{self.recommended_aerobic_time}")
        self.progress_label_aerobic.grid(row=2, column=3, padx=10, sticky="w")

        # 무산소 진척도 게이지 바
        self.recommended_anaerobic_time = self.user_info['exercise_recommendation']['추천 무산소 운동']['시간'] * 7
        self.progress_anaerobic = ttk.Progressbar(self, length=700, mode='determinate', maximum=self.recommended_anaerobic_time)
        self.progress_anaerobic.grid(row=3, column=0, columnspan=3, pady=20, sticky="ew")
        self.progress_label_anaerobic = tk.Label(self, text=f"무산소: {self.user_info['무산소']}/{self.recommended_anaerobic_time}")
        self.progress_label_anaerobic.grid(row=3, column=3, padx=10, sticky="w")

        # 이미지 표시 (하단에 위치 조정)
        self.filepath = self.user_info["selected_food"]["details"]["image"]
        self.image = ImageTk.PhotoImage(Image.open(self.filepath))
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.grid(row=4, column=0, columnspan=4, pady=20, sticky="nsew")  # 위치를 row=4으로 변경

    def configure_grid(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_rowconfigure(4, weight=1)  # 이미지를 보여줄 행
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=1)
        self.master.grid_columnconfigure(3, weight=0)

    def on_entry_click(self, event, default_text):
        if event.widget.get() == default_text:
            event.widget.delete(0, tk.END)

    def on_focusout(self, event, default_text):
        if not event.widget.get():
            event.widget.insert(0, default_text)

    def relaunch_food_selection(self):
        self.master.destroy()
        self.main_screen.master.destroy()  # Close the MainScreen window
        subprocess.run(['python', 'GUI_Sel_Food.py'])

    def update_progress(self, exercise_type):
        limit_time = datetime.strptime(self.user_info['limit_time'], "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        if limit_time <= current_time:
            messagebox.showinfo("알림", "재료의 유통기한이 만료되었습니다.\n냉장고의 재료가 모두 사라집니다. 음식을 다시 선택해 주세요.")
            self.user_info['유산소'] = 0
            self.user_info['무산소'] = 0
            self.user_info['ingredient'] = []
            self.save_user_info()
            self.master.after(100, self.relaunch_food_selection)

        else:    
            try:
                if exercise_type == "유산소":
                    entry_widget = self.entry_aerobic
                    progress_bar = self.progress_aerobic
                    label_widget = self.progress_label_aerobic
                    recommended_time = self.recommended_aerobic_time
                else:
                    entry_widget = self.entry_anaerobic
                    progress_bar = self.progress_anaerobic
                    label_widget = self.progress_label_anaerobic
                    recommended_time = self.recommended_anaerobic_time

                new_amount = int(entry_widget.get())
                self.user_info[exercise_type] += new_amount
                self.user_info[exercise_type] = min(self.user_info[exercise_type], recommended_time)  # 최대 추천 시간을 기준으로 제한

                progress_bar['value'] = self.user_info[exercise_type]
                label_widget.config(text=f"{exercise_type}: {self.user_info[exercise_type]}/{recommended_time}")
                entry_widget.delete(0, tk.END)

                self.save_user_info()  # 업데이트된 값 저장
                self.check_ingredient_collection()  # 재료 수집 체크
            except ValueError:
                messagebox.showinfo("오류", "유효한 정수를 입력하세요.")

    def update_progress_bars(self):
        self.progress_aerobic['value'] = self.user_info['유산소']
        self.progress_label_aerobic.config(text=f"유산소: {self.user_info['유산소']}/{self.recommended_aerobic_time}")
        self.progress_anaerobic['value'] = self.user_info['무산소']
        self.progress_label_anaerobic.config(text=f"무산소: {self.user_info['무산소']}/{self.recommended_anaerobic_time}")

    def check_ingredient_collection(self):
        if self.user_info['유산소'] >= self.recommended_aerobic_time and self.user_info['무산소'] >= self.recommended_anaerobic_time:
            next_ingredient_index = len(self.user_info['ingredient']) + 1
            self.user_info['유산소'] = 0
            self.user_info['무산소'] = 0
            timelimit_str = self.user_info['limit_time']
            timelimit = datetime.strptime(timelimit_str, "%Y-%m-%d %H:%M:%S")
            timelimit = timelimit + timedelta(weeks=1)
            self.user_info['limit_time'] = timelimit.strftime("%Y-%m-%d %H:%M:%S")
            self.save_user_info()
            if next_ingredient_index <= 4:
                ingredient_index = next_ingredient_index
                ingredient_image_path = f"{self.user_info['selected_food']['details']['ingredient_path']}{ingredient_index}.png"
                self.user_info['ingredient'].append(f"{ingredient_index}.png")
                self.save_user_info()
                self.show_ingredient_notification(ingredient_image_path, "재료가 냉장고에 추가되었습니다.")
                self.update_progress_bars()
                time.sleep(0.3)
                if len(self.user_info['ingredient']) >= 4:
                    messagebox.showinfo("축하합니다!", "모든 재료를 모았습니다! 음식이 만들어집니다.")
                    self.user_info['ingredient'] = []  # 재료 초기화
                    if 'made_food' not in self.user_info:
                        self.user_info['made_food'] = []
                        self.save_user_info()
                    made_food = self.user_info["selected_food"]["details"]["image"]
                    self.user_info['made_food'].append(f"{made_food}")
                    self.save_user_info()
                    GUI_Rank.show_rank_up_message()  # 레벨 업 메시지 호출
                    self.master.after(100, self.relaunch_food_selection)
                    
    def show_ingredient_notification(self, ingredient_image_path, message):
        notification_window = tk.Toplevel(self.master)
        notification_window.title("재료 추가 알림")
        notification_window.resizable(False, False)
        notification_window.geometry("300x250")

        # 이미지 표시
        ingredient_image = Image.open(ingredient_image_path)
        ingredient_photo = ImageTk.PhotoImage(ingredient_image)
        ingredient_label = tk.Label(notification_window, image=ingredient_photo)
        ingredient_label.image = ingredient_photo  # Keep a reference to the image to prevent garbage collection
        ingredient_label.pack()
        
        # 메시지 표시
        message_label = tk.Label(notification_window, text=message)
        message_label.pack()