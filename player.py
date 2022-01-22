import random
import copy


class Player:

    def __init__(self, color):
        self.color = color

    def random_move(self, board):
        x = random.randint(0, 8)

        while board[int(x / 3)][x % 3] != 0:
            x = random.randint(0, 8)
        board[int(x / 3)][x % 3] = self.color

    def human_move(self, board):
        x = int(input('x: '))
        y = int(input('y: '))
        if x > 3 or x < 0:
            print('x is not 1,2 or 3')
        if y > 3 or y < 0:
            print('y is not 1,2 or 3')
        while board[int(y)-1][int(x)-1] != 0:
            print('Field not empty')
            x = int(input('x: '))
            y = int(input('y: '))
            if x > 3:
                print('x is not 1,2 or 3')
            if y > 3:
                print('y is not 1,2 or 3')
        board[int(y)-1][int(x)-1] = self.color

    def get_board_features(self, board):
        x0 = 1  # Constant
        x1 = 0  # Number of rows/columns/diagonals with two of our own pieces and one emtpy field
        x2 = 0  # Number of rows/columns/diagonals with two of opponent's pieces and one empty field
        x3 = 0  # Is our own piece on the center field
        x4 = 0  # Number of own pieces in corners
        x5 = 0  # Number of rows/columns/diagonals with one own piece and two empty fields
        x6 = 0  # Number of rows/columns/diagonals with three own pieces

        if board[1][1] == self.color:
            x3 += 1
        if board[0][0] == self.color:
            x4 += 1
        if board[2][2] == self.color:
            x4 += 1
        if board[0][2] == self.color:
            x4 += 1
        if board[2][0] == self.color:
            x4 += 1
        if self.color == 'x':
            enemy_color = 'o'
        else:
            enemy_color = 'x'

        for i in range(3):
            own_rows = 0
            own_columns = 0
            enemy_rows = 0
            enemy_columns = 0
            empty_rows = 0
            empty_columns = 0
            for j in range(3):
                if board[i][j] == 0:
                    empty_rows += 1
                elif board[i][j] == self.color:
                    own_rows += 1
                elif board[i][j] == enemy_color:
                    enemy_rows += 1
                if board[j][i] == 0:
                    empty_columns += 1
                elif board[j][i] == self.color:
                    own_columns += 1
                elif board[j][i] == enemy_color:
                    enemy_columns += 1

            if own_rows == 2 and empty_rows == 1:
                x1 += 1
            if enemy_rows == 2 and empty_rows == 1:
                x2 += 1
            if own_columns == 2 and empty_columns == 1:
                x1 += 1
            if enemy_columns == 2 and empty_columns == 1:
                x2 += 1

            if own_rows == 1 and empty_rows == 2:
                x5 += 1
            if own_columns == 1 and empty_columns == 2:
                x5 += 1
            if own_rows == 3:
                x6 += 1
            if own_columns == 3:
                x6 += 1

        for i in range(2):
            own_diagonal = 0
            enemy_diagonal = 0
            empty_diagonal = 0
            for j in range(3):
                if i == 0:
                    diagonal = board[2-j][j]
                else:
                    diagonal = board[j][j]
                if diagonal == self.color:
                    own_diagonal += 1
                if diagonal == 0:
                    empty_diagonal += 1
                if diagonal == enemy_color:
                    enemy_diagonal += 1
            if own_diagonal == 2 and empty_diagonal == 1:
                x1 += 1
            if enemy_diagonal == 2 and empty_diagonal == 1:
                x2 += 1
            if own_diagonal == 1 and empty_diagonal == 2:
                x5 += 1
            if own_diagonal == 3:
                x6 += 1


        return [x0, x1, x2, x3, x4, x5, x6]

    def evalApproximation(self, features, weights):
        val = 0.0
        for i in range(len(weights)):
            val += features[i] * weights[i]
        return val

    def make_move(self, board, weights):
        new_boards = list()
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = self.color
                    new_boards.append((new_board, (i, j)))
        val = -9999999
        for i in new_boards:
            features = self.get_board_features(i[0])
            curr_val = self.evalApproximation(features, weights)
            if val < curr_val:
                val = curr_val
                best_move = i[1]
        board[best_move[0]][best_move[1]] = self.color