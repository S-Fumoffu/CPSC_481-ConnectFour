from games import *
import pygame as pg
# Modified For Pygame
class ConnectFourBase(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, game, h=6, v=7, k=4):
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
                print(state)

                print("Player: ", player)
                print("Victory Probability: ", winning_probability(state))

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
        self.match_result = 0
        self.victory_probability = winning_probability(self.state)

        self.current_player_index = 0
        self.game_over = False
        self.display(self.state)
        print("")

    def play_turn(self):
        """Plays as many moves as needed until a human input is needed."""
        if self.game_over:
            return

        player = self.current_players[self.current_player_index]

        # Calculates Victory Probability Via Heuristic
        self.victory_probability = winning_probability(self.state)
        
        move = player(self, self.state)  # Human returns None if waiting for input

        if move is None:
            # No move yet (e.g., human needs to click)
            return
        
        # Otherwise, move is valid -> apply it
        self.state = self.result(self.state, move)
        self.display(self.state)
        print("")

        if self.terminal_test(self.state):
            self.game_over = True
            self.match_result = self.utility(self.state, self.to_move(self.initial))
            if self.match_result > 0: winner = "Player 1"
            elif self.match_result < 0: winner = "Player 2"
            else: winner = "No-one"
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
    return alpha_beta_cutoff_search(state, game, 6, None, None)

# AI Helper Text
def ai_helper(game, state, depth = 7):
    optimal = alpha_beta_cutoff_search(state, game, depth, None, winning_probability)
    print("HOLD IT!")
    print("Pssst, the most optimal move is: ", optimal)
    return optimal

# For running in Base
def text_player(game, state):
    """Make a move by querying standard input."""
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        ai_helper(game, state)
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move

# Uses evaluation function to find probability.
def winning_probability(state):
    player = state.to_move
    opponent = 'O' if player == 'X' else 'X'
    board = state.board
    
    # Helper function to get cell value
    def get_cell(r, c):
        return board.get((r, c), ' ')  # Empty if not in board
    
    # Generate all possible 4-length windows
    windows = []
    rows, cols = 6, 7
    
    # Horizontal windows
    for r in range(1, rows + 1):
        for c in range(1, cols - 3 + 1):
            windows.append([get_cell(r, c + i) for i in range(4)])
    
    # Vertical windows
    for r in range(1, rows - 3 + 1):
        for c in range(1, cols + 1):
            windows.append([get_cell(r + i, c) for i in range(4)])
    
    # Positive diagonal (bottom-left to top-right)
    for r in range(1, rows - 3 + 1):
        for c in range(1, cols - 3 + 1):
            windows.append([get_cell(r + i, c + i) for i in range(4)])
    
    # Negative diagonal (top-left to bottom-right)
    for r in range(4, rows + 1):
        for c in range(1, cols - 3 + 1):
            windows.append([get_cell(r - i, c + i) for i in range(4)])
    
    # Check for immediate win/loss
    for window in windows:
        if window.count(player) == 4:
            return 1.0  # 100% win
        if window.count(opponent) == 4:
            return 0.0  # 0% win
    
    # Feature counting
    player_threes = sum(1 for w in windows if w.count(player) == 3 and w.count(' ') == 1)
    opponent_threes = sum(1 for w in windows if w.count(opponent) == 3 and w.count(' ') == 1)
    player_twos = sum(1 for w in windows if w.count(player) == 2 and w.count(' ') == 2)
    opponent_twos = sum(1 for w in windows if w.count(opponent) == 2 and w.count(' ') == 2)
    
    # Center control (columns 3-5 are center)
    center_cols = [3, 4, 5]
    player_center = sum(1 for c in center_cols for r in range(1, rows + 1) if get_cell(r, c) == player)
    opponent_center = sum(1 for c in center_cols for r in range(1, rows + 1) if get_cell(r, c) == opponent)
    
    # Calculate probability components (weights can be adjusted)
    immediate_threat = 0.0
    if player_threes > 0:
        immediate_threat += 0.3  # High chance to win next move
    if opponent_threes > 0:
        immediate_threat -= 0.3  # High chance to lose if not blocked
    
    potential = (0.1 * (player_twos - opponent_twos) + 
                0.25 * (player_threes - opponent_threes))
    
    center_control = 0.05 * (player_center - opponent_center)
    
    # Normalize to [0, 1] range
    base_prob = 0.5  # Starting assumption
    prob = base_prob + immediate_threat + potential + center_control
    
    # Clamp between 0 and 1
    return max(0.0, min(1.0, prob))

if __name__ == "__main__":
    connectFour = ConnectFourBase(game = 0)
    
    human_player = text_player

    connectFour.input_mode()
    connectFour.initialize_mode()
    
    utility = connectFour.play_game(connectFour.player1, connectFour.player2)
    
    if (utility < 0):
        print("Player 2 won the game")
    elif (utility > 0):
        print("Player 1 won the game")
    else: print("You're all losers.")


    
