import pygame
import sys

def run_pygame():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("미로 찾기")

    clock = pygame.time.Clock()

    # 미로 (0=길, 1=벽)
    maze = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,0,1,0,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,0,1,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,1],
        [1,1,1,1,1,0,1,1,1,1,0,1,0,1,0,1],
        [1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,1],
        [1,0,1,0,1,1,1,1,0,1,1,1,1,1,0,1],
        [1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

    TILE_SIZE = 40
    WALL_COLOR = (50, 50, 150)
    PATH_COLOR = (200, 200, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 배경 색 칠하기
        screen.fill((0, 0, 0))

        # 미로 그리기
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                if maze[row][col] == 1:
                    pygame.draw.rect(screen, WALL_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(screen, PATH_COLOR, (x, y, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_pygame()