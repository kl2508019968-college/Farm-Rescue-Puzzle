# main.py
import pygame
import sys
import os
from settings import *
from menu import Menu
from game import Game

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    bgm_path = "assets/bgm.mp3"
    if os.path.exists(bgm_path):
        try:
            pygame.mixer.music.load(bgm_path)
            # -1 bermaksud muzik akan diulang tanpa henti (infinite loop)
            pygame.mixer.music.play(-1)
            # Tetapkan kelantangan (0.0 hingga 1.0) supaya tidak terlalu kuat
            pygame.mixer.music.set_volume(0.3) 
        except Exception as e:
            print(f"Gagal memuatkan BGM: {e}")
    else:
        print("Fail assets/bgm.mp3 tidak dijumpai. Muzik ditiadakan.")

    menu = Menu()
    game = None
    state = "menu"

    running = True
    while running:
        # Menghitung delta-time dengan tepat untuk pengemaskinian masa tahap permainan
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if menu.start_btn.is_clicked(pos):
                        game = Game(lang=menu.lang)
                        state = "game"
                    elif menu.inst_btn.is_clicked(pos):
                        state = "instruction"
                    elif menu.lang_btn.is_clicked(pos):
                        menu.lang = "MY" if menu.lang == "EN" else "EN"
                        menu.refresh_buttons()
                    elif menu.exit_btn.is_clicked(pos):
                        running = False

            elif state == "instruction":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = "menu"

            elif state == "game":
                if game:
                    game.update(event, dt)
                    # Jika menekan SPACEBAR, bot akan digerakkan menyeberang sungai
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game.trigger_boat_movement()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        state = "menu"
                        game = None

        if state == "menu":
            menu.draw_menu(screen)
        elif state == "instruction":
            menu.draw_instructions(screen)
        elif state == "game" and game:
            game.draw(screen)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
