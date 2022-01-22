import random
from player import Player
from tic import printBoard, weight_update, finished

weights = [1.0 for _ in range(7)]


player1 = Player('x')
player2 = Player('o')
# Learning rate from 0.1 is too damn high! use smaller learning rate
lr = 0.001
print('Start Training ...')
for i in range(10000):
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    while (True):
        pre_features = player1.get_board_features(board)
        pre_approx = player1.evalApproximation(pre_features, weights)
        # every second game the other player is beginning
        if i % 2 == 0:
            player1.make_move(board, weights)
            outcome = finished(board, player1)
            if outcome[0] != -1:
                break
            player2.make_move(board, weights)
            outcome = finished(board, player2)
            if outcome[0] != -1:
                break
        else:
            player2.make_move(board, weights)
            outcome = finished(board, player2)
            if outcome[0] != -1:
                break
            player1.make_move(board, weights)
            outcome = finished(board, player1)
            if outcome[0] != -1:
                break
        succ_features = player1.get_board_features(board)
        succ_approx = player1.evalApproximation(succ_features, weights)
        weight_update(weights=weights,learningConstant=lr, train_val=succ_approx, approx=pre_approx,
                        features=pre_features)
    if outcome[0] == 1 and outcome[1].color == 'o':
        result = -1
    elif outcome[0] == 0:
        result = 0
    elif outcome[0] == 1 and outcome[1].color == 'x':
        result = 1
    curr_features = player1.get_board_features(board)
    curr_approx = player1.evalApproximation(curr_features, weights)
    weight_update(weights=weights, learningConstant=lr, train_val=result, approx=curr_approx, features=pre_features)

print('Start Evaluation against Random Player')
count_win = 0
count_loss = 0
count_draw = 0
for i in range(1000):
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    # random start player
    start = random.randint(0, 1)
    while (True):
        if start == 1:
            player1.random_move(board)
            outcome = finished(board, player1)
            if outcome[0] != -1:
                break
            player2.random_move(board)
            outcome = finished(board, player2)
            if outcome[0] != -1:
                break
        else:
            player2.random_move(board)
            outcome = finished(board, player2)
            if outcome[0] != -1:
                break
            player1.random_move(board)
            outcome = finished(board, player1)
            if outcome[0] != -1:
                break
    if outcome[0] == 1 and outcome[1].color == 'o':
        result = -1
        count_loss += 1
    elif outcome[0] == 0:
        result = 0
        count_draw += 1
    elif outcome[0] == 1 and outcome[1].color == 'x':
        result = 1
        count_win += 1
print('Wins: ' + str(count_win))
print('Draws: ' + str(count_draw))
print('Loss: ' + str(count_loss))

print('Play yourself')
while(True):
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    start = random.randint(0, 1)
    x = input('Play? y or n: ')

    while(x not in ('y','n')):
        x = input('Play? y or n: ')

    if x == 'n':
        break

    while(True):
        if start == 0:
            print('Bot Move')
            printBoard(board)
            player1.make_move(board, weights)
            outcome = finished(board, player1)
            print(player1.get_board_features(board))
            if outcome[0] != -1:
                break
            print('Human Move')
            printBoard(board)
            player2.human_move(board)
            outcome = finished(board, player2)
            if outcome[0] != -1:
                break
        else:
            print('Human Move')
            printBoard(board)
            player2.human_move(board)
            outcome = finished(board, player2)
            if outcome[0] != -1:
                break
            print('Bot Move')
            printBoard(board)
            player1.make_move(board, weights)
            print(player1.get_board_features(board))
            outcome = finished(board, player1)
            if outcome[0] != -1:
                break

    if outcome[0] == 1 and outcome[1].color == 'o':
        print('Human won')
        printBoard(board)
    elif outcome[0] == 0:
        print('Draw')
        printBoard(board)
    elif outcome[0] == 1 and outcome[1].color == 'x':
        print('Bot won. Shame on you.')
        printBoard(board)