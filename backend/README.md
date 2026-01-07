# Gomoku Flask API Server

A RESTful API server for playing Gomoku (Five in a Row) against an AI opponent.

## Features

- RESTful API with JSON responses
- In-memory game state management
- Smart AI opponent using Minimax algorithm with alpha-beta pruning
- Cross-origin resource sharing (CORS) enabled
- Comprehensive error handling
- Game state persistence for active sessions

## Requirements

- Python 3.7+
- Flask 2.3.3
- Flask-CORS 4.0.0

## Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the Flask development server:
```bash
python app.py
```

The server will start on `http://localhost:5000`.

## API Endpoints

### 1. Test Server Status
**GET /**
Check if the server is running.

**Response:**
```json
{
  "status": "running",
  "message": "Gomoku API Server is running",
  "endpoints": {
    "new_game": "POST /api/new-game",
    "make_move": "POST /api/move",
    "get_ai_move": "GET /api/ai-move/<game_id>",
    "get_board": "GET /api/board/<game_id>",
    "get_status": "GET /api/status/<game_id>"
  }
}
```

### 2. Create New Game
**POST /api/new-game**
Start a new Gomoku game.

**Request Body (optional):**
```json
{
  "size": 15,
  "ai_depth": 3,
  "ai_player": 2
}
```

- `size`: Board size (default: 15, range: 5-20)
- `ai_depth`: AI search depth (default: 3, range: 1-5)
- `ai_player`: Which player the AI controls (1 or 2, default: 2)

**Response:**
```json
{
  "game_id": "uuid-string",
  "board": [[0,0,0,...], ...],
  "size": 15,
  "current_player": 1,
  "ai_player": 2,
  "message": "New game created successfully"
}
```

### 3. Make a Move
**POST /api/move**
Make a player move in an existing game.

**Request Body:**
```json
{
  "game_id": "uuid-string",
  "row": 7,
  "col": 7
}
```

**Response:**
```json
{
  "game_id": "uuid-string",
  "move": {"row": 7, "col": 7},
  "board": [[0,0,0,...], ...],
  "current_player": 2,
  "game_over": false
}
```

If game is over:
```json
{
  "game_id": "uuid-string",
  "move": {"row": 7, "col": 11},
  "board": [[0,0,0,...], ...],
  "current_player": 2,
  "game_over": true,
  "winner": 1,
  "result": "player_1_wins"
}
```

### 4. Get AI Move
**GET /api/ai-move/<game_id>**
Get the AI's best move for the current game state.

**Response:**
```json
{
  "game_id": "uuid-string",
  "move": {"row": 6, "col": 6},
  "current_player": 2,
  "ai_player": 2,
  "message": "AI move calculated successfully"
}
```

### 5. Get Board State
**GET /api/board/<game_id>**
Get the current board state of a game.

**Response:**
```json
{
  "game_id": "uuid-string",
  "board": [[0,0,0,...], ...],
  "size": 15,
  "current_player": 1,
  "game_over": false,
  "winner": null
}
```

### 6. Get Game Status
**GET /api/status/<game_id>**
Check if a game is over (win/draw).

**Response:**
```json
{
  "game_id": "uuid-string",
  "game_over": false,
  "current_player": 1,
  "result": "in_progress",
  "message": "Game in progress. Current player: 1"
}
```

If game is over:
```json
{
  "game_id": "uuid-string",
  "game_over": true,
  "current_player": 2,
  "result": "win",
  "winner": 1,
  "message": "Player 1 wins!"
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid input parameters
- **404 Not Found**: Game not found
- **405 Method Not Allowed**: Invalid HTTP method
- **500 Internal Server Error**: Server-side errors

Error response format:
```json
{
  "error": "Error message description"
}
```

## Game Rules

- Board: N×N grid (default 15×15)
- Players: 1 (human) and 2 (AI by default)
- Objective: Get 5 stones in a row (horizontal, vertical, or diagonal)
- Turns: Players alternate turns
- Draw: When the board is full with no winner

## AI Implementation

The AI uses:
- Minimax algorithm with alpha-beta pruning
- Heuristic evaluation function considering:
  - Consecutive stones (2, 3, 4, 5 in a row)
  - Open-ended sequences
  - Defensive blocking
  - Center control
- Search depth configurable via `ai_depth` parameter

## Example Game Flow

1. **Create a new game:**
   ```bash
   curl -X POST http://localhost:5000/api/new-game \
     -H "Content-Type: application/json" \
     -d '{"size": 15, "ai_depth": 3}'
   ```

2. **Make a move:**
   ```bash
   curl -X POST http://localhost:5000/api/move \
     -H "Content-Type: application/json" \
     -d '{"game_id": "your-game-id", "row": 7, "col": 7}'
   ```

3. **Get AI move:**
   ```bash
   curl http://localhost:5000/api/ai-move/your-game-id
   ```

4. **Check board state:**
   ```bash
   curl http://localhost:5000/api/board/your-game-id
   ```

5. **Check game status:**
   ```bash
   curl http://localhost:5000/api/status/your-game-id
   ```

## Development

### Project Structure
```
backend/
├── app.py              # Flask API server
├── ai.py               # AI implementation
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── __pycache__/       # Python cache
```

### Testing
Run the server and test endpoints using curl or a tool like Postman.

### Notes
- Game state is stored in memory and will be lost when the server restarts
- For production use, consider adding:
  - Database persistence
  - Authentication
  - Rate limiting
  - Logging
  - Unit tests