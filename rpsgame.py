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
pygame.display.set_caption("가위바위보 게임")

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

# 폰트
try:
    TITLE_FONT = pygame.font.SysFont('malgungothic', 60, bold=True)
    BIG_RESULT_FONT = pygame.font.SysFont('malgungothic', 72, bold=True)
    TEXT_FONT = pygame.font.SysFont('malgungothic', 36)
    SMALL_FONT = pygame.font.SysFont('malgungothic', 28)
except:
    TITLE_FONT = pygame.font.Font(None, 60)
    BIG_RESULT_FONT = pygame.font.Font(None, 72)
    TEXT_FONT = pygame.font.Font(None, 36)
    SMALL_FONT = pygame.font.Font(None, 28)


# 이미지 로드 함수
def load_image(filename, size=(150, 150), fallback_color=DARK_GRAY):
    filepath = os.path.join(BASE_PATH, filename)
    if os.path.exists(filepath):
        img = pygame.image.load(filepath).convert_alpha()
        img = pygame.transform.scale(img, size)
        return img
    else:
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        text = SMALL_FONT.render(filename.split('.')[0], True, WHITE)
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
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface, mouse_pos):
        color = LIGHT_GRAY if self.rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surface = TEXT_FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# 버튼 위치
buttons = [
    ImageButton(120, 420, scissors_img, "가위"),
    ImageButton(340, 420, rock_img, "바위"),
    ImageButton(560, 420, paper_img, "보")
]
retry_button = TextButton(225, 450, 150, 70, "다시하기")
exit_button = TextButton(425, 450, 150, 70, "종료하기")

# 게임 변수
GAME_DURATION = 30


def reset_game():
    global player_score, computer_score, result_text, computer_result_text
    global start_time, game_over, player_choice, computer_choice, just_reset
    player_score = 0
    computer_score = 0
    result_text = "가위, 바위, 보 중 하나를 선택하세요!"
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
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(event.pos):
                        player_choice = ["가위", "바위", "보"][i]
                        computer_choice = random.choice(["가위", "바위", "보"])
                        computer_result_text = f"컴퓨터는 {computer_choice}를 냈습니다."
                        if player_choice == computer_choice:
                            result_text = "DRAW!"
                        elif (player_choice == "가위" and computer_choice == "보") or \
                             (player_choice == "바위" and computer_choice == "가위") or \
                             (player_choice == "보" and computer_choice == "바위"):
                            result_text = "WIN!"
                            player_score += 1
                        else:
                            result_text = "LOSE!"
                            computer_score += 1
            else:
                if retry_button.is_clicked(event.pos):
                    reset_game()
                elif exit_button.is_clicked(event.pos):
                    running = False

    # 시간 종료
    if not just_reset:
        if remaining_time <= 0 and not game_over:
            game_over = True
            if player_score > computer_score:
                result_text = "시간 종료!\n플레이어 승리!"
            elif computer_score > player_score:
                result_text = "시간 종료!\n컴퓨터 승리!"
            else:
                result_text = "시간 종료!\n무승부!"
            computer_result_text = ""
    else:
        just_reset = False

    # 제목
    title_surface = TITLE_FONT.render("가위바위보 게임", True, BLUE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 40))

    # 점수 표시
    score_text = SMALL_FONT.render(f"플레이어: {player_score}  컴퓨터: {computer_score}", True, WHITE)
    screen.blit(score_text, (50, 140))

    # 남은 시간 progress bar
    pygame.draw.rect(screen, GRAY, (WIDTH - 300, 140, 200, 20), border_radius=10)
    bar_width = int(200 * progress_ratio)
    color = RED if remaining_time <= 10 else BLUE
    pygame.draw.rect(screen, color, (WIDTH - 300, 140, bar_width, 20), border_radius=10)
    time_text = SMALL_FONT.render(f"{int(remaining_time)}초", True, WHITE)
    screen.blit(time_text, (WIDTH - 85, 130))

    if not game_over:
        # 메시지 표시
        if result_text == "가위, 바위, 보 중 하나를 선택하세요!":
            guide_surface = SMALL_FONT.render(result_text, True, WHITE)
            screen.blit(guide_surface, (WIDTH // 2 - guide_surface.get_width() // 2, 180))
        elif result_text in ["WIN!", "LOSE!", "DRAW!"]:
            color = GREEN if result_text == "WIN!" else (RED if result_text == "LOSE!" else YELLOW)
            result_surface = BIG_RESULT_FONT.render(result_text, True, color)
            screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, 220))
            if computer_result_text:
                comp_surface = SMALL_FONT.render(computer_result_text, True, WHITE)
                screen.blit(comp_surface, (WIDTH // 2 - comp_surface.get_width() // 2, 320))
        else:
            result_surface = TEXT_FONT.render(result_text, True, WHITE)
            screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, 230))
            if computer_result_text:
                comp_surface = SMALL_FONT.render(computer_result_text, True, WHITE)
                screen.blit(comp_surface, (WIDTH // 2 - comp_surface.get_width() // 2, 300))
        for btn in buttons:
            btn.draw(screen, mouse_pos)
    else:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(DARK_GRAY)
        screen.blit(overlay, (0, 0))

        lines = result_text.split("\n")
        start_y = HEIGHT // 2 - (len(lines) - 1) * 40
        for i, line in enumerate(lines):
            if i == 0:
                surf = BIG_RESULT_FONT.render(line, True, WHITE)
            else:
                big_font = pygame.font.SysFont('malgungothic', 100, bold=True)
                color = YELLOW if "승리" in line else (RED if "컴퓨터" in line else GREEN)
                surf = big_font.render(line, True, color)
            rect = surf.get_rect(center=(WIDTH // 2, start_y + i * 80))
            screen.blit(surf, rect)

        retry_button.draw(screen, mouse_pos)
        exit_button.draw(screen, mouse_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
