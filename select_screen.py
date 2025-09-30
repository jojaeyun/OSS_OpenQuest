import subprocess
import os
import pygame
import sys

pygame.init()
pygame.mixer.init()  # 사운드 초기화

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("미니게임 선택")

FONT_PATH = "C:/Windows/Fonts/malgun.ttf"
FONT = pygame.font.Font(FONT_PATH, 40)

clock = pygame.time.Clock()

# 메뉴 선택 사운드
select_sound = pygame.mixer.Sound("ui-sounds-pack.mp3")

menu_items = [
    "가위바위보",
    "미로 찾기",
    "단어 맞추기",
    "벽돌깨기",
    "숫자 맞추기",
    "종료"
]
selected = 0

def draw_menu():
    screen.fill((30, 30, 50))
    title = FONT.render("미니게임을 선택하세요", True, (255, 255, 200))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

    for i, text in enumerate(menu_items):
        color = (255, 255, 255) if i == selected else (180, 180, 180)
        item = FONT.render(text, True, color)
        x = WIDTH//2 - item.get_width()//2
        y = 200 + i * 60
        screen.blit(item, (x, y))
        if i == selected:
            pygame.draw.rect(screen, (80, 200, 120), (x-20, y-10, item.get_width()+40, item.get_height()+20), 3)

def run_selected(idx):
    if idx == 0: print("가위바위보 실행")
    elif idx == 1: print("미로 찾기 실행")
    elif idx == 2: print("단어 맞추기 실행")
    elif idx == 3: print("벽돌깨기 실행")
    elif idx == 4: print("숫자 맞추기 실행")
    elif idx == 5: 
        pygame.quit()
        sys.exit()

def run_selected(idx):
    branches = [
        "feature/game-rps",
        "feature/game-maze",
        "feature/game-hangman",
        "feature/game-breakout"
    ]
    scripts = ["main.py"] * 4  # 각 브랜치의 실행 스크립트 이름

    if idx < 5:
        branch = branches[idx]
        script = scripts[idx]

        # 현재 저장소의 브랜치 체크아웃
        subprocess.run(["git", "checkout", branch])
        # 스크립트 실행
        path = os.path.join(os.getcwd(), script)
        subprocess.run(["python", path])
        # 게임 종료 후 다시 main 브랜치로
        subprocess.run(["git", "checkout", "main"])
    else:
        pygame.quit()
        sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 창 닫기
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 키보드가 눌림
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:  # 아래방향키 or s
                selected = (selected + 1) % len(menu_items)
                select_sound.play()  # 메뉴 이동 효과음
            elif event.key == pygame.K_UP or event.key == pygame.K_w:  # 위방향키 or w
                selected = (selected - 1) % len(menu_items)
                select_sound.play()  # 메뉴 이동 효과음
            elif event.key == pygame.K_RETURN:  # 엔터
                run_selected(selected)

    draw_menu()
    pygame.display.flip()
    clock.tick(60)