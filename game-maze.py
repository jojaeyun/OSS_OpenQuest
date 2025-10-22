import pygame
import sys
import random
from collections import deque

def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve_passages(r, c):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows-1 and 1 <= nc < cols-1 and maze[nr][nc] == 1:
                maze[nr][nc] = 0
                maze[r + dr//2][c + dc//2] = 0
                carve_passages(nr, nc)

    start_r, start_c = 1, 1
    maze[start_r][start_c] = 0
    carve_passages(start_r, start_c)
    return maze

def find_path(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set([start])
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
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))
    return []

def get_random_empty_cell(maze):
    """빈 칸(0) 중 랜덤 위치 반환"""
    rows, cols = len(maze), len(maze[0])
    while True:
        r, c = random.randint(1, rows-2), random.randint(1, cols-2)
        if maze[r][c] == 0:
            return r, c

def run_pygame():
    pygame.init()

    ROWS, COLS = 21, 31
    maze = generate_maze(ROWS, COLS)

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TILE_SIZE = min(SCREEN_WIDTH // COLS, SCREEN_HEIGHT // ROWS)
    screen = pygame.display.set_mode((COLS*TILE_SIZE, ROWS*TILE_SIZE))
    pygame.display.set_caption("랜덤 미로 게임")

    WALL_COLOR = (50, 50, 150)
    PATH_COLOR = (200, 200, 200)
    PLAYER_COLOR = (255, 50, 50)
    EXIT_COLOR = (50, 200, 50)
    ENEMY_COLOR = (0, 0, 0)
    ITEM_COLOR = (255, 200, 0)

    clock = pygame.time.Clock()

    # 플레이어 초기 위치
    player_row, player_col = 1, 1
    player_x = player_col * TILE_SIZE
    player_y = player_row * TILE_SIZE
    player_speed = 4

    # 탈출구
    exit_row, exit_col = ROWS-2, COLS-2
    maze[exit_row][exit_col] = 0

    # 적 위치
    enemy_row, enemy_col = get_random_empty_cell(maze)
    enemy_timer = 0
    enemy_active = True
    enemy_speed = 0.02  # 느리게 쫓아오게

    # 아이템 위치
    item_row, item_col = get_random_empty_cell(maze)
    item_active = True
    item_effect_duration = 180  # 프레임 단위 (3초 정도)

    running = True
    won = False
    lost = False

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

        def can_move(nx, ny):
            col = nx // TILE_SIZE
            row = ny // TILE_SIZE
            if 0 <= row < ROWS and 0 <= col < COLS:
                return maze[row][col] == 0
            return False

        if can_move(player_x + dx, player_y):
            player_x += dx
        if can_move(player_x, player_y + dy):
            player_y += dy

        player_row = player_y // TILE_SIZE
        player_col = player_x // TILE_SIZE

        # 아이템 획득
        if item_active and (player_row, player_col) == (item_row, item_col):
            item_active = False
            enemy_active = False
            enemy_timer = item_effect_duration

        # 적 추적 로직
        if enemy_active:
            path_to_player = find_path(maze, (enemy_row, enemy_col), (player_row, player_col))
            if path_to_player:
                next_r, next_c = path_to_player[0]
                enemy_row = next_r
                enemy_col = next_c
        else:
            enemy_timer -= 1
            if enemy_timer <= 0:
                enemy_active = True

        # 승리 / 패배 판정
        if (player_row, player_col) == (exit_row, exit_col):
            won = True
            running = False

        if (player_row, player_col) == (enemy_row, enemy_col):
            lost = True
            running = False

        # 그리기
        screen.fill((0,0,0))
        for row in range(ROWS):
            for col in range(COLS):
                x, y = col*TILE_SIZE, row*TILE_SIZE
                color = WALL_COLOR if maze[row][col]==1 else PATH_COLOR
                pygame.draw.rect(screen, color, (x,y,TILE_SIZE,TILE_SIZE))

        # 탈출구
        pygame.draw.rect(screen, EXIT_COLOR, (exit_col*TILE_SIZE, exit_row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # 아이템
        if item_active:
            pygame.draw.rect(screen, ITEM_COLOR, (item_col*TILE_SIZE, item_row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # 적
        if enemy_active:
            pygame.draw.rect(screen, ENEMY_COLOR, (enemy_col*TILE_SIZE, enemy_row*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        else:
            # 비활성화 상태에서는 반투명 표시
            s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            s.fill((0, 0, 0, 100))
            screen.blit(s, (enemy_col*TILE_SIZE, enemy_row*TILE_SIZE))

        # 플레이어
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(10)

    # 결과 화면
    font = pygame.font.SysFont(None, 72)
    if won:
        text = font.render("Victory!", True, (255, 255, 0))
    elif lost:
        text = font.render("Lost!", True, (255, 0, 0))
    else:
        text = font.render("Exit", True, (255, 255, 255))

    screen.fill((0,0,0))
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_pygame()