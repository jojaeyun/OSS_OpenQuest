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
---
- game-maze(미로 게임)

플레이어를 조종하여 적의 추적을 뿌리치고 골 지점까지 도달해야 하는 게임입니다.

- 기능
1. 무작위 미로 생성 (DFS 기반)
2. 플레이어 이동 및 충돌 감지
3. 플레이어를 쫓아오는 적 (BFS 기반)
4. 난이도 선택 시스템
5. 적을 일시적으로 무력화 할 수 있는 아이템
6. 맵에 남아있는 아이템의 개수를 알려주는 카운터

- 게임 방법

이동: 방향키

아이템: 획득 시 적이 일시적으로 움직일 수 없고 플레이어가 적을 통과할 수 있는 상태가 된다.

---
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
