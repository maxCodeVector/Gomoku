"""
Integration test for Gomoku AI with the GomokuGame class.
Demonstrates how to use the AI in a complete game.
"""

import sys
import os

# Add parent directory to path to import gomoku
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gomoku import GomokuGame
from ai import GomokuAI


def play_ai_vs_ai():
    """Play a complete game between two AI players."""
    print("Starting AI vs AI game...")
    game = GomokuGame(size=15)

    # Create two AI players
    ai_player1 = GomokuAI(depth=2, player=1)  # Slightly weaker AI for player 1
    ai_player2 = GomokuAI(depth=3, player=2)  # Stronger AI for player 2

    move_count = 0
    max_moves = 50  # Limit to prevent infinite games

    while not game.game_over and move_count < max_moves:
        current_player = game.current_player

        if current_player == 1:
            ai = ai_player1
            player_name = "AI Player 1"
        else:
            ai = ai_player2
            player_name = "AI Player 2"

        # Get AI's move
        row, col = ai.find_best_move(game)

        print(f"\nMove {move_count + 1}: {player_name} plays at ({row}, {col})")

        # Make the move
        if game.make_move(row, col):
            move_count += 1

            # Print board every 5 moves
            if move_count % 5 == 0:
                print(f"\nBoard after {move_count} moves:")
                game.print_board()
        else:
            print(f"Invalid move by {player_name} at ({row}, {col})")
            break

    print("\n" + "="*50)
    print("Game Over!")

    if game.winner == 0:
        print("It's a draw!")
    else:
        print(f"Player {game.winner} wins!")

    print(f"Total moves: {move_count}")
    print("\nFinal board:")
    game.print_board()


def play_human_vs_ai():
    """Play a game between human and AI."""
    print("Starting Human vs AI game...")
    print("You are Player 1 (stones: 1)")
    print("AI is Player 2 (stones: 2)")
    print("Enter moves as 'row col' (0-14)")
    print("Enter 'q' to quit\n")

    game = GomokuGame(size=15)
    ai = GomokuAI(depth=3, player=2)

    while not game.game_over:
        game.print_board()

        if game.current_player == 1:
            # Human's turn
            while True:
                try:
                    move_input = input("\nYour move (row col): ").strip()

                    if move_input.lower() == 'q':
                        print("Game quit by user.")
                        return

                    row_str, col_str = move_input.split()
                    row, col = int(row_str), int(col_str)

                    if game.make_move(row, col):
                        break
                    else:
                        print("Invalid move. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter 'row col' (e.g., '7 7')")
        else:
            # AI's turn
            print("\nAI is thinking...")
            row, col = ai.find_best_move(game)
            print(f"AI plays at ({row}, {col})")
            game.make_move(row, col)

    print("\n" + "="*50)
    print("Game Over!")

    if game.winner == 0:
        print("It's a draw!")
    elif game.winner == 1:
        print("Congratulations! You win!")
    else:
        print("AI wins!")

    print("\nFinal board:")
    game.print_board()


def demonstrate_ai_capabilities():
    """Demonstrate specific AI capabilities."""
    print("Demonstrating AI capabilities...")

    # Test 1: Blocking threats
    print("\n1. Blocking opponent's four-in-a-row:")
    game = GomokuGame(size=15)

    # Setup a threatening position for player 1
    for col in range(7, 11):
        game.make_move(7, col)  # Player 1 creates four in a row

    print("Board state (Player 1 has four in a row at row 7, cols 7-10):")
    game.print_board()

    ai = GomokuAI(depth=3, player=2)
    row, col = ai.find_best_move(game)
    print(f"AI's move to block: ({row}, {col})")
    print("Expected: Block at (7, 11) or (7, 6)")

    # Test 2: Creating winning opportunity
    print("\n2. Creating winning opportunity:")
    game = GomokuGame(size=15)

    # Setup a winning position for AI
    for col in range(6, 10):
        game.make_move(6, col)  # AI has three in a row

    print("Board state (AI has three in a row at row 6, cols 6-8):")
    game.print_board()

    row, col = ai.find_best_move(game)
    print(f"AI's move to create threat: ({row}, {col})")
    print("Expected: Extend to four at (6, 9) or (6, 5)")

    # Test 3: Center control
    print("\n3. Center control on empty board:")
    game = GomokuGame(size=15)
    row, col = ai.find_best_move(game)
    print(f"AI's first move on empty board: ({row}, {col})")
    print("Expected: Center at (7, 7)")


def main():
    """Main function to run different demonstrations."""
    print("Gomoku AI Integration Tests")
    print("="*50)

    while True:
        print("\nChoose an option:")
        print("1. Watch AI vs AI game")
        print("2. Play Human vs AI")
        print("3. Demonstrate AI capabilities")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == '1':
            play_ai_vs_ai()
        elif choice == '2':
            play_human_vs_ai()
        elif choice == '3':
            demonstrate_ai_capabilities()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()