#!/usr/bin/env python3
"""
Test script for Gomoku Flask API.

This script tests the basic functionality of the Gomoku API server.
Run it after starting the server with `python app.py`.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"


def test_server_status():
    """Test that the server is running."""
    print("Testing server status...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Server is running: {data['message']}")
            return True
        else:
            print(f"✗ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure it's running on localhost:5000")
        return False


def test_new_game():
    """Test creating a new game."""
    print("\nTesting new game creation...")

    # Test with default parameters
    response = requests.post(f"{BASE_URL}/api/new-game", json={})

    if response.status_code == 201:
        data = response.json()
        print(f"✓ New game created successfully")
        print(f"  Game ID: {data['game_id']}")
        print(f"  Board size: {data['size']}x{data['size']}")
        print(f"  Current player: {data['current_player']}")
        print(f"  AI player: {data['ai_player']}")
        return data['game_id']
    else:
        print(f"✗ Failed to create new game: {response.status_code}")
        print(f"  Response: {response.text}")
        return None


def test_custom_game():
    """Test creating a game with custom parameters."""
    print("\nTesting custom game creation...")

    custom_params = {
        "size": 10,
        "ai_depth": 2,
        "ai_player": 1
    }

    response = requests.post(f"{BASE_URL}/api/new-game", json=custom_params)

    if response.status_code == 201:
        data = response.json()
        print(f"✓ Custom game created successfully")
        print(f"  Game ID: {data['game_id']}")
        print(f"  Board size: {data['size']}x{data['size']} (requested: 10)")
        print(f"  Current player: {data['current_player']}")
        print(f"  AI player: {data['ai_player']} (requested: 1)")
        return data['game_id']
    else:
        print(f"✗ Failed to create custom game: {response.status_code}")
        return None


def test_invalid_game_params():
    """Test creating a game with invalid parameters."""
    print("\nTesting invalid game parameters...")

    invalid_params = [
        {"size": 3},  # Too small
        {"size": 25},  # Too large
        {"ai_depth": 0},  # Too low
        {"ai_depth": 10},  # Too high
        {"ai_player": 3},  # Invalid player
    ]

    for params in invalid_params:
        response = requests.post(f"{BASE_URL}/api/new-game", json=params)
        if response.status_code == 400:
            data = response.json()
            print(f"✓ Correctly rejected invalid params: {params}")
            print(f"  Error: {data['error']}")
        else:
            print(f"✗ Should have rejected invalid params: {params}")
            print(f"  Got status: {response.status_code}")


def test_make_move(game_id):
    """Test making a valid move."""
    print("\nTesting valid move...")

    # Make a move in the center
    move_data = {
        "game_id": game_id,
        "row": 7,
        "col": 7
    }

    response = requests.post(f"{BASE_URL}/api/move", json=move_data)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Move made successfully")
        print(f"  Move: ({data['move']['row']}, {data['move']['col']})")
        print(f"  New current player: {data['current_player']}")
        print(f"  Game over: {data['game_over']}")
        return True
    else:
        print(f"✗ Failed to make move: {response.status_code}")
        print(f"  Response: {response.text}")
        return False


def test_invalid_moves(game_id):
    """Test making invalid moves."""
    print("\nTesting invalid moves...")

    invalid_moves = [
        {"game_id": game_id, "row": -1, "col": 7},  # Out of bounds (negative)
        {"game_id": game_id, "row": 20, "col": 7},  # Out of bounds (too large)
        {"game_id": game_id, "row": 7, "col": 7},   # Already occupied
        {"game_id": "invalid-game-id", "row": 5, "col": 5},  # Invalid game ID
    ]

    for move in invalid_moves:
        response = requests.post(f"{BASE_URL}/api/move", json=move)
        if response.status_code in [400, 404]:
            data = response.json()
            print(f"✓ Correctly rejected invalid move: {move}")
            print(f"  Error: {data['error']}")
        else:
            print(f"✗ Should have rejected invalid move: {move}")
            print(f"  Got status: {response.status_code}")


def test_get_board(game_id):
    """Test getting board state."""
    print("\nTesting get board state...")

    response = requests.get(f"{BASE_URL}/api/board/{game_id}")

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Board state retrieved successfully")
        print(f"  Game ID: {data['game_id']}")
        print(f"  Board size: {data['size']}x{data['size']}")
        print(f"  Current player: {data['current_player']}")
        print(f"  Game over: {data['game_over']}")

        # Show a small portion of the board
        board = data['board']
        print(f"  Board preview (first 3 rows):")
        for i in range(min(3, len(board))):
            print(f"    Row {i}: {board[i][:5]}...")
        return True
    else:
        print(f"✗ Failed to get board: {response.status_code}")
        return False


def test_get_status(game_id):
    """Test getting game status."""
    print("\nTesting get game status...")

    response = requests.get(f"{BASE_URL}/api/status/{game_id}")

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Game status retrieved successfully")
        print(f"  Game ID: {data['game_id']}")
        print(f"  Game over: {data['game_over']}")
        print(f"  Result: {data['result']}")
        print(f"  Message: {data['message']}")
        return True
    else:
        print(f"✗ Failed to get status: {response.status_code}")
        return False


def test_get_ai_move(game_id):
    """Test getting AI move."""
    print("\nTesting get AI move...")

    response = requests.get(f"{BASE_URL}/api/ai-move/{game_id}")

    if response.status_code == 200:
        data = response.json()
        print(f"✓ AI move calculated successfully")
        print(f"  AI move: ({data['move']['row']}, {data['move']['col']})")
        print(f"  Current player: {data['current_player']}")
        print(f"  AI player: {data['ai_player']}")
        return data['move']
    elif response.status_code == 400:
        data = response.json()
        print(f"  Note: {data['error']}")
        print(f"  This is expected if it's not AI's turn")
        return None
    else:
        print(f"✗ Failed to get AI move: {response.status_code}")
        print(f"  Response: {response.text}")
        return None


def test_complete_game_flow():
    """Test a complete game flow from start to finish."""
    print("\n" + "="*60)
    print("Testing complete game flow...")
    print("="*60)

    # 1. Create new game
    game_id = test_new_game()
    if not game_id:
        print("✗ Cannot proceed without a game ID")
        return

    # 2. Get initial board state
    test_get_board(game_id)

    # 3. Get initial status
    test_get_status(game_id)

    # 4. Try to get AI move (should fail since it's player 1's turn)
    test_get_ai_move(game_id)

    # 5. Make a valid move
    if test_make_move(game_id):
        # 6. Now it should be AI's turn - get AI move
        ai_move = test_get_ai_move(game_id)

        if ai_move:
            # 7. Make the AI move
            move_data = {
                "game_id": game_id,
                "row": ai_move["row"],
                "col": ai_move["col"]
            }
            response = requests.post(f"{BASE_URL}/api/move", json=move_data)
            if response.status_code == 200:
                print(f"\n✓ Successfully made AI's suggested move")
                data = response.json()
                print(f"  Move: ({data['move']['row']}, {data['move']['col']})")
                print(f"  New current player: {data['current_player']}")

    # 8. Test invalid moves
    test_invalid_moves(game_id)

    # 9. Final status check
    test_get_status(game_id)

    print("\n" + "="*60)
    print("Complete game flow test finished!")
    print("="*60)


def main():
    """Run all tests."""
    print("Gomoku API Test Suite")
    print("="*60)

    # Check if server is running
    if not test_server_status():
        print("\nPlease start the server first:")
        print("  cd backend")
        print("  python app.py")
        return

    # Run individual tests
    game_id = test_new_game()

    if game_id:
        test_custom_game()
        test_invalid_game_params()
        test_make_move(game_id)
        test_get_board(game_id)
        test_get_status(game_id)
        test_get_ai_move(game_id)
        test_invalid_moves(game_id)

    # Run complete flow test
    test_complete_game_flow()

    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    main()