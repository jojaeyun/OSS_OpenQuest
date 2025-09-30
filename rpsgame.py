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

# 폰트
FONT = pygame.font.SysFont("malgungothic", 36)

# 버튼 클래스
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect, border_radius=15)

        # 텍스트 표시 (버튼 가운데 정렬)
        text_surface = FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# 버튼 생성 (한글만 표시)
buttons = [
    Button(100, 400, 150, 100, "가위"),
    Button(300, 400, 150, 100, "바위"),
    Button(500, 400, 150, 100, "보")
]

# 결과 메시지
result_text = ""

# 메인 루프
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, btn in enumerate(buttons):
                if btn.is_clicked(event.pos):
                    player_choice = ["가위", "바위", "보"][i]
                    computer_choice = random.choice(["가위", "바위", "보"])

                    if player_choice == computer_choice:
                        result_text = f"비겼습니다! (컴퓨터: {computer_choice})"
                    elif (player_choice == "가위" and computer_choice == "보") or \
                         (player_choice == "바위" and computer_choice == "가위") or \
                         (player_choice == "보" and computer_choice == "바위"):
                        result_text = f"이겼습니다! (컴퓨터: {computer_choice})"
                    else:
                        result_text = f"졌습니다! (컴퓨터: {computer_choice})"

    # 버튼 그리기
    for btn in buttons:
        btn.draw(screen)

    # 결과 표시
    if result_text:
        result_surface = FONT.render(result_text, True, BLACK)
        screen.blit(result_surface, (200, 200))

    pygame.display.flip()

pygame.quit()
sys.exit()
