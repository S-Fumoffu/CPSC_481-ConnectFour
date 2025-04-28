import pygame as pg
import sys
from colors import *
from fonts import *
from button import Button
from connectFourText import *

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Connect Four")

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
    connectFour = ConnectFourPygame()
    
    # Main loop
    while True:
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if connectFour.game_states[connectFour.state_index] == "MODE_SELECT":
                    if pvp_button.rect.collidepoint(event.pos):

                        connectFour.mode_index = 1          # PvP
                        connectFour.difficulty_index = 0    # N/A Difficulty

                        connectFour.state_index = 2         # State = Playing

                    elif pvai_button.rect.collidepoint(event.pos):
                        connectFour.mode_index = 2          # PvAI
                        connectFour.state_index = 1         # State = Difficulty Select

                elif connectFour.game_states[connectFour.state_index] == "DIFFICULTY_SELECT":
                    if easy_button.rect.collidepoint(event.pos):
                        connectFour.difficulty_index = 1    # Easy Difficulty
                        connectFour.state_index = 2         # State = Playing

                    elif medium_button.rect.collidepoint(event.pos):
                        connectFour.difficulty_index = 2    # Medium Difficulty
                        connectFour.state_index = 2         # State = Playing

                    elif hard_button.rect.collidepoint(event.pos):
                        connectFour.difficulty_index = 3    # Hard Difficulty
                        connectFour.state_index = 2         # State = Playing

                elif connectFour.game_states[connectFour.state_index] == "PLAYING":
                    pass

        # Highlighting (hover effect)
        if connectFour.game_states[connectFour.state_index] == "MODE_SELECT":
            pvp_button.set_highlight(mouse_pos)
            pvai_button.set_highlight(mouse_pos)
        elif connectFour.game_states[connectFour.state_index] == "DIFFICULTY_SELECT":
            easy_button.set_highlight(mouse_pos)
            medium_button.set_highlight(mouse_pos)
            hard_button.set_highlight(mouse_pos)

        # Draw everything
        screen.fill(BLACK)
        if connectFour.game_states[connectFour.state_index] == "MODE_SELECT":
            pvp_button.draw()
            pvai_button.draw()
        elif connectFour.game_states[connectFour.state_index] == "DIFFICULTY_SELECT":
            easy_button.draw()
            medium_button.draw()
            hard_button.draw()
        elif connectFour.game_states[connectFour.state_index] == "PLAYING":
            pass
            # draw_board()

        pg.display.flip()
