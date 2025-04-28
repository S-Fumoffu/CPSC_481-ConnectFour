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
        while True:
            for player in players:
                self.display(state)

                move = player(self, state)
                state = self.result(state, move)

                print("Player: ", player)
                print("Move: ", move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))

# AlphaBetaGamer
def alpha_beta_player_easy(game, state):
    return alpha_beta_cutoff_search(state, game, 2, None, None)

def alpha_beta_player_medium(game, state):
    return alpha_beta_cutoff_search(state, game, 4, None, None)

def alpha_beta_player_hard(game, state):
    return alpha_beta_cutoff_search(state, game, 8, None, None)

if __name__ == "__main__":
    connectFour = ConnectFourPygame() # a much larger tree to search

    utility = connectFour.play_game(alpha_beta_player_hard, query_player) # computer moves first

    if (utility < 0):
        print("MIN won the game")
    else:
        print("MAX won the game")

    # print ("\n utility is ", utility)
