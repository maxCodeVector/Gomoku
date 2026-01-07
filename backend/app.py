"""
Flask API server for Gomoku game.

This module provides a RESTful API for playing Gomoku against an AI opponent.
It maintains game state in memory and provides endpoints for game operations.

Endpoints:
- POST /api/new-game: Start a new game
- POST /api/move: Make a player move
- GET /api/ai-move/<game_id>: Get AI's best move
- GET /api/board/<game_id>: Get current board state
- GET /api/status/<game_id>: Check game status (win/draw)
- GET /: Test route to verify server is running
"""

import uuid
from typing import Dict, Tuple, Any
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import game logic
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gomoku import GomokuGame
from backend.ai import GomokuAI


# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend integration

# In-memory storage for active games
# Structure: {game_id: {"game": GomokuGame instance, "ai": GomokuAI instance}}
games: Dict[str, Dict[str, Any]] = {}


@app.route('/')
def index():
    """
    Test route to verify the server is running.

    Returns:
        JSON response with server status
    """
    return jsonify({
        "status": "running",
        "message": "Gomoku API Server is running",
        "endpoints": {
            "new_game": "POST /api/new-game",
            "make_move": "POST /api/move",
            "get_ai_move": "GET /api/ai-move/<game_id>",
            "get_board": "GET /api/board/<game_id>",
            "get_status": "GET /api/status/<game_id>"
        }
    })


@app.route('/api/new-game', methods=['POST'])
def new_game():
    """
    Start a new Gomoku game.

    Request body (optional):
        - size: Board size (default: 15)
        - ai_depth: AI search depth (default: 3)
        - ai_player: Which player the AI controls (1 or 2, default: 2)

    Returns:
        JSON response with game ID and initial board state
    """
    try:
        # Parse request parameters
        data = request.get_json() or {}
        size = data.get('size', 15)
        ai_depth = data.get('ai_depth', 3)
        ai_player = data.get('ai_player', 2)

        # Validate parameters
        if not isinstance(size, int) or size < 5 or size > 20:
            return jsonify({
                "error": "Invalid board size. Must be an integer between 5 and 20."
            }), 400

        if not isinstance(ai_depth, int) or ai_depth < 1 or ai_depth > 5:
            return jsonify({
                "error": "Invalid AI depth. Must be an integer between 1 and 5."
            }), 400

        if ai_player not in [1, 2]:
            return jsonify({
                "error": "Invalid AI player. Must be 1 or 2."
            }), 400

        # Generate unique game ID
        game_id = str(uuid.uuid4())

        # Initialize game and AI
        game = GomokuGame(size=size)
        ai = GomokuAI(depth=ai_depth, player=ai_player)

        # Store game in memory
        games[game_id] = {
            "game": game,
            "ai": ai,
            "size": size,
            "ai_player": ai_player
        }

        # Return game information
        return jsonify({
            "game_id": game_id,
            "board": game.get_board(),
            "size": size,
            "current_player": game.current_player,
            "ai_player": ai_player,
            "message": "New game created successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "error": f"Failed to create new game: {str(e)}"
        }), 500


@app.route('/api/move', methods=['POST'])
def make_move():
    """
    Make a player move in an existing game.

    Request body:
        - game_id: ID of the game
        - row: Row index (0-based)
        - col: Column index (0-based)

    Returns:
        JSON response with updated game state
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data:
            return jsonify({"error": "Request body is required"}), 400

        game_id = data.get('game_id')
        row = data.get('row')
        col = data.get('col')

        if not game_id:
            return jsonify({"error": "game_id is required"}), 400

        if row is None or col is None:
            return jsonify({"error": "row and col are required"}), 400

        # Check if game exists
        if game_id not in games:
            return jsonify({"error": "Game not found"}), 404

        game_data = games[game_id]
        game = game_data["game"]

        # Validate move coordinates
        if not isinstance(row, int) or not isinstance(col, int):
            return jsonify({"error": "row and col must be integers"}), 400

        if row < 0 or row >= game.size or col < 0 or col >= game.size:
            return jsonify({
                "error": f"Move ({row}, {col}) is out of bounds. Board size is {game.size}x{game.size}."
            }), 400

        # Make the move
        success = game.make_move(row, col)

        if not success:
            # Check why the move failed
            if game.game_over:
                return jsonify({"error": "Game is already over"}), 400
            elif game.board[row][col] != 0:
                return jsonify({"error": f"Position ({row}, {col}) is already occupied"}), 400
            else:
                return jsonify({"error": "Invalid move"}), 400

        # Prepare response
        response = {
            "game_id": game_id,
            "move": {"row": row, "col": col},
            "board": game.get_board(),
            "current_player": game.current_player,
            "game_over": game.game_over
        }

        # Add winner information if game is over
        if game.game_over:
            response["winner"] = game.winner
            if game.winner == 0:
                response["result"] = "draw"
            else:
                response["result"] = f"player_{game.winner}_wins"

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": f"Failed to make move: {str(e)}"
        }), 500


@app.route('/api/ai-move/<game_id>', methods=['GET'])
def get_ai_move(game_id):
    """
    Get the AI's best move for the current game state.

    Args:
        game_id: ID of the game

    Returns:
        JSON response with AI's recommended move
    """
    try:
        # Check if game exists
        if game_id not in games:
            return jsonify({"error": "Game not found"}), 404

        game_data = games[game_id]
        game = game_data["game"]
        ai = game_data["ai"]

        # Check if game is over
        if game.game_over:
            return jsonify({
                "error": "Game is already over",
                "winner": game.winner
            }), 400

        # Check if it's AI's turn
        if game.current_player != ai.player:
            return jsonify({
                "error": f"It's not AI's turn. Current player is {game.current_player}",
                "current_player": game.current_player,
                "ai_player": ai.player
            }), 400

        # Get AI's best move
        row, col = ai.find_best_move(game)

        return jsonify({
            "game_id": game_id,
            "move": {"row": row, "col": col},
            "current_player": game.current_player,
            "ai_player": ai.player,
            "message": "AI move calculated successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Failed to get AI move: {str(e)}"
        }), 500


@app.route('/api/board/<game_id>', methods=['GET'])
def get_board(game_id):
    """
    Get the current board state of a game.

    Args:
        game_id: ID of the game

    Returns:
        JSON response with current board state
    """
    try:
        # Check if game exists
        if game_id not in games:
            return jsonify({"error": "Game not found"}), 404

        game_data = games[game_id]
        game = game_data["game"]

        return jsonify({
            "game_id": game_id,
            "board": game.get_board(),
            "size": game.size,
            "current_player": game.current_player,
            "game_over": game.game_over,
            "winner": game.winner if game.game_over else None
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Failed to get board state: {str(e)}"
        }), 500


@app.route('/api/status/<game_id>', methods=['GET'])
def get_status(game_id):
    """
    Check if a game is over (win/draw).

    Args:
        game_id: ID of the game

    Returns:
        JSON response with game status
    """
    try:
        # Check if game exists
        if game_id not in games:
            return jsonify({"error": "Game not found"}), 404

        game_data = games[game_id]
        game = game_data["game"]

        status = {
            "game_id": game_id,
            "game_over": game.game_over,
            "current_player": game.current_player
        }

        if game.game_over:
            if game.winner == 0:
                status["result"] = "draw"
                status["message"] = "Game ended in a draw"
            else:
                status["result"] = "win"
                status["winner"] = game.winner
                status["message"] = f"Player {game.winner} wins!"
        else:
            status["result"] = "in_progress"
            status["message"] = f"Game in progress. Current player: {game.current_player}"

        return jsonify(status), 200

    except Exception as e:
        return jsonify({
            "error": f"Failed to get game status: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.

    Returns:
        JSON response for not found errors
    """
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Handle 405 errors.

    Returns:
        JSON response for method not allowed errors
    """
    return jsonify({
        "error": "Method not allowed",
        "message": "The HTTP method is not supported for this endpoint"
    }), 405


if __name__ == '__main__':
    """
    Run the Flask development server.

    Usage:
        python app.py

    The server will run on http://localhost:5000 by default.
    """
    print("Starting Gomoku API Server...")
    print("Server running at http://localhost:5000")
    print("Test endpoint: GET /")
    print("\nAvailable endpoints:")
    print("  POST /api/new-game - Start a new game")
    print("  POST /api/move - Make a player move")
    print("  GET /api/ai-move/<game_id> - Get AI's best move")
    print("  GET /api/board/<game_id> - Get current board state")
    print("  GET /api/status/<game_id> - Check game status")

    app.run(debug=True, host='0.0.0.0', port=5000)