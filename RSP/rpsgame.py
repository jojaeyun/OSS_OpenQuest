import pygame
import os
import random
import sys

# 초기화
pygame.init()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Game")

# 색상
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
BLUE = (80, 150, 255)
RED = (255, 80, 80)
GREEN = (80, 200, 120)
YELLOW = (240, 200, 60)
DARK_GRAY = (40, 40, 40)

FONT_PATH = os.path.join(BASE_PATH, "..", "fonts", "PressStart2P-Regular.ttf")

font_title = pygame.font.Font(FONT_PATH, 26)
font_result_big = pygame.font.Font(FONT_PATH, 62)
font_text = pygame.font.Font(FONT_PATH, 26)
font_small = pygame.font.Font(FONT_PATH, 18)
font_tiny = pygame.font.Font(FONT_PATH, 10)

# 이미지 로드 함수 (assets 폴더 적용)
def load_image(filename, size=(150, 150), fallback_color=DARK_GRAY):
    filepath = os.path.join(BASE_PATH, "assets", filename)
    if os.path.exists(filepath):
        img = pygame.image.load(filepath).convert_alpha()
        img = pygame.transform.scale(img, size)
        return img
    else:
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        text = font_small.render(filename.split('.')[0], True, WHITE)
        surf.blit(text, (10, 10))
        return surf

# 이미지 로드
background_img = load_image("background.png", size=(WIDTH, HEIGHT), fallback_color=DARK_GRAY)
rock_img = load_image("rock.png", size=(150, 150))
paper_img = load_image("paper.png", size=(150, 150))
scissors_img = load_image("scissors.png", size=(150, 150))

# 버튼 클래스
class ImageButton:
    def __init__(self, x, y, image, text=""):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.text = text

    def draw(self, surface, mouse_pos):
        surface.blit(self.image, self.rect)
        if self.rect.collidepoint(mouse_pos):
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 60))
            surface.blit(overlay, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class TextButton:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font

    def draw(self, surface, mouse_pos):
        color = LIGHT_GRAY if self.rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# 버튼 위치
buttons = [
    ImageButton(120, 420, scissors_img, "Scissors"),
    ImageButton(340, 420, rock_img, "Rock"),
    ImageButton(560, 420, paper_img, "Paper")
]

retry_button = TextButton(225, 450, 150, 70, "RETRY", font_text)
exit_button = TextButton(425, 450, 150, 70, "EXIT", font_text)
exit_button_top_left = TextButton(20, 20, 120, 40, "EXIT", font_small)

# 게임 시간
GAME_DURATION = 30

def reset_game():
    global current_streak, max_streak, result_text, computer_result_text
    global start_time, game_over, player_choice, computer_choice, just_reset
    global player_hp, computer_hp

    current_streak = 0
    max_streak = 0
    player_hp = 100
    computer_hp = 100
    result_text = "SELECT"
    computer_result_text = ""
    player_choice = None
    computer_choice = None
    start_time = pygame.time.get_ticks()
    game_over = False
    just_reset = True

reset_game()

# 메인 루프
running = True
clock = pygame.time.Clock()

while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(background_img, (0, 0))

    # 시간 계산
    current_time = (pygame.time.get_ticks() - start_time) / 1000
    remaining_time = max(0, GAME_DURATION - current_time)
    progress_ratio = remaining_time / GAME_DURATION

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                if exit_button_top_left.is_clicked(event.pos):
                    running = False
                else:
                    for i, btn in enumerate(buttons):
                        if btn.is_clicked(event.pos):

                            player_choice = ["Scissors", "Rock", "Paper"][i]
                            computer_choice = random.choice(["Scissors", "Rock", "Paper"])
                            computer_result_text = f"COMPUTER: {computer_choice}"

                            # 승부 판정
                            if player_choice == computer_choice:
                                result_text = "DRAW"
                                current_streak = 0
                            elif (player_choice == "Scissors" and computer_choice == "Paper") or \
                                 (player_choice == "Rock" and computer_choice == "Scissors") or \
                                 (player_choice == "Paper" and computer_choice == "Rock"):
                                result_text = "WIN"
                                current_streak += 1
                                max_streak = max(max_streak, current_streak)
                                computer_hp -= 10
                            else:
                                result_text = "LOSE"
                                current_streak = 0
                                player_hp -= 10

                            if player_hp <= 0 or computer_hp <= 0:
                                game_over = True
                                if player_hp <= 0 and computer_hp <= 0:
                                    result_text = "DRAW"
                                elif player_hp <= 0:
                                    result_text = "KO\nCOMPUTER WINS"
                                else:
                                    result_text = "KO\nPLAYER WINS"
            else:
                if retry_button.is_clicked(event.pos):
                    reset_game()
                elif exit_button.is_clicked(event.pos):
                    running = False

    # 시간 종료
    if not just_reset:
        if remaining_time <= 0 and not game_over:
            game_over = True
            if player_hp > computer_hp:
                result_text = f"TIME UP\nPLAYER WINS\nBEST {max_streak}"
            elif computer_hp > player_hp:
                result_text = f"TIME UP\nCOMPUTER WINS\nBEST {max_streak}"
            else:
                result_text = f"TIME UP\nDRAW\nBEST {max_streak}"
            computer_result_text = ""
    else:
        just_reset = False

    # 제목
    title_surface = font_title.render("ROCK PAPER SCISSORS", True, BLUE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 40))

    # 연승 표시
    streak_text = font_small.render(f"STREAK {current_streak}   BEST {max_streak}", True, WHITE)
    screen.blit(streak_text, (60, 150))

    # 체력바 표시
    pygame.draw.rect(screen, DARK_GRAY, (60, 230, 250, 25), border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, (WIDTH - 315, 230, 250, 25), border_radius=10)

    player_bar_width = int(250 * (player_hp / 100))
    computer_bar_width = int(250 * (computer_hp / 100))

    pygame.draw.rect(screen, GREEN, (60, 230, player_bar_width, 25), border_radius=10)
    pygame.draw.rect(screen, RED, (WIDTH - 315 + (250 - computer_bar_width), 230, computer_bar_width, 25), border_radius=10)

    player_name = font_small.render("PLAYER", True, WHITE)
    comp_name = font_small.render("COMPUTER", True, WHITE)
    screen.blit(player_name, (60, 200))
    screen.blit(comp_name, (WIDTH - 210, 200))

    # 남은 시간 progress bar
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 100, 100, 200, 15), border_radius=10)
    bar_width = int(200 * progress_ratio)
    color = RED if remaining_time <= 10 else BLUE
    pygame.draw.rect(screen, color, (WIDTH // 2 - 100, 100, bar_width, 15), border_radius=10)

    # 시간 텍스트
    time_text = font_small.render(f"{int(remaining_time)}s", True, WHITE)
    screen.blit(time_text, (WIDTH // 2 + 120, 100))

    # 상단 종료 버튼
    exit_button_top_left.draw(screen, mouse_pos)

    # 게임 중 화면
    if not game_over:
        if result_text == "SELECT":
            guide_surface = font_small.render("SELECT ROCK PAPER SCISSORS!", True, WHITE)
            screen.blit(guide_surface, (WIDTH // 2 - guide_surface.get_width() // 2, 287))
        elif result_text in ["WIN", "LOSE", "DRAW"]:
            color = GREEN if result_text == "WIN" else (RED if result_text == "LOSE" else YELLOW)
            result_surface = font_result_big.render(result_text, True, color)
            screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, 280))

            if computer_result_text:
                comp_surface = font_small.render(computer_result_text, True, WHITE)
                screen.blit(comp_surface, (WIDTH // 2 - comp_surface.get_width() // 2, 370))
        else:
            result_surface = font_text.render(result_text, True, WHITE)
            screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, 280))
            if computer_result_text:
                comp_surface = font_small.render(computer_result_text, True, WHITE)
                screen.blit(comp_surface, (WIDTH // 2 - comp_surface.get_width() // 2, 350))

        for btn in buttons:
            btn.draw(screen, mouse_pos)

    # 종료 화면
    else:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(DARK_GRAY)
        screen.blit(overlay, (0, 0))

        lines = result_text.split("\n")
        start_y = HEIGHT // 2 - (len(lines) - 1) * 40 - 80
        for i, line in enumerate(lines):
            surf = font_result_big.render(line, True, WHITE if i == 0 else YELLOW)
            rect = surf.get_rect(center=(WIDTH // 2, start_y + i * 80))
            screen.blit(surf, rect)

        retry_button.draw(screen, mouse_pos)
        exit_button.draw(screen, mouse_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()