from random import shuffle
import numpy as np

from tic_tac.Game import Game

board = [' ' for x in range(10)]

playUntil = 0
nextFlag = True

x_win = 0
o_win = 0
draw_match = 0
feature = [x for x in range(7)]
initState = '123456789'
w = 0.1 * np.ones(6)


def inputWithPosition(letter, pos):
    board[pos] = letter


def checkIfBlank(pos):
    return board[pos] == ' '


def displayBoard(board):
    print("\n")
    print(board[1] + " | " + board[2] + " | " + board[3] + "     1 | 2 | 3")
    print('---------     ---------')
    print(board[4] + " | " + board[5] + " | " + board[6] + "     4 | 5 | 6")
    print('---------     ---------')
    print(board[7] + " | " + board[8] + " | " + board[9] + "     7 | 8 | 9")
    print("\n")



def checkIfWon(bo, le):
    return (bo[7] == le and bo[8] == le and bo[9] == le) or (bo[4] == le and bo[5] == le and bo[6] == le) or (
                bo[1] == le and bo[2] == le and bo[3] == le) or (bo[1] == le and bo[4] == le and bo[7] == le) or (
                       bo[2] == le and bo[5] == le and bo[8] == le) or (
                       bo[3] == le and bo[6] == le and bo[9] == le) or (
                       bo[1] == le and bo[5] == le and bo[9] == le) or (bo[3] == le and bo[5] == le and bo[7] == le)


def playerMove():
    run = True
    while run:
        move = input('Please select a position to place an \'X\' (1-9): ')
        try:
            move = int(move)
            if move > 0 and move < 10:
                if checkIfBlank(move):
                    run = False
                    inputWithPosition('X', move)
                else:
                    print('Sorry, this space is occupied!')
            else:
                print('Please type a number within the range!')
        except:
            print('Please type a number!')


def validate_move():
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
    move = 0

    for let in ['O', 'X']:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let
            if checkIfWon(boardCopy, let):
                move = i
                return move

    cornersOpen = []
    for i in possibleMoves:
        if i in [1, 3, 7, 9]:
            cornersOpen.append(i)

    if len(cornersOpen) > 0:
        move = selectRandom(cornersOpen)
        return move

    if 5 in possibleMoves:
        move = 5
        return move

    edgesOpen = []
    for i in possibleMoves:
        if i in [2, 4, 6, 8]:
            edgesOpen.append(i)

    if len(edgesOpen) > 0:
        move = selectRandom(edgesOpen)

    return move



def playMove(state):
        print("state...",state)
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
    game = Game()
    feature[0] = 1

    feature[1], feature[2] = game.feature12(boardstate)  # Feature 1 is # of 'X' & Feature 2 to is # of 'O'
    feature[3], feature[4] = game.feature34(boardstate)  # Feature 3 is # of two 'X' per row & Feature 4 to is # of two 'O' per row
    feature[5], feature[6] = game.feature56(boardstate)  # Feature 5 is # of three 'X' & Feature 6 to is # of three 'O' per row
    vHat = 0
    for i in range(6):
        vHat = vHat + w[i] * feature[i];
    return vHat


def selectRandom(li):
    import random
    ln = len(li)
    r = random.randrange(0, ln)
    print("random ",li,r)
    return li[r]


def checkIsBoardNotEmpty(board):
    if board.count(' ') > 1:
        return False
    else:
        return True


def main():
    print('Welcome to Tic Tac Toe!')
    displayBoard(board)
    global x_win
    global o_win
    global draw_match

    #----------
    seq = []

    index = 0
    randlist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    shuffle(randlist)  # Randomize the slot list
    game = Game()
    toggle = 1
    state = initState  # Reset board state

    while not (checkIsBoardNotEmpty(board)):
        if not (checkIfWon(board, 'O')):
            playerMove()
            displayBoard(board)

        else:
            o_win =+ 1
            print('Sorry, O\'s won this time!')
            break

        if not (checkIfWon(board, 'X')):
            #move = validate_move()
            #pos = playMove(state)

            move = playMove(state)
            temp = list(state)
            player = 'X' if toggle % 2 == 1 else 'O'  # Toggle between x & o
            temp[move] = player  # marking an empty slot on the board
            state = ''.join(temp)
            seq.append(state)
            win = game.checkWin(index, state)

            print('Computer plays at', move)

            print("winnwe",win)
            if move == 0:
                print('Tie Game!')
                draw_match += 1
            else:
                inputWithPosition('O', move)
                print('Computer placed an \'O\' in position', move, ':')
                displayBoard(board)
        else:
            x_win += 1
            print('X\'s won this time! Good Job!')
            break

    if checkIsBoardNotEmpty(board):
        print('Tie Game!')

def selectoption():

    global playUntil
    global nextFlag
    global board
    option = int(input("1. Teacher Mode\n2. Non Teacher mode\nOption:"))

    if option == 1:
        print("Not implemented")
    elif option == 2:
        gameshouldwork = input('Enter number of time the game should work : ')
        playUntil = gameshouldwork
        spam = 0
        while spam < int(playUntil):
            spam = spam + 1
            board = [' ' for x in range(10)]
            print("==============================")
            print("Playing game count ",spam)
            print("===============================")
            main()
            printwinningpercentage(int(playUntil))

def printwinningpercentage(game):
    global x_win
    global o_win
    global draw_match
    print(game)

    print('Win percentage = ', 100 * x_win / game)
    print('Loss percentage = ', 100 * o_win / game)
    print('Draw percentage = ', 100 * draw_match / game, '\n')


selectoption()



#while True:
#    answer = input('Do you want to play again? (Y/N)')
#    if answer.lower() == 'y' or answer.lower == 'yes':
#        board = [' ' for x in range(10)]
#        print('-----------------------------------')
#       main()
#    else:
#        break