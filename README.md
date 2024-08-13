# BreadTacToe

BreadTacToe is a tic tac toe clone made with a Raspberry Pi 3 Model B Vl.2 and BreadBoards

![](https://github.com/KruemelDev/BreadTacToe/gifs/BreadTacToe.gif)
## What you need
- BreadBoards(I recommend three)
- Raspberry pi
- 9 Transistors(I am using 2N3904H331)
- 9 leds
- 2 buttons
- 11 200Ω or 220Ω resistors
- 2 1kΩ resistors
- Several jumper wires

## How to play
### Rules
- [Tic tac toe rules](https://en.wikipedia.org/wiki/Tic-tac-toe)
### Buttons
#### Left Button
- A single click on the button moves the position at which the character is to be placed one step further from left to right
- If you hold down the button, the current player's sign will be placed in the position to which the court position has been moved if the other player has not placed it there
#### Right Button
- A single click on the button changes the view of the placed signs. So if you press once, you will see all the signs placed by the opponent and vice versa

## Planned features
- Status led that shows when a player has tried to place but cannot place
- Led indicating who the current player is
