
from random import shuffle
from Game import Game

feature = [x for x in range(7)]
gamePlays = []
initState = '123456789'


class Player(object):
    '''
    Plays the deciding move
    '''
    w = []
    Xwins = 0
    Owins = 0
    draws = 0

    '''
    Get the best state
    '''

    def vCap(self, boardstate):
        game = Game()
        feature[0] = 1

        feature[1], feature[2] = game.feature12(boardstate)  # Feature 1 is # of 'x' & Feature 2 to is # of 'o'
        feature[3], feature[4] = game.feature34(boardstate)  # Feature 3 is # of two 'x' per row & Feature 4 to is # of two 'o' per row
        feature[5], feature[6] = game.feature56(boardstate)  # Feature 5 is # of three 'x' & Feature 6 to is # of three 'o' per row
        vHat = 0
        for i in range(6):
            vHat = vHat + self.w[i] * feature[i];

        return vHat

    def checkEmpty(self, ch):
        return (ord(ch) >= 49 and ord(ch) <= 57)

    def playMove(self, state):
        maxValue = -100
        position = 0
        commonValues = []
        for i in range(9):
            if ord(state[i]) >= 49 and ord(state[i]) <= 57:
                temp = list(state)
                temp[i] = 'x'
                temp = ''.join(temp)
                v = self.vCap(temp)
                if maxValue < v:
                    maxValue = v
                    commonValues = []
                    commonValues.append(i)
                    position = i
                elif maxValue == v:
                    commonValues.append(i)

            shuffle(commonValues)
            position = commonValues[0] if commonValues else 0
        return position

    '''
    To initiate a game against human
    '''

    def playGame(self, var):
        seq = []
        state = initState  # Reset board state
        win = False
        index = 0
        randlist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        shuffle(randlist)  # Randomize the slot list
        toggle = var  # setting player 1
        game = Game()
        while (win == False and index < 9):
            if toggle % 2 == 1:

                print("state ....",state)
                pos = self.playMove(state)
                print('Computer plays at', pos + 1)
                index += 1
                temp = list(state)
                player = 'x' if toggle % 2 == 1 else 'o'  # Toggle between x & o
                temp[pos] = player  # marking an empty slot on the board
                state = ''.join(temp)
                seq.append(state)
                win = game.checkWin(index, state)  # Checking win or draw
                if win == True:
                    gamePlays.append(seq)
                    break
            else:
                # Human turn
                while True:  # checks if position is valid
                    pos = int(input("\nInput 'o' in pos: "))
                    if self.checkEmpty(state[pos - 1]):
                        break
                    else:
                        print('Invalid Position, Retry')

                index += 1
                temp = list(state)
                temp[pos - 1] = 'o'  # marking 'o' an slot inputed above on the board
                state = ''.join(temp)
                seq.append(state)
                win = game.checkWin(index, state)  # checking win status
                if win == True:
                    gamePlays.append(seq)
                    break
            toggle += 1
            Game().printgame(state)

    # Summary for games played
    def declareWinner(self, state):
        game = Game()
        xWin, oWin = game.feature56(state)  # Feature 5 is # of three 'x' & Feature 6 to is # of three 'o' per row
        game.printgame(state)
        # checking for win
        target = 1 if xWin > 0 else -1 if oWin > 0 else 0
        if target > 0:
            print('X wins')
            self.Xwins += 1
        elif target < 0:
            print('O wins')
            self.Owins += 1
        else:
            print('Draw match')
            self.draws += 1
        print('\n')

    # main method to intiate a game
    def initGame(self, weights):
        self.w = weights  # Getting the weights learnt
        gameCount = int(input("Enter Number of games to play:"))
        for i in range(gameCount):
            print('\nNew game:\n', i + 1)
            self.playGame(1)  # Calls the main method for playing a game
            seq = gamePlays[i][len(gamePlays[i]) - 1]  # Get the final board state
            self.declareWinner(seq)

        # Final summary of games played
        print('Computer Win percentage = ', 100 * self.Xwins / gameCount)
        print('Computer Loss percentage = ', 100 * self.Owins / gameCount)
        print('Draw percentage = ', 100 * self.draws / gameCount)