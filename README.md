# OSS_OpenQuest
# 프로젝트명 - Playground

Pygame을 이용한 여러 게임을 하나의 플랫폼에서 즐길 수 있도록 만드는 것이 목표입니다.

## 소개

이 프로젝트는 오픈소스 협업 과제의 일환으로 개발된 프로젝트입니다.  
사용자는 Pygame을 통해 여러 가지 게임을 하나의 화면에서 선택하여 즐길 수 있습니다.


## 기능
- 게임선택창 (게임 선택 시 해당 게임 실행)
- breakout! (벽돌 깨기 게임)
- hangman (단어 맞추기 게임)
- mazegame (미로 찾기 게임)
- rpsgame (가위바위보 게임)

## 설치 방법

```bash
# 1. 저장소 클론
git clone https://github.com/jojaeyun/OSS_OpenQuest.git
cd OSS_OpenQuest

# 2. 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# 3. 패키지 설치
pip install pygame

# 4. 실행
python main.py
