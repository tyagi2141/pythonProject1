import random
from player import Player

def printBoard(board):
    for i in board:
        for j in i:
            print(str(j), end=' ')
        print()

def weight_update(weights, learningConstant, train_val, approx, features):
    for i in range(len(weights)):
        weights[i] = weights[i] + learningConstant * (train_val - approx) * features[i]

def finished(board, player):
    free = 0
    # horizontal win?
    if board[0][0] == player.color and board[0][1] == player.color and board[0][2] == player.color:
        return 1, player
    elif board[1][0] == player.color and board[1][1] == player.color and board[1][2] == player.color:
        return 1, player
    elif board[2][0] == player.color and board[2][1] == player.color and board[2][2] == player.color:
        return 1, player
    # vertical win ?
    elif board[0][0] == player.color and board[1][0] == player.color and board[2][0] == player.color:
        return 1, player
    elif board[0][1] == player.color and board[1][1] == player.color and board[2][1] == player.color:
        return 1, player
    elif board[0][2] == player.color and board[1][2] == player.color and board[2][2] == player.color:
        return 1, player
    # diagonal win?
    elif board[0][0] == player.color and board[1][1] == player.color and board[2][2] == player.color:
        return 1, player
    elif board[0][2] == player.color and board[1][1] == player.color and board[2][0] == player.color:
        return 1, player
    for i in board:
        for j in i:
            if j == 0:
                free += 1
    if free > 0:
        return -1, player
    else:
        return 0, player