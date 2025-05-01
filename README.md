# CPSC_481-ConnectFour

Connect Four game built using https://github.com/aimacode/aima-python as a base.
Fully featured GUI supporting Player vs Player, Player vs AI, AI vs AI
Players can use a hint button to return the best calculated optimal move.

Project Members:

- Cristina Hernandez

- Sinan Abdul-Hafiz

To Run:
- If you have all dependencies: Run ConnectFourGUI.
- Else, you can run the standalone application by simply opening it.

To Compile:
py -m PyInstaller --onefile ^
--add-data "assets\fonts\Grand9K Pixel.ttf;assets\fonts" ^
--add-data "assets\icon\connectFouricon.png;assets\icon" ^
--icon=assets\icon\connectFour.ico ^
ConnectFourGUI.py