import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("가위바위보 게임")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

# 폰트
FONT = pygame.font.SysFont("malgungothic", 36)

# 버튼 클래스
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface, color=GRAY):
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        text_surface = FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# 버튼 생성
buttons = [
    Button(100, 400, 150, 100, "가위"),
    Button(300, 400, 150, 100, "바위"),
    Button(500, 400, 150, 100, "보")
]
retry_button = Button(325, 350, 150, 70, "다시하기")

# 게임 변수 초기화 함수
def reset_game():
    global player_score, computer_score, result_text, start_time, game_over, just_reset
    player_score = 0
    computer_score = 0
    result_text = ""
    start_time = pygame.time.get_ticks()
    game_over = False
    just_reset = True  # 새로 시작한 직후 1프레임 예외 처리

# 초기화
reset_game()
GAME_DURATION = 30  # 제한 시간 (초)

# 메인 루프
running = True
while running:
    screen.fill(WHITE)
    current_time = (pygame.time.get_ticks() - start_time) / 1000
    remaining_time = max(0, GAME_DURATION - int(current_time))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                # 가위바위보 버튼 클릭
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(event.pos):
                        player_choice = ["가위", "바위", "보"][i]
                        computer_choice = random.choice(["가위", "바위", "보"])

                        if player_choice == computer_choice:
                            result_text = f"비겼습니다! (컴퓨터: {computer_choice})"
                            player_score += 1
                            computer_score += 1
                        elif (player_choice == "가위" and computer_choice == "보") or \
                             (player_choice == "바위" and computer_choice == "가위") or \
                             (player_choice == "보" and computer_choice == "바위"):
                            result_text = f"이겼습니다! (컴퓨터: {computer_choice})"
                            player_score += 1
                        else:
                            result_text = f"졌습니다! (컴퓨터: {computer_choice})"
                            computer_score += 1
            else:
                # 다시하기 버튼 클릭
                if retry_button.is_clicked(event.pos):
                    reset_game()

    # 시간 종료 체크 (리셋 직후 한 프레임은 제외)
    if not just_reset:
        if remaining_time <= 0 and not game_over:
            game_over = True
            if player_score > computer_score:
                result_text = "시간 종료! 플레이어 승리!"
            elif computer_score > player_score:
                result_text = "시간 종료! 컴퓨터 승리!"
            else:
                result_text = "시간 종료! 무승부!"
    else:
        just_reset = False

    # ---------- 화면 표시 구간 ----------
    if not game_over:
        # (1) 게임 진행 중
        for btn in buttons:
            btn.draw(screen)

        score_text = FONT.render(f"플레이어: {player_score}   컴퓨터: {computer_score}", True, BLACK)
        screen.blit(score_text, (180, 100))

        result_surface = FONT.render(result_text, True, BLACK)
        screen.blit(result_surface, (150, 200))

        time_text = FONT.render(f"남은 시간: {remaining_time}초", True, BLACK)
        screen.blit(time_text, (300, 40))

    else:
        # (2) 게임 종료 시 — 결과와 다시하기 버튼만 표시
        screen.fill(WHITE)
        result_surface = FONT.render(result_text, True, BLACK)
        result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(result_surface, result_rect)
        retry_button.draw(screen, LIGHT_GRAY)

    pygame.display.flip()

pygame.quit()
sys.exit()
