import numpy as np
import sys
from random import randint

#Constants for each turn piece
pieces = {1: 'X', 2: 'O'}
X = 1
O = 2

#Constants for the game states
states = {3: 'Win',
          4: 'Los',
          5: 'Draw',
          6: 'Continue'}
WIN = 3
LOSS = 4
DRAW = 5
CONTINUE = 6

#Attempts to place a certain piece in a certain place
def turn(board, (x, y), piece):
    if board[y][x] == 0:
        board[y][x] = piece
    else:
        raise Exception("Grid space already taken")


#Prints the Board
def print_board(board, (piece1, string1), (piece2, string2)):
    for j in range(len(board)):
        print
        for i in range(len(board[j])):
            sys.stdout.write(' ')
            if board[j][i] == 0:
                sys.stdout.write('☐')
            if board[j][i] == piece1:
                sys.stdout.write(string1)
            if board[j][i] == piece2:
                sys.stdout.write(string2)

    print
    print


#Counts the number of times x appears in a 2D array
def count_elements(array, ele):
    elements = {0: 0, 1: 0, 2: 0, 3: 0}
    for j in range(len(array)):
        for i in range(len(array[j])):
            if array[j][i] not in elements:
                elements[array[j][i]] = 0

            elements[array[j][i]] += 1

    return elements[ele]


#Evaluates the current game state and informs of a WIN/LOSS/DRAW scenario.
def evaluate(board, piece1, piece2):

    #Check rows
    for j in range(len(board)):
        if board[j][0] != 0:
            piece = board[j][0]
            if (board[j][1] == piece) and (board[j][2] == piece):
                return WIN, piece

    #Check columns
    for i in range(len(board[0])):
        if board[0][i] != 0:
            piece = board[0][i]
            if (board[1][i] == piece) and (board[2][i] == piece):
                return WIN, piece

    #Check Diagonal Down
    if board[0][0] != 0:
        piece = board[0][0]
        if (board[1][1] == piece) and (board[2][2] == piece):
            return WIN, piece

    #Check Diagonal Up
    if board[0][2] != 0:
        piece = board[0][2]
        if (board[1][1] == piece) and (board[2][0] == piece):
            return WIN, piece

    #Check if board is full
    if count_elements(board, 0) == 0:
        return DRAW, None
    else:
        if count_elements(board, piece1) > count_elements(board, piece2):
            next = piece2
        else:
            next = piece1
        return CONTINUE, next

def play_game():
    grid = np.zeros(9).reshape((3, 3))
    player = X
    state = evaluate(grid, X, O)

    while (state[0] != WIN) and (state[0] != DRAW):
        spaces_left = count_elements(grid, 0)
        chosen_space = randint(0, spaces_left - 1)

        print(states[state[0]] + " " + pieces[state[1]])
        print("Spaces left = " + str(spaces_left))
        print("Chosen Space = " + str(chosen_space))

        space = 0
        placed_piece = False

        for j in range(len(grid)):
            for i in range(len(grid[j])):
                if grid[j][i] == 0:
                    if space == chosen_space:
                        turn(grid, (i, j), player)
                        placed_piece = True

                        if player == X:
                            player = O
                        else:
                            player = X

                        print_board(grid, (X, "X"), (O, "O"))

                        break

                    space += 1

            if placed_piece:
                break

        state = evaluate(grid, X, O)

    if state[0] == DRAW:
        print("It's a Draw!")

    if state[0] == WIN:
        print(pieces[state[1]] + " wins!")


if __name__ == "__main__":
    play_game()
