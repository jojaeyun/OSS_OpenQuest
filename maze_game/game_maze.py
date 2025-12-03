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
        ready_sound = pygame.mixer.Sound("maze_game/gamestart.mp3")
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

    # ---------------- 사운드 로드 ----------------
    try:
        wall_hit_sound = pygame.mixer.Sound("maze_game/wall_hit.wav")
    except Exception:
        wall_hit_sound = None

    try:
        item_pickup_sound = pygame.mixer.Sound("maze_game/item_pickup.mp3")
    except Exception:
        item_pickup_sound = None

    try:
        moving_sound = pygame.mixer.Sound("maze_game/moving.mp3")
        moving_sound.set_volume(0.2)
        moving_channel = pygame.mixer.Channel(5)
    except Exception:
        moving_sound = None
        moving_channel = None

    try:
        victory_sound = pygame.mixer.Sound("maze_game/victory.mp3")
        defeat_sound = pygame.mixer.Sound("maze_game/defeat.mp3")
    except Exception:
        victory_sound = None
        defeat_sound = None

    FONT_PATH = "./fonts/PressStart2P-Regular.ttf"
    try:
        font_small = pygame.font.Font(FONT_PATH, 24)
        font_large = pygame.font.Font(FONT_PATH, 60)
    except FileNotFoundError:
        font_small = pygame.font.SysFont(None, 24)
        font_large = pygame.font.SysFont(None, 60)

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("아케이드 미로 게임")
    clock = pygame.time.Clock()

    # ---------------- 랭킹 표시 ----------------
    def draw_ranking(screen, font_small, difficulty="normal"):
        ranking_file = f"ranking_{difficulty}.txt"
        try:
            with open(ranking_file, "r") as f:
                times = [float(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            times = []

        if times:
            screen.blit(font_small.render("RANKING:", True, (255,255,255)), (SCREEN_WIDTH//2 - 70, 220))
            for i, t in enumerate(times):
                text = font_small.render(f"{i+1}. {t:.2f}s", True, (255,255,0))
                screen.blit(text, (SCREEN_WIDTH//2 - 50, 250 + i*25))


    # ---------------- 랭킹 저장 ----------------
    def save_ranking(elapsed_time, difficulty="normal", top_n=5):
        ranking_file = f"ranking_{difficulty}.txt"
        try:
            with open(ranking_file, "r") as f:
                times = [float(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            times = []

        times.append(elapsed_time)
        times.sort()  # 오름차순: 빠른 시간 먼저
        times = times[:top_n]  # 상위 N개만

        with open(ranking_file, "w") as f:
            for t in times:
                f.write(f"{t:.2f}\n")


    # ---------------- 이미지 로드 ----------------
    try:
        player_img = pygame.image.load("maze_game/player.png").convert_alpha()
    except Exception as e:
        print("플레이어 이미지 로드 실패:", e)
        player_img = None

    enemy_imgs_all = []
    for i in range(1, 4):
        try:
            img = pygame.image.load(f"maze_game/enemy{i}.png").convert_alpha()
            enemy_imgs_all.append(img)
        except Exception as e:
            print(f"enemy{i}.png 로드 실패:", e)

    if not enemy_imgs_all:
        enemy_imgs_all = [None]

    while True:
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

        try:
            pygame.mixer.music.load("maze_game/bgm.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("BGM 로드 실패:", e)

        if difficulty == "easy":
            enemy_count, item_count, enemy_speed, enemy_img_count = 1, 8, 2.2, 1
        elif difficulty == "normal":
            enemy_count, item_count, enemy_speed, enemy_img_count = 2, 6, 2.8, 2
        else:
            enemy_count, item_count, enemy_speed, enemy_img_count = 3, 5, 3.3, 3

        enemy_imgs = enemy_imgs_all[:enemy_img_count]

        TILE_SIZE = 24
        COLS = SCREEN_WIDTH // TILE_SIZE
        ROWS = SCREEN_HEIGHT // TILE_SIZE
        if ROWS % 2 == 0: ROWS -= 1
        if COLS % 2 == 0: COLS -= 1

        TILE_SIZE_W = SCREEN_WIDTH / COLS
        TILE_SIZE_H = SCREEN_HEIGHT / ROWS
        TILE_SIZE = int(min(TILE_SIZE_W, TILE_SIZE_H))

        maze = generate_maze(ROWS, COLS)
        player_x, player_y = TILE_SIZE, TILE_SIZE
        player_vx, player_vy = 0, 0
        player_accel, player_max_speed = 0.6, 4.5
        exit_row, exit_col = ROWS - 2, COLS - 2
        maze[exit_row][exit_col] = 0

        if player_img:
            player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
        enemy_imgs = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in enemy_imgs if img]
        player_angle = 0

        enemies = []
        for _ in range(enemy_count):
            while True:
                r, c = random.randint(ROWS//2, ROWS-2), random.randint(COLS//2, COLS-2)
                if maze[r][c] == 0:
                    enemy_img = random.choice(enemy_imgs) if enemy_imgs else None
                    enemies.append({"x": c*TILE_SIZE,"y": r*TILE_SIZE,"path": [],"disabled": False,"timer": 0,"path_timer": 0,"img": enemy_img})
                    break

        items = []
        while True:
            r, c = random.randint(1, 3), random.randint(1, 3)
            if maze[r][c] == 0:
                items.append((r, c))
                break
        for _ in range(item_count - 1):
            while True:
                r, c = random.randint(1, ROWS-2), random.randint(1, COLS-2)
                if maze[r][c] == 0 and (r, c) not in [(1,1), (exit_row, exit_col)] + items:
                    items.append((r, c))
                    break

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


        start_time = time.time()
        # ---------------- 메인 게임 루프 ----------------
        while running:
            t += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    if moving_channel:
                        moving_channel.stop()
                    return run_pygame(difficulty=None)

            keys = pygame.key.get_pressed()
            moving = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]

            if keys[pygame.K_LEFT]: player_vx -= player_accel
            if keys[pygame.K_RIGHT]: player_vx += player_accel
            if keys[pygame.K_UP]: player_vy -= player_accel
            if keys[pygame.K_DOWN]: player_vy += player_accel

            move_dir_x = 0; move_dir_y = 0
            if keys[pygame.K_LEFT]: move_dir_x = -1
            elif keys[pygame.K_RIGHT]: move_dir_x = 1
            if keys[pygame.K_UP]: move_dir_y = -1
            elif keys[pygame.K_DOWN]: move_dir_y = 1
            if move_dir_x != 0 or move_dir_y != 0:
                player_angle = -math.degrees(math.atan2(move_dir_y, move_dir_x))

            player_vx *= 0.9; player_vy *= 0.9
            player_vx = max(-player_max_speed, min(player_max_speed, player_vx))
            player_vy = max(-player_max_speed, min(player_max_speed, player_vy))

            new_x, new_y = player_x + player_vx, player_y + player_vy

            if rect_can_move(new_x, player_y):
                player_x = new_x
            else:
                player_vx = 0
                if wall_hit_sound: wall_hit_sound.play()
            if rect_can_move(player_x, new_y):
                player_y = new_y
            else:
                player_vy = 0
                if wall_hit_sound: wall_hit_sound.play()

            # ---------------- 움직임 사운드 ----------------
            if moving and moving_channel and not moving_channel.get_busy():
                moving_channel.play(moving_sound)
            elif not moving and moving_channel:
                moving_channel.stop()

            player_row, player_col = int(player_y // TILE_SIZE), int(player_x // TILE_SIZE)

            for item in items[:]:
                if (player_row, player_col) == item:
                    items.remove(item)
                    if item_pickup_sound:
                        ch = pygame.mixer.find_channel()
                        if ch:  
                            ch.play(item_pickup_sound)
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
                    color = (0,0,0) if maze[r][c]==1 else (70,70,70)
                    pygame.draw.rect(screen, color, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))

            for (r,c) in items:
                pygame.draw.rect(screen, (255,255,100), (c*TILE_SIZE+TILE_SIZE//4, r*TILE_SIZE+TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2))

            pygame.draw.rect(screen, (50,255,100), (exit_col*TILE_SIZE, exit_row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

            for e in enemies:
                if e["img"]:
                    img = e["img"].copy()
                    if e["disabled"]: img.set_alpha(100)
                    screen.blit(img, (e["x"], e["y"]))
                else:
                    color = (100,100,100) if e["disabled"] else (255,50,255)
                    pygame.draw.rect(screen, color, (e["x"], e["y"], TILE_SIZE, TILE_SIZE))

            if player_img:
                rotated_img = pygame.transform.rotate(player_img, player_angle)
                rect = rotated_img.get_rect(center=(player_x + TILE_SIZE/2, player_y + TILE_SIZE/2))
                screen.blit(rotated_img, rect.topleft)
            else:
                pygame.draw.rect(screen, (0,255,255), (player_x, player_y, TILE_SIZE, TILE_SIZE))

            elapsed = time.time() - start_time
            time_text = font_small.render(f"TIME: {elapsed:.2f}s", True, (255,255,255))
            screen.blit(time_text, (SCREEN_WIDTH - 300, 10))

            hud = font_small.render(f"ITEMS LEFT: {len(items)}", True, (255,255,255))
            screen.blit(hud, (10,10))
            pygame.display.flip()
            clock.tick(60)

        # ---------------- 게임 종료 화면 ----------------
        pygame.mixer.music.stop()
        if moving_channel:
            moving_channel.stop()

        # 종료 직전 기록 저장
        elapsed = time.time() - start_time  # 마지막 시간 계산
        if won:
            save_ranking(elapsed, difficulty=difficulty)

        # 승리/패배 사운드
        victory_sound_played = False
        defeat_sound_played = False
        while True:
            screen.fill((0, 0, 0))
            msg = "VICTORY!" if won else "DEFEAT!"
            text = font_large.render(msg, True, (50,255,50) if won else (255,80,80))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150))


            ranking_file = f"ranking_{difficulty}.txt"
            try:
                with open(ranking_file, "r") as f:
                    times = [float(line.strip()) for line in f.readlines()]
            except FileNotFoundError:
                times = []
            if times:
                screen.blit(font_small.render("RANKING:", True, (255,255,255)), (SCREEN_WIDTH - 350, 300))
                for i, t in enumerate(times):
                    text_r = font_small.render(f"{i+1}. {t:.2f}s", True, (255,255,0))
                    screen.blit(text_r, (SCREEN_WIDTH - 350, 330 + i*25))

            # 버튼 표시
            main_btn = pygame.Rect(50, 300, 300, 60)
            retry_btn = pygame.Rect(50, 380, 300, 60)
            quit_btn = pygame.Rect(50, 460, 300, 60)
            draw_button(screen, main_btn, "MAIN", font_small, (50,50,200), (255,255,255))
            draw_button(screen, retry_btn, "TRY AGAIN", font_small, (50,200,50), (255,255,255))
            draw_button(screen, quit_btn, "QUIT", font_small, (200,50,50), (255,255,255))
            pygame.display.flip()

            if won and not victory_sound_played and victory_sound:
                pygame.mixer.Channel(6).play(victory_sound)
                victory_sound_played = True
            elif not won and not defeat_sound_played and defeat_sound:
                pygame.mixer.Channel(7).play(defeat_sound)
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
            break

if __name__ == "__main__":
    run_pygame()
