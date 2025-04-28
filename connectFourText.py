from games import *

# Modified For Pygame
class ConnectFourPygame(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def actions(self, state):
        return [(x, y) for (x, y) in state.moves
                if x == self.h or (x + 1 , y ) in state.board]
    
    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial

        self.display(state)
        # TODO: CONVERT THIS DISPLAY INTO PYGAME

        while True:
            for player in players:

                print("Player: ", player)
                # TODO: DISPLAY WHO'S TURN IT IS ON PYGAME

                move = player(self, state)
                state = self.result(state, move)

                print("Move: ", move)

                self.display(state)
                # TODO: CONVERT THIS DISPLAY INTO PYGAME

                if self.terminal_test(state):
                    print(state)
                    return self.utility(state, self.to_move(self.initial))

# Query Player
def human_player(game, state):
    """Make a move by querying standard input."""
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        move_string = human_move()
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move

# TODO: UPDATE THIS TO RETURN A MOVE VIA PYGAME CLICK
def human_move():
    move_string = input('Your move? ')
    return move_string

# AlphaBetaGamer
def ai_player_easy(game, state):
    return alpha_beta_cutoff_search(state, game, 2, None, None)

def ai_player_medium(game, state):
    return alpha_beta_cutoff_search(state, game, 4, None, None)

def ai_player_hard(game, state):
    return alpha_beta_cutoff_search(state, game, 8, None, None)

# Initialize Game

def initialize_mode():
    is_input_valid = False
    input_mode = 0
    input_difficulty = 0
    
    game_modes = {1: "Player vs Player",
                  2: "Player vs AI"}
    
    ai_difficulties = {0: "N/A",
                       1: "Easy",
                       2: "Medium",
                       3: "Hard"}

    # Display Prompt
    print("Select Game Mode:" \
        "\n 1. Player vs Player" \
        "\n 2. Player vs AI")

    # While the input is not valid:
    while not is_input_valid:
        input_mode = int(input('Input game mode number: '))
        if input_mode in game_modes.keys():
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
                    if input_difficulty in ai_difficulties.keys() and not input_difficulty == 0: is_input_valid = True
                    else:
                        print("Invalid Input. Input 1 for easy, 2 for medium, 3 for hard.")
        
        else:
            print("Invalid Input. Input 1 for PvP or 2 for PvAI")

    print("Game Mode: ", game_modes[input_mode])
    print ("AI Difficulty: ", ai_difficulties[input_difficulty])


    if game_modes[input_mode] == "Player vs Player":
        player1 = human_player
        player2 = human_player
    elif game_modes[input_mode] == "Player vs AI":
        player1 = human_player
        if ai_difficulties[input_difficulty] == "Easy":
            player2 = ai_player_easy
        elif ai_difficulties[input_difficulty] == "Medium":
            player2 = ai_player_medium
        elif ai_difficulties[input_difficulty] == "Hard":
            player2 = ai_player_hard

    return player1, player2

if __name__ == "__main__":
    connectFour = ConnectFourPygame()

    player1, player2 = initialize_mode()

    utility = connectFour.play_game(player1, player2)

    if (utility < 0):
        print("Player 2 won the game")
    else:
        print("Player 1 won the game")
