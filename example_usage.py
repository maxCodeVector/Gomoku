#!/usr/bin/env python3
"""
Example usage of the Gomoku AI.
Demonstrates how to integrate the AI with the game.
"""

import sys
import os

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gomoku import GomokuGame
from backend.ai import GomokuAI


def play_simple_game():
    """Play a simple game between human and AI."""
    print("=== Gomoku: Human vs AI ===")
    print("You are Player 1 (stones: 1)")
    print("AI is Player 2 (stones: 2)")
    print("Board size: 15x15")
    print("Enter moves as 'row col' (0-14)")
    print("Enter 'q' to quit\n")

    # Initialize game and AI
    game = GomokuGame(size=15)
    ai = GomokuAI(depth=3, player=2)  # AI with search depth 3

    while not game.game_over:
        print(f"\n=== Turn {sum(1 for row in game.board for cell in row if cell != 0) + 1} ===")
        print(f"Current player: {game.current_player}")
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

    # Game over
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


def demonstrate_ai_strength():
    """Demonstrate the AI's capabilities with different search depths."""
    print("\n=== AI Strength Demonstration ===")

    # Create a game state with a threat
    game = GomokuGame(size=15)

    # Player 1 creates a three-in-a-row
    game.make_move(7, 7)
    game.make_move(7, 8)
    game.make_move(7, 9)

    print("Board state: Player 1 has three in a row at (7, 7-9)")
    game.print_board()

    # Test AI with different depths
    for depth in [1, 2, 3]:
        print(f"\nAI with depth {depth}:")
        ai = GomokuAI(depth=depth, player=2)
        row, col = ai.find_best_move(game)
        print(f"  Best move: ({row}, {col})")
        print(f"  Expected: Should block at (7, 10) or (7, 6)")


def ai_vs_ai_match():
    """Watch two AI players compete against each other."""
    print("\n=== AI vs AI Match ===")

    game = GomokuGame(size=15)

    # Create two AIs with different strengths
    weak_ai = GomokuAI(depth=2, player=1)   # Weaker AI (depth 2)
    strong_ai = GomokuAI(depth=4, player=2)  # Stronger AI (depth 4)

    print("Weak AI (depth 2) is Player 1")
    print("Strong AI (depth 4) is Player 2")
    print("Starting match...\n")

    move_count = 0
    max_moves = 30  # Limit for demonstration

    while not game.game_over and move_count < max_moves:
        current_player = game.current_player

        if current_player == 1:
            ai = weak_ai
            ai_name = "Weak AI"
        else:
            ai = strong_ai
            ai_name = "Strong AI"

        # Get AI's move
        row, col = ai.find_best_move(game)

        print(f"Move {move_count + 1}: {ai_name} plays at ({row}, {col})")

        # Make the move
        game.make_move(row, col)
        move_count += 1

        # Show board every 5 moves
        if move_count % 5 == 0:
            print(f"\nBoard after {move_count} moves:")
            game.print_board()

    print("\n" + "="*50)
    print("Match Result:")

    if game.game_over:
        if game.winner == 0:
            print("It's a draw!")
        else:
            print(f"Player {game.winner} ({'Weak AI' if game.winner == 1 else 'Strong AI'}) wins!")
    else:
        print(f"Match stopped after {move_count} moves (limit reached)")

    print("\nFinal board:")
    game.print_board()


if __name__ == "__main__":
    print("Gomoku AI Examples")
    print("="*50)

    while True:
        print("\nChoose an example:")
        print("1. Play Human vs AI")
        print("2. Demonstrate AI strength with different depths")
        print("3. Watch AI vs AI match")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == '1':
            play_simple_game()
        elif choice == '2':
            demonstrate_ai_strength()
        elif choice == '3':
            ai_vs_ai_match()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")