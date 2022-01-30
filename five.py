from graphics import *;
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
    win = GraphWin("Tic Tac Toe", 800, 800);
    winWidth = win.getWidth();
    winHeight = win.getHeight()
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
        board = Rectangle(Point(x, y), Point(x + width, y + height))
        return board

    def makeLine(self, p1, p2):
        line = Line(p1, p2)
        return line

    def makeCircle(self, x1, y1, x2, y2, radius):
        circle = Circle(Point(x1 + radius * (3 / 2), y1 + radius * (3 / 2)), radius)
        circle.draw(self.win)

        self.erasables.append(circle)

    def makeCross(self, x1, y1, x2, y2, radius):
        lineA = Line(Point(x1 + radius / 2, y1 + radius / 2), Point(x2 - radius / 2, y2 - radius / 2))
        lineA.setArrow("both")
        lineA.draw(self.win)

        lineB = Line(Point(x1 + radius / 2, y2 - radius / 2), Point(x2 - radius / 2, y1 + radius / 2))
        lineB.setArrow("both")
        lineB.draw(self.win)

        self.erasables.append(lineA)
        self.erasables.append(lineB)

    def makeDialog(self):
        centerX = self.winWidth / 2

        messageBox = Text(Point(centerX, (21 / 24) * self.winHeight), "Do you want to play again?")
        messageBox.setSize(16)

        buttonYes = Rectangle(Point(centerX - 60, (22 / 24) * self.winHeight),
                              Point(centerX - 10, (23 / 24) * self.winHeight))
        buttonNo = Rectangle(Point(centerX + 10, (22 / 24) * self.winHeight),
                             Point(centerX + 60, (23 / 24) * self.winHeight))

        msgYes = Text(Point(centerX - 35, (22.5 / 24) * self.winHeight), "Yes")
        msgNo = Text(Point(centerX + 35, (22.5 / 24) * self.winHeight), "No")

        objs = [messageBox, buttonYes, buttonNo, msgYes, msgNo]
        self.erasables.extend(objs)
        for obj in objs:
            obj.draw(self.win)

        ## Detect mouse on the dialogs -- Start
        while True:
            click = self.win.getMouse()
            x = click.getX()
            y = click.getY()
            p1 = buttonYes.getP1()
            p2 = buttonYes.getP2()
            p3 = buttonNo.getP1()
            p4 = buttonNo.getP2()
            if x > p1.getX() and x < p2.getX() and y > p1.getY() and y < p2.getY():
                self.clearErasables()
                self.makeGame()
            if x > p3.getX() and x < p4.getX() and y > p3.getY() and y < p4.getY():
                self.win.close()
                break
        ## -- End

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
                click = self.win.getMouse()
                x = click.getX()
                y = click.getY()
            else:
                slot = self.calculateNewPath(playerRecord2, playerRecord1)
                for key in self.keyMaps:
                    if self.keyMaps[key] == slot:
                        x = self.pointMaps[key][0] + 1
                        y = self.pointMaps[key][1] + 1
                playerRecord2 += str(slot)

            for row, col in itertools.product(range(self.squareNum), repeat=2):
                x1 = self.pointMaps[(row, col)][0]
                y1 = self.pointMaps[(row, col)][1]
                x2 = self.pointMaps[(row + 1, col + 1)][0]
                y2 = self.pointMaps[(row + 1, col + 1)][1]
                key = self.keyMaps[(row, col)]
                radius = (y2 - y1) / 3
                if x > x1 and y > y1 and x < x2 and y < y2 and usableSlots[key]:
                    if self.playerTurn:
                        self.makeCircle(x1, y1, x2, y2, radius)
                        playerRecord1 += str(key)
                    else:
                        self.makeCross(x1, y1, x2, y2, radius)

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

    def makeUI(self, border=True):

        titleLabel = Text(Point(self.winWidth / 2, (1 / 12) * self.winHeight), "Tic Tac Toe")
        titleLabel.setSize(26)
        titleLabel.draw(self.win)

        dynamicWidth_board = self.winWidth - ((2 / 6) * self.winWidth)
        dynamicHeight_board = self.winHeight - ((2 / 6) * self.winHeight)
        dynamicPoint_board = Point((1 / 6) * self.winWidth, (1 / 6) * self.winHeight)
        board = self.makeBoard(dynamicPoint_board.getX(), dynamicPoint_board.getY(), dynamicWidth_board,
                               dynamicHeight_board)

        if border:
            board.draw(self.win)

        for i in range(self.squareNum):
            ratio = dynamicWidth_board / self.squareNum

            p1 = Point(dynamicPoint_board.getX() + i * ratio, dynamicPoint_board.getY())
            p2 = Point(dynamicPoint_board.getX() + i * ratio, dynamicPoint_board.getY() + dynamicWidth_board)
            line = self.makeLine(p1, p2) if i > 0 else Line(Point(0, 0), Point(0, 0))
            line.draw(self.win)

            p1 = Point(dynamicPoint_board.getX(), dynamicPoint_board.getY() + i * ratio)
            p2 = Point(dynamicPoint_board.getX() + dynamicHeight_board, dynamicPoint_board.getY() + i * ratio)
            line = self.makeLine(p1, p2) if i > 0 else Line(Point(0, 0), Point(0, 0))
            line.draw(self.win)

        self.makeSystem(dynamicWidth_board, dynamicHeight_board)

    def main(self):
        self.makeUI(border=False)
        self.makeGame()

    def displayBoard(board):
        print("\n")
        print(board[1] + " | " + board[2] + " | " + board[3] + "     1 | 2 | 3")
        print('---------     ---------')
        print(board[4] + " | " + board[5] + " | " + board[6] + "     4 | 5 | 6")
        print('---------     ---------')
        print(board[7] + " | " + board[8] + " | " + board[9] + "     7 | 8 | 9")
        print("\n")


thisGame = Game()
thisGame.main()