import numpy as np
import random

spot_placeholders = [0, 0, 0, 0, 0, 0, 0, 0, 0]


class Player():
    def __init__(self, name, start=False):
        self.values = {0: 0}
        self.name = name
        self.turn = start
        self.epsilon = 1


def get_action(player1, player2):
    global spot_placeholders

    """Find out which players turn it is, and set thier marker and epsilon."""
    if player1.turn == True:
        marker = 1
        epsilon = player1.epsilon
    else:
        marker = 2
        epsilon = player2.epsilon

    players = [player1, player2]
    possible_next_states = {}
    top_value = -1

    """loop through every spot and, if it's empty, record the state that
    would come from the player moving in that spot"""
    for i in range(len(spot_placeholders)):
        if spot_placeholders[i] == 0:
            copy = np.copy(spot_placeholders)
            copy[i] = marker
            s_p = state_to_num(copy)
            possible_next_states[i] = s_p

    """Epsilon greedy"""
    if np.random.rand() < epsilon:
        if players[marker - 1].epsilon > .05:
            players[marker - 1].epsilon -= .001
        return random.sample(possible_next_states.keys(), 1)[0]

    else:
        i = 0
        for state in possible_next_states.values():
            try:
                """if the current players value for this state is higher than the 
                top recorded value, set the top value to the value of this state 
                and set action = the spot that will lead to this state"""
                if players[marker - 1].values[state] > top_value:
                    top_value = players[marker - 1].values[state]
                    action = list(possible_next_states.keys())[i]
            except:
                pass
            i += 1

        if players[marker - 1].epsilon > .05:
            players[marker - 1].epsilon -= .001

        """if there was no action set, return a random action"""
        try:
            return action
        except:
            return random.sample(possible_next_states.keys(), 1)[0]


def state_to_num(state):
    N = state[0] + 3 * state[1] + 9 * state[2] + 27 * state[3] + 81 * state[4] + 243 * state[5] + 729 * state[
        6] + 2187 * state[7] + 6561 * state[8]
    return N



def check_for_winner():
    if spot_placeholders[0] == spot_placeholders[1] and spot_placeholders[1] == spot_placeholders[2] and \
            spot_placeholders[2] != 0:
        return True
    if spot_placeholders[0] == spot_placeholders[3] and spot_placeholders[3] == spot_placeholders[6] and \
            spot_placeholders[6] != 0:
        return True
    if spot_placeholders[0] == spot_placeholders[4] and spot_placeholders[4] == spot_placeholders[8] and \
            spot_placeholders[8] != 0:
        return True
    if spot_placeholders[1] == spot_placeholders[4] and spot_placeholders[4] == spot_placeholders[7] and \
            spot_placeholders[7] != 0:
        return True
    if spot_placeholders[2] == spot_placeholders[4] and spot_placeholders[4] == spot_placeholders[6] and \
            spot_placeholders[6] != 0:
        return True
    if spot_placeholders[2] == spot_placeholders[5] and spot_placeholders[5] == spot_placeholders[8] and \
            spot_placeholders[8] != 0:
        return True
    if spot_placeholders[6] == spot_placeholders[7] and spot_placeholders[7] == spot_placeholders[8] and \
            spot_placeholders[8] != 0:
        return True
    if spot_placeholders[3] == spot_placeholders[4] and spot_placeholders[4] == spot_placeholders[5] and \
            spot_placeholders[5] != 0:
        return True
    elif (spot_placeholders[0] != 0 and spot_placeholders[1] != 0 and
          spot_placeholders[2] != 0 and spot_placeholders[3] != 0 and
          spot_placeholders[4] != 0 and spot_placeholders[5] != 0 and
          spot_placeholders[6] != 0 and spot_placeholders[7] != 0 and
          spot_placeholders[8] != 0):
        return 'CatGame'
    else:
        return False


def play_game(player1, player2):
    global spot_placeholders
    state_history = []
    if np.random.rand() >= .5:
        player1.turn = True
    player2.turn = not player1.turn

    while True:

        if player1.turn == True:
            a = get_action(player1, player2)
            spot_placeholders[a] = 1
            state_history.append(state_to_num(spot_placeholders))

            if check_for_winner() == True:
                # print('Winner = ' + player1.name)
                spot_placeholders = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                update_values(player1, state_history, True)
                update_values(player2, state_history)
                break

        if player2.turn == True:
            a = get_action(player1, player2)
            spot_placeholders[a] = 2
            state_history.append(state_to_num(spot_placeholders))

            if check_for_winner() == True:
                # print('Winner = ' + player2.name)
                spot_placeholders = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                update_values(player2, state_history, True)
                update_values(player1, state_history)

                break

        if check_for_winner() == 'CatGame':
            # print('CatGame!')
            spot_placeholders = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            update_values(player1, state_history)
            update_values(player2, state_history)
            break

        player1.turn = not player1.turn
        player2.turn = not player2.turn


def update_values(player, state_history, winner=False):
    player.values[state_history[-1]] = -1
    if winner == True:
        player.values[state_history[-1]] = 1

    for state in state_history:
        if state not in player.values:
            player.values[state] = 0

    for i in range(len(state_history) - 1, 0, -1):
        player.values[state_history[i - 1]] += .1 * (
                    player.values[state_history[i]] - player.values[state_history[i - 1]])


p1 = Player('Computer 1', True)
p2 = Player('Computer 2')

for i in range(100000):
    play_game(p1, p2)
    if i % 10000 == 0:
        print(i)


def print_board():
    board = []
    for spot in spot_placeholders:
        if spot == 0:
            board.append('_')
        if spot == 1:
            board.append('X')
        if spot == 2:
            board.append('O')
    print(board[0], board[1], board[2])
    print(board[3], board[4], board[5])
    print(board[6], board[7], board[8])


def test(computer):
    global spot_placeholders

    p1.turn = True
    p2.turn = False
    p1.epsilon = 0
    p2.epsilon = 0

    while True:
        if computer.turn == True:
            a = get_action(p1, p2)
            spot_placeholders[a] = 1

            if check_for_winner() == True:
                print('You Lose!')
                print_board()
                spot_placeholders = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                break
        else:
            print_board()
            while True:
                action = int(input('Where would you like to go?\n Move: '))
                if spot_placeholders[action] == 0:
                    spot_placeholders[action] = 2
                    break
                else:
                    continue
            if check_for_winner() == True:
                print('You Win!')
                spot_placeholders = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                break
        if check_for_winner() == 'CatGame':
            print('CatGame!')
            spot_placeholders = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            break

        p1.turn = not p1.turn
        p2.turn = not p2.turn


while True:
    place = input('Would you like to go first or second? Input 1 or 2.\nInput:')
    if place == '1':
        test(p2)
    else:
        test(p1)