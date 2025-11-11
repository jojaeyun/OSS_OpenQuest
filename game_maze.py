import pygame
import sys
import random
import math
from collections import deque
import time

# ---------------- 미로 생성 ----------------
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    def carve_passages(r, c):
        directions = [(0,-2),(0,2),(-2,0),(2,0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows-1 and 1 <= nc < cols-1 and maze[nr][nc] == 1:
                maze[nr][nc] = 0
                maze[r + dr//2][c + dc//2] = 0
                carve_passages(nr, nc)
    maze[1][1] = 0
    carve_passages(1,1)
    return maze

# ---------------- 경로 탐색 (BFS) ----------------
def find_path(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = {start}
    parent = {}
    while queue:
        r, c = queue.popleft()
        if (r, c) == end:
            path = []
            while (r, c) != start:
                path.append((r, c))
                r, c = parent[(r, c)]
            path.reverse()
            return path
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc]==0 and (nr,nc) not in visited:
                visited.add((nr,nc))
                parent[(nr,nc)] = (r,c)
                queue.append((nr,nc))
    return []

# ---------------- READY & GO 연출 ----------------
def show_ready_go(screen, font_large, screen_w, screen_h):
    try:
        ready_sound = pygame.mixer.Sound("gamestart.mp3")
        ready_sound.play()
    except Exception:
        pass

    start_time = time.time()
    show_ready = True
    while time.time() - start_time < 2.0:
        screen.fill((0, 0, 0))
        text = font_large.render("READY!", True, (255,255,255) if show_ready else (0,0,0))
        screen.blit(text, (screen_w//2 - text.get_width()//2, screen_h//2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(300)
        show_ready = not show_ready
    screen.fill((0,0,0))
    go_text = font_large.render("GO!", True, (255,255,255))
    screen.blit(go_text, (screen_w//2 - go_text.get_width()//2, screen_h//2 - go_text.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(1000)

# ---------------- 버튼 표시 함수 ----------------
def draw_button(screen, rect, text, font, color_bg, color_text):
    pygame.draw.rect(screen, color_bg, rect, border_radius=10)
    text_surface = font.render(text, True, color_text)
    screen.blit(
        text_surface,
        (rect.centerx - text_surface.get_width() // 2,
         rect.centery - text_surface.get_height() // 2)
    )

# ---------------- 게임 실행 ----------------
def run_pygame(difficulty=None):
    pygame.init()
    pygame.mixer.init()

    try:
        wall_hit_sound = pygame.mixer.Sound("wall_hit.wav")
    except Exception:
        wall_hit_sound = None

    FONT_PATH = "PressStart2P-Regular.ttf"
    try:
        font_small = pygame.font.Font(FONT_PATH, 24)
        font_large = pygame.font.Font(FONT_PATH, 60)
    except FileNotFoundError:
        font_small = pygame.font.SysFont(None, 24)
        font_large = pygame.font.SysFont(None, 60)

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("네온 미로 아케이드")
    clock = pygame.time.Clock()

    while True:
        # ---------------- 난이도 선택 ----------------
        if difficulty is None:
            choosing = True
            while choosing:
                screen.fill((0, 0, 0))
                title = font_large.render("SELECT LEVEL", True, (255, 255, 255))
                easy = font_small.render("[E] EASY", True, (100, 255, 100))
                normal = font_small.render("[N] NORMAL", True, (255, 255, 100))
                hard = font_small.render("[H] HARD", True, (255, 100, 100))
                screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
                screen.blit(easy, (SCREEN_WIDTH//2 - easy.get_width()//2, 300))
                screen.blit(normal, (SCREEN_WIDTH//2 - normal.get_width()//2, 350))
                screen.blit(hard, (SCREEN_WIDTH//2 - hard.get_width()//2, 400))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e: difficulty = "easy"; choosing = False
                        elif event.key == pygame.K_n: difficulty = "normal"; choosing = False
                        elif event.key == pygame.K_h: difficulty = "hard"; choosing = False

        show_ready_go(screen, font_large, SCREEN_WIDTH, SCREEN_HEIGHT)

        # ---------------- 난이도별 설정 ----------------
        if difficulty == "easy":
            enemy_count, item_count, enemy_speed = 1, 8, 2.2
        elif difficulty == "normal":
            enemy_count, item_count, enemy_speed = 2, 6, 2.8
        else:
            enemy_count, item_count, enemy_speed = 3, 5, 3.3

        # ---------------- 게임 로직 초기화 ----------------
        ROWS, COLS = 21, 31
        TILE_SIZE = min(SCREEN_WIDTH // COLS, SCREEN_HEIGHT // ROWS)
        maze = generate_maze(ROWS, COLS)
        player_x, player_y = TILE_SIZE, TILE_SIZE
        player_vx, player_vy = 0, 0
        player_accel, player_max_speed = 0.6, 4.5
        exit_row, exit_col = ROWS - 2, COLS - 2
        maze[exit_row][exit_col] = 0

        # ---------------- 적 초기화 ----------------
        enemies = []
        for _ in range(enemy_count):
            while True:
                r, c = random.randint(ROWS//2, ROWS-2), random.randint(COLS//2, COLS-2)
                if maze[r][c] == 0:
                    enemies.append({"x": c*TILE_SIZE, "y": r*TILE_SIZE, "path": [], "disabled": False, "timer": 0, "path_timer": 0})
                    break

        # ---------------- 아이템 초기화 (플레이어 근처 최소 1개) ----------------
        items = []

        # 1️⃣ 플레이어 근처에 최소 1개 아이템
        while True:
            r = random.randint(1, 3)
            c = random.randint(1, 3)
            if maze[r][c] == 0:
                items.append((r, c))
                break

        # 나머지 아이템
        for _ in range(item_count - 1):
            while True:
                r, c = random.randint(1, ROWS-2), random.randint(1, COLS-2)
                if maze[r][c] == 0 and (r, c) not in [(1,1), (exit_row, exit_col)] + items:
                    items.append((r, c))
                    break

        WALL_COLOR = (0,0,0)
        PATH_COLOR = (70,70,70)
        PLAYER_COLOR = (0,255,255)
        EXIT_COLOR = (50,255,100)
        ENEMY_COLOR = (255,50,255)
        ITEM_COLOR = (255,255,100)

        def rect_can_move(x, y):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            for r in range(ROWS):
                for c in range(COLS):
                    if maze[r][c] == 1:
                        wall_rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if rect.colliderect(wall_rect):
                            return False
            return True

        running, won = True, False
        disable_duration = 180
        t = 0

        # ---------------- 메인 게임 루프 ----------------
        while running:
            t += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: player_vx -= player_accel
            if keys[pygame.K_RIGHT]: player_vx += player_accel
            if keys[pygame.K_UP]: player_vy -= player_accel
            if keys[pygame.K_DOWN]: player_vy += player_accel

            player_vx *= 0.9; player_vy *= 0.9
            player_vx = max(-player_max_speed, min(player_max_speed, player_vx))
            player_vy = max(-player_max_speed, min(player_max_speed, player_vy))

            new_x, new_y = player_x + player_vx, player_y + player_vy

            # ---------------- 벽 충돌 & 소리 ----------------
            if rect_can_move(new_x, player_y):
                player_x = new_x
            else:
                player_vx = 0
                if wall_hit_sound:
                    wall_hit_sound.play()
            if rect_can_move(player_x, new_y):
                player_y = new_y
            else:
                player_vy = 0
                if wall_hit_sound:
                    wall_hit_sound.play()

            player_row, player_col = int(player_y // TILE_SIZE), int(player_x // TILE_SIZE)

            for item in items[:]:
                if (player_row, player_col) == item:
                    items.remove(item)
                    for e in enemies:
                        e["disabled"] = True
                        e["timer"] = disable_duration

            for e in enemies:
                if e["disabled"]:
                    e["timer"] -= 1
                    if e["timer"] <= 0: e["disabled"] = False
                    continue
                er, ec = int(e["y"]//TILE_SIZE), int(e["x"]//TILE_SIZE)
                e["path_timer"] += 1
                if e["path_timer"] % 30 == 0:
                    e["path"] = find_path(maze, (er, ec), (player_row, player_col))
                if e["path"]:
                    next_r, next_c = e["path"][0]
                    target_x, target_y = next_c*TILE_SIZE, next_r*TILE_SIZE
                    dir_x, dir_y = target_x - e["x"], target_y - e["y"]
                    dist = max(1, math.hypot(dir_x, dir_y))
                    move_x = enemy_speed * dir_x / dist
                    move_y = enemy_speed * dir_y / dist
                    # 벽 체크 후 이동
                    if rect_can_move(e["x"] + move_x, e["y"]):
                        e["x"] += move_x
                    if rect_can_move(e["x"], e["y"] + move_y):
                        e["y"] += move_y
                    if abs(e["x"] - target_x) < 2 and abs(e["y"] - target_y) < 2:
                        e["path"].pop(0)

            if (player_row, player_col) == (exit_row, exit_col):
                won = True; running = False
            for e in enemies:
                if not e["disabled"]:
                    er, ec = int(e["y"]//TILE_SIZE), int(e["x"]//TILE_SIZE)
                    if abs(player_row - er) < 1 and abs(player_col - ec) < 1:
                        won = False; running = False

            # ---------------- 렌더링 ----------------
            screen.fill((0, 0, 0))
            for r in range(ROWS):
                for c in range(COLS):
                    color = WALL_COLOR if maze[r][c] == 1 else PATH_COLOR
                    pygame.draw.rect(screen, color, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            for (r,c) in items:
                pygame.draw.rect(screen, ITEM_COLOR, (c*TILE_SIZE+TILE_SIZE//4, r*TILE_SIZE+TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2))
            pygame.draw.rect(screen, EXIT_COLOR, (exit_col*TILE_SIZE, exit_row*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            for e in enemies:
                color = (100,100,100) if e["disabled"] else ENEMY_COLOR
                pygame.draw.rect(screen, color, (e["x"], e["y"], TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, TILE_SIZE, TILE_SIZE))
            hud = font_small.render(f"ITEMS LEFT: {len(items)}", True, (255,255,255))
            screen.blit(hud, (10,10))
            pygame.display.flip()
            clock.tick(60)

        # ---------------- 게임 종료 화면 ----------------
        victory_sound_played = False
        defeat_sound_played = False
        while True:
            screen.fill((0, 0, 0))
            msg = "VICTORY!" if won else "DEFEAT!"
            text = font_large.render(msg, True, (50,255,50) if won else (255,80,80))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150))

            # 버튼
            main_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, 300, 300, 60)
            retry_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, 380, 300, 60)
            quit_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, 460, 300, 60)

            draw_button(screen, main_btn, "MAIN", font_small, (50,50,200), (255,255,255))
            draw_button(screen, retry_btn, "TRY AGAIN", font_small, (50,200,50), (255,255,255))
            draw_button(screen, quit_btn, "QUIT", font_small, (200,50,50), (255,255,255))
            pygame.display.flip()

            # 승리/패배 사운드 재생
            if won and not victory_sound_played:
                try:
                    pygame.mixer.Sound("victory.mp3").play()
                except Exception:
                    pass
                victory_sound_played = True
            elif not won and not defeat_sound_played:
                try:
                    pygame.mixer.Sound("defeat.mp3").play()
                except Exception:
                    pass
                defeat_sound_played = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if main_btn.collidepoint(event.pos):
                        difficulty = None
                        break
                    elif retry_btn.collidepoint(event.pos):
                        run_pygame(difficulty=difficulty)
                    elif quit_btn.collidepoint(event.pos):
                        pygame.quit(); sys.exit()
            else:
                continue
            break  # main_btn 클릭 시 while 루프 탈출, 난이도 선택 화면으로 돌아감

if __name__ == "__main__":
    run_pygame()