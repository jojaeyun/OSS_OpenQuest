import subprocess
import os
import pygame
import sys

pygame.init()
pygame.mixer.init()  # 사운드 초기화

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("미니게임 선택")

# 🎮 아케이드 폰트 적용
FONT_PATH = "PressStart2P-Regular.ttf"
TITLE_FONT = pygame.font.Font(FONT_PATH, 70)
MENU_FONT = pygame.font.Font(FONT_PATH, 30)

clock = pygame.time.Clock()

# 메뉴 선택 사운드
select_sound = pygame.mixer.Sound("ui-sounds-pack.mp3")

menu_items = [
    "Rock-Paper-Scissors",
    "Maze game",
    "Hangman",
    "Break Out!",
    "Guessing the numbers",
    "Quit"
]
selected = 0

# 각 게임 스크립트 경로 (폴더별로 브랜치 코드 복사)
game_paths = [
    "game-rps/main.py",
    "game-maze/main.py",
    "game-hangman/main.py",
    "game-breakout/main.py",
    "game-guessing/main.py"
]

def draw_menu():
    screen.fill((0, 0, 0))
    # 타이틀
    title = TITLE_FONT.render("PLAYGROUND", True, (255, 255, 0))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

    # 메뉴 항목
    for i, text in enumerate(menu_items):
        color = (255, 255, 255) if i == selected else (180, 180, 180)
        item = MENU_FONT.render(text, True, color)
        x = WIDTH//2 - item.get_width()//2
        y = 200 + i * 60
        screen.blit(item, (x, y))
        if i == selected:
            pygame.draw.rect(screen, (80, 200, 120), 
                             (x-20, y-10, item.get_width()+40, item.get_height()+20), 3)

def run_selected(idx):
    if idx < len(game_paths):
        path = os.path.join(os.getcwd(), game_paths[idx])
        if os.path.exists(path):
            subprocess.run([sys.executable, path])
        else:
            print(f"Game script not found: {path}")
            pygame.time.delay(1000)
    else:
        pygame.quit()
        sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 창 닫기
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 키보드 입력
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                selected = (selected + 1) % len(menu_items)
                select_sound.play()
            elif event.key in [pygame.K_UP, pygame.K_w]:
                selected = (selected - 1) % len(menu_items)
                select_sound.play()
            elif event.key == pygame.K_RETURN:
                run_selected(selected)

    draw_menu()
    pygame.display.flip()
    clock.tick(60)