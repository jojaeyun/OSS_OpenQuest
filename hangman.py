import pygame
import random
import hangman_words

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("행맨 게임")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 150, 0)

FONT_PATH = "PressStart2P-Regular.ttf"   # 프로젝트 폴더/fonts/arcade.ttf

font_title = pygame.font.Font(FONT_PATH, 60)
font_wrong = pygame.font.Font(FONT_PATH, 18)
font_word = pygame.font.Font(FONT_PATH, 25)
font_use = pygame.font.Font(FONT_PATH, 20)
font_success = pygame.font.Font(FONT_PATH, 40)
font_fail = pygame.font.Font(FONT_PATH, 50)
font_fail_word = pygame.font.Font(FONT_PATH, 25)

def draw_hangman(stage):
    if stage >= 0:
        pygame.draw.line(screen, WHITE, (70, 500), (210, 500), 5)
        pygame.draw.line(screen, WHITE, (140, 500), (140, 150), 5)
        pygame.draw.line(screen, WHITE, (140, 150), (270, 150), 5)
        pygame.draw.line(screen, WHITE, (270, 150), (270, 200), 5)
    if stage >= 1:
        pygame.draw.circle(screen, WHITE, (270, 230), 30, 4)
    if stage >= 2:
        pygame.draw.line(screen, WHITE, (270, 260), (270, 350), 4)
    if stage >= 3:
        pygame.draw.line(screen, WHITE, (270, 260), (230, 320), 4)
    if stage >= 4:
        pygame.draw.line(screen, WHITE, (270, 260), (310, 320), 4)
    if stage >= 5:
        pygame.draw.line(screen, WHITE, (270, 350), (240, 420), 4)
    if stage >= 6:
        pygame.draw.line(screen, WHITE, (270, 350), (300, 420), 4)

def draw_word(word, guessed):
    display_text = " ".join([ch if ch in guessed else "_" for ch in word])
    text = font_word.render(display_text, True, WHITE)
    rect = text.get_rect(center=(580, 480))
    screen.blit(text, rect)

def draw_guessed(guessed):
    text = font_use.render("Using: " + " ".join(sorted(guessed)), True, (100, 100, 100))
    screen.blit(text, (60, 530))

def main():
    running = True
    clock = pygame.time.Clock()
    word = random.choice(hangman_words.word_list)
    guessed = []    # 입력한 알파벳들
    wrong = 0
    MAX_TRIES = 6
    win = False
    lose = False

    while running:
        screen.fill(BLACK)

        title = font_title.render("HANGMAN", True, WHITE)
        rect = title.get_rect(center=(WIDTH//2, 70))
        screen.blit(title, rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not win and not lose:
                if event.unicode.isalpha():
                    letter = event.unicode.lower()
                    if letter not in guessed:
                        guessed.append(letter)
                        if letter not in word:
                            wrong += 1
                        # 남은 알파벳이 없으면 성공
                        if all(ch in guessed for ch in word):
                            win = True
                        # 기회 소진 시 실패
                        elif wrong >= MAX_TRIES:
                            lose = True

        # 그림, 단어, 입력 표시
        draw_hangman(wrong)
        draw_word(word, guessed)
        draw_guessed(guessed)

        info_text = font_wrong.render(
            f"Wrong Count: {wrong} / 6", True, (100, 100, 100)
        )
        screen.blit(info_text, (420, 150))

        if(win==True):
            success = font_success.render("Succeed!", True, GREEN)
            rect = success.get_rect(center=(580, 300))
            screen.blit(success, rect)
        
        if(lose==True):
            fail = font_fail.render("Fail!", True, RED)
            screen.blit(fail, (470, 250))
            fail_word = font_fail_word.render(f"word: {word}", True, RED)
            rect = fail_word.get_rect(center=(580, 350))
            screen.blit(fail_word, rect)

        pygame.display.flip()
        clock.tick(30)
            
    pygame.quit()

main()