import pygame as pg
import sys
from colors import *
from fonts import *
from button import Button

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Connect Four")

# Game States
MENU = 0
DIFFICULTY = 1
PLAYING = 2

game_state = MENU
game_mode = None
difficulty = None

# For positioning
screen_width = screen.get_rect().width
screen_height = screen.get_rect().height
# Create Buttons
pvp_button = Button(si_game=type('', (), {'screen': screen})(), msg="Player vs Player", pos=(screen_width * 0.5, screen_height * 0.35))
pvai_button = Button(si_game=type('', (), {'screen': screen})(), msg="Player vs AI", pos=(screen_width * 0.5, screen_height * 0.65))

easy_button = Button(si_game=type('', (), {'screen': screen})(), msg="Easy", pos=(screen_width * 0.5, screen_height * 0.30))
medium_button = Button(si_game=type('', (), {'screen': screen})(), msg="Medium", pos=(screen_width * 0.5, screen_height * 0.50))
hard_button = Button(si_game=type('', (), {'screen': screen})(), msg="Hard", pos=(screen_width * 0.5, screen_height * 0.70))

def draw_board():
    pass

if __name__ == "__main__":
    # Main loop
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if game_state == MENU:
                    if pvp_button.rect.collidepoint(event.pos):
                        game_mode = "PvP"
                        game_state = PLAYING
                    elif pvai_button.rect.collidepoint(event.pos):
                        game_mode = "PvAI"
                        game_state = DIFFICULTY

                elif game_state == DIFFICULTY:
                    if easy_button.rect.collidepoint(event.pos):
                        difficulty = "Easy"
                        game_state = PLAYING
                    elif medium_button.rect.collidepoint(event.pos):
                        difficulty = "Medium"
                        game_state = PLAYING
                    elif hard_button.rect.collidepoint(event.pos):
                        difficulty = "Hard"
                        game_state = PLAYING

                elif game_state == PLAYING:
                    pass

        # Highlighting (hover effect)
        if game_state == MENU:
            pvp_button.set_highlight(mouse_pos)
            pvai_button.set_highlight(mouse_pos)
        elif game_state == DIFFICULTY:
            easy_button.set_highlight(mouse_pos)
            medium_button.set_highlight(mouse_pos)
            hard_button.set_highlight(mouse_pos)

        # Draw everything
        screen.fill(BLACK)
        if game_state == MENU:
            pvp_button.draw()
            pvai_button.draw()
        elif game_state == DIFFICULTY:
            easy_button.draw()
            medium_button.draw()
            hard_button.draw()
        elif game_state == PLAYING:
            pass
            # draw_board()

        pg.display.flip()
