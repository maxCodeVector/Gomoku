import numpy as np
import random
import queue
import time
from operator import *

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0



S = [[0, 0, 0, 0, 16000], [0, 5, 20, 600, 16000], [1, 30, 60, 800, 16000]]
L = [[0, 0, 0, 0, 4000], [0, 1, 10, 40, 4000], [0, 20, 30, 500, 4000]]


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out, use_ab=True):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not exceed the time limit
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of
        # your candidate_list as your decision .
        self.candidate_list = []
        self.self_chess = np.zeros((chessboard_size, chessboard_size, 5))
        self.other_chess = np.zeros((chessboard_size, chessboard_size, 5))
        self.step = 0
        self.fail = 0
        self.use_ab = use_ab
        # if color == COLOR_BLACK:
        #     # L[1][2] = 10
        #     # L[2][1] = 10
        #     S[1][2] = 30
        #     self.use_ab = True

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list
        self.step += 1
        self.candidate_list.clear()
        if self.use_ab:
            action = self.ab_search(chessboard, d=5, eval_fn=self.eval_fn)
            if action:
                self.candidate_list.append((action[0], action[1]))
        if len(self.candidate_list) == 0:
            self.__random_p(chessboard)
        # self.predict()

    def predict(self):
        if self.fail > 1:
            exit(0)

    def __random_p(self, chessboard):
        # mid = self.chessboard_size >> 1
        # if chessboard[6][4] == COLOR_NONE:
        #     self.candidate_list.append((6, 4))
        #     return
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

    def search(self, chessboard, FIFq, checked, role=None):
        if not role:
            role = self.color
        while not FIFq.empty():
            node = FIFq.get()
            if chessboard[node[0]][node[1]] == COLOR_NONE:
                target1 = self.self_chess[node[0]][node[1]]
                target2 = self.other_chess[node[0]][node[1]]
                det = self.__analyze(node, chessboard, role=role)
                det(target1, self.color)
                det(target2, self.color * -1)
            for child in self.get_childs(node):
                if not checked[child[0]][child[1]] and child[2] < 3:
                    FIFq.put(child)
                    checked[child[0]][child[1]] = 1

    def __initial_queue(self, chessboard):
        self.fail = 0
        size = self.chessboard_size
        checked = [[0] * size for _ in range(size)]
        FIFq = queue.Queue(maxsize=self.chessboard_size**2)
        for i in range(size):
            for j in range(size):
                if chessboard[i][j] != COLOR_NONE:
                    FIFq.put((i, j, 0))
                    checked[i][j] = 1
                self.self_chess[i][j] = 0
                self.other_chess[i][j] = 0
        return FIFq, checked

    def __analyze(self, node, chessboard: list, role=None):
        size = self.chessboard_size
        r1 = range(node[0] - 1, max(node[0] - 6, -1), -1)
        r2 = range(node[0] + 1, min(node[0] + 6, size))
        r3 = range(node[1] - 1, max(node[1] - 6, -1), -1)
        r4 = range(node[1] + 1, min(node[1] + 6, size))
        if not role:
            role = self.color

        def detect(target: list, color: int):
            d1 = (list(zip([node[0]] * 5, r3)), list(zip([node[0]] * 5, r4)))
            d2 = (list(zip(r1, [node[1]] * 5)), list(zip(r2, [node[1]] * 5)))
            d3 = (list(zip(r1, r3)), list(zip(r2, r4)))
            d4 = (list(zip(r1, r4)), list(zip(r2, r3)))
            if color == role:
                SL = S
            else:
                SL = L
            tag = [0, 0]
            i = 0
            for dir in [d1, d2, d3, d4]:
                w = self.score(chessboard, dir, color)
                if w[0] == 2 and w[1] == 2:
                    tag[0] += 1
                if w[0] == 1 and w[1] == 3:  # rush 4
                    tag[1] += 1
                if w[2]:
                    target[i] = SL[w[0]][w[1]] - 10
                else:
                    target[i] = SL[w[0]][w[1]]
                i += 1
            if tag[1] + tag[0] > 1:
                if color == role:
                    if tag[1] == 0:
                        target[4] = 300 - tag[0] * 60 - tag[1] * 80
                    else:
                        target[4] = 700 - tag[0] * 60 - tag[1] * 80
                else:
                    if tag[1] == 0:
                        target[4] = 200 - tag[0] * SL[2][2] - tag[1] * SL[1][3]
                    else:
                        target[4] = 400 - tag[0] * SL[2][2] - tag[1] * SL[1][3]

        return detect

    def score(self, chessboard, dir, color):
        def __number(dir, tag=None):
            w1, w2, space1, space2 = (0, 0, 0, 0)
            for indx in dir[0]:
                if chessboard[indx[0]][indx[1]] == color:
                    w1 += 1
                elif chessboard[indx[0]][indx[1]] == COLOR_NONE:
                    if tag == 0:
                        tag = 1
                    else:
                        space1 = 1
                        break
                else:
                    break
            for indx in dir[1]:
                if chessboard[indx[0]][indx[1]] == color:
                    w2 += 1
                elif chessboard[indx[0]][indx[1]] == COLOR_NONE:
                    space2 = 1
                    break
                else:
                    break
            chesses = min(w1 + w2, 4)
            level = space1 + space2
            if tag and chesses == 3 and level == 2:
                level = 1
            return level, chesses

        res_rl = [__number(dir, tag=0), __number([dir[1], dir[0]], tag=0)]
        nojump = __number(dir)
        res_rl.sort(key=lambda x: S[x[0]][x[1]])
        temp_score = S[res_rl[1][0]][res_rl[1][1]] - 10
        if 4 > res_rl[1][1] > 1 and S[nojump[0]][nojump[1]] < temp_score:
            return res_rl[1][0], res_rl[1][1], True
        else:
            return nojump[0], nojump[1], None

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

    def ini_ab_search(self, state, role):
        fifq, visted = self.__initial_queue(state)
        self.search(state, fifq, visted, role=role)
        des = []
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                score = self.self_chess[i][j].sum()
                score2 = self.other_chess[i][j].sum()
                if score >= 5 or score2 >= 5:
                    des.append((i, j, max(score, score2), min(score, score2)))
                # s = max(score, score2)
                # if s > 0:
                #     des.append((i, j, s))
        # des.sort(key=lambda x: x[2])
        des = sorted(des, key=itemgetter(2, 3), reverse=True)
        if len(des) > 9:
            des = des[0:10]
        return des

    def ab_search(self, chessboard, d=4, cutoff_test=None, eval_fn=None):
        infinity = 10000
        FIFq = self.ini_ab_search(chessboard, self.color)

        if len(FIFq) != 0:
            self.candidate_list.append(FIFq[0][0:2])
            if FIFq[0][2] > 500:
                return

        def max_value(action, alpha, beta, depth):
            v = -infinity
            fifq = self.ini_ab_search(chessboard, self.color)[0:4]
            if cutoff_test(action, depth):
                return -eval_fn(chessboard, fifq, -self.color)
            for node in fifq:
                if chessboard[node[0]][node[1]] == COLOR_NONE:
                    chessboard[node[0]][node[1]] = self.color
                    v = max(v, min_value(node, alpha, beta, depth + 1))
                    chessboard[node[0]][node[1]] = COLOR_NONE
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v

        def min_value(action, alpha, beta, depth):
            v = infinity
            fifq = self.ini_ab_search(chessboard, -self.color)[0:4]
            if cutoff_test(action, depth):
                return eval_fn(chessboard, fifq, self.color)
            for node in fifq:
                if chessboard[node[0]][node[1]] == COLOR_NONE:
                    chessboard[node[0]][node[1]] = -self.color
                    v = min(v, max_value(node, alpha, beta, depth + 1))
                    chessboard[node[0]][node[1]] = COLOR_NONE
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v

        cutoff_test = (cutoff_test or (lambda action, depth: depth >= d or self.terminal_test(action)))

        best_score = -infinity
        beta = infinity
        best_action = None
        for node in FIFq:
            if chessboard[node[0]][node[1]] == COLOR_NONE:
                chessboard[node[0]][node[1]] = self.color
                v = min_value(node, best_score, beta, 1)
                chessboard[node[0]][node[1]] = COLOR_NONE
                if v > best_score:
                    best_score = v
                    best_action = node
        return best_action

    def terminal_test(self, action):
        return action[2] > 3500

    def eval_fn(self, state, fifq, color):
        res1 = self.__eval_board(state, color)
        res1 = np.array(res1[0][4:] + res1[1][1:] + res1[2][1:])
        weight = np.array([1600, 10, 20, 50, 1600, 20, 50, 1200, 1600])
        # weight2 = np.array([20, 30, 60, 600, 50, 700, 300, 600])
        score1 = np.dot(weight, res1.T)
        if len(fifq) != 0:
            other = fifq[0][0:2]
            state[other[0]][other[1]] = -color
            res2 = self.__eval_board(state, -color)
            state[other[0]][other[1]] = COLOR_NONE
        else:
            res2 = self.__eval_board(state, -color)
        res2 = np.array(res2[0][4:] + res2[1][1:] + res2[2][1:])
        score2 = np.dot(weight, res2.T)
        return score1 - score2

    def __eval_board(self, chessboard, role):
        record = [[0] * 5, [0] * 5, [0] * 5]
        size = chessboard.shape[0]
        tag = [0, 0, 0]

        def match(i, j, tag):
            if chessboard[i][j] == COLOR_NONE:
                if tag[2]:  # have not started numbering
                    tag[0] = 1
                else:
                    tag[0] += 1
                    level = min(tag[1] - 1, 4)
                    record[tag[0]][level] += 1
                    tag[0] = 0
                    tag[1] = 0
                    tag[2] = 1  # typ, num, nend
            elif chessboard[i][j] == role:
                tag[2] = 0  # means start numbering!
                tag[1] += 1
                if j == size - 1 or i == size - 1:
                    level = min(tag[1] - 1, 4)
                    record[tag[0]][level] += 1
            else:
                if tag[2]:  # have not started numbering
                    tag[0] = 0
                else:
                    level = min(tag[1] - 1, 4)
                    record[tag[0]][level] += 1
                    tag[0] = 0
                    tag[1] = 0
                    tag[2] = 1  # typ, num, nend

        for i in range(size):
            tag[0] = 0
            tag[1] = 0
            tag[2] = 1
            for j in range(size):
                match(i, j, tag)
            tag[0] = 0
            tag[1] = 0
            tag[2] = 1
            for j in range(size):
                match(j, i, tag)

        for bias in range(1 - size, 0):
            tag[0] = 0
            tag[1] = 0
            tag[2] = 1  # typ, num, nend
            for i in range(-bias, size):
                match(i, i + bias, tag)
        for bias in range(0, size):
            tag[0] = 0
            tag[1] = 0
            tag[2] = 1
            for j in range(bias, size):
                match(j - bias, j, tag)

        for bias in range(0, size):
            tag[0] = 0
            tag[1] = 0
            tag[2] = 1  # typ, num, nend
            for i in range(0, bias + 1):
                match(i, -i + bias, tag)
        for bias in range(size, 2 * size - 1):
            tag[0] = 0
            tag[1] = 0
            tag[2] = 1
            for i in range(bias - size + 1, size):
                match(i, -i + bias, tag)

            # for j in range(size):
            #     typ, num, nend = (0, 0, 1)
            #     for i in range(size):
            #         if chessboard[i][j] == COLOR_NONE:
            #             if nend:  # have not started numbering
            #                 typ = 1
            #             else:
            #                 typ += 1
            #                 level = min(num - 1, 4)
            #                 record[typ][level] += 1
            #                 typ, num, nend = (0, 0, 1)
            #         elif chessboard[i][j] == role:
            #             nend = 0  # means start numbering!
            #             num += 1
            #             if j == size:
            #                 level = min(num - 1, 4)
            #                 record[typ][level] += 1
            #         else:
            #             if nend:
            #                 typ = 0
            #             else:
            #                 level = min(num - 1, 4)
            #                 record[typ][level] += 1
            #                 typ, num, nend = (0, 0, 1)

        return record
