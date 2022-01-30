#from graphics import *;
import random;
import time;
import itertools;
import os;

'''
    Changelog 11/3/2015:
    -- Improved on how the program handle window closing.

    Changelog 9/3/2015:
    -- Code clean up a more modular design.
    -- Enhanced detection accuracy.
    -- Bug fixes

'''


class Game:
    option = int();
    intel = list();
    erasables = list();
    pointMaps = dict();
    keyMaps = dict();
    winningSequences = ["012", "345", "678", "036", "147", "258", "048", "246"]
    squareNum = 3;
    playerTurn = True
    board = [' ' for x in range(10)]

    def clearErasables(self):
        if len(self.erasables) > 0:
            for obj in self.erasables:
                obj.undraw()
            for obj in self.erasables:
                self.erasables.remove(obj)

    def makeBoard(self, x, y, width, height):
        return self.board



    def checkForWinner(self, track1, track2):
        for i in range(8):
            winningMove = self.winningSequences[i]
            if winningMove[0] in track1 and winningMove[1] in track1 and winningMove[2] in track1:
                return 1
            if winningMove[0] in track2 and winningMove[1] in track2 and winningMove[2] in track2:
                return 2

        return 0

    def calculateNewPath(self, playerRecordA, playerRecordB):
        slotsRecord = [0 for i in range(9)]
        openSlots = ""

        for i in range(9):
            if str(i) not in (playerRecordA + playerRecordB):
                openSlots += str(i)

        ExpandableChoices = openSlots

        for i in range(200):
            gameDidFinished = False
            localChoices = ExpandableChoices
            varyChoicesOldLength = len(ExpandableChoices)
            AIRecordA = playerRecordA
            AIRecordB = playerRecordB
            AITurnA = True

            while gameDidFinished == False:
                take = localChoices[random.randint(0, len(localChoices)) - 1]
                localChoices = localChoices.replace(take, "")

                if AITurnA:
                    AIRecordA += take
                    ExpandableChoices += take
                else:
                    AIRecordB += take

                ## Check for winner -- Start
                result = self.checkForWinner(AIRecordA, AIRecordB)
                if result == 1 or result == 2 or not localChoices:
                    gameDidFinished = True
                if result == 2:
                    ExpandableChoices = ExpandableChoices[0:varyChoicesOldLength]
                ## -- End

                AITurnA = not AITurnA

        for i in openSlots:
            slotsRecord[int(i)] = ExpandableChoices.count(i)

        return slotsRecord.index(sorted(slotsRecord, reverse=True)[0])

    def makeGame(self):
        usableSlots = [True for i in range(self.squareNum * self.squareNum)]
        gameDidFinished = False
        self.playerTurn = True
        playerRecord1 = ""
        playerRecord2 = ""
        while gameDidFinished == False:
            x = int()
            y = int()
            if self.playerTurn == True:
                click = self.board
                x = click
                y = click
            else:
                slot = self.calculateNewPath(playerRecord2, playerRecord1)
                for key in self.keyMaps:
                    if self.keyMaps[key] == slot:
                        x = self.pointMaps[key][0] + 1
                        y = self.pointMaps[key][1] + 1
                playerRecord2 += str(slot)

            for row, col in itertools.product(range(self.squareNum), repeat=2):


                    ## Checking for winning sequence -- starts
                    result = self.checkForWinner(playerRecord1, playerRecord2)
                    if result == 1 or result == 2:
                        gameDidFinished = True
                        print("Player1 won!" if self.playerTurn else "Player2 won!")
                    ## -- ends

                    usableSlots[key] = False
                    self.playerTurn = not self.playerTurn

            ##                    print("Square", (row, col), "--> (X:{:.2f},Y:{:.2f})".format(x1, y1))

            if sum(usableSlots) <= 0:
                gameDidFinished = True

        self.makeDialog()

    def makeSystem(self, boardWidth, boardHeight):
        widthRatio = boardWidth / self.squareNum
        heightRatio = boardHeight / self.squareNum
        for row, col in itertools.product(range(self.squareNum + 1), repeat=2):
            self.pointMaps[(row, col)] = (
            (1 / 6) * self.winWidth + col * widthRatio, (1 / 6) * self.winHeight + row * heightRatio)
        for i in range(self.squareNum * self.squareNum):
            self.keyMaps[(int(i / self.squareNum), i % self.squareNum)] = i

    ##        print(self.keyMaps)
    ##        print(self.pointMaps)


    def main(self):

        self.displayBoard(self.board)
        self.makeGame()

    def displayBoard(self,board):
        print("\n")
        print(board[1] + " | " + board[2] + " | " + board[3] + "     1 | 2 | 3")
        print('---------     ---------')
        print(board[4] + " | " + board[5] + " | " + board[6] + "     4 | 5 | 6")
        print('---------     ---------')
        print(board[7] + " | " + board[8] + " | " + board[9] + "     7 | 8 | 9")
        print("\n")


thisGame = Game()
thisGame.main()