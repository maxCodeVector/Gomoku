import numpy as np
import random
import queue
import time
from operator import *

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(time.time())

S = [[0, 0, 0, 0, 16000], [0, 5, 20, 60, 16000], [1, 30, 60, 800, 16000]]
L = [[0, 0, 0, 0, 4000], [0, 1, 10, 40, 4000], [0, 20, 30, 500, 4000]]


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of
        # your candidate_list as your decision .
        self.candidate_list = []

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()

        if len(self.candidate_list) == 0:
            self.__random_p(chessboard)

    def __random_p(self, chessboard):
        random.seed(time.time())
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        pos_idx = random.randint(0, len(idx) - 1)
        new_pos = idx[pos_idx]
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)

    def alpha_beta_cutoff_search(self, state, game, d=4, cutoff_test=None, eval_fn=None):
        infinity = 10000

        player = game.to_move(state)

        def max_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(state)

            v = -infinity
            for action in game.actions(state):
                v = max(v, min_value(game.result(state, action),
                                     alpha, beta, depth + 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(state)

            v = infinity
            for action in game.actions(state):
                v = min(v, max_value(game.result(state, action),
                                     alpha, beta, depth + 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        cutoff_test = (cutoff_test or
                       (lambda action, depth: depth >= d or game.terminal_test(state)))

        eval_fn = eval_fn or (lambda state: game.utility(state, player))

        best_score = -infinity
        beta = infinity
        best_action = None

        for action in game.actions(state):
            v = min_value(game.result(state, action), best_score, beta, 1)
            if v > best_score:
                best_score = v
                best_action = action
        return best_action

    def get_childs(self, node):
        res = []
        size = self.chessboard_size - 1
        tag = node[2] + 1
        if node[0] > 0:
            res.append((node[0] - 1, node[1], tag))
            if node[1] < size:
                res.append((node[0] - 1, node[1] + 1, tag))
            if node[1] > 0:
                res.append((node[0] - 1, node[1] - 1, tag))
        if node[1] > 0:
            res.append((node[0], node[1] - 1, tag))
        if node[0] < size:
            res.append((node[0] + 1, node[1], tag))
            if node[1] < size:
                res.append((node[0] + 1, node[1] + 1, tag))
            if node[1] > 0:
                res.append((node[0] + 1, node[1] - 1, tag))
        if node[1] < size:
            res.append((node[0], node[1] + 1, tag))
        return res
