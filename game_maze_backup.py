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

    # 플레이어 초기 위치
    player_row, player_col = 1, 1
    player_x, player_y = player_col * TILE_SIZE, player_row * TILE_SIZE
    player_speed = 4

    # 출구
    exit_row, exit_col = ROWS - 2, COLS - 2
    maze[exit_row][exit_col] = 0

    # 적: 플레이어 반대쪽
    enemy_row, enemy_col = ROWS - 2, COLS - 2
    enemy_x, enemy_y = enemy_col * TILE_SIZE, enemy_row * TILE_SIZE
    enemy_speed = 2

    # 아이템 여러 개 배치
    items = []
    for _ in range(10):
        while True:
            r, c = random.randint(1, ROWS - 2), random.randint(1, COLS - 2)
            if maze[r][c] == 0 and (r, c) not in [(player_row, player_col), (exit_row, exit_col)]:
                items.append((r, c))
                break

    # 적 무력화 관련
    enemy_disabled = False
    disable_timer = 0
    disable_duration = 180  # 3초

    path_to_player = []
    path_timer = 0  # BFS 업데이트 타이머

    running = True
    won = False

    def can_move(x, y):
        col = int(x // TILE_SIZE)
        row = int(y // TILE_SIZE)
        if 0 <= row < ROWS and 0 <= col < COLS:
            return maze[row][col] == 0
        return False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -player_speed
        if keys[pygame.K_RIGHT]: dx = player_speed
        if keys[pygame.K_UP]: dy = -player_speed
        if keys[pygame.K_DOWN]: dy = player_speed

        # 플레이어 이동
        new_x, new_y = player_x + dx, player_y + dy
        if can_move(new_x, player_y): player_x = new_x
        if can_move(player_x, new_y): player_y = new_y

        player_row, player_col = int(player_y // TILE_SIZE), int(player_x // TILE_SIZE)

        # 아이템 획득 → 적 무력화
        for item in items[:]:
            if (player_row, player_col) == item:
                items.remove(item)
                enemy_disabled = True
                disable_timer = disable_duration

        # 적 이동
        if not enemy_disabled:
            path_timer += 1
            if path_timer % 20 == 0:  # 20프레임마다 BFS 갱신 (성능 절약)
                path_to_player = find_path(maze, (int(enemy_y // TILE_SIZE), int(enemy_x // TILE_SIZE)),
                                           (player_row, player_col))

            if path_to_player:
                next_cell = path_to_player[0]
                next_x, next_y = next_cell[1] * TILE_SIZE, next_cell[0] * TILE_SIZE
                dir_x = next_x - enemy_x
                dir_y = next_y - enemy_y
                dist = max(1, (dir_x ** 2 + dir_y ** 2) ** 0.5)
                step_x = enemy_speed * dir_x / dist
                step_y = enemy_speed * dir_y / dist

                enemy_x += step_x
                enemy_y += step_y

                # 목표 칸 도착 시 다음 칸으로
                if abs(enemy_x - next_x) < 2 and abs(enemy_y - next_y) < 2:
                    path_to_player.pop(0)
        else:
            disable_timer -= 1
            if disable_timer <= 0:
                enemy_disabled = False

        enemy_row, enemy_col = int(enemy_y // TILE_SIZE), int(enemy_x // TILE_SIZE)

        # 충돌 판정
        if (player_row, player_col) == (exit_row, exit_col):
            won = True
            running = False
        elif not enemy_disabled and abs(player_row - enemy_row) < 1 and abs(player_col - enemy_col) < 1:
            won = False
            running = False

        # 화면 렌더링
        screen.fill((0, 0, 0))
        for r in range(ROWS):
            for c in range(COLS):
                color = WALL_COLOR if maze[r][c] == 1 else PATH_COLOR
                pygame.draw.rect(screen, color, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # 아이템
        for (r, c) in items:
            pygame.draw.rect(screen, ITEM_COLOR, (c * TILE_SIZE + TILE_SIZE//4, r * TILE_SIZE + TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2))

        # 출구
        pygame.draw.rect(screen, EXIT_COLOR, (exit_col * TILE_SIZE, exit_row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # 적
        color = (150, 150, 150) if enemy_disabled else ENEMY_COLOR
        pygame.draw.rect(screen, color, (enemy_x, enemy_y, TILE_SIZE, TILE_SIZE))

        # 플레이어
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(60)

    # 종료 화면
    font = pygame.font.SysFont(None, 72)
    text = font.render("victory!" if won else "Failed!", True, (255, 255, 0) if won else (255, 50, 50))
    screen.fill((0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_pygame()
