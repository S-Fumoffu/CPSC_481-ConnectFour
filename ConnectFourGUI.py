import pygame as pg
import sys
from colors import *
from fonts import *
from button import Button
from connectFourBase import *

import ctypes
ctypes.windll.user32.SetProcessDPIAware()
class ConnectFourGUI:
    def __init__(self):
        
        pg.init()
        self.screen = pg.display.set_mode((800, 600))

        pg.display.set_caption("Connect Four")

        # For positioning
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height

        # Create Buttons
        self.pvp_button = Button(self, "Player vs Player", (self.screen_width * 0.5, self.screen_height * 0.35))
        self.pvai_button = Button(self, "Player vs AI", (self.screen_width * 0.5, self.screen_height * 0.65))

        self.easy_button = Button(self, "Easy", (self.screen_width * 0.5, self.screen_height * 0.30))
        self.medium_button = Button(self, "Medium", (self.screen_width * 0.5, self.screen_height * 0.50))
        self.hard_button = Button(self, "Hard", (self.screen_width * 0.5, self.screen_height * 0.70))

        self.connectFour = ConnectFourPygame()

    def draw_board():
        pass

    def run(self):
        # Main loop
        while True:
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.connectFour.game_states[self.connectFour.state_index] == "MODE_SELECT":
                        if self.pvp_button.rect.collidepoint(event.pos):

                            self.connectFour.mode_index = 1          # PvP
                            self.connectFour.difficulty_index = 0    # N/A Difficulty

                            self.connectFour.state_index = 2         # State = Playing

                        elif self.pvai_button.rect.collidepoint(event.pos):
                            self.connectFour.mode_index = 2          # PvAI
                            self.connectFour.state_index = 1         # State = Difficulty Select

                    elif self.connectFour.game_states[self.connectFour.state_index] == "DIFFICULTY_SELECT":
                        if self.easy_button.rect.collidepoint(event.pos):
                            self.connectFour.difficulty_index = 1    # Easy Difficulty
                            self.connectFour.state_index = 2         # State = Playing

                        elif self.medium_button.rect.collidepoint(event.pos):
                            self.connectFour.difficulty_index = 2    # Medium Difficulty
                            self.connectFour.state_index = 2         # State = Playing

                        elif self.hard_button.rect.collidepoint(event.pos):
                            self.connectFour.difficulty_index = 3    # Hard Difficulty
                            self.connectFour.state_index = 2         # State = Playing

                    elif self.connectFour.game_states[self.connectFour.state_index] == "PLAYING":
                        pass

            # Highlighting (hover effect)
            if self.connectFour.game_states[self.connectFour.state_index] == "MODE_SELECT":
                self.pvp_button.set_highlight(mouse_pos)
                self.pvai_button.set_highlight(mouse_pos)
            elif self.connectFour.game_states[self.connectFour.state_index] == "DIFFICULTY_SELECT":
                self.easy_button.set_highlight(mouse_pos)
                self.medium_button.set_highlight(mouse_pos)
                self.hard_button.set_highlight(mouse_pos)

            # Draw everything
            self.screen.fill(BLACK)
            if self.connectFour.game_states[self.connectFour.state_index] == "MODE_SELECT":
                self.pvp_button.draw()
                self.pvai_button.draw()
            elif self.connectFour.game_states[self.connectFour.state_index] == "DIFFICULTY_SELECT":
                self.easy_button.draw()
                self.medium_button.draw()
                self.hard_button.draw()
            elif self.connectFour.game_states[self.connectFour.state_index] == "PLAYING":
                pass
                # draw_board()
        
            pg.display.flip()

if __name__ == "__main__":
    connectFour = ConnectFourGUI()
    connectFour.run()