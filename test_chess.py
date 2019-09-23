import numpy as np
import chess_tree
from board import Board


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


def test_tree_score_termial():
    """
    test if it can stop player 成五
    :return:
    """
    chessboard = Board(15)
    chessboard.board[3][1] = chess_tree.COLOR_BLACK
    chessboard.board[3][2] = chess_tree.COLOR_WHITE
    chessboard.board[3][3] = chess_tree.COLOR_WHITE
    chessboard.board[3][4] = chess_tree.COLOR_WHITE
    chessboard.board[3][5] = chess_tree.COLOR_WHITE
    chessboard.board[5][4] = chess_tree.COLOR_BLACK
    ai = chess_tree.AI(15, chess_tree.COLOR_BLACK, 5)
    ai.go(chessboard.board)
    res = ai.candidate_list[-1]
    assert res == (3, 6)


def test_tree_score_terminal2():
    """
    test if it can stop player 活四
    :return:
    """
    chessboard = Board(15)
    chessboard.board[3][1] = chess_tree.COLOR_WHITE
    chessboard.board[3][2] = chess_tree.COLOR_WHITE
    chessboard.board[3][4] = chess_tree.COLOR_WHITE
    chessboard.board[3][5] = chess_tree.COLOR_WHITE
    ai = chess_tree.AI(15, chess_tree.COLOR_BLACK, 5)
    ai.go(chessboard.board)
    res = ai.candidate_list[-1]
    assert res == (3, 3)


def test_tree_score_live4():
    """
    test if it can stop player 活四
    :return:
    """
    chessboard = Board(15)
    chessboard.board[3][2] = chess_tree.COLOR_WHITE
    chessboard.board[3][3] = chess_tree.COLOR_WHITE
    chessboard.board[3][4] = chess_tree.COLOR_WHITE
    ai = chess_tree.AI(15, chess_tree.COLOR_BLACK, 5)
    ai.go(chessboard.board)
    res = ai.candidate_list[-1]
    assert res == (3, 6) or res == (3, 1)


def test_tree_score_live4_2():
    """
    test if it can stop player 活四
    :return:
    """
    chessboard = Board(15)
    chessboard.board[3][2] = chess_tree.COLOR_WHITE
    chessboard.board[3][4] = chess_tree.COLOR_WHITE
    chessboard.board[3][5] = chess_tree.COLOR_WHITE
    ai = chess_tree.AI(15, chess_tree.COLOR_BLACK, 5)
    ai.go(chessboard.board)
    res = ai.candidate_list[-1]
    assert res == (3, 3) or res == (3, 1) or res == (3, 6)


if __name__ == '__main__':
    check_terminal()
    check_match()
    check_match_live4()
    check_match_live3()
    check_match_rush4()
    test_tree_score_termial()
    test_tree_score_terminal2()
    test_tree_score_live4()
    test_tree_score_live4_2()
    print("all test passed!")
