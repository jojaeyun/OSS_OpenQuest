import pygame
import sys
import random
from collections import deque

# ---------------- 미로 생성 ----------------
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve_passages(r, c):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and maze[nr][nc] == 1:
                maze[nr][nc] = 0
                maze[r + dr // 2][c + dc // 2] = 0
                carve_passages(nr, nc)

    maze[1][1] = 0
    carve_passages(1, 1)
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


# ---------------- 게임 실행 ----------------
def run_pygame():
    pygame.init()

    # 🔹 폰트 설정
    FONT_PATH = "PressStart2P-Regular.ttf"
    try:
        font_small = pygame.font.Font(FONT_PATH, 30)
        font_medium = pygame.font.Font(FONT_PATH, 40)
        font_large = pygame.font.Font(FONT_PATH, 60)
    except FileNotFoundError:
        print(f"[경고] 폰트 파일 '{FONT_PATH}'을(를) 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        font_small = pygame.font.SysFont(None, 30)
        font_medium = pygame.font.SysFont(None, 40)
        font_large = pygame.font.SysFont(None, 60)

    ROWS, COLS = 21, 31
    maze = generate_maze(ROWS, COLS)

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    TILE_SIZE = min(SCREEN_WIDTH // COLS, SCREEN_HEIGHT // ROWS)
    screen = pygame.display.set_mode((COLS * TILE_SIZE, ROWS * TILE_SIZE))
    pygame.display.set_caption("랜덤 미로 게임")

    WALL_COLOR = (50, 50, 150)
    PATH_COLOR = (200, 200, 200)
    PLAYER_COLOR = (255, 50, 50)
    EXIT_COLOR = (50, 200, 50)
    ENEMY_COLOR = (200, 50, 200)
    ITEM_COLOR = (255, 255, 0)

    clock = pygame.time.Clock()

    # ---------------- 난이도 선택 ----------------
    choosing = True
    difficulty = None

    while choosing:
        screen.fill((0, 0, 0))
        title = font_large.render("SELECT LEVEL", True, (255, 255, 255))
        easy = font_medium.render("[E] EASY", True, (100, 255, 100))
        normal = font_medium.render("[N] NORMAL", True, (255, 255, 100))
        hard = font_medium.render("[H] HARD", True, (255, 100, 100))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(easy, (SCREEN_WIDTH//2 - easy.get_width()//2, 300))
        screen.blit(normal, (SCREEN_WIDTH//2 - normal.get_width()//2, 380))
        screen.blit(hard, (SCREEN_WIDTH//2 - hard.get_width()//2, 460))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    difficulty = "easy"; choosing = False
                elif event.key == pygame.K_n:
                    difficulty = "normal"; choosing = False
                elif event.key == pygame.K_h:
                    difficulty = "hard"; choosing = False

    # ---------------- 난이도별 설정 ----------------
    if difficulty == "easy":
        enemy_count = 1
        item_count = 10
        enemy_speed = 2
    elif difficulty == "normal":
        enemy_count = 2
        item_count = 7
        enemy_speed = 2.5
    else:
        enemy_count = 3
        item_count = 5
        enemy_speed = 3

    # ---------------- 초기화 ----------------
    player_row, player_col = 1, 1
    player_x, player_y = player_col * TILE_SIZE, player_row * TILE_SIZE
    player_speed = 4

    exit_row, exit_col = ROWS - 2, COLS - 2
    maze[exit_row][exit_col] = 0

    enemies = []
    for _ in range(enemy_count):
        while True:
            r, c = random.randint(ROWS//2, ROWS - 2), random.randint(COLS//2, COLS - 2)
            if maze[r][c] == 0:
                enemies.append({
                    "x": c * TILE_SIZE,
                    "y": r * TILE_SIZE,
                    "path": [],
                    "disabled": False,
                    "disable_timer": 0
                })
                break

    items = []
    for _ in range(item_count):
        while True:
            r, c = random.randint(1, ROWS - 2), random.randint(1, COLS - 2)
            if maze[r][c] == 0 and (r, c) not in [(player_row, player_col), (exit_row, exit_col)]:
                items.append((r, c))
                break

    disable_duration = 180
    path_timer = 0
    running = True
    won = False

    def can_move(x, y):
        col = int(x // TILE_SIZE)
        row = int(y // TILE_SIZE)
        if 0 <= row < ROWS and 0 <= col < COLS:
            return maze[row][col] == 0
        return False

    # ---------------- 게임 루프 ----------------
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -player_speed
        if keys[pygame.K_RIGHT]: dx = player_speed
        if keys[pygame.K_UP]: dy = -player_speed
        if keys[pygame.K_DOWN]: dy = player_speed

        new_x, new_y = player_x + dx, player_y + dy
        if can_move(new_x, player_y): player_x = new_x
        if can_move(player_x, new_y): player_y = new_y
        player_row, player_col = int(player_y // TILE_SIZE), int(player_x // TILE_SIZE)

        # 아이템 획득
        for item in items[:]:
            if (player_row, player_col) == item:
                items.remove(item)
                for e in enemies:
                    e["disabled"] = True
                    e["disable_timer"] = disable_duration

        # 적 이동
        path_timer += 1
        for e in enemies:
            if e["disabled"]:
                e["disable_timer"] -= 1
                if e["disable_timer"] <= 0:
                    e["disabled"] = False
                continue

            if path_timer % 20 == 0:
                e["path"] = find_path(
                    maze,
                    (int(e["y"] // TILE_SIZE), int(e["x"] // TILE_SIZE)),
                    (player_row, player_col)
                )

            if e["path"]:
                next_cell = e["path"][0]
                next_x, next_y = next_cell[1] * TILE_SIZE, next_cell[0] * TILE_SIZE
                dir_x = next_x - e["x"]
                dir_y = next_y - e["y"]
                dist = max(1, (dir_x ** 2 + dir_y ** 2) ** 0.5)
                e["x"] += enemy_speed * dir_x / dist
                e["y"] += enemy_speed * dir_y / dist

                if abs(e["x"] - next_x) < 2 and abs(e["y"] - next_y) < 2:
                    e["path"].pop(0)

        # 충돌 판정
        if (player_row, player_col) == (exit_row, exit_col):
            won = True
            running = False

        for e in enemies:
            enemy_row, enemy_col = int(e["y"] // TILE_SIZE), int(e["x"] // TILE_SIZE)
            if not e["disabled"] and abs(player_row - enemy_row) < 1 and abs(player_col - enemy_col) < 1:
                won = False
                running = False

        # ---------------- 렌더링 ----------------
        screen.fill((0, 0, 0))
        for r in range(ROWS):
            for c in range(COLS):
                color = WALL_COLOR if maze[r][c] == 1 else PATH_COLOR
                pygame.draw.rect(screen, color, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        for (r, c) in items:
            pygame.draw.rect(screen, ITEM_COLOR, (c * TILE_SIZE + TILE_SIZE//4, r * TILE_SIZE + TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2))

        pygame.draw.rect(screen, EXIT_COLOR, (exit_col * TILE_SIZE, exit_row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        for e in enemies:
            color = (150, 150, 150) if e["disabled"] else ENEMY_COLOR
            pygame.draw.rect(screen, color, (e["x"], e["y"], TILE_SIZE, TILE_SIZE))

        pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, TILE_SIZE, TILE_SIZE))

        # 인게임 HUD
        hud_text = font_small.render(f"ITEMS LEFT: {len(items)}", True, (255, 255, 255))
        screen.blit(hud_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # ---------------- 종료 화면 ----------------
    text = font_large.render("VICTORY!" if won else "FAILED!", True, (255, 255, 0) if won else (255, 50, 50))
    screen.fill((0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_pygame()