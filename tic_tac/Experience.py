from random import shuffle
from Game import Game

feature = [x for x in range(7)]
testgame = []
initState = '123456789'


class Experience:

    # Method to extract
    def generateRandomStates(self, var):
        game = Game()
        seq = []
        state = initState  # Reset board state
        win = False
        index = 0
        randlist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        shuffle(randlist)  # Randomize the slot list
        randindex = 0
        toggle = var  # setting player 1
        while (win == False and index < 9):
            toggle += 1
            pos = randlist[randindex]  # Enter into a random position
            randindex += 1
            index += 1
            #print("state ",state)

            temp = list(state)
            player = 'x' if toggle % 2 == 0 else 'o'  # Toggle between x & o
            temp[pos - 1] = player  # marking an empty slot on the board
            state = ''.join(temp)
            seq.append(state)
            win = game.checkWin(index, state)  # Checking win or draw

            if win == True:
                testgame.append(seq)
                print("testgame",testgame)
                break

    # Generate random states for Non teacher mode
    def testGenerator(self):
        for _ in range(20):
            self.generateRandomStates(1)  # Generate 20 games for x
        for _ in range(20):
            self.generateRandomStates(2)  # Generate 20 games for o
        return testgame

#l = Experience()
#l.testGenerator()