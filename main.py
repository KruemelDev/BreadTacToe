import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
gpio_list_leds = [8, 11, 13, 15, 16, 18, 19, 21, 22]
gpio_list_buttons = [24, 26]


class Player:
    def __init__(self, id, sign):
        self.id = id
        self.sign = sign
        self.placedPos = ["", "", "", "", "", "", "", "", ""]
        self.winningBoard = ["", "", "", "X", "", "X", "X", "", "", ""]

    def place(self, inputManager):
        inputManager.place(self.placedPos)


class GameManager:
    def __init__(self, player1, player2):
        self.board = ["", "", "", "", "", "", "", "", ""]
        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = player1
        self.winner = None
        self.winning = False

    def start_game(self):
        self.game_loop()

    def game_loop(self):
        
        input_manager = InputManager(gpio_list_buttons[0], gpio_list_buttons[1])
        
        begin_screen = ["", "X", "", "X", "X", "X","", "X", ""]
        print("hier")
 
        self.draw_board(begin_screen, "X")
        while not self.winning:
            if self.possible_to_place():
                input_manager.input_handling()
                if self.check_for_win():
                    self.winning = True
                    self.winner = self.currentPlayer.id
        self.draw_board(self.currentPlayer.winningBoard, self.currentPlayer.sign)

    def possible_to_place(self):
        for signPosition in self.board:
            if signPosition == "":
                return True
            else:
                return False

    def next_player(self):
        if self.currentPlayer.id == 1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

    def get_current_player_id(self):
        return self.currentPlayer.id

    def place_sign_and_next_player(self, pos):
        if self.allowed_to_place_pos(pos):
            self.board[pos] = self.currentPlayer.sign
            self.currentPlayer.placedPos[pos] = self.currentPlayer.sign
            self.next_player()
            return True
        else:
            return False

    def allowed_to_place_pos(self, pos):
        if self.board[pos] == "":
            return True
        else:
            return False

    def check_for_win(self):
        if self.board[0] == self.currentPlayer.sign and self.board[1] == self.currentPlayer.sign and self.board[2] == self.currentPlayer.sign:
            return True
        elif self.board[3] == self.currentPlayer.sign and self.board[4] == self.currentPlayer.sign and self.board[5] == self.currentPlayer.sign:
            return True
        elif self.board[6] == self.currentPlayer.sign and self.board[7] == self.currentPlayer.sign and self.board[8] == self.currentPlayer.sign:
            return True
        elif self.board[0] == self.currentPlayer.sign and self.board[3] == self.currentPlayer.sign and self.board[6] == self.currentPlayer.sign:
            return True
        elif self.board[1] == self.currentPlayer.sign and self.board[4] == self.currentPlayer.sign and self.board[7] == self.currentPlayer.sign:
            return True
        elif self.board[2] == self.currentPlayer.sign and self.board[5] == self.currentPlayer.sign and self.board[8] == self.currentPlayer.sign:
            return True
        elif self.board[0] == self.currentPlayer.sign and self.board[4] == self.currentPlayer.sign and self.board[8] == self.currentPlayer.sign:
            return True
        elif self.board[2] == self.currentPlayer.sign and self.board[4] == self.currentPlayer.sign and self.board[6] == self.currentPlayer.sign:
            return True
        else:
            return False

    @staticmethod
    def draw_board(board, sign):

        for i in range(len(board)):
            if board[i] == sign:
                GPIO.setup(gpio_list_leds[i], GPIO.OUT)
                GPIO.output(gpio_list_leds[i], GPIO.HIGH)
                print("on")
            else:
                GPIO.setup(gpio_list_leds[i], GPIO.OUT)
                GPIO.output(gpio_list_leds[i], GPIO.LOW)


class InputManager:
    def __init__(self, buttonLeftPin, buttonRightPin):
        self.buttonLeftPin = buttonLeftPin
        self.buttonRightPin = buttonRightPin
        GPIO.setup(self.buttonLeftPin, GPIO.IN)
        GPIO.setup(self.buttonRightPin, GPIO.IN)
        self.board_to_draw = 1

        self.first_click = None
        self.second_click = None
        self.current_place_pos = 0

    def input_handling(self):
        print("in input_handling")
        self.right_button()
        self.left_button()

    def right_button(self):
        print(GPIO.input(self.buttonRightPin))
        if GPIO.input(self.buttonRightPin) == 1:
            if self.board_to_draw == 1:
                GameManager.draw_board(player2.placedPos, player2.sign)
                self.board_to_draw = 2
                print("draw_board 1")
            elif self.board_to_draw == 2:
                GameManager.draw_board(player1.placedPos, player1.sign)
                self.board_to_draw = 1
                print("draw_board 2")
                time.sleep(1.0)

    def left_button(self):

        if GPIO.input(self.buttonLeftPin):
            if self.first_click is None:
                self.first_click = time.time()
            else:
                self.second_click = time.time()
            if self.second_click - self.first_click > 0.2:
                gameManager.place_sign_and_next_player(self.current_place_pos)
                self.first_click = None
                self.second_click = None
            else:
                if not self.current_place_pos == 8:
                    self.current_place_pos += 1
                else:
                    self.current_place_pos = 0


if __name__ == "__main__":
    player1 = Player(1, "X")
    player2 = Player(2, "0")
    gameManager = GameManager(player1, player2)
    gameManager.start_game()
