from games import *
import pygame as pg
# Modified For Pygame
class ConnectFourBase(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, game, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)
        self.gui = game
        
        # Intializing Unique Features
        self.game_states = {    0: "MODE_SELECT",
                                1: "DIFFICULTY_SELECT",
                                2: "PLAYING",
                                3: "GAME OVER"
        }

        self.game_modes = {1: "Player vs Player",
                           2: "Player vs AI",
                           3: "AI vs AI"}
        
        self.ai_difficulties = {0: "N/A",
                                1: "Easy",
                                2: "Medium",
                                3: "Hard"}
        self.state_index = 0
        self.mode_index = 0
        self.difficulty_index = 0

        # Players
        self.player1 = self.player2 = human_player

        # Flags
        self.has_printed_available_moves = False

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if x == self.h or (x + 1 , y ) in state.board]
    
    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial

        self.display(state)

        while True:
            for player in players:

                # For debugging
                # print(state)

                print("Player: ", player)

                move = player(self, state)
                state = self.result(state, move)

                print("Move: ", move)

                self.display(state)

                if self.terminal_test(state):
                    print(state)
                    return self.utility(state, self.to_move(self.initial))

    def start_game(self):
        self.initialize_mode()
        self.state = self.initial
        self.current_players = [self.player1, self.player2]
        
        self.current_player_index = 0
        self.game_over = False
        self.display(self.state)

    def play_turn(self):
        """Plays as many moves as needed until a human input is needed."""
        if self.game_over:
            return

        player = self.current_players[self.current_player_index]
        move = player(self, self.state)  # Human returns None if waiting for input

        if move is None:
            # No move yet (e.g., human needs to click)
            return
        
        # Otherwise, move is valid -> apply it
        self.state = self.result(self.state, move)
        self.display(self.state)
        pg.display.flip()

        if self.terminal_test(self.state):
            self.game_over = True
            winner = "Player 1" if self.utility(self.state, self.to_move(self.initial)) > 0 else "Player 2"
            print(f"{winner} won!")
            return  # Game is over, no further moves

        # Switch player
        self.current_player_index = 1 - self.current_player_index

    # Input Settings
    def input_mode(self):
        is_input_valid = False
        input_mode = 0
        input_difficulty = 0

        # Display Prompt
        print("Select Game Mode:" \
            "\n 1. Player vs Player" \
            "\n 2. Player vs AI" \
            "\n 3. AI vs AI")

        # While the input is not valid:
        while not is_input_valid:
            input_mode = int(input('Input game mode number: '))
            if input_mode in self.game_modes.keys():
                is_input_valid = True
                
                # If selecting AI,
                if input_mode == 2 or input_mode == 3:
                    # Display Prompt
                    print("Select AI Difficulty:" \
                        "\n 1. Easy" \
                        "\n 2. Medium" \
                        "\n 3. Hard")
                    
                    # Reset Input Validity
                    is_input_valid = False
                    
                    # Break once a valid input is set
                    while not is_input_valid:
                        input_difficulty = int(input('Input difficulty number: '))
                        if input_difficulty in self.ai_difficulties.keys() and not input_difficulty == 0: is_input_valid = True
                        else:
                            print("Invalid Input. Input 1 for easy, 2 for medium, 3 for hard.")
            
            else:
                print("Invalid Input. Input 1 for PvP, 2 for PvAI, 3 for AIvAI")

            self.mode_index = input_mode
            self.difficulty_index = input_difficulty

    # Initialize Game
    def initialize_mode(self):
        print("Game Mode: ", self.game_modes[self.mode_index])
        print ("AI Difficulty: ", self.ai_difficulties[self.difficulty_index])
        
        if self.game_modes[self.mode_index] == "Player vs Player":
            self.player1 = human_player
            self.player2 = human_player
        elif self.game_modes[self.mode_index] == "Player vs AI":
            self.player1 = human_player
            if self.ai_difficulties[self.difficulty_index] == "Easy":
                self.player2 = ai_player_easy
            elif self.ai_difficulties[self.difficulty_index] == "Medium":
                self.player2 = ai_player_medium
            elif self.ai_difficulties[self.difficulty_index] == "Hard":
                self.player2 = ai_player_hard
        elif self.game_modes[self.mode_index] == "AI vs AI":
            if self.ai_difficulties[self.difficulty_index] == "Easy":
                self.player1 = ai_player_easy
                self.player2 = ai_player_easy
            elif self.ai_difficulties[self.difficulty_index] == "Medium":
                self.player1 = ai_player_medium
                self.player2 = ai_player_medium
            elif self.ai_difficulties[self.difficulty_index] == "Hard":
                self.player1 = ai_player_hard
                self.player2 = ai_player_hard

# Query Player
def human_player(game, state):
    """Make a move by querying available actions and the selected column."""
    available_moves = game.actions(state)  # Get the list of valid moves (tuples)
    
    if not game.has_printed_available_moves:
        print("Available moves:", available_moves)
        game.has_printed_available_moves = True

    move_column = game.gui.selected_move  # Get the selected move from the GUI

    if move_column is not None:
        # Find the move where the second value matches the selected column
        for move in available_moves:
            if move[1] == move_column:
                game.gui.selected_move = None  # Reset the move for the next turn
                print("Chosen move:", move)
                game.has_printed_available_moves = False
                return move
        print("Invalid move! Please choose a valid column.")
        game.gui.selected_move = None  # Reset the move if it's invalid
    return None  # If no valid move, return None and wait for a valid selection

# AlphaBetaGamer
def ai_player_easy(game, state):
    return alpha_beta_cutoff_search(state, game, 2, None, None)

def ai_player_medium(game, state):
    return alpha_beta_cutoff_search(state, game, 4, None, None)

def ai_player_hard(game, state):
    return alpha_beta_cutoff_search(state, game, 8, None, None)

def text_player(game, state):
    """Make a move by querying standard input."""
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move

if __name__ == "__main__":
    connectFour = ConnectFourBase(game = 0)
    
    human_player = text_player

    connectFour.input_mode()
    connectFour.initialize_mode()
    
    utility = connectFour.play_game(connectFour.player1, connectFour.player2)
    
    if (utility < 0):
        print("Player 2 won the game")
    else:
        print("Player 1 won the game")


    
