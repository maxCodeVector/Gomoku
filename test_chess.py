import numpy as np
import chess_tree


def check_match():
    # 成五
    assert chess_tree.match([1, 1, 1, 1, 1], np.array([1, 1, 1, 1, -1, 1, 1, 0])) == False
    assert chess_tree.match([1, 1, 1, 1, 1], np.array([1, 1, -1, 1, -1, 1, 1, 0])) == False
    assert chess_tree.match([1, 1, 1, 1, 1], np.array([1, 1, 1, 1, 1, -1, 1, 0])) == True
    assert chess_tree.match([1, 1, 1, 1, 1], np.array([1, 1, 1, 1, 1, 1, -1, 0])) == True

def check_match_live4():
    # 活四
    assert chess_tree.match([0, 1, 1, 1, 1, 0], np.array([0, 1, 1, 1, 1, 0, 1, -1, 0])) == True
    assert chess_tree.match([0, 1, 1, 1, 1, 0], np.array([-1, 0, 1, 1, 1, 1, 0, -1, 0])) == True
    assert chess_tree.match([0, 1, 1, 1, 1, 0], np.array([0, 1, 1, -1, 1, 0, 1, -1, 0])) == False
    assert chess_tree.match([0, 1, 1, 1, 1, 0], np.array([0, 1, 1, 1, 1, 1, 1, -1, 0])) == False
    assert chess_tree.match([0, 1, 1, 1, 1, 0], np.array([0, 1, 1, 1, 1, -1, 1, -1, 0])) == False

def check_match_live3():
    # 活三
    assert chess_tree.match([0, 1, 1, 1, 0], np.array([1, 1, 1, 1, 1, 1, -1, 0])) == False
    assert chess_tree.match([0, 1, 1, 1, 0], np.array([1, 0, 1, 1, 1, 0, -1, 0])) == True
    assert chess_tree.match([0, 1, 1, 1, 0], np.array([1, 1, 0, 1, 1, 1, -1, 0])) == False
    assert chess_tree.match([0, 1, 1, 1, 0], np.array([1, 1, 0, 1, 1, 1, 0, 0])) == True

def check_match_rush4():
    # 冲四
    assert chess_tree.match([-1, 1, 1, 1, 1, 0], np.array([1, -1, 1, 1, 1, 1, 0, 0])) == True
    assert chess_tree.match([-1, 1, 1, 1, 1, 0], np.array([1, -1, -1, 1, 1, 1, 0, 0])) == False
    assert chess_tree.match([-1, 1, 1, 1, 1, 0], np.array([0, 1, 1, 1, -1, 1, -1, 0])) == False
    assert chess_tree.match([0, 1, 1, 1, 1, -1], np.array([0, 1, 1, 1, 1, -1, -1, 0])) == True
    assert chess_tree.match([0, 1, 1, 1, 1, -1], np.array([0, 1, 1, 1, 1, 1, 1, 0])) == False
    assert chess_tree.match([0, 1, 1, 1, 1, -1], np.array([0, 1, 1, 1, -1, 1, -1, 0])) == False

def check_terminal():
    ai = chess_tree.AI(15, chess_tree.COLOR_BLACK, 5)
    board = np.zeros((15, 15), dtype=int)
    board[7][6] = chess_tree.COLOR_BLACK
    board[7][5] = chess_tree.COLOR_BLACK
    board[7][4] = chess_tree.COLOR_BLACK
    board[7][3] = chess_tree.COLOR_BLACK
    board[7][10] = chess_tree.COLOR_BLACK
    assert ai.terminal_test(board, (7, 7, chess_tree.COLOR_BLACK))


if __name__ == '__main__':
    check_terminal()
    check_match()
    check_match_live4()
    check_match_live3()
    check_match_rush4()
    print("all test passed!")