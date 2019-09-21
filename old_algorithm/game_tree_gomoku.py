import numpy as np
import random
import time
import copy

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
infinity = 10000000
random.seed(0)
score_list_me = [[0 for _ in range(15)] for _ in range(15)]
score_list_he = [[0 for _ in range(15)] for _ in range(15)]
score_list_total = [[0 for _ in range(15)] for _ in range(15)]


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []
        self.chessboard = [[0 for _ in range(15)] for _ in range(15)]

    def first_chess(self):
        assert self.color == COLOR_BLACK
        self.candidate_list.clear()
        self.candidate_list.append((self.chessboard_size // 2, self.chessboard_size // 2))
        # self.chessboard[7][7] = self.color
        log = open('chess_log.txt')
        line = log.readline()
        while line:
            s = line.split(',')
            point = tuple(map(int, s))
            self.chessboard[point[0]][point[1]] = point[2]
            line = log.readline()
        return self.chessboard

    def go(self, chessboard):
        start = time.time()
        self.candidate_list.clear()
        self.chessboard = chessboard
        c = np.array(chessboard)
        idx = np.where(c == COLOR_NONE)
        ban = np.where(c != COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        ban = list(zip(ban[0], ban[1]))
        pos_list = idx
        if ban:
            for p in ban:
                score_list_me[p[0]][p[1]] = -1
                score_list_he[p[0]][p[1]] = 1
                score_list_total[p[0]][p[1]] = -1
        else:
            self.candidate_list.append((7, 7))
            return

        for p in pos_list:
            score_me = self.pos_score(p, 1)
            if p == (6,2):
                a=1
            score_he = self.pos_score(p, 0)
            score_list_me[p[0]][p[1]] = score_me
            score_list_he[p[0]][p[1]] = -score_he
            score_list_total[p[0]][p[1]] = score_he + score_me
        best_list = self.find_candidate(score_list_total, 1)
        # self.color = -self.color
        # for p in pos_list:
        #     score_me = self.pos_score(p, 1)
        #     score_he = self.pos_score(p, 0)
        #     score_list_he[p[0]][p[1]] = - (score_me - score_he)
        # self.color = -self.color
        best_list = self.max_min(best_list, 4)
        end = time.time()
        new_pos = best_list[0]
        print('time:', end - start)
        print('step', new_pos)
        assert self.chessboard[new_pos[0]][new_pos[1]] == 0
        self.candidate_list.append(new_pos)
        self.chessboard[new_pos[0]][new_pos[1]] = self.color
        return self.chessboard, new_pos

    def gen(self, idx):
        pos_list = []
        for p in idx:
            if self.isNeighbor(p):
                pos_list.append(p)
        return pos_list

    def max_min(self, best_list, deep):
        def min_value(deep, alpha, beta):
            global score_list_he, score_list_me, score_list_total
            p_l = self.find_candidate(score_list_total, 1)
            v = infinity
            if deep <= 0:
                return self.get_state(p_l)
            for p in p_l:
                a, b, c = copy.deepcopy(score_list_me[:]), copy.deepcopy(score_list_he[:]), copy.deepcopy(
                    score_list_total[:])
                self.chessboard[p[0]][p[1]] = -self.color
                self.update(p)
                if self.terminal_test(p, 0):
                    self.chessboard[p[0]][p[1]] = 0
                    score_list_me, score_list_he = a, b
                    return -infinity
                v = min(v, max_value(deep - 1, alpha, beta))
                self.chessboard[p[0]][p[1]] = 0
                score_list_me, score_list_he, score_list_total = a, b, c
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        def max_value(deep, alpha, beta):
            global score_list_me, score_list_he, score_list_total
            p_l = self.find_candidate(score_list_total, 1)
            v = -infinity
            if deep <= 0:
                return self.get_state(p_l)
            for p in p_l:
                self.chessboard[p[0]][p[1]] = self.color
                a, b, c = copy.deepcopy(score_list_me[:]), copy.deepcopy(score_list_he[:]), copy.deepcopy(
                    score_list_total)
                self.update(p)
                if self.terminal_test(p, 1):
                    self.chessboard[p[0]][p[1]] = 0
                    score_list_me, score_list_he = a, b
                    return infinity
                v = max(v, min_value(deep - 1, alpha, beta))
                self.chessboard[p[0]][p[1]] = 0
                score_list_me, score_list_he, score_list_total = a, b, c
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        global score_list_me, score_list_he, score_list_total
        best = -100000000
        best_position = []
        alpha = -infinity
        beta = infinity
        for p in best_list:
            self.chessboard[p[0]][p[1]] = self.color
            store_score_me, store_score_he, store_score_total = copy.deepcopy(score_list_me[:]), copy.deepcopy(
                score_list_he[:]), copy.deepcopy(score_list_total[:])
            if self.terminal_test(p, 1):
                best_position.append(p)
                self.chessboard[p[0]][p[1]] = 0
                return best_position
            # elif score_list_total[p[0]][p[1]] >= 20000:
            #     best_position.append(p)
            #     self.chessboard[p[0]][p[1]] = 0
            #     score_list_me, score_list_he = store_score_me, store_score_he
            #     return best_position
            self.update(p)
            v = min_value(deep - 1, alpha, beta)
            if v == best:
                best_position.append(p)
            elif v > best:
                best = v
                best_position = []
                best_position.append(p)
            if not best_position:
                a = 1
            self.chessboard[p[0]][p[1]] = 0
            score_list_me, score_list_he, score_list_total = store_score_me, store_score_he, store_score_total
        return best_position

    # def estimate(self, pos_list, flag):
    #     if not flag:
    #         self.color = -self.color
    #     max_score = 0
    #     for p in pos_list:
    #         score = self.pos_score(p, 1) + self.pos_score(p, 0)
    #         if score > max_score:
    #             max_score = score
    #     if not flag:
    #         self.color = -self.color
    #     return max_score

    def get_state(self, p_l):
        state = 0
        for p in p_l:
            if self.chessboard[p[0]][p[1]] == 0:
                state += (self.pos_score(p, 1) - 0.5 * self.pos_score(p, 0))
        return state

    def find_candidate(self, list, flag):
        p_list = copy.deepcopy(list)
        c_list = []
        best_score = [0]
        if flag == 1:
            for i in range(6):
                c = np.array(p_list)
                max_s = np.max(c)
                p = np.where(c == max_s)
                max_p = (p[0][0], p[1][0])
                c_list.append(max_p)
                p_list[max_p[0]][max_p[1]] = -1

        else:
            for i in range(6):
                c = np.array(p_list)
                min_s = np.min(c)
                p = np.where(c == min_s)
                min_p = (p[0][0], p[1][0])
                c_list.append(min_p)
                p_list[min_p[0]][min_p[1]] = 1
        return c_list

    def isNeighbor(self, pos):
        x_range = range(pos[0] - 1, pos[0] + 2)
        y_range = range(pos[1] - 1, pos[1] + 2)
        for i in y_range:
            if 0 <= i < self.chessboard_size:
                if self.chessboard[i][pos[1]] != 0:
                    return True
        for i in y_range:
            if 0 <= i < self.chessboard_size:
                if self.chessboard[pos[0]][i] != 0:
                    return True
        for (i, j) in zip(x_range, y_range):
            if 0 <= i < self.chessboard_size and 0 <= j < self.chessboard_size:
                if self.chessboard[i][j] != 0:
                    return True
        for (i, j) in zip(x_range, y_range[::-1]):
            if 0 <= i < self.chessboard_size and 0 <= j < self.chessboard_size:
                if self.chessboard[i][j] != 0:
                    return True
        return False

    def Analyse(self, pos, direction):
        x_range = range(pos[0] - 4, pos[0] + 5)
        y_range = range(pos[1] - 4, pos[1] + 5)
        analyse_result = []
        if direction == 1:
            for i in x_range:
                if 0 <= i < self.chessboard_size:
                    analyse_result.append(self.chessboard[i][pos[1]])
        elif direction == 2:
            for i in y_range:
                if 0 <= i < self.chessboard_size:
                    analyse_result.append(self.chessboard[pos[0]][i])
        elif direction == 3:
            for (i, j) in zip(x_range, y_range):
                if 0 <= i < self.chessboard_size and 0 <= j < self.chessboard_size:
                    analyse_result.append(self.chessboard[i][j])
        elif direction == 4:
            for (i, j) in zip(x_range, y_range[::-1]):
                if 0 <= i < self.chessboard_size and 0 <= j < self.chessboard_size:
                    analyse_result.append(self.chessboard[i][j])
        str_analyse = "".join(map(str, analyse_result))
        str_analyse = str_analyse.replace('-1', '3')
        return str_analyse

    def pos_score(self, pos, flag):
        score = 0
        if pos == (7, 7):
            score += 1
        an_result = self.pos_analyse(pos, flag)
        '''
                         己方      敌方
         成五            100000    50000
         活四            20000     18000
         高死四           9000     6000
         低死四           5500      4000
         高活三           10000     8000
         低活三           7000      5000
         高死三           4000      3000
         低死三           2000       1000
         高活二           1000       500
         低活二            200        100
         死二              2          1
         '''
        if flag:
            if an_result['five'] >= 1:
                score += 100000
            if an_result['alive_four'] >= 1:
                score += 20000 * an_result['alive_four']
            if an_result['alive_three_1'] >= 1:
                score += 10000 * an_result['alive_three_1']
            if an_result['dead_four_1'] >= 1:
                score += 9000 * an_result['dead_four_1']
            if an_result['dead_four_2'] >= 1:
                score += 5500 * an_result['dead_four_2']
            if an_result['alive_three_2'] >= 1:
                score += 7000 * an_result['alive_three_2']
            if an_result['dead_three_1'] >= 1:
                score += 4000 * an_result['dead_three_1']
            if an_result['dead_three_2'] >= 1:
                score += 2000 * an_result['dead_three_2']
            if an_result['alive_two_1'] >= 1:
                score += 1000 * an_result['alive_two_1']
            if an_result['alive_two_2'] >= 1:
                score += 200 * an_result['alive_two_2']
            if an_result['dead_two'] >= 1:
                score += 2 * an_result['dead_two']
        else:
            if an_result['five'] >= 1:
                score += 50000
            if an_result['alive_four'] >= 1:
                score += 18000 * an_result['alive_four']
            if an_result['alive_three_1'] >= 1:
                score += 8000 * an_result['alive_three_1']
            if an_result['dead_four_1'] >= 1:
                score += 6000 * an_result['dead_four_1']
            if an_result['dead_four_2'] >= 1:
                score += 4000 * an_result['dead_four_2']
            if an_result['alive_three_2'] >= 1:
                score += 5000 * an_result['alive_three_2']
            if an_result['dead_three_1'] >= 1:
                score += 3000 * an_result['dead_three_1']
            if an_result['dead_three_2'] >= 1:
                score += 1000 * an_result['dead_three_2']
            if an_result['alive_two_1'] >= 1:
                score += 500 * an_result['alive_two_1']
            if an_result['alive_two_2'] >= 1:
                score += 100 * an_result['alive_two_2']
            if an_result['dead_two'] >= 1:
                score += 1 * an_result['dead_two']
        return score

    def pos_analyse(self, pos, flag):
        ana_dic = {'five': 0, 'alive_four': 0, 'alive_three_1': 0, 'alive_three_2': 0, 'alive_two_1': 0,
                   'alive_two_2': 0, 'dead_four_1': 0, 'dead_four_2': 0,
                   'dead_three_1': 0, 'dead_three_2': 0, 'dead_two': 0}
        if (self.color == 1 and flag) or (self.color == -1 and not flag):
            five = ['11112', '11121', '11211']
            alive_four = ['021110', '012110']
            alive_three_1 = ['02110', '01210']
            alive_three_2 = ['021010', '012010', '011020']
            alive_two_1 = ['02100', '00210']
            alive_two_2 = ['02010', '010020']
            dead_four_1 = ['321110', '312110', '311210', '311120']
            dead_four_2 = ['21101', '12101', '11201', '11102',
                           '21011', '12011', '11021', '11012']
            dead_three_1 = ['321100', '312100', '311200']
            dead_three_2 = ['321010', '312010', '311020',
                            '320110', '310210', '310120',
                            '20101', '10201', '10102']
            dead_two = ['3210', '3120']
        else:
            five = ['33332', '33323', '33233']
            alive_four = ['023330', '032330']
            alive_three_1 = ['02330', '03230']
            alive_three_2 = ['023030', '032030', '033020']
            alive_two_1 = ['02300', '00230']
            alive_two_2 = ['02030', '030020']
            dead_four_1 = ['123330', '132330', '133230', '133320']
            dead_four_2 = ['123303', '132303', '133203', '133302',
                           '123033', '132033', '133023', '133032']
            dead_three_1 = ['123300', '132300', '133200']
            dead_three_2 = ['123030', '132030', '133020',
                            '120330', '130230', '130320',
                            '20303', '30203', '30302']
            dead_two = ['123000', '132000']

        def pos_cal(condition):
            for i in five:
                if i in condition or i[::-1] in condition:
                    ana_dic['five'] += 1
                    break
            for i in alive_four:
                if i in condition or i[::-1] in condition:
                    ana_dic['alive_four'] += 1
                    break
            for i in alive_three_1:
                if i in condition or i[::-1] in condition:
                    ana_dic['alive_three_1'] += 1
                    break
            for i in alive_three_2:
                if i in condition or i[::-1] in condition:
                    ana_dic['alive_three_2'] += 1
                    break
            for i in alive_two_1:
                if i in condition or i[::-1] in condition:
                    ana_dic['alive_two_1'] += 1
                    break
            for i in alive_two_2:
                if i in condition or i[::-1] in condition:
                    ana_dic['alive_two_2'] += 1
                    break
            for i in dead_four_1:
                if i in condition or i[::-1] in condition:
                    ana_dic['dead_four_1'] += 1
                    break
            for i in dead_four_2:
                if i in condition or i[::-1] in condition:
                    ana_dic['dead_four_2'] += 1
                    break
            for i in dead_three_1:
                if i in condition or i[::-1] in condition:
                    ana_dic['dead_three_1'] += 1
                    break
            for i in dead_three_2:
                if i in condition or i[::-1] in condition:
                    ana_dic['dead_three_2'] += 1
                    break
            for i in dead_two:
                if i in condition or i[::-1] in condition:
                    ana_dic['dead_two'] += 1
                    break

        analyse = []
        self.chessboard[pos[0]][pos[1]] = 2
        for i in range(1, 5):
            str_analyse = self.Analyse(pos, i)
            pos_cal(str_analyse)
        self.chessboard[pos[0]][pos[1]] = 0
        return ana_dic

    def update(self, pos):
        def update_score(p):
            if self.chessboard[p[0]][p[1]] == 0:
                score_list_he[p[0]][p[1]] = -self.pos_score(p, 0)
                score_list_me[p[0]][p[1]] = self.pos_score(p, 1)
                score_list_total[p[0]][p[1]] = -score_list_he[p[0]][p[1]] + score_list_me[p[0]][p[1]]

        score_list_he[pos[0]][pos[1]] = 1
        score_list_me[pos[0]][pos[1]] = -1
        score_list_total[pos[0]][pos[1]] = -1

        x_range = range(pos[0] - 4, pos[0] + 5)
        y_range = range(pos[1] - 4, pos[1] + 5)
        for i in y_range:
            if 0 <= i < self.chessboard_size and i != pos[0]:
                p = (i, pos[1])
                update_score(p)
        for i in y_range:
            if 0 <= i < self.chessboard_size and i != pos[1]:
                p = (pos[0], i)
                update_score(p)
        for (i, j) in zip(x_range, y_range):
            if 0 <= i < self.chessboard_size and 0 <= j < self.chessboard_size and (i, j) != pos:
                p = (i, j)
                update_score(p)
        for (i, j) in zip(x_range, y_range[::-1]):
            if 0 <= i < self.chessboard_size and 0 <= j < self.chessboard_size and (i, j) != pos:
                p = (i, j)
                update_score(p)

    def terminal_test(self, p, flag):
        if (flag and self.color == 1) or (not flag and self.color == -1):
            for i in range(1, 5):
                an = self.Analyse(p, i)
                if '11111' in an:
                    return True
        else:
            for i in range(1, 5):
                an = self.Analyse(p, i)
                if '33333' in an:
                    return True
        return False


def print_go(chessboard):
    for i in range(15):
        for j in range(15):
            if chessboard[i][j] == 1:
                print("*", end=' ')
            elif chessboard[i][j] == -1:
                print("o", end=' ')
            elif chessboard[j][j] == 3:
                print("X", end=' ')
            else:
                print("-", end=' ')
        print()


# #
# white = AI(15, 1, 5)
# black = AI(15, -1, 5)
# b = black.first_chess()
# print_go(b)
# b, b_p = black.go(b)
# print_go(b)
# w, w_p = white.go(b)
# print_gomo(w)
# for i in range(10):
#     w, w_p = white.go(b)
#     print_go(w)
#     b, b_p = black.go(w)
#     print_go(b)

'''
3 result (7, 6) 17700
3 result (10, 7) 16280
3 result (6, 6) 15500
3 result (9, 9) 20100
3 result (9, 7) 12700
3 result (9, 5) 12700
time: 0.5198421478271484
[(9, 9)]
'''
