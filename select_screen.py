import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("미니게임 선택")

FONT_PATH = "C:/Windows/Fonts/malgun.ttf"
FONT = pygame.font.Font(FONT_PATH, 40)

clock = pygame.time.Clock()

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % len(menu_items)
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                run_selected(selected)

    draw_menu()
    pygame.display.flip()
    clock.tick(60)