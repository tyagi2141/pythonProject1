from random import shuffle
import numpy as np

from mygame.Game import feature56, checkIfWon
from mygame.Player import vCap, feature, playMove
from mygame.experience import  craete_x_and_0_data

playUntil = 0
nextFlag = True

x_win = 0
o_win = 0
draw_match = 0
initState = '123456789'
w = 0.1 * np.ones(6)
gameSeq = []
learningRate = 0.01

board = [' ' for x in range(10)]



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


def inputWithPosition(letter, pos):
    board[pos] = letter


def checkIfBlank(pos):
    return board[pos] == ' '




def readStates():
    filename = "board_states.txt"  # Reading the file
    fp = open(filename, "r")
    while True:
        line = fp.readline()
        if line == "":
            break
        line_split = line.split('\n')  # Splitting each line
        for i in line_split:
            if i == "":
                break
            state = (i.split(' '))  # Splitting each board state
            gameSeq.append(state)
    fp.close()

def checkStart(boardstate):

        x, o = feature56(boardstate)  # Feature 5 is # of three 'x' & Feature 6 to is # of three 'o' per row
        target = 1 if x > o else 2
        return target

def winCheck(boardstate):
        global x_win ,o_win,draw_match
        xWin, oWin = feature56(boardstate)  # Feature 5 is # of three 'x' & Feature 6 to is # of three 'o' per row
        x_win += xWin
        o_win += oWin
        target = 100 if xWin > 0 else -100 if oWin > 0 else 0
        if target == 0:
            draw_match += 1
        return target

def calculateweights(game):

        global learningRate
        for row in range(len(game)):
            index = len(game[row]) - 1  # Calculating weights from the final board state
            start = checkStart(game[row][index])
            vTrain = winCheck(game[row][index])  # getting the Vtrain value based on the win status of the game
            index = len(game[row]) - start
            while index > -1:
                boardstate = game[row][index]
                for i in range(6):
                    vhat = vCap(boardstate)  # Calculating the vhat for the current board state
                    w[i] += (learningRate * (vTrain - vhat) * feature[i])  # updating the weights
                vTrain = vhat  # Updating the Vtrain value with the Vhat for the next best move
                index -= 2


def possibleStep():
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
    for let in ['O', 'X']:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let
            if checkIfWon(boardCopy, let):
                move = i
                print("moves...to..be..taken..",move)
                return move


def validate_move():
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
    move = 0
    print("possibale move ..",possibleMoves)

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
    from mygame.Player import displayBoard
    #displayBoard(board)
    global x_win
    global o_win
    global draw_match

    #----------
    randlist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    shuffle(randlist)  # Randomize the slot list
    state = initState  # Reset board state

    index = 0
    toggle = 1
    seq = []
    while not (checkIsBoardNotEmpty(board)):
        if not (checkIfWon(board, 'X')):
            move = validate_move()

            #move = playMove(possibleMoves)

            print('Computer plays at', move)
            index += 1
            temp = list(state)
            player = 'x' if toggle % 2 == 1 else 'o'  # Toggle between x & o
            temp[move] = player  # marking an empty slot on the board
            state = ''.join(temp)
            print("sequence",state)
            seq.append(state)


            # print("winnwe",win)
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

        if not (checkIfWon(board, 'O')):
            playerMove()
            displayBoard(board)
        else:
            o_win = + 1
            print('Sorry, O\'s won this time!')
            break








    if checkIsBoardNotEmpty(board):
        print('Tie Game!')

def selectoption():

    global playUntil
    global nextFlag
    global board
    option = int(input("1. Teacher Mode\n2. Non Teacher mode\nOption:"))

    if option == 1:
        gameshouldwork = input('Enter number of time the game should work : ')
        playUntil = gameshouldwork
        spam = 0

        readStates()  # Reading games from the board_states.txt file
        calculateweights(gameSeq)
        weights = w
        print('\n', weights, '\n')
        printpercentage(gameSeq)

        while spam < int(playUntil):
            spam = spam + 1
            board = [' ' for x in range(10)]
            print("==============================")
            print("Playing game count ", spam)
            print("===============================")
            main()


    elif option == 2:
        gameshouldwork = input('Enter number of time the game should work : ')
        playUntil = gameshouldwork
        spam = 0
        #printwinningpercentage(int(playUntil))
        trainingData = craete_x_and_0_data()
        print(trainingData)
        calculateweights(trainingData)
        printpercentage(trainingData)


        while spam < int(playUntil):
            spam = spam + 1
            board = [' ' for x in range(10)]
            print("==============================")
            print("Playing game count ",spam)
            print("===============================")
            main()


def printpercentage(game):
    global x_win
    global o_win
    global draw_match
    print(game)

    print('Win percentage = ', 10 * x_win / len(game))
    print('Loss percentage = ', 10 * o_win / len(game))
    print('Draw percentage = ', 100 * draw_match / len(game), '\n')


selectoption()

