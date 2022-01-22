import numpy as np
from Experience import Experience
from Player import Player
from Game import Game

feature = [x for x in range(7)]
gameSeq = []
w = 0.1 * np.ones(6)


class Learner:
    learningRate = 0.01
    weights = []
    Xwins = 0
    Owins = 0
    draws = 0

    def readStates(self):
        filename = "board_statess.txt"  # Reading the file
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

    def vCap(self, boardstate):
        game = Game()
        feature[0] = 1
        feature[1], feature[2] = game.feature12(
            boardstate)  # Feature 1 is 'x' in the same row as two 'o' & Feature 2 the viceversa
        feature[3], feature[4] = game.feature34(
            boardstate)  # Feature 3 is # of two 'x' per row & Feature 4 to is # of two 'o' per row
        feature[5], feature[6] = game.feature56(
            boardstate)  # Feature 5 is # of three 'x' & Feature 6 to is # of three 'o' per row

        vHat = 0;
        for i in range(6):
            vHat = vHat + w[i] * feature[i];
        return vHat

    # checking the win status to assign values for the calculation of weights
    def winCheck(self, boardstate):
        game = Game()
        xWin, oWin = game.feature56(boardstate)  # Feature 5 is # of three 'x' & Feature 6 to is # of three 'o' per row
        self.Xwins += xWin
        self.Owins += oWin
        target = 100 if xWin > 0 else -100 if oWin > 0 else 0
        if target == 0:
            self.draws += 1
        return target

    def checkStart(self, boardstate):
        game = Game()
        x, o = game.feature56(boardstate)  # Feature 5 is # of three 'x' & Feature 6 to is # of three 'o' per row
        target = 1 if x > o else 2
        return target

    def calculateweights(self, game):

        for row in range(len(game)):
            index = len(game[row]) - 1  # Calculating weights from the final board state
            start = self.checkStart(game[row][index])
            vTrain = self.winCheck(game[row][index])  # getting the Vtrain value based on the win status of the game
            index = len(game[row]) - start
            while index > -1:

                boardstate = game[row][index]

                for i in range(6):
                    vhat = self.vCap(boardstate)  # Calculating the vhat for the current board state
                    w[i] += (self.learningRate * (vTrain - vhat) * feature[i])  # updating the weights
                vTrain = vhat  # Updating the Vtrain value with the Vhat for the next best move
                index -= 2

    def printSummary(self, game):
        print('Win percentage = ', 10 * self.Xwins / len(game))
        print('Loss percentage = ', 10 * self.Owins / len(game))
        print('Draw percentage = ', 100 * self.draws / len(game), '\n')

    def main(self):
        flag = True
        play = Player()
        option = int(input("1. Teacher Mode\n2. Non Teacher mode\nOption:"))
        if option == 1:
            self.readStates()  # Reading games from the board_states.txt file
            self.calculateweights(gameSeq)
            self.weights = w
            print('\n', self.weights, '\n')
            self.printSummary(gameSeq)
        elif option == 2:
            # Generating random games for Non teacher mode
            obj = Experience()
            trainingData = obj.testGenerator()
            print(trainingData)
            self.calculateweights(trainingData)
            self.printSummary(trainingData)
            print('\n', w, '\n')
        else:
            print('Invalid Entry')
            flag = False

        if flag == True:
            print("\n\nPlaying Game\n")
            play.initGame(w)


l = Learner()
l.main()