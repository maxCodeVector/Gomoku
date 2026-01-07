"""
Gomoku AI implementation using Minimax algorithm with alpha-beta pruning.
This module provides a smart AI opponent for the Gomoku game.
"""

import math
from typing import Tuple, List, Optional


class GomokuAI:
    """
    A smart AI opponent for Gomoku using Minimax algorithm with alpha-beta pruning.

    The AI evaluates board positions using a heuristic function that considers:
    - Consecutive stones (2, 3, 4, 5 in a row)
    - Open-ended sequences (can be extended on both sides)
    - Defensive considerations (blocking opponent's threats)
    - Center control and mobility

    Attributes:
        depth (int): Search depth for the Minimax algorithm
        player (int): Which player the AI represents (1 or 2)
        opponent (int): The opponent player (2 or 1)
        size (int): Board size (default 15)
    """

    def __init__(self, depth: int = 3, player: int = 2):
        """
        Initialize the Gomoku AI.

        Args:
            depth (int): Search depth for Minimax algorithm. Higher depth means
                        stronger but slower AI. Depth 3-4 is reasonable for 15x15 board.
            player (int): Which player the AI represents (1 or 2). Default is 2.
        """
        self.depth = depth
        self.player = player
        self.opponent = 2 if player == 1 else 1
        self.size = 15  # Default board size, will be updated from game

        # Heuristic weights for different patterns
        # Higher values mean more valuable patterns
        self.weights = {
            'five': 1000000,      # Winning move
            'open_four': 10000,   # Four in a row with both ends open
            'four': 1000,         # Four in a row with one end open
            'open_three': 1000,   # Three in a row with both ends open
            'three': 100,         # Three in a row with one end open
            'open_two': 50,       # Two in a row with both ends open
            'two': 10,            # Two in a row with one end open
            'center': 5,          # Center control bonus
        }

        # Directions to check: horizontal, vertical, diagonal, anti-diagonal
        self.directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    def find_best_move(self, game) -> Tuple[int, int]:
        """
        Find the best move for the current player in the given game state.

        Args:
            game: A GomokuGame instance representing the current game state.

        Returns:
            Tuple[int, int]: The (row, col) coordinates of the best move.
        """
        self.size = game.size

        # If it's the first move, play in the center
        if self.is_first_move(game.board):
            center = self.size // 2
            return center, center

        # Get all possible moves (empty cells near existing stones for efficiency)
        possible_moves = self.get_possible_moves(game.board)

        # If no possible moves (shouldn't happen), return a default move
        if not possible_moves:
            return self.size // 2, self.size // 2

        best_move = None
        best_value = -math.inf

        # Use alpha-beta pruning to search for the best move
        alpha = -math.inf
        beta = math.inf

        for move in possible_moves:
            row, col = move

            # Make the move
            game.board[row][col] = self.player

            # Evaluate the move using Minimax
            move_value = self.minimax(
                game,
                depth=self.depth - 1,
                alpha=alpha,
                beta=beta,
                maximizing_player=False
            )

            # Undo the move
            game.board[row][col] = 0

            # Update best move
            if move_value > best_value:
                best_value = move_value
                best_move = move

            # Update alpha
            alpha = max(alpha, best_value)

        return best_move

    def minimax(self, game, depth: int, alpha: float, beta: float,
                maximizing_player: bool) -> float:
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            game: GomokuGame instance
            depth (int): Current search depth
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing_player (bool): True if current player is maximizing

        Returns:
            float: Evaluation score for the position
        """
        # Terminal conditions: depth reached or game over
        if depth == 0 or game.game_over:
            return self.evaluate_board(game.board)

        # Get possible moves
        possible_moves = self.get_possible_moves(game.board)

        if maximizing_player:
            max_eval = -math.inf
            for move in possible_moves:
                row, col = move

                # Make move
                game.board[row][col] = self.player

                # Check if this move wins the game
                if game.check_win(row, col):
                    game.board[row][col] = 0  # Undo move
                    return math.inf  # Winning move is infinitely good

                # Recursive call
                eval_score = self.minimax(game, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)

                # Undo move
                game.board[row][col] = 0

                # Alpha-beta pruning
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff

            return max_eval
        else:
            min_eval = math.inf
            for move in possible_moves:
                row, col = move

                # Make move for opponent
                game.board[row][col] = self.opponent

                # Check if this move wins the game for opponent
                if game.check_win(row, col):
                    game.board[row][col] = 0  # Undo move
                    return -math.inf  # Opponent winning move is infinitely bad

                # Recursive call
                eval_score = self.minimax(game, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)

                # Undo move
                game.board[row][col] = 0

                # Alpha-beta pruning
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff

            return min_eval

    def evaluate_board(self, board: List[List[int]]) -> float:
        """
        Evaluate the board position from the AI's perspective.

        Args:
            board: 2D list representing the game board

        Returns:
            float: Evaluation score (positive is good for AI, negative for opponent)
        """
        score = 0

        # Evaluate all positions on the board
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == self.player:
                    score += self.evaluate_position(board, row, col, self.player)
                elif board[row][col] == self.opponent:
                    score -= self.evaluate_position(board, row, col, self.opponent)

        # Add center control bonus
        center = self.size // 2
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = center + dr, center + dc
                if 0 <= r < self.size and 0 <= c < self.size:
                    if board[r][c] == self.player:
                        score += self.weights['center']
                    elif board[r][c] == self.opponent:
                        score -= self.weights['center']

        return score

    def evaluate_position(self, board: List[List[int]], row: int, col: int,
                         player: int) -> float:
        """
        Evaluate a specific position for a given player.

        Args:
            board: 2D list representing the game board
            row (int): Row index
            col (int): Column index
            player (int): Player to evaluate for (1 or 2)

        Returns:
            float: Evaluation score for this position
        """
        if board[row][col] != player:
            return 0

        score = 0

        # Check all four directions from this position
        for dr, dc in self.directions:
            # Check positive direction
            length = 1
            open_ends = 0

            # Check if the start is open
            r_prev, c_prev = row - dr, col - dc
            if 0 <= r_prev < self.size and 0 <= c_prev < self.size:
                if board[r_prev][c_prev] == 0:
                    open_ends += 1
            else:
                open_ends += 1  # Board edge counts as closed

            # Count consecutive stones in positive direction
            for i in range(1, 6):  # Check up to 5 stones
                r, c = row + i * dr, col + i * dc
                if 0 <= r < self.size and 0 <= c < self.size:
                    if board[r][c] == player:
                        length += 1
                    elif board[r][c] == 0:
                        open_ends += 1
                        break
                    else:
                        break  # Opponent's stone blocks
                else:
                    break  # Board edge

            # Check if the end is open (we already counted if it's empty)
            # We need to check one more step beyond the last stone
            if length < 5:
                r_next, c_next = row + length * dr, col + length * dc
                if 0 <= r_next < self.size and 0 <= c_next < self.size:
                    if board[r_next][c_next] == 0:
                        open_ends += 1
                else:
                    open_ends += 1  # Board edge counts as closed

            # Score based on pattern length and openness
            score += self.score_pattern(length, open_ends)

        return score

    def score_pattern(self, length: int, open_ends: int) -> float:
        """
        Score a pattern based on its length and number of open ends.

        Args:
            length (int): Number of consecutive stones
            open_ends (int): Number of open ends (0, 1, or 2)

        Returns:
            float: Score for this pattern
        """
        if length >= 5:
            return self.weights['five']

        if length == 4:
            if open_ends == 2:
                return self.weights['open_four']
            elif open_ends == 1:
                return self.weights['four']

        if length == 3:
            if open_ends == 2:
                return self.weights['open_three']
            elif open_ends == 1:
                return self.weights['three']

        if length == 2:
            if open_ends == 2:
                return self.weights['open_two']
            elif open_ends == 1:
                return self.weights['two']

        return 0

    def get_possible_moves(self, board: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Get all possible moves (empty cells near existing stones).
        This significantly reduces the search space.

        Args:
            board: 2D list representing the game board

        Returns:
            List[Tuple[int, int]]: List of (row, col) coordinates of possible moves
        """
        moves = set()

        # First, check if board is empty
        if self.is_first_move(board):
            center = self.size // 2
            return [(center, center)]

        # Look for empty cells adjacent to existing stones
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] != 0:
                    # Check all adjacent positions
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            if dr == 0 and dc == 0:
                                continue
                            r, c = row + dr, col + dc
                            if (0 <= r < self.size and 0 <= c < self.size and
                                board[r][c] == 0):
                                moves.add((r, c))

        # If no adjacent moves found (shouldn't happen), return all empty cells
        if not moves:
            moves = [(r, c) for r in range(self.size) for c in range(self.size)
                    if board[r][c] == 0]

        return list(moves)

    def is_first_move(self, board: List[List[int]]) -> bool:
        """
        Check if the board is empty (first move of the game).

        Args:
            board: 2D list representing the game board

        Returns:
            bool: True if board is empty, False otherwise
        """
        for row in board:
            for cell in row:
                if cell != 0:
                    return False
        return True


def test_ai():
    """Test function to demonstrate the AI's capabilities."""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from gomoku import GomokuGame

    print("Testing Gomoku AI...")

    # Create a game
    game = GomokuGame(size=15)

    # Create AI player
    ai = GomokuAI(depth=3, player=2)

    # Test 1: First move should be center
    print("\nTest 1: First move")
    best_move = ai.find_best_move(game)
    print(f"AI's first move: {best_move}")
    print(f"Expected: (7, 7) for 15x15 board")

    # Test 2: Make a move and see AI's response
    print("\nTest 2: Responding to human move")
    game.make_move(7, 7)  # Human plays center
    best_move = ai.find_best_move(game)
    print(f"AI's response to center move: {best_move}")

    # Test 3: Create a threat and see if AI blocks it
    print("\nTest 3: Blocking opponent's threat")
    game = GomokuGame(size=15)

    # Create a three-in-a-row for player 1
    game.make_move(7, 7)  # Player 1
    game.make_move(6, 6)  # Player 2 (AI would play this)
    game.make_move(7, 8)  # Player 1
    game.make_move(5, 5)  # Player 2
    game.make_move(7, 9)  # Player 1 (now has three in a row)

    print("Board state:")
    game.print_board()

    ai2 = GomokuAI(depth=3, player=2)
    best_move = ai2.find_best_move(game)
    print(f"AI's move to block threat: {best_move}")
    print(f"Expected to block at (7, 10) or (7, 6)")

    # Test 4: Winning move
    print("\nTest 4: Creating winning opportunity")
    game = GomokuGame(size=15)

    # Setup a four-in-a-row for AI
    game.make_move(7, 7)  # Player 1
    game.make_move(6, 6)  # Player 2 (AI)
    game.make_move(7, 8)  # Player 1
    game.make_move(6, 7)  # Player 2 (AI)
    game.make_move(7, 9)  # Player 1
    game.make_move(6, 8)  # Player 2 (AI)
    game.make_move(7, 10) # Player 1
    game.make_move(6, 9)  # Player 2 (AI) - now has four in a row

    print("Board state:")
    game.print_board()

    ai3 = GomokuAI(depth=3, player=2)
    best_move = ai3.find_best_move(game)
    print(f"AI's winning move: {best_move}")
    print(f"Expected to win at (6, 10) or (6, 5)")


if __name__ == "__main__":
    test_ai()