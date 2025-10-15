import pygame
import sys
import random

def generate_maze(rows, cols):
    # 모든 칸을 벽으로 초기화
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve_passages(r, c):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows-1 and 1 <= nc < cols-1 and maze[nr][nc] == 1:
                maze[nr][nc] = 0
                maze[r + dr//2][c + dc//2] = 0  # 중간 벽 제거
                carve_passages(nr, nc)

    start_r, start_c = 1, 1
    maze[start_r][start_c] = 0
    carve_passages(start_r, start_c)

    return maze

def find_path(maze, start, end):
    """BFS로 최단 경로 찾기"""
    from collections import deque
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set()
    visited.add(start)
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
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr,nc) not in visited:
                visited.add((nr,nc))
                parent[(nr,nc)] = (r,c)
                queue.append((nr,nc))
    return []

def run_pygame():
    pygame.init()

    ROWS, COLS = 21, 31  # 홀수로 해야 랜덤 미로 생성 가능
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
    PATH_HIGHLIGHT = (255, 255, 0, 100)

    clock = pygame.time.Clock()

    # 플레이어 초기 위치
    player_row, player_col = 1, 1
    player_x = player_col * TILE_SIZE
    player_y = player_row * TILE_SIZE
    player_speed = 4

    # 탈출구
    exit_row, exit_col = ROWS-2, COLS-2
    maze[exit_row][exit_col] = 0

    # 자동 경로 표시
    path_cells = find_path(maze, (player_row, player_col), (exit_row, exit_col))

    running = True
    won = False
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

        # 충돌 처리
        def can_move(nx, ny):
            col = nx // TILE_SIZE
            row = ny // TILE_SIZE
            for r in [row, row + (TILE_SIZE-1)//TILE_SIZE]:
                for c in [col, col + (TILE_SIZE-1)//TILE_SIZE]:
                    if maze[r][c] == 1:
                        return False
            return True

        if can_move(player_x + dx, player_y):
            player_x += dx
        if can_move(player_x, player_y + dy):
            player_y += dy

        # 승리 체크
        if player_x // TILE_SIZE == exit_col and player_y // TILE_SIZE == exit_row:
            won = True
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
     
      
        # 플레이어
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(30)

    # 승리 화면
    if won:
        font = pygame.font.SysFont(None, 72)
        text = font.render("승리!", True, (255, 255, 0))
        screen.fill((0,0,0))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(3000)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_pygame()