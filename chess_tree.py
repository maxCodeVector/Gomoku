import random
import time

import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(time.time())

S = [[0, 0, 0, 0, 16000], [0, 5, 20, 60, 16000], [1, 30, 60, 800, 16000]]
L = [[0, 0, 0, 0, 4000], [0, 1, 10, 40, 4000], [0, 20, 30, 500, 4000]]


def match(pattern, dest):
    """
    judge if dest contain a special pattern
    :param pattern:
    :param dest:
    :return: true if contains, otherwise false
    """
    pattern_len = len(pattern)
    for i in range(len(dest) - pattern_len + 1):
        if np.where(pattern ^ dest[i:i + pattern_len] == 0)[0].shape[0] == pattern_len:
            return True
    return False


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

        action = self.alpha_beta_cutoff_search(chessboard, eval_fn=self.eval_fn)
        if action:
            self.candidate_list.append(action)
        if len(self.candidate_list) == 0:
            self.__random_p(chessboard)

    def __random_p(self, chessboard):
        np.random.seed(0)
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        pos_idx = np.random.randint(0, len(idx) - 1)
        new_pos = idx[pos_idx]
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)

    def terminal_test(self, state, action):
        """
        test if the state with next action will be terminal, noted that this action has been done
        :param state: in this case, state is current chess board
        :param action: the next position that a player want to go, format:(x, y, role)
        :return: true means game over, otherwise continue
        """
        x = action[0]
        y = action[1]
        role = state[x][y]
        # state[x][y] = role
        fivePattern = np.array([role] * 5)
        directions = ((1, 0), (0, 1), (1, 1), (1, -1))  # column, row, diag, re-diag
        for dir in directions:
            dest = [state[x + i * dir[0]][y + i * dir[1]] for i in range(-4, 5)
                    if 0 <= x + i * dir[0] < self.chessboard_size and 0 <= y + i * dir[1] < self.chessboard_size]
            if match(fivePattern, dest):
                # state[x][y] = COLOR_NONE
                return True
        # state[x][y] = COLOR_NONE
        return False

    def eval_fn(self, state, action):
        """
        evaluate current state if do this action, noted that this action has been done, but it may be different from
        function terminal_test
        :param state: in this case, state is current chess board
        :param action: the next position that a player want to go, format:(x, y, role)
        :return: a number represented current score
        """
        competitor_score, self_score = self.utility(action, state)
        attack_flag = self_score < competitor_score
        if attack_flag:
            return competitor_score, attack_flag
        else:
            return self_score, attack_flag
        # final_score = max(self_score, competitor_score)
        # if state[action[0]][action[1]] != self.color:
        #     return -final_score
        # if competitor_score > 0:
        #     competitor_score = 16000 - competitor_score
        # return final_score

    def utility(self, action, state):
        """
        evlaue current blackboard two player's state with this action
        :param action: the action
        :param state: current blackboard
        :return: two score for self and competitor respectively
        """
        x = action[0]
        y = action[1]
        role = state[x][y]
        self_score = 0
        competitor_score = 0
        live_fivePattern = np.array([0, 1, 1, 1, 1, 1, 0])  # 成五
        rush_fivePattern1 = np.array([-1, 1, 1, 1, 1, 1, 0])  # 成五
        rush_fivePattern2 = np.array([0, 1, 1, 1, 1, 1, -1])  # 成五
        common_fivePattern = np.array([1] * 5)  # 成五
        live4Pattern = np.array([0, 1, 1, 1, 1, 0])  # 活四
        live3Pattern = np.array([0, 1, 1, 1, 0])  # 活三
        rush4Pattern1 = np.array([-1, 1, 1, 1, 1, 0])  # 冲四1
        rush4Pattern2 = np.array([0, 1, 1, 1, 1, -1])  # 冲四2
        score_item_list = [
            (live_fivePattern, S[2][4]),
            (rush_fivePattern1, S[2][4]-10),
            (rush_fivePattern2, S[2][4]-10),
            (common_fivePattern, S[2][4]-10),
            (live4Pattern, S[2][3]),
            (live3Pattern, S[2][2]),
            (rush4Pattern1, S[2][2]),
            (rush4Pattern2, S[1][3]),
        ]
        directions = ((1, 0), (0, 1), (1, 1), (1, -1))  # column, row, diag, re-diag
        for dir in directions:

            state[x][y] = role
            dest = [state[x + i * dir[0]][y + i * dir[1]] for i in range(-6, 7)
                    if 0 <= x + i * dir[0] < self.chessboard_size and 0 <= y + i * dir[1] < self.chessboard_size]
            for score_item in score_item_list:
                if match(score_item[0] * role, dest):
                    self_score += score_item[1]
                    break

            state[x][y] = -role
            dest = [state[x + i * dir[0]][y + i * dir[1]] for i in range(-6, 7)
                    if 0 <= x + i * dir[0] < self.chessboard_size and 0 <= y + i * dir[1] < self.chessboard_size]
            for score_item in score_item_list:
                if match(score_item[0] * -role, dest):
                    competitor_score += score_item[1]
                    break
        state[x][y] = role
        return competitor_score, self_score

    def capture_max_value(self, v, state, action):
        # if()
        pass




    def alpha_beta_cutoff_search(self, state, d=3, cutoff_test=None, eval_fn=None):
        infinity = 1e300

        # player = game.to_move(state)

        def max_value(state, action, alpha, beta, depth):
            if cutoff_test(state, action, depth):
                return eval_fn(state, action)

            v = -infinity
            wait_queue = dict()
            attack_queue = dict
            best_action = None
            for action in self.get_actions(state):
                state[action] = self.color
                info = min_value(state, action, alpha, beta, depth + 1)
                wait_queue[action] = info[0]
                attack_queue[action] = info[1]
                # if info[1]:
                #     wait_queue[action] = -info[0]

                # wait_queue[action] = min_value(state, action,
                #                      alpha, beta, depth + 1) - depth
                if v < wait_queue[action]:
                    v = wait_queue[action]
                    best_action = action
                v = max(v, wait_queue[action])
                state[action] = COLOR_NONE
                # if v >= beta:
                #     return v
                alpha = max(alpha, v)
            return v, attack_queue[best_action]

        def min_value(state, action, alpha, beta, depth):
            if cutoff_test(state, action, depth):
                return eval_fn(state, action)[0]

            v = infinity
            wait_queue = dict()
            for action in self.get_actions(state):
                state[action] = -self.color
                info = max_value(state, action, alpha, beta, depth + 1)
                if info[1]:
                    wait_queue[action] = -info[0]

                # wait_queue[action] = -max_value(state, action,
                #            alpha, beta, depth + 1) + depth
                v = min(v, wait_queue[action])
                state[action] = COLOR_NONE
                # if v <= alpha:
                #     return v
                beta = min(beta, v)
            return v

        cutoff_test = (cutoff_test or
                       (lambda state, action, depth: depth >= d or self.terminal_test(state, action)))

        # eval_fn = eval_fn or (lambda state: game.utility(state, player))

        best_score = -infinity
        beta = infinity
        best_action = None
        wait_queue = dict()

        for action in self.get_actions(state):
            state[action] = self.color
            v = min_value(state, action, best_score, beta, 1)
            state[action] = COLOR_NONE
            wait_queue[action] = v
            if v > best_score:
                best_score = v
                best_action = action
        return best_action

    def get_actions(self, chessboard, filter=10):
        actions = []
        checked = np.zeros((self.chessboard_size, self.chessboard_size), dtype=int)
        idx = np.where(chessboard != COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        for node in idx:

            for child in self.get_childs(node):
                if chessboard[child] == COLOR_NONE and not checked[child]:
                    actions.append(child)
                    checked[child[0]][child[1]] = 1

        return self.action_filter(actions)

    def action_filter(self, actions):
        return actions

    def get_childs(self, node):
        res = []
        size = self.chessboard_size - 1
        # tag = node[2] + 1
        if node[0] > 0:
            res.append((node[0] - 1, node[1]))
            if node[1] < size:
                res.append((node[0] - 1, node[1] + 1))
            if node[1] > 0:
                res.append((node[0] - 1, node[1] - 1))
        if node[1] > 0:
            res.append((node[0], node[1] - 1))
        if node[0] < size:
            res.append((node[0] + 1, node[1]))
            if node[1] < size:
                res.append((node[0] + 1, node[1] + 1))
            if node[1] > 0:
                res.append((node[0] + 1, node[1] - 1))
        if node[1] < size:
            res.append((node[0], node[1] + 1))
        return res
