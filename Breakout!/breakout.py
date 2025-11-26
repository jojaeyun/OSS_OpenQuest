import pygame
import sys
import random
import math
import os

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

FONT_PATH = "./fonts/PressStart2P-Regular.ttf"
font_main = pygame.font.Font(FONT_PATH, 50)
font_small = pygame.font.Font(FONT_PATH, 15)
font_info = pygame.font.Font(FONT_PATH, 20)
font_result = pygame.font.Font(FONT_PATH, 25)
font_quit = pygame.font.Font(FONT_PATH, 18)

# 최고점수 불러오기
if os.path.exists("Breakout!/breakout_score.txt"):
    f = open("Breakout!/breakout_score.txt", "r")
    f_score = f.read().strip()
    if f_score == "":
        high = 0
    else:
        high = int(f_score)
else:
    high = 0

# 점수(갱신 가능)
global score
score = 0

# 공과 벽돌 충돌 여부 확인
def collision(x, y, r, rect):
    # 원의 중심에서 가장 가까운 사각형 내부 점과 원의 중심 간의 거리 계산
    closest_x = max(rect.left, min(x, rect.right))
    closest_y = max(rect.top, min(y, rect.bottom))
    
    distance_x = x - closest_x
    distance_y = y - closest_y
    distance = math.sqrt(distance_x**2 + distance_y**2)
    
    return distance < r

# 게임 초기화 함수
def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, paddle_y, bricks, game_over, result_text

    ball_x = SCREEN_WIDTH // 2
    ball_y = 3 * SCREEN_HEIGHT // 4
    ball_dx = 4 * random.choice([-1, 1])
    ball_dy = -4

    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    paddle_y = SCREEN_HEIGHT - 30

    stage = random.randint(0,19)

    # 벽돌배치
    bricks = [] 
    if (stage == 0):
        for row in range(5):
            for col in range(10):
                bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 80, BRICK_WIDTH, BRICK_HEIGHT))
    if (stage == 1):
        for row in range(9):
            for col in range(10):
                if ((row % 2 == 0 and col % 2 == 1) or (row % 2 == 1 and col % 2 == 0)):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
    if (stage == 2):
        for row in range(7):
            if (row == 0 or row == 6):
                for col in range(10):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            if (row == 1 or row == 5):
                    bricks.append(pygame.Rect(0 * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
                    bricks.append(pygame.Rect(9 * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            if (row == 2 or row == 4):
                bricks.append(pygame.Rect(0 * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
                bricks.append(pygame.Rect(9 * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT)) 
                for col in range(2,8):
                        bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))    
            if (row == 3):
                bricks.append(pygame.Rect(0 * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
                bricks.append(pygame.Rect(2 * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))  
                bricks.append(pygame.Rect(7 * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT)) 
                bricks.append(pygame.Rect(9 * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))                                      
    if (stage == 3):
        for col in range(10):
            if (col == 0 or col == 9):
                for row in range(9):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            if (col == 1 or col == 8):
                for row in range(1,8):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 2 or col == 7):
                for row in range(2,7):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 3 or col == 6):
                for row in range(3,6):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 4 or col == 5):
                for row in range(4,5):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))                                                
    if (stage == 4):
        for col in range(10):
            if (col == 0 or col == 9):
                for row in range(4,5):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            if (col == 1 or col == 8):
                for row in range(3,6):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 2 or col == 7):
                for row in range(2,7):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 3 or col == 6):
                for row in range(1,8):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 4 or col == 5):
                for row in range(9):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
    if (stage == 5):
        for col in range(10):
            for row in range(col):
                bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT)) 
    if (stage == 6):
        for col in range(10):
            for row in range(9-col):
                bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT)) 
    if (stage == 7):
        for row in range(0,10,2):
            for col in range(10):
                bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))                                      
    if (stage == 8):
        for col in [0,2,7,9]:
            for row in range(10):
                bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
        for col in range(3,7):
            for row in [0,9]:
                bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
    if (stage == 9):
        for row in range(10):
            for col in range(10):
                if (row == 4 or row == 5 or col == 4 or col == 5) and not(4 <= row <= 5 and 4 <= col <= 5):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
                if (1 <= row <= 2 and 1 <= col <= 2) or (7 <= row <= 8 and 7 <= col <= 8) or (1 <= row <= 2 and 7 <= col <= 8) or (7 <= row <= 8 and 1 <= col <= 2):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
    if (stage == 10):
        for col in range(10):
            if (col == 0 or col == 3 or col == 6 or col == 9):
                for row in range(10):
                    if (row < 4 or row > 5):
                        bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            if (col == 1 or col == 2 or col == 7 or col == 8):
                for row in range(10):
                    if (row == 0 or row == 3 or row == 6 or row == 9):
                        bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 4 or col == 5):
                for row in range(4,6):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))      
    if (stage == 11):
        for col in range(1,10,2):
            for row in range(9):
                bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
        for col in [0,4,8]:
            row = 0
            bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))  
        for col in [4,8]:
            row = 8
            bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT)) 
    if (stage == 12):
        for col in [0,1,2,6,7,8]:
            for row in [0,1,5,6]:
                bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
        for col in [3,9]:
            for row in range(11):
                bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))  
    if (stage == 13):
        for col in range(10):
            if (col == 1 or col == 3 or col == 5 or col == 7):
                for row in range(6,7):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            if (col == 0):
                for row in [5,7]:
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 2 or col == 6):
                for row in range(4,9):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 4):
                for row in range(3,10):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 8):
                for row in range(13):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))    
            if (col == 9) :
                for row in range(1,12):
                    if (row != 4):
                        bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))    
    if (stage == 14):
        for row in range(9):
            if (row == 1 or row == 7):
                for col in range(10):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            if (row == 0 or row == 3 or row == 5 or row == 8):
                for col in [1,3,6,8]:
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (row == 2 or row == 6):
                for col in [0,4,5,9]:
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))              
            if (row == 4):
                for col in [2,7]:
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))   
    if (stage == 15):
        for col in range(10):
            if (col == 0 or col == 9):
                for row in range(20):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            else:
                for row in range(0,2):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT)) 
    if (stage == 16):
        for col in range(10):
            if (col == 0 or col == 4 or col == 8):
                for row in range(0,5):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            if (col == 1 or col == 3 or col == 5 or col == 7 or col == 9):
                for row in range(1,6):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 2 or col == 6):
                for row in range(2,7):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))   
    if (stage == 17):
        for col in range(10):
            if (col % 2 == 0):
                for row in range(0,5):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            else:
                for row in range(5,10):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))            
    if (stage == 18):
        for col in range(10):
            if (col == 0 or col == 9):
                for row in range(1):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            if (col == 1 or col == 8):
                for row in range(3):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 2 or col == 7):
                for row in range(5):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 3 or col == 6):
                for row in range(7):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        
            if (col == 4 or col == 5):
                for row in range(9):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
    if (stage == 19):
        for col in range(10):
            if (col == 1 or col == 8):
                for row in [0,1,6,7]:
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            elif (col < 3 or col > 6):
                for row in range(8):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))
            else:
                for row in range(3,5):
                    bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 57, BRICK_WIDTH, BRICK_HEIGHT))        

    game_over = False
    result_text = ""

    global start_time
    start_time = pygame.time.get_ticks()

    global speedup_time, speedup_alpha, show_speedup, speedup, speedup_rect, score_up, gameover_sound, clear_sound, show_quit_text
    score_up = 10   # 기본점수
    speedup_time = 0
    speedup_alpha = 0
    show_speedup = False
    speedup = font_info.render("SPEED UP!", True, RED)
    speedup_rect = speedup.get_rect(center=(SCREEN_WIDTH // 2, 25))
    gameover_sound = True
    clear_sound = True
    show_quit_text = False

esc_pressed_time = None     # esc 누른 시간
ESC_HOLD_DURATION = 3000    # 눌러야 하는 시간 (3초)

# 초기화 실행
reset_game()

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    # 키보드 입력
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 엔터키로 재시작
        if result_text == "GAME OVER" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            score = 0
            reset_game()

        if result_text == "CLEAR!!" and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            reset_game()

        # esc 누름
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                esc_pressed_time = pygame.time.get_ticks()
                show_quit_text = True
        # esc 뗌
        if game_over and event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                esc_pressed_time = None
                show_quit_text = False

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
            score_up += 10  # 보너스 점수
            show_speedup = True
            speedup_alpha = 255  # 문구 완전 불투명으로 시작
            pygame.mixer.Sound("Breakout!/breakout_sound/speedup.wav").play()

        if show_speedup:
            speedup.set_alpha(speedup_alpha)
            screen.blit(speedup, speedup_rect)
            speedup_alpha -= 5
            if speedup_alpha <= 0:
                show_speedup = False
            
        # 공 벽 충돌
        if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            ball_dx *= -1
            pygame.mixer.Sound("Breakout!/breakout_sound/collision.wav").play()
        if ball_y <= BALL_RADIUS + 53:
            ball_dy *= -1
            pygame.mixer.Sound("Breakout!/breakout_sound/collision.wav").play()
        if ball_y >= SCREEN_HEIGHT:
            # 실패
            game_over = True
            result_text = "GAME OVER"

        # 공 패들 충돌
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        if paddle_rect.collidepoint(ball_x, ball_y + BALL_RADIUS):
            ball_dy *= -1
            pygame.mixer.Sound("Breakout!/breakout_sound/collision.wav").play()

        # 공 벽돌 충돌
        for brick in bricks[:]:
            if collision(ball_x, ball_y, BALL_RADIUS, brick):
                bricks.remove(brick)
                score += score_up
                ball_dy *= -1
                pygame.mixer.Sound("Breakout!/breakout_sound/break.wav").play()
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
        # 최고점수 갱신
        if score > high:
            high = score
            f = open("Breakout!/breakout_score.txt", "w")
            f.write(str(high))

        # 결과 메시지 표시
        result = font_main.render(result_text, True, WHITE)
        rect = result.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180))
        screen.blit(result, rect)

        time = pygame.time.get_ticks()
        brightness = int(((math.sin(time * 0.005) + 1)/3 + 1/3) * 255) # sin 파형으로 깜빡거리도록 함
        blink = (brightness, brightness, brightness)

        if result_text == "GAME OVER":
            final_text = font_result.render("Final Score", True, (150,150,150))
            final_rect = final_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(final_text, final_rect)
            restart = font_small.render("Press ENTER to Restart", True, blink)
            rect2 = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180))
            screen.blit(restart, rect2)
            if (gameover_sound):
                pygame.mixer.Sound("Breakout!/breakout_sound/gameover.wav").play()
            gameover_sound = False

        if result_text == "CLEAR!!":
            current_text = font_result.render("Current Score", True, (150,150,150))
            current_rect = current_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(current_text, current_rect)
            restart = font_small.render("Press ENTER to Continue", True, blink)
            rect2 = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180))
            screen.blit(restart, rect2)
            if (clear_sound):
                pygame.mixer.Sound("Breakout!/breakout_sound/clear.wav").play()
            clear_sound = False

        result_score = font_result.render(f"{score}", True, (150,150,150))
        score_rect = result_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        screen.blit(result_score, score_rect)

        high_text = font_result.render("High Score", True, (200,200,200))
        high_rect = high_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(high_text, high_rect)

        high_score = font_result.render(f"{high}", True, (200,200,200))
        high_score_rect = high_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        screen.blit(high_score, high_score_rect)

        if show_quit_text:  # 종료문구 표시
            quit_text = font_quit.render("quit...", True, (100,100,100))
            quit_rect = quit_text.get_rect(center=(80, 20))
            screen.blit(quit_text, quit_rect)

        if esc_pressed_time is not None:    # 게임종료
            if pygame.time.get_ticks() - esc_pressed_time >= ESC_HOLD_DURATION:
                running = False

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()