import pygame as pg
import sys
from colors import *
from fonts import *
from button import Button
from invisible_button import InvisibleButton
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

        self.connectFour = ConnectFourBase(game = self)
        
        # Moves
        self.selected_move = None

        # Triggers
        self.setup_invisible_buttons()

    def draw_board(self):
        SQUARESIZE = 80  # Size of each square
        RADIUS = SQUARESIZE // 2 - 5  # Size of the pieces
        
        NUM_COLUMNS = 6
        NUM_ROWS = 7
        
        # Calculate centering
        board_width = NUM_COLUMNS * SQUARESIZE
        board_start_x = (self.screen_width - board_width) // 2
        
        # Draw the background and empty circles
        for c in range(NUM_COLUMNS):
            for r in range(NUM_ROWS):
                rect_x = board_start_x + c * SQUARESIZE
                rect_y = r * SQUARESIZE + (SQUARESIZE / 2) # Offset vertically
                pg.draw.rect(self.screen, (0, 0, 255), (rect_x, rect_y, SQUARESIZE, SQUARESIZE))
                
                circle_x = rect_x + SQUARESIZE // 2
                circle_y = rect_y + SQUARESIZE // 2
                pg.draw.circle(self.screen, (0, 0, 0), (circle_x, circle_y), RADIUS)

        # Draw the pieces based on current state
        for (row, col), player in self.connectFour.state.board.items():
            if player == 'X':
                color = (255, 0, 0)  # Red for Player 1 (X)
            else:
                color = (255, 255, 0)  # Yellow for Player 2 (O)
            
            piece_x = board_start_x + (col - 1) * SQUARESIZE + SQUARESIZE // 2
            piece_y = (row - 1) * SQUARESIZE + (SQUARESIZE/2) + SQUARESIZE // 2
            pg.draw.circle(self.screen, color, (piece_x, piece_y), RADIUS)

    def setup_invisible_buttons(self):
        SQUARESIZE = 80
        NUM_COLUMNS = 6
        NUM_ROWS = 7
        self.invisible_buttons = []
        
        board_width = NUM_COLUMNS * SQUARESIZE
        board_start_x = (self.screen_width - board_width) // 2

        for c in range(NUM_COLUMNS):
            x = board_start_x + c * SQUARESIZE
            y = SQUARESIZE / 2  # Same vertical offset as draw_board
            width = SQUARESIZE
            height = SQUARESIZE * NUM_ROWS  # Covers all rows
            button = InvisibleButton(x, y, width, height)
            self.invisible_buttons.append(button)


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
                            self.connectFour.start_game()

                        elif self.pvai_button.rect.collidepoint(event.pos):
                            self.connectFour.mode_index = 2          # PvAI
                            self.connectFour.state_index = 1         # State = Difficulty Select

                    elif self.connectFour.game_states[self.connectFour.state_index] == "DIFFICULTY_SELECT":
                        if self.easy_button.rect.collidepoint(event.pos):
                            self.connectFour.difficulty_index = 1    # Easy Difficulty
                            self.connectFour.state_index = 2         # State = Playing
                            self.connectFour.start_game()

                        elif self.medium_button.rect.collidepoint(event.pos):
                            self.connectFour.difficulty_index = 2    # Medium Difficulty
                            self.connectFour.state_index = 2         # State = Playing
                            self.connectFour.start_game()

                        elif self.hard_button.rect.collidepoint(event.pos):
                            self.connectFour.difficulty_index = 3    # Hard Difficulty
                            self.connectFour.state_index = 2         # State = Playing
                            self.connectFour.start_game()
                    
                    # BUGS MAY BE FOUND HERE
                    elif self.connectFour.game_states[self.connectFour.state_index] == "PLAYING":
                        # Check if any invisible button is clicked (column selection)
                        for i, button in enumerate(self.invisible_buttons):
                            if button.is_clicked(event.pos):
                                self.connectFour.gui.selected_move = i + 1  # Store the selected column (1-indexed)
                                print(i + 1)

                                break  # Exit loop after the first valid click

                        # After event handling (OUTSIDE event for-loop! Every frame):
                        if not self.connectFour.game_over:
                            self.connectFour.play_turn()

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
                self.draw_board()
        
            pg.display.flip()

if __name__ == "__main__":
    connectFour = ConnectFourGUI()
    connectFour.run()