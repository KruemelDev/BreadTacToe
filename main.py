import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
gpio_list_leds = [8, 11, 13, 15, 16, 18, 19, 21, 22]
gpio_list_buttons = [24, 26]


class Player:
    def __init__(self, id, sign, winning_board):
        self.id = id
        self.sign = sign
        self.placed_pos = ["", "", "", "", "", "", "", "", ""]
        self.winning_board = ["", "", "", "", "", "", "", "", "", ""]

    def place(self, inputManager):
        inputManager.place(self.placed_pos)


class GameManager:
    def __init__(self, player1, player2):
        self.board = ["", "", "", "", "", "", "", "", ""]
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
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

        self.draw_board(self.winner.winning_board, self.winner.sign)
        time.sleep(5.0)
    def possible_to_place(self):
        space_to_place = False
        for signPosition in self.board:
            if signPosition == "":
                space_to_place = True
        return space_to_place

    def next_player(self):
        if self.current_player.id == 1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def get_current_player_id(self):
        return self.current_player.id

    def place_sign_and_next_player(self, pos):
        if self.allowed_to_place_pos(pos):
            self.board[pos] = self.current_player.sign
            self.current_player.placed_pos[pos] = self.current_player.sign
            print("last player was" + str(self.current_player.id))
            print("places at " + str(pos))
            self.draw_board(self.current_player.placed_pos, self.current_player.sign)
            if self.check_for_win():
                self.winning = True
                self.winner = self.current_player
            self.next_player()
            self.draw_board(self.current_player.placed_pos, self.current_player.sign)
            return True
        else:
            return False

    def allowed_to_place_pos(self, pos):
        if self.board[pos] == "":
            return True
        else:
            return False

    def check_for_win(self):
        if self.board[0] == self.current_player.sign and self.board[1] == self.current_player.sign and self.board[2] == self.current_player.sign:
            return True
        elif self.board[3] == self.current_player.sign and self.board[4] == self.current_player.sign and self.board[5] == self.current_player.sign:
            return True
        elif self.board[6] == self.current_player.sign and self.board[7] == self.current_player.sign and self.board[8] == self.current_player.sign:
            return True
        elif self.board[0] == self.current_player.sign and self.board[3] == self.current_player.sign and self.board[6] == self.current_player.sign:
            return True
        elif self.board[1] == self.current_player.sign and self.board[4] == self.current_player.sign and self.board[7] == self.current_player.sign:
            return True
        elif self.board[2] == self.current_player.sign and self.board[5] == self.current_player.sign and self.board[8] == self.current_player.sign:
            return True
        elif self.board[0] == self.current_player.sign and self.board[4] == self.current_player.sign and self.board[8] == self.current_player.sign:
            return True
        elif self.board[2] == self.current_player.sign and self.board[4] == self.current_player.sign and self.board[6] == self.current_player.sign:
            return True
        else:
            return False

    @staticmethod
    def draw_board(board, sign):

        for i in range(9):
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
        self.current_place_pos = 0

    def input_handling(self):
        self.right_button()
        self.left_button()

    def right_button(self):
        if GPIO.input(self.buttonRightPin) == 1:
            if self.board_to_draw == 1:
                GameManager.draw_board(player2.placed_pos, player2.sign)
                self.board_to_draw = 2
                time.sleep(0.15)
                print("draw_board 1")
            elif self.board_to_draw == 2:
                GameManager.draw_board(player1.placed_pos, player1.sign)
                self.board_to_draw = 1
                print("draw_board 2")
                time.sleep(0.15)

    def left_button(self):

        if GPIO.input(self.buttonLeftPin):
            time.sleep(0.3)
            if GPIO.input(self.buttonLeftPin):
                if gameManager.place_sign_and_next_player(self.current_place_pos):
                    print("placed at pos " + str(self.current_place_pos))
                    self.current_place_pos = 0
            else:
                if not self.current_place_pos == 8:
                    self.current_place_pos += 1
                    print("current place pos" + str(self.current_place_pos))
                else:
                    self.current_place_pos = 0
                    print("current place pos" + str(self.current_place_pos))

            time.sleep(0.2)


if __name__ == "__main__":
    player1 = Player(1, "X", ["", "X", "", "X", "X", "", "", "X", ""])
    player2 = Player(2, "0", ["", "0", "0", "0", "0", "", "0", "0", "0"])
    gameManager = GameManager(player1, player2)
    gameManager.start_game()
