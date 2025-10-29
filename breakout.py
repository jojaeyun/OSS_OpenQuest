import pygame
import sys
import random
import math

# 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("벽돌깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (225, 225, 0)

# 공, 패들, 벽돌 설정
BALL_RADIUS = 10
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BRICK_WIDTH = 75
BRICK_HEIGHT = 20

FONT_PATH = "PressStart2P-Regular.ttf"
font_main = pygame.font.Font(FONT_PATH, 50)
font_small = pygame.font.Font(FONT_PATH, 15)
font_info = pygame.font.Font(FONT_PATH, 20)

# 게임 초기화 함수
def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, paddle_y, bricks, game_over, result_text

    ball_x = SCREEN_WIDTH // 2
    ball_y = 3 * SCREEN_HEIGHT // 4
    ball_dx = 4 * random.choice([-1, 1])
    ball_dy = -4

    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - 30

    bricks = []
    for row in range(5):
        for col in range(10):
            bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 80, BRICK_WIDTH, BRICK_HEIGHT))

    game_over = False
    result_text = ""

    global start_time
    start_time = pygame.time.get_ticks()

    global score
    score = 0

    global speedup_time, speedup_alpha, show_speedup, speedup, speedup_rect
    speedup_time = 0
    speedup_alpha = 0
    show_speedup = False
    speedup = font_info.render("SPEED UP!", True, RED)
    speedup_rect = speedup.get_rect(center=(SCREEN_WIDTH // 2, 25))

# 초기화 실행
reset_game()

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 엔터키로 재시작
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            reset_game()

    if not game_over:
        # 패들 이동
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle_x > 0:
            paddle_x -= 6
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
            paddle_x += 6

        # 공 이동
        ball_x += ball_dx
        ball_y += ball_dy

        # 위에 상태창 구분선 그리기
        pygame.draw.line(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50), 3)

        # 시간 정보
        current_time = (pygame.time.get_ticks() - start_time) / 1000
        sec2_time = current_time % 10
        sec1_time = (current_time % 60) // 10
        min_time = current_time // 60
        sec = font_info.render(f"{int(min_time)}:{int(sec1_time)}{int(sec2_time)}", True, WHITE)
        sec_rect = sec.get_rect(center=(750, 25))
        screen.blit(sec, sec_rect)

        # 점수 정보
        current_score = font_info.render(f"Score:{score}", True, WHITE)
        screen.blit(current_score, (15, 15))

        # 30초마다 속도 증가
        if (current_time - speedup_time >= 30):
            speedup_time = current_time  # 마지막 증가 시점 기록
            ball_dx *= 1.2
            ball_dy *= 1.2
            show_speedup = True
            speedup_alpha = 255  # 문구 완전 불투명으로 시작

        if show_speedup:
            speedup.set_alpha(speedup_alpha)
            screen.blit(speedup, speedup_rect)
            speedup_alpha -= 5
            if speedup_alpha <= 0:
                show_speedup = False
            
        # 공 벽 충돌
        if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            ball_dx *= -1
        if ball_y <= BALL_RADIUS + 53:
            ball_dy *= -1
        if ball_y >= SCREEN_HEIGHT:
            # 실패
            game_over = True
            result_text = "GAME OVER"

        # 공 패들 충돌
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        if paddle_rect.collidepoint(ball_x, ball_y + BALL_RADIUS):
            ball_dy *= -1

        # 공 벽돌 충돌
        for brick in bricks[:]:
            if brick.collidepoint(ball_x, ball_y):
                bricks.remove(brick)
                score += 100
                ball_dy *= -1
                break

        # 모든 벽돌 제거 시
        if not bricks:
            game_over = True
            result_text = "CLEAR!!"

        # 벽돌 그리기
        for brick in bricks:
            pygame.draw.rect(screen, YELLOW, brick)

        # 패들 그리기
        pygame.draw.rect(screen, WHITE, paddle_rect)

        # 공 그리기
        pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)

    else:
        # 결과 메시지 표시
        result = font_main.render(result_text, True, WHITE)
        rect = result.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(result, rect)

        time = pygame.time.get_ticks()
        brightness = int(((math.sin(time * 0.005) + 1)/3 + 1/3) * 255) # sin 파형으로 깜빡거리도록 함
        blink = (brightness, brightness, brightness)
        restart = font_small.render("Press ENTER to Restart", True, blink)
        rect2 = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(restart, rect2)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()