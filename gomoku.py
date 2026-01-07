"""
This module contains the core logic for a game of Gomoku.
"""

class GomokuGame:
    """
    Represents the state and rules of a Gomoku game.
    The board is represented by a 2D list where:
    - 0: Empty spot
    - 1: Player 1's stone
    - 2: Player 2's stone
    """

    def __init__(self, size=15):
        """
        Initializes the Gomoku game.

        Args:
            size (int): The size of the board (e.g., 15 for a 15x15 board).
        """
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def get_board(self):
        """
        Returns the current state of the board.

        Returns:
            list[list[int]]: A 2D list representing the board.
        """
        return self.board

    def make_move(self, row, col):
        """
        Places a stone on the board for the current player.

        Args:
            row (int): The row index to place the stone.
            col (int): The column index to place the stone.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self.game_over:
            print("Error: Game is already over.")
            return False

        # Validate the move
        if not (0 <= row < self.size and 0 <= col < self.size):
            print(f"Error: Move ({row}, {col}) is out of bounds.")
            return False
        if self.board[row][col] != 0:
            print(f"Error: Position ({row}, {col}) is already occupied.")
            return False

        # Place the stone
        self.board[row][col] = self.current_player

        # Check for a win
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            return True

        # Check for a draw
        if self.is_board_full():
            self.game_over = True
            self.winner = 0  # 0 can represent a draw
            return True

        # Switch to the next player
        self.current_player = 2 if self.current_player == 1 else 1
        return True

    def check_win(self, row, col):
        """
        Checks if the last move resulted in a win.

        This method checks for five consecutive stones in all four directions
        (horizontal, vertical, and both diagonals) from the last placed stone.

        Args:
            row (int): The row index of the last move.
            col (int): The column index of the last move.

        Returns:
            bool: True if the current player has won, False otherwise.
        """
        player = self.board[row][col]
        if player == 0:
            return False

        # Directions to check: horizontal, vertical, diagonal, anti-diagonal
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            # Count in the positive direction (e.g., right, down)
            for i in range(1, 5):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                    count += 1
                else:
                    break

            # Count in the negative direction (e.g., left, up)
            for i in range(1, 5):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                    count += 1
                else:
                    break

            if count >= 5:
                return True

        return False

    def is_board_full(self):
        """
        Checks if the board is completely full, resulting in a draw.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def print_board(self):
        """
        A utility function to print the board to the console for debugging.
        """
        for row in self.board:
            print(" ".join(map(str, row)))
        print("-" * (self.size * 2 - 1))

if __name__ == '__main__':
    # Example usage:
    game = GomokuGame()

    # A sequence of moves leading to a horizontal win for Player 1
    moves = [
        (7, 7), (6, 7),
        (7, 8), (6, 8),
        (7, 9), (6, 9),
        (7, 10), (6, 10),
        (7, 11) # Player 1 wins here
    ]

    for i, (row, col) in enumerate(moves):
        player = game.current_player
        print(f"Player {player} makes a move at ({row}, {col})")
        if game.make_move(row, col):
            game.print_board()
            if game.game_over:
                if game.winner:
                    print(f"Game over! Player {game.winner} wins!")
                else:
                    print("Game over! It's a draw.")
                break
        else:
            print("Invalid move. Please try again.")
            # In a real game, you would re-prompt the player for a move.
            # Here we just stop.
            break

        if i == len(moves) -1 and not game.game_over:
            print("Example finished without a winner.")
