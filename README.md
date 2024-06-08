# Health_Kitchen_Project

충북대학교 컴퓨터공학과 오픈소스 프로젝트 __현규동__ 팀이 진행하는 건강 관리 프로그램입니다.

## 👨‍🏫 프로젝트 소개

Health Kitchen은 사용자의 신체 정보 데이터를 입력받고 만들고 싶은 음식을 선정하면, 사용자에게 받은 데이터를 고려하여 적절한 운동량 및 감량 목표 등을 정해줌으로써 사용자의 능동적 참여를 유도하는 건강 관리 프로그램입니다.

사용자는 단기적 목표들을 달성함으로써 초기에 선정했던 음식의 가상 재료를 보상으로 받아 프로그램 내에 있는 가상 냉장고에 해당 재료를 보관하게 됩니다. 재료에 설정된 유통기한이 지나기 전에 다음 목표들을 달성하여 모든 재료들을 모으면 최종적으로 완성된 가상의 음식을 얻게 됩니다. 완성된 가상 음식을 만든 갯수를 토대로 사용자의 레벨(티어)이 향상되는 시스템으로, 사용자의 흥미와 참여를 독려합니다.
## ⏲️ 개발 기간

* 2024.03.22(금) ~ 2023.06.08(토)
  
## 🧑‍🤝‍🧑 개발자 소개 

- **심현석** : 팀장, [sst7050](https://github.com/sst7050)
- **이규민** : 팀원, [cOcOa-aa](https://github.com/cOcOa-aa)
- **김동균** : 팀원, [gimbab2002](https://github.com/gimbab2002)

## 💻 개발환경

- **Version** : Python 3
- **IDE** : Visual Studio Code

## 📦 의존성
이 프로젝트의 주요 의존성은 다음과 같습니다.
- Python 3.x
- pillow 10.3.0

## 🚀 설치 및 실행 방법

### 필수 조건
- Python 3.x 설치 필요
- pip (Python 패키지 관리자)

### 설치 방법
1. 저장소를 로컬 머신에 클론합니다.
   ```sh
   git clone https://github.com/sst7050/Health_Kitchen_Project.git
   cd Health_Kitchen_Project

2. 필수 패키지를 설치합니다.
   ```sh
   pip install -r requirements.txt

### 실행 방법
1. 메인 스크립트를 실행합니다.
   ```sh
   python GUI_Main.py

## 📄 라이선스
MIT License

Copyright (c) 2024 sst7050

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
