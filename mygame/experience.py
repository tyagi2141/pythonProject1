from random import shuffle

from mygame.Game import checkWin

feature = [x for x in range(7)]
testgame = []
initState = '123456789'


def generateRandomStates(var):
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
        # print("state ",state)

        temp = list(state)
        player = 'X' if toggle % 2 == 0 else 'O'  # Toggle between x & o
        temp[pos - 1] = player  # marking an empty slot on the board
        state = ''.join(temp)
        seq.append(state)
        win = checkWin(index, state)  # Checking win or draw

        if win == True:
            testgame.append(seq)
            print("testgame", testgame)
            break


# Generate random states for Non teacher mode
def craete_x_and_0_data():
    for _ in range(20):
        generateRandomStates(1)  # Generate 20 games for x
    for _ in range(20):
        generateRandomStates(2)  # Generate 20 games for o
    return testgame
