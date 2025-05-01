import pygame as pg
import sys
import os
from colors import *
from fonts import *
from button import Button
from invisible_button import InvisibleButton
from connectFourBase import *

import ctypes
        
class ConnectFourGUI:
    def __init__(self):
        # Initializing PyGame
        pg.init()

        # Setting Screen
        self.screen = pg.display.set_mode((900, 900))

        # Setting Caption
        pg.display.set_caption("Connect Four")

        # Setting Icon
        icon_path = resource_path("assets/icon/connectFourIcon.png")
        icon_surface = pg.image.load(icon_path)
        pg.display.set_icon(icon_surface)


        # For positioning
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height

        # Text
        self.initialize_title()
        self.initialize_title_game()

        # Create Buttons
        self.pvp_button = Button(self, "Player vs Player", (self.screen_width * 0.5, self.screen_height * 0.35))
        self.pvai_button = Button(self, "Player vs AI", (self.screen_width * 0.5, self.screen_height * 0.50))
        self.aivai_button = Button(self, "AI vs AI", (self.screen_width * 0.5, self.screen_height * 0.65))

        self.easy_button = Button(self, "Easy", (self.screen_width * 0.5, self.screen_height * 0.35))
        self.medium_button = Button(self, "Medium", (self.screen_width * 0.5, self.screen_height * 0.50))
        self.hard_button = Button(self, "Hard", (self.screen_width * 0.5, self.screen_height * 0.65))

        self.cheat_button = Button(self, "Cheat", (self.screen_width * 0.3, self.screen_height * 0.9))

        self.menu_button = Button(self, "Menu", (self.screen_width * 0.5, self.screen_height * 0.9))
        self.reset_button = Button(self, "Reset", (self.screen_width * 0.7, self.screen_height * 0.9))
        self.exit_button = Button(self, "Exit", (self.screen_width * 0.5, self.screen_height * 0.9))

        self.connectFour = ConnectFourBase(game = self)
        
        # Moves
        self.selected_move = None

        # Triggers
        self.setup_invisible_buttons()

    def initialize_title(self):
        self.font_title = pg.font.Font(PIXEL, 70)
        self.title_connect = self.font_title.render(f"CONNECT", True, ORANGE)
        self.title_four = self.font_title.render(f" FOUR", True, BLUE)

        # Find offset
        difference = self.title_four.get_width() - self.title_connect.get_width()

        # Vertical Position
        y_pos = self.screen_height * 0.15

        self.connectRect = self.title_connect.get_rect()
        self.connectRect.midright = ((self.screen_width / 2) - (difference / 2), y_pos)

        self.fourRect = self.title_four.get_rect()
        self.fourRect.midleft = ((self.screen_width / 2) - (difference / 2), y_pos)

    def draw_title(self):
        self.screen.blit(self.title_connect, self.connectRect)
        self.screen.blit(self.title_four, self.fourRect)

    def initialize_title_game(self):
        self.font_game = pg.font.Font(PIXEL, 50)
        self.title_in = self.font_game.render(f"MATCH IN ", True, YELLOW)
        self.title_progress = self.font_game.render(f"PROGRESS", True, RED)

        # Find offset
        difference = self.title_progress.get_width() - self.title_in.get_width()
        y_pos = self.screen_height * 0.10

        self.inRect = self.title_in.get_rect()
        self.inRect.midright = ((self.screen_width / 2) - (difference / 2), y_pos)

        self.progressRect = self.title_progress.get_rect()
        self.progressRect.midleft = ((self.screen_width / 2) - (difference / 2), y_pos)

    def draw_title_game(self):
        self.screen.blit(self.title_in, self.inRect)
        self.screen.blit(self.title_progress, self.progressRect)

    def prep_winner_text(self):
        declaration = ""
        color = BLACK
        
        if self.connectFour.match_result > 0:
            declaration, color = "RED IS THE WINNER!", RED
        elif self.connectFour.match_result < 0:
            declaration, color = "YELLOW IS THE WINNER!", YELLOW
        else:
            declaration, color = "EVERYONE IS A LOSER!", ORANGE

        self.title_winner = self.font_game.render(f"{declaration}", True, color)

        y_pos = self.screen_height * 0.10

        self.winnerRect = self.title_winner.get_rect()
        self.winnerRect.center = ((self.screen_width / 2), y_pos)

    def draw_winner_text(self):
        self.screen.blit(self.title_winner, self.winnerRect)

    def initialize_ai_assistant_text(self):
        font_ai = pg.font.Font(PIXEL, 35)

        self.titan_text = font_ai.render("Titan", True, BLUE)
        self.ai_text = font_ai.render("AI:  ", True, ORANGE)

        x_pos = self.screen_width * 0.01
        y_pos = self.screen_height * 0.20

        self.titanRect = self.titan_text.get_rect()
        self.aiRect = self.ai_text.get_rect()

        self.titanRect.midleft = (x_pos, y_pos)
        self.aiRect.midleft = (x_pos + self.titan_text.get_width(), y_pos)

    def draw_ai_assistant_text(self):
        self.screen.blit(self.titan_text, self.titanRect)
        self.screen.blit(self.ai_text, self.aiRect)

    def initialize_cheat_text(self):
        self.display_cheat = False
        self.has_prepped_cheat = False
        self.has_displayed_process = False
        self.prep_cheat_text()

    def prep_cheat_text(self, declaration = "Cheat!", color = ORANGE):
        font_cheat = pg.font.Font(PIXEL, 35)

        self.cheat_text = font_cheat.render(f"{declaration}", True, color)
        self.cheatRect = self.cheat_text.get_rect()

        x_pos = self.screen_width * 0.01 + self.titanRect.width + self.aiRect.width
        y_pos = self.screen_height * 0.20

        self.cheatRect.midleft = (x_pos, y_pos)

    def draw_cheat_text(self):
        self.screen.blit(self.cheat_text, self.cheatRect)

    def update_cheat_text(self):
        if not self.has_prepped_cheat and self.display_cheat:
            if self.connectFour.game_modes[self.connectFour.mode_index] == "AI vs AI":
                self.prep_cheat_text(f"You're not even playing!")
                self.has_prepped_cheat = True
            elif self.connectFour.game_states[self.connectFour.state_index] == "GAME OVER":
                self.prep_cheat_text(f"You already lost, LOSER!")
                self.has_prepped_cheat = True
            elif self.connectFour.game_states[self.connectFour.state_index] == "PLAYING":
                if not self.has_displayed_process:
                    self.prep_cheat_text(f"Processing. . .", BLUE)
                    self.has_displayed_process = True
                elif self.has_displayed_process:
                    optimal = ai_helper(self.connectFour, self.connectFour.state)
                    self.prep_cheat_text(f"Column: {optimal[1]}")
                    self.has_prepped_cheat = True
        
        # if self.display_cheat:
        self.draw_cheat_text()

    def prep_probability_text(self):
        font_p = pg.font.Font(PIXEL, 35)

        # Formatting
        probability = 1.0
        percent = f"{int(round(probability * 100)):>3d}%"

        # Vertical Spacing
        vertical_spacer = font_p.render(" ", True, BLUE).get_rect().height

        self.victory_colors = [RED, YELLOW]

        self.percent_colors_thresholds = [
            (0.8, MAGENTA),
            (0.6, CYAN),
            (0.4, GREEN),
            (0.2, YELLOW),
            (0.0, RED)]

        self.chance_text = font_p.render("Chance", True, ORANGE)
        self.of_text = font_p.render("Of", True, BLUE)
        self.victory_text = font_p.render("Victory", True, ORANGE)
        self.percent_text = font_p.render(f"{percent}", True, GREEN)

        x_pos = self.screen_width * 0.10
        y_pos = self.screen_height * 0.27

        self.chanceRect = self.chance_text.get_rect()
        self.ofRect = self.of_text.get_rect()
        self.victoryRect = self.victory_text.get_rect()
        self.percentRect = self.percent_text.get_rect()
        

        self.chanceRect.center = (x_pos, y_pos)
        self.ofRect.center = (x_pos, y_pos + vertical_spacer)
        self.victoryRect.center = (x_pos, y_pos + 2*vertical_spacer)
        self.percentRect.center = (x_pos, y_pos + 3*vertical_spacer)
    
    def draw_probability_text(self):
        self.screen.blit(self.chance_text, self.chanceRect)
        self.screen.blit(self.of_text, self.ofRect)
        self.screen.blit(self.victory_text, self.victoryRect)
        self.screen.blit(self.percent_text, self.percentRect)

    def update_probability_text(self):
        font_p = pg.font.Font(PIXEL, 35)

        probability = self.connectFour.victory_probability

        for threshold, color in self.percent_colors_thresholds:
            if probability >= threshold:
                percent_color = color
                break

        percent = f"{int(round(probability * 100)):>3d}%"
        self.percent_text = font_p.render(f"{percent}", True, percent_color)
        
        victory_color = self.victory_colors[0 if self.connectFour.current_player_index == 0 else 1]
        self.victory_text = font_p.render("Victory", True, victory_color)

        self.draw_probability_text()

    def draw_board(self):
        SQUARESIZE = 80  # Size of each square
        RADIUS = SQUARESIZE // 2 - 5  # Size of the pieces
        
        NUM_COLUMNS = 7
        NUM_ROWS = 6
        
        # Calculate centering
        board_width = NUM_COLUMNS * SQUARESIZE
        board_start_x = (self.screen_width - board_width) // 2
        
        # Draw the background and empty circles
        for c in range(NUM_COLUMNS):
            for r in range(NUM_ROWS):
                rect_x = board_start_x + c * SQUARESIZE
                rect_y = r * SQUARESIZE + 3*SQUARESIZE # Offset vertically
                pg.draw.rect(self.screen, BLUE, (rect_x, rect_y, SQUARESIZE, SQUARESIZE))
                
                circle_x = rect_x + SQUARESIZE // 2
                circle_y = rect_y + SQUARESIZE // 2
                pg.draw.circle(self.screen, BLACK, (circle_x, circle_y), RADIUS)

        # Draw the pieces based on current state
        for (row, col), player in self.connectFour.state.board.items():
            if player == 'X':
                color = RED  # Red for Player 1 (X)
            else:
                color = YELLOW  # Yellow for Player 2 (O)
            
            piece_x = board_start_x + (col - 1) * SQUARESIZE + SQUARESIZE // 2
            piece_y = (row - 1) * SQUARESIZE + 3*SQUARESIZE + SQUARESIZE // 2   # DONT FORGET THE OFFSET
            pg.draw.circle(self.screen, color, (piece_x, piece_y), RADIUS)

    def setup_invisible_buttons(self):
        SQUARESIZE = 80
        NUM_COLUMNS = 7
        NUM_ROWS = 6
        self.invisible_buttons = []
        
        board_width = NUM_COLUMNS * SQUARESIZE
        board_start_x = (self.screen_width - board_width) // 2

        for c in range(NUM_COLUMNS):
            x = board_start_x + c * SQUARESIZE
            y = 3*SQUARESIZE  # Same vertical offset as draw_board
            width = SQUARESIZE
            height = SQUARESIZE * NUM_ROWS  # Covers all rows
            button = InvisibleButton(x, y, width, height)
            self.invisible_buttons.append(button)

    def update(self):
        # After event handling (OUTSIDE event for-loop! Every frame):
        if self.connectFour.game_states[self.connectFour.state_index] == "PLAYING":
            if not self.connectFour.game_over:
                self.connectFour.play_turn()
            elif self.connectFour.game_over:
                self.to_game_over()
    
    def check_exit_button(self, event):
        if self.exit_button.rect.collidepoint(event.pos):
            pg.quit()
            sys.exit()

    def check_pvp_button(self, event):
        if self.pvp_button.rect.collidepoint(event.pos):
            self.connectFour.mode_index = 1          # PvP
            self.connectFour.difficulty_index = 0    # N/A Difficulty

            self.to_play_game()

    def check_pvai_button(self, event):
        if self.pvai_button.rect.collidepoint(event.pos):
            self.connectFour.mode_index = 2          # PvAI
            
            self.to_difficulty_select()

    def check_aivai_button(self, event):
        if self.aivai_button.rect.collidepoint(event.pos):
            self.connectFour.mode_index = 3          # AIvAI
            
            self.to_difficulty_select()

    def check_easy_button(self, event):
        if self.easy_button.rect.collidepoint(event.pos):
            self.connectFour.difficulty_index = 1    # Easy Difficulty
            self.to_play_game()

    def check_medium_button(self, event):
        if self.medium_button.rect.collidepoint(event.pos):
            self.connectFour.difficulty_index = 2    # Medium Difficulty
            
            self.to_play_game()

    def check_hard_button(self, event):
        if self.hard_button.rect.collidepoint(event.pos):
            self.connectFour.difficulty_index = 3    # Hard Difficulty
            
            self.to_play_game()

    def check_menu_button(self,event):
        if self.menu_button.rect.collidepoint(event.pos):
            self.to_mode_select()

    def check_reset_button(self, event):
        if self.reset_button.rect.collidepoint(event.pos):
            self.to_play_game()

    def check_cheat_button(self, event):
        if self.cheat_button.rect.collidepoint(event.pos):
            self.has_prepped_cheat = False
            self.has_displayed_process = False
            self.display_cheat = True

    def check_invisible_buttons(self, event):
        # Check if any invisible button is clicked (column selection)
        for i, button in enumerate(self.invisible_buttons):
            if button.is_clicked(event.pos):
                self.connectFour.gui.selected_move = i + 1  # Store the selected column (1-indexed)
                self.display_cheat = False  # Move has been made. Cheat is now obsolete
                self.has_displayed_process = False
                self.prep_cheat_text()      # Resetting to default
                # print(i + 1)
                break  # Exit loop after the first valid click
    
    # Code for transitioning to states
    def to_mode_select(self):
        self.connectFour.state_index = 0        # Mode Select
        self.connectFour.mode_index = 0         # N/A Mode
        self.connectFour.difficulty_index = 0   # N/A Difficulty

    def to_play_game(self):
        self.initialize_ai_assistant_text()
        self.initialize_cheat_text()
        self.prep_probability_text()

        self.connectFour.state_index = 2         # State = Playing
        self.connectFour.start_game()

    def to_difficulty_select(self):
        self.connectFour.state_index = 1         # State = Difficulty Select

    def to_game_over(self):
        self.prep_winner_text()
        self.initialize_ai_assistant_text()
        self.initialize_cheat_text()
        self.prep_probability_text()

        self.connectFour.state_index = 3

    def run(self):
        # Main loop
        while True:
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and event.button in (1, 2, 3):
                    if self.connectFour.game_states[self.connectFour.state_index] == "MODE_SELECT":
                        self.check_exit_button(event)
                        self.check_pvp_button(event)
                        self.check_pvai_button(event)
                        self.check_aivai_button(event)

                    elif self.connectFour.game_states[self.connectFour.state_index] == "DIFFICULTY_SELECT":
                        self.check_easy_button(event)
                        self.check_medium_button(event)
                        self.check_hard_button(event)

                        self.check_menu_button(event)
                    
                    elif self.connectFour.game_states[self.connectFour.state_index] == "PLAYING":
                        self.check_invisible_buttons(event)

                        self.check_menu_button(event)
                        self.check_reset_button(event)
                        self.check_cheat_button(event)
                    
                    elif self.connectFour.game_states[self.connectFour.state_index] == "GAME OVER":
                        self.check_menu_button(event)
                        self.check_reset_button(event)
                        self.check_cheat_button(event)

            # Highlighting (hover effect)
            if self.connectFour.game_states[self.connectFour.state_index] == "MODE_SELECT":
                self.pvp_button.set_highlight(mouse_pos)
                self.pvai_button.set_highlight(mouse_pos)
                self.aivai_button.set_highlight(mouse_pos)
                self.exit_button.set_highlight(mouse_pos)

            elif self.connectFour.game_states[self.connectFour.state_index] == "DIFFICULTY_SELECT":
                self.easy_button.set_highlight(mouse_pos)
                self.medium_button.set_highlight(mouse_pos)
                self.hard_button.set_highlight(mouse_pos)
                self.menu_button.set_highlight(mouse_pos)

            elif self.connectFour.game_states[self.connectFour.state_index] == "PLAYING":
                self.menu_button.set_highlight(mouse_pos)
                self.reset_button.set_highlight(mouse_pos)
                self.cheat_button.set_highlight(mouse_pos)

            elif self.connectFour.game_states[self.connectFour.state_index] == "GAME OVER":
                self.menu_button.set_highlight(mouse_pos)
                self.reset_button.set_highlight(mouse_pos)
                self.cheat_button.set_highlight(mouse_pos)

            # Update and Draw
            self.screen.fill(BLACK)
            if self.connectFour.game_states[self.connectFour.state_index] == "MODE_SELECT":
                self.draw_title()
                
                self.pvp_button.draw()
                self.pvai_button.draw()
                self.aivai_button.draw()
                self.exit_button.draw()

            elif self.connectFour.game_states[self.connectFour.state_index] == "DIFFICULTY_SELECT":
                self.easy_button.draw()
                self.medium_button.draw()
                self.hard_button.draw()
                self.menu_button.draw()

            elif self.connectFour.game_states[self.connectFour.state_index] == "PLAYING":
                self.update()
                self.draw_title_game()
                self.draw_board()
                self.menu_button.draw()
                self.reset_button.draw()
                
                self.draw_ai_assistant_text()
                self.cheat_button.draw()
                self.update_cheat_text()
                self.update_probability_text()

            elif self.connectFour.game_states[self.connectFour.state_index] == "GAME OVER":
                self.draw_winner_text()
                self.draw_board()
                self.menu_button.draw()
                self.reset_button.draw()

                self.draw_ai_assistant_text()
                self.cheat_button.draw()
                self.update_cheat_text()
                self.update_probability_text()
        
            pg.display.flip()

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# This is to ensure Windows does not mess with the display.
def windows_bugger_off():
    # If Windows:
    if os.name == "nt":
        try:
            # Tell Windows to bugger off.
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            # Do nothing
            pass

def main():
    windows_bugger_off()
    connectFour = ConnectFourGUI()
    connectFour.run()
    

if __name__ == "__main__":
    main()