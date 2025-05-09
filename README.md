# CPSC_481-ConnectFour

Connect Four game built using https://github.com/aimacode/aima-python as a base.
Fully featured GUI supporting Player vs Player, Player vs AI, AI vs AI
Players can use a hint button to return the best calculated optimal move.

## Project Members:

- Sinan Abdul-Hafiz

- Cristina Hernandez

## Instructions

To Run:

- If you have all dependencies: Run ConnectFourGUI.
- Else, you can run the standalone application by simply opening it.

To Compile for Windows: 
py -m PyInstaller --onefile ^
--add-data "assets\fonts\Grand9K Pixel.ttf;assets\fonts" ^
--add-data "assets\icon\connectFourIcon.png;assets\icon" ^
--icon=assets\icon\connectFourIcon.ico ^
ConnectFourGUI.py

## Layout:

Core:
- connectFourGUI.py - GUI front-end of the connect four game
- connectFourBase.py - Logical back-end of the game. You can also run text-based version here.
- games.py - Sourced from AIMA PYTHON. ConnectFourBase inherits from Tic Tac Toe from here.
                It also made use of its query player, alpha_beta_gamer, and minimax cutoff search algorithm,
                until we modified them and placed them in connectFourBase.
- utils.py - A dependency of games.py

Peripheral:
- Assets Folder - contains fonts and icons used for the GUI.
- button.py - Repurposed code from another project that handles the logic for creating buttons in PyGame.
- invisible_button.py - Handles logic for creating invisible buttons.
                        ConnectFourGUI uses these to determine which column the player has clicked to place their piece.
- colors.py - Globally assigns tuples (RR,GG,BB) to variables with color names such as GREEN that is then used for color in Pygame.
- fonts.py - Loads in the fonts from assets which is then imported to connectFourGUI.py and button.py.