_author = "Popescu Ionut-Alexandru"
import random
from termcolor import cprint, colored

class Player:
    def __init__(self, username):
        self.username = username
        self.players_view = [[0 for i in range(10)] for j in range(10)]
        self.planes = 3

    def __str__(self):

        line_board = [x for x in range(1, 11)]
        column_board = [chr(ord('A') + i) for i in range(10)]
        column_board.insert(0, '  ')
        line = colored(self.username,'white', 'on_blue', attrs=['bold']) + "  " + \
            colored(f'Planes alive: {self.planes}','red', attrs=['bold']) + '\n'
        line += colored(" ".join(column_board), 'white', 'on_blue', attrs=['bold']) + '\n'
        for i in range(len(self.players_view)):
            if i == 9:
                line += colored(str(line_board[i]), 'white', 'on_blue', attrs=['bold'])
                line +=" "+" ".join(colored(x, 'white', 'on_yellow', attrs=['bold']) if x == 'H' else colored(x, 'white', 'on_red', attrs=['bold']) \
                        if x == 'X' else colored(x, 'white', 'on_cyan', attrs=['bold']) if x == 'M' else colored(str(x), attrs=['bold']) \
                        for x in self.players_view[i])
            else:
                line += colored(str(line_board[i]) + " ", 'white', 'on_blue', attrs=['bold'])
                line += " "+" ".join(colored(x, 'white', 'on_yellow', attrs=['bold']) if x == 'H' else colored(x, 'white', 'on_red', attrs=['bold']) \
                        if x == 'X' else colored(x, 'white', 'on_cyan', attrs=['bold']) if x == 'M' else colored(str(x),attrs=['bold']) \
                        for x in self.players_view[i])
            line += '\n'
        return line

    def plane_hit(self, x, y, letter):
        self.players_view[x][y] = letter
        if letter == 'H':
            self.planes -= 1

class Game:
    def __init__(self):
        self.game_board = [[0 for i in range(10)] for j in range(10)]

    def __str__(self):
        line = ''
        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                line = line + str(self.game_board[i][j]) + " "
            line += '\n'
        return line

    @staticmethod
    def is_right(x, y):
        right = [[(x - 2, y + 1), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)],
                    [(x, y + 2)],
                    [(x - 1, y + 3), (x, y + 3), (x + 1, y + 3)]]
        return right

    @staticmethod
    def is_left(x, y):
        left = [[(x - 2, y - 1), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 2, y - 1)],
                   [(x, y - 2)],
                   [(x - 1, y - 3), (x, y - 3), (x + 1, y - 3)]]
        return left

    @staticmethod
    def is_top(x, y):
        top = [[(x - 1, y + 2), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x - 1, y - 2)],
                  [(x - 2, y)],
                  [(x - 3, y - 1), (x - 3, y), (x - 3, y + 1)]]
        return top

    @staticmethod
    def is_bottom(x, y):
        bottom = [[(x + 1, y + 2), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x + 1, y - 2)],
                     [(x + 2, y)],
                     [(x + 3, y - 1), (x + 3, y), (x + 3, y + 1)]]
        return bottom

    def place_plane(self, x, y, position='is_right', head_letter='A', body_number=1):
        self.game_board[x][y] = head_letter

        pos = self.is_right(x, y) if position == 'is_right' else self.is_left(x, y)\
            if position == 'is_left' else self.is_bottom(x, y) \
            if position == 'is_bottom' else self.is_top(x, y)

        self.game_board[x][y] = head_letter

        for i in range(len(pos)):
            for j in range(len(pos[i])):
                self.game_board[pos[i][j][0]][pos[i][j][1]] = body_number

        # self.players[self.playerTurn].planes[headLetter] = position

    def plane_verification(self, x, y, position='is_right'):
        pos = self.is_right(x, y) if position == 'is_right' else self.is_left(x, y)\
            if position == 'is_left' else self.is_bottom(x, y) \
            if position == 'is_bottom' else self.is_top(x, y)

        if self.game_board[x][y] != 0:
            return False
        for i in range(len(pos)):
            for j in range(len(pos[i])):
                if (pos[i][j][0] > 9 or pos[i][j][0] < 0 or pos[i][j][1] > 9 or pos[i][j][1] < 0 or
                        self.game_board[pos[i][j][0]][pos[i][j][1]] != 0):
                    return False
        return True

    def switch(self, argument):
        switcher = {
            0: self.is_right,
            1: self.is_left,
            2: self.is_top,
            3: self.is_bottom,
        }
        return switcher.get(argument, 'Invalid position')

    def planes_placer(self):
        numbers_of_planes = 0
        plane_heads = ['A', 'B', 'C']
        numbers_of_tries = 0
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            for i in range(4):
                if self.plane_verification(x, y, self.switch(i).__name__):
                    numbers_of_planes += 1
                    self.place_plane(x, y, self.switch(i).__name__, plane_heads[numbers_of_planes - 1],
                                     numbers_of_planes)

            if numbers_of_planes == 3:
                break

            if numbers_of_tries > 10000:
                numbers_of_planes = 0
                self.game_board = [[0 for i in range(10)] for j in range(10)]
                numbers_of_tries = 0
            numbers_of_tries += 1
