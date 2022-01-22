import numpy as np

# Combinations of winning sequences
winComb = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]])


class Game(object):

    # Printing in a tabular format
    def printgame(self, state):
        print(state[0], ' ', state[1], ' ', state[2])
        print(state[3], ' ', state[4], ' ', state[5])
        print(state[6], ' ', state[7], ' ', state[8])
        print('\n')

    '''
    Feature Extraction
    '''

    # Feature evaluation for blocking two 'x's or two 'o's
    def feature12(self, st):
        x = 0
        o = 0
        for f in winComb:
            # Feature 1 is one 'x' in the same row as two 'o'
            if (st[f[0] - 1] == 'o' and st[f[1] - 1] == 'o' and st[f[2] - 1] == 'x') or (
                    st[f[0] - 1] == 'x' and st[f[1] - 1] == 'o' and st[f[2] - 1] == 'o') or (
                    st[f[0] - 1] == 'o' and st[f[2] - 1] == 'x' and st[
                f[2] - 1] == 'o'):  # comparing combination of the boardstate with winning combination array
                x += 2

                # Feature 2 is one 'o' in the same row as two 'x'
            if (st[f[0] - 1] == 'x' and st[f[1] - 1] == 'x' and st[f[2] - 1] == 'o') or (
                    st[f[0] - 1] == 'o' and st[f[1] - 1] == 'x' and st[f[2] - 1] == 'x') or (
                    st[f[0] - 1] == 'x' and st[f[1] - 1] == 'o' and st[
                f[2] - 1] == 'x'):  # comparing combination of the boardstate with winning combination array
                o += 2
        return x, o

        # Feature evaluation for two 'x' & 'o' per row

    def feature34(self, st):
        x = 0
        o = 0
        for f in winComb:
            if (st[f[0] - 1] == 'x' and st[f[1] - 1] == 'x') or (st[f[1] - 1] == 'x' and st[f[2] - 1] == 'x') or (
                    st[f[0] - 1] == 'x' and st[
                f[2] - 1] == 'x'):  # comparing combination of the boardstate with winning combination array
                x += 0.2

            if (st[f[0] - 1] == 'o' and st[f[1] - 1] == 'o') or (st[f[1] - 1] == 'o' and st[f[2] - 1] == 'o') or (
                    st[f[0] - 1] == 'o' and st[
                f[2] - 1] == 'o'):  # comparing combination of the boardstate with winning combination array
                o += 0.2;
        return x, o  # returns number of two 'x' & 'o' per row

    # Feature evaluation for three 'x' & 'o' per row
    def feature56(self, st):
        x = 0
        o = 0
        for f in winComb:
            if st[f[0] - 1] == 'x' and st[f[1] - 1] == 'x' and st[
                f[2] - 1] == 'x':  # comparing combination of the boardstate with winning combination array
                x += 10

            if st[f[0] - 1] == 'o' and st[f[1] - 1] == 'o' and st[
                f[2] - 1] == 'o':  # comparing combination of the boardstate with winning combination array
                o += 10;
        return x, o  # returns number of three 'x' & 'o' per row

    def checkWin(self, index, state):
        x, o = self.feature56(state)
        outcome = True if x > 0 else True if o > 0 else False
        if index == 9:
            return True
        if outcome == False and index < 9:
            return False
        return outcome