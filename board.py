import numpy as np
import random
import time
import os
import math
import chess as greed
import chess_tree as tree

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)

black = []
white = []


def cc():
    os.system("clear")


def change(ch):
    if ch == COLOR_NONE:
        return '_'
    elif ch == COLOR_WHITE:
        return 'o'
    else:
        return '*'


class Board(object):

    def __init__(self, size=15, blackboard=None):
        if blackboard:
            self.board = np.array(blackboard)
        else:
            self.board = np.zeros([size, size], int)
        self.dec = None

    def show(self):
        cc()
        print('next')
        size = self.board.shape[0]
        for x in range(size):
            for y in range(size):
                if self.dec:
                    if self.dec[0] == x and self.dec[1] == y:
                        print('\033[1;35m%s\033[0m' % change(self.board[x][y]), end=' ')
                    else:
                        print(change(self.board[x][y]), end=' ')
                else:
                    print(change(self.board[x][y]), end=' ')
            print()
        color = self.board[self.dec[0]][self.dec[1]]
        return self.judge(self.dec, color)

    def judge(self, node, color):
        size = self.board.shape[0]
        r1 = range(node[0] - 1, max(node[0] - 5, -1), -1)
        r2 = range(node[0] + 1, min(node[0] + 5, size))
        r3 = range(node[1] - 1, max(node[1] - 5, -1), -1)
        r4 = range(node[1] + 1, min(node[1] + 5, size))
        d1 = list(zip([node[0]] * 5, r3)), list(zip([node[0]] * 5, r4))
        d2 = list(zip(r1, [node[1]] * 5)), list(zip(r2, [node[1]] * 5))
        d3 = list(zip(r1, r3)), list(zip(r2, r4))
        d4 = list(zip(r1, r4)), list(zip(r2, r3))
        chessboard = self.board

        def __number(dir):
            w = 0
            for indx in dir[0]:
                if chessboard[indx[0]][indx[1]] == color:
                    w += 1
                else:
                    break
            for indx in dir[1]:
                if chessboard[indx[0]][indx[1]] == color:
                    w += 1
                else:
                    break
            return w >= 4

        for dir in (d1, d2, d3, d4):
            if __number(dir):
                return True
        return False

    def load(self, ai):
        diction = ai.candidate_list[-1]
        assert self.board[diction[0]][diction[1]] == COLOR_NONE
        self.board[diction[0]][diction[1]] = ai.color
        self.dec = diction

    def read(self, path, reverse=False):
        with open(path, 'rt') as f:
            li = f.readlines()
        for l in li:
            seg = l.split(',')
            if reverse:
                self.board[int(seg[0])][int(seg[1])] = -int(seg[2])
            else:
                self.board[int(seg[0])][int(seg[1])] = int(seg[2])


def main():
    size = 15
    time_delay = 1
    chessboard = Board(size)
    tree_ai = tree.AI(size, COLOR_BLACK, time_delay)
    greed_ai = greed.AI(size, COLOR_WHITE, time_delay)

    # chessboard.read('chess_log.txt')
    end1 = False
    end2 = False
    while not (end1 or end2):
        start1 = time.time()
        tree_ai.go(chessboard.board)
        cost1 = time.time() - start1
        chessboard.load(tree_ai)
        end1 = chessboard.show()
        black.append(cost1)
        if cost1 > 15:
            print('\033[1;35m * cost > 5s: %fs!\033[0m' % cost1)
            break
        # time.sleep(1)
        start = time.time()
        greed_ai.go(chessboard.board)
        cost = time.time()-start
        chessboard.load(greed_ai)
        end2 = chessboard.show()
        white.append(cost)
        # if cost > 15:
        #     print('\033[1;35m o cost > 5s: %fs!\033[0m' % cost)
        #     break
        # time.sleep(1)
    if end1:
        print("tree win")
    if end2:
        print("greedy win")


if __name__ == '__main__':
    main()