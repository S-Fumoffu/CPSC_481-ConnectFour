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
        }

        self.game_modes = {1: "Player vs Player",
                           2: "Player vs AI"}
        
        self.ai_difficulties = {0: "N/A",
                                1: "Easy",
                                2: "Medium",
                                3: "Hard"}
        self.state_index = 0
        self.mode_index = 0
        self.difficulty_index = 0

        # Players
        self.player1 = self.player2 = human_player

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if x == self.h or (x + 1 , y ) in state.board]
    
    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial

        self.display(state)

        while True:
            for player in players:

                print (state.board.items())

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

    # BUGS MAY BE FOUND HERE
    def play_turn(self):
        """Plays one move per call."""
        if self.game_over:
            return

        # Get the selected move for the human player
        player = self.current_players[self.current_player_index]
        move = player(self, self.state)  # This will return a valid move or None
        
        if move is None:
            return  # Wait for a valid move (in case the player clicked an invalid column)
        
        # Find the first available space in the column (starting from the bottom)
        for row in range(5, -1, -1):  # Check from bottom row (5) to top row (0)
            if (row + 1, move[1]) not in self.state.board:  # If space is empty
                self.state.board[(row + 1, move[1])] = player  # Place the piece
                break
        
        # Update the game state after placing the piece
        self.state = self.result(self.state, move)
        self.display(self.state)

        # Check if the game is over
        if self.terminal_test(self.state):
            self.game_over = True
            winner = "Player 1" if self.utility(self.state, self.to_move(self.initial)) > 0 else "Player 2"
            print(f"{winner} won!")
            # Optional: GUI popup for "Player X Wins!"

        self.current_player_index = 1 - self.current_player_index  # Switch players


    # Input Settings
    def input_mode(self):
        is_input_valid = False
        input_mode = 0
        input_difficulty = 0

        # Display Prompt
        print("Select Game Mode:" \
            "\n 1. Player vs Player" \
            "\n 2. Player vs AI")

        # While the input is not valid:
        while not is_input_valid:
            input_mode = int(input('Input game mode number: '))
            if input_mode in self.game_modes.keys():
                is_input_valid = True
                
                # If selecting AI,
                if input_mode == 2:
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
                print("Invalid Input. Input 1 for PvP or 2 for PvAI")

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

# BUGS MAY BE FOUND HERE
# Query Player
def human_player(game, state):
    """Make a move by querying available actions and the selected column."""
    available_moves = game.actions(state)  # Get the list of valid moves (columns with available space)
    print("Available moves:", available_moves)
    
    move = game.gui.selected_move  # Get the selected move from the GUI

    if move:
        # Check if the selected move is valid
        if move in available_moves:
            game.gui.selected_move = None  # Reset the move for the next turn
            return move
        else:
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

if __name__ == "__main__":
    connectFour = ConnectFourBase()
    
    connectFour.input_mode()
    connectFour.initialize_mode()
    
    utility = connectFour.play_game(connectFour.player1, connectFour.player2)
    
    if (utility < 0):
        print("Player 2 won the game")
    else:
        print("Player 1 won the game")


    
