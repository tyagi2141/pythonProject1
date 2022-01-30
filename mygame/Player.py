from mygame.Game import feature12, feature34, feature56
import numpy as np
from random import shuffle

feature = [x for x in range(7)]
w = 0.1 * np.ones(6)

def displayBoard(board):
    print("\n")
    print(board[1] + " | " + board[2] + " | " + board[3] + "     1 | 2 | 3")
    print('---------     ---------')
    print(board[4] + " | " + board[5] + " | " + board[6] + "     4 | 5 | 6")
    print('---------     ---------')
    print(board[7] + " | " + board[8] + " | " + board[9] + "     7 | 8 | 9")
    print("\n")

def playMove(state):
        print("state...", state)
        maxValue = -100
        move = 0
        commonValues = []
        for i in range(9):
            if ord(state[i]) >= 49 and ord(state[i]) <= 57:
                temp = list(state)
                temp[i] = 'X'
                temp = ''.join(temp)
                v = vCap(temp)
                if maxValue < v:
                    maxValue = v
                    commonValues = []
                    commonValues.append(i)
                    move = i
                elif maxValue == v:
                    commonValues.append(i)

            shuffle(commonValues)
            move = commonValues[0] if commonValues else 0
        return move

def vCap(boardstate):
    feature[0] = 1
    feature[1], feature[2] = feature12(boardstate)  # Feature 1 is # of 'x' & Feature 2 to is # of 'o'
    feature[3], feature[4] = feature34(boardstate)  # Feature 3 is # of two 'x' per row & Feature 4 to is # of two 'o' per row
    feature[5], feature[6] = feature56(boardstate)  # Feature 5 is # of three 'x' & Feature 6 to is # of three 'o' per row
    vHat = 0
    for i in range(6):
        vHat = vHat + w[i] * feature[i];
    return vHat
