import datetime
import time
import RPi.GPIO as GPIO
import threading

GPIO.setmode(GPIO.BCM)
gpio_list_leds = [8, 21, 11, 12, 13, 15, 16, 18, 19]
gpio_list_buttons = [22, 24]


class Player:
    def __init__(self, id, sign):
        self.id = id
        self.sign = sign
        self.placedPos = ["", "", "", "", "", "", "", "", ""]
        self.winningBoard = ["", "", "", "", "", "", "", "", "", ""]

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
        GPIO.setmode(GPIO.BCM)

    def start_game(self):
        self.game_loop()

    def game_loop(self):
        input_manager = InputManager(gpio_list_buttons[0], gpio_list_buttons[1])
        threading.Thread(target=input_manager.input_change_sign_view()).start()
        while not self.winning:
            if self.possible_to_place():
                self.currentPlayer.place(input_manager)
                if self.check_for_win():
                    self.winning = True
                    self.winner = self.currentPlayer.id
                else:
                    self.next_player()
        self.draw_board(self.currentPlayer.winningBoard, self.currentPlayer.sign)

    def possible_to_place(self):
        for signPosition in self.board:
            if signPosition == " ":
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

    def place_sign(self, pos):
        if self.allowed_to_place_pos(pos):
            self.board[pos] = self.currentPlayer.sign
            self.currentPlayer.placedPos[pos] = self.currentPlayer.sign
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
        sign_to_render = None
        if sign == "X":
            sign_to_render = sign
        elif sign == "0":
            sign_to_render = sign
        else:
            raise Exception

        for i in range(len(board) - 1):
            if board[i] == sign_to_render:
                GPIO.setup(gpio_list_leds[i], GPIO.OUT)
                GPIO.output(gpio_list_leds[i], GPIO.HIGH)
            else:
                GPIO.setup(gpio_list_leds[i], GPIO.OUT)
                GPIO.output(gpio_list_leds[i], GPIO.LOW)


class InputManager:
    def __init__(self, buttonLeftPin, buttonRightPin):
        self.buttonLeftPin = buttonLeftPin
        self.buttonRightPin = buttonRightPin
        GPIO.setup(self.buttonLeftPin, GPIO.IN)
        GPIO.setup(self.buttonRightPin, GPIO.IN)

    def input_change_sign_view(self):
        while not gameManager.winning:
            if GPIO.input(self.buttonLeftPin) == 1:
                if gameManager.get_current_player_id() == 1:
                    GameManager.draw_board(player1.placedPos, player1.sign)
                else:
                    GameManager.draw_board(player2.placedPos, player2.sign)

    def input_place(self):
        current_place_pos = 0
        GPIO.setup(self.buttonLeftPin, GPIO.IN)
        first_click = None
        second_click = None
        while True:
            if GPIO.input(self.buttonLeftPin):
                if first_click is None:
                    first_click = time.time()
                else:
                    second_click = time.time()
                if second_click - first_click > 0.2:
                    if gameManager.place_sign(current_place_pos):
                        break
                    first_click = None
                    second_click = None
                else:
                    current_place_pos += 1


if __name__ == "__main__":
    player1 = Player("1", "X")
    player2 = Player("2", "0")
    gameManager = GameManager(player1, player2)
    gameManager.start_game()
