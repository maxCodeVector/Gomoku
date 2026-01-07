# Gomoku Game Frontend

A modern Gomoku (Five in a Row) game built with Vue 3, TypeScript, and Element Plus.

## Features

- **Interactive Game Board**: 15x15 board with smooth stone placement
- **Game Logic**: Complete win detection (horizontal, vertical, diagonal)
- **Game Controls**: New game, reset, undo move functionality
- **Board Size Selection**: Choose from 9x9, 13x13, 15x15, or 19x19 boards
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean interface with Element Plus components
- **State Management**: Pinia store for centralized game state
- **API Integration**: Ready-to-use API service layer for backend communication

## Tech Stack

- **Vue 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Next-generation frontend tooling
- **Pinia** - State management
- **Element Plus** - UI component library
- **Axios** - HTTP client for API calls
- **ESLint** - Code linting
- **Vitest** - Testing framework

## Project Structure

```
src/
├── components/         # Vue components
│   ├── GameBoard.vue   # Game board component
│   └── GameControls.vue # Game controls component
├── views/             # Page components (if needed)
├── stores/            # Pinia stores
│   └── gameStore.ts   # Game state management
├── services/          # API services
│   └── api.ts         # API client configuration
├── types/             # TypeScript type definitions
│   └── game.ts        # Game-related types
├── utils/             # Utility functions
├── App.vue            # Root component
└── main.ts            # Application entry point
```

## Getting Started

### Prerequisites

- Node.js 18.0.0 or higher
- npm 8.0.0 or higher

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Building for Production

Build the project:

```bash
npm run build
```

Preview the production build:

```bash
npm run serve
```

### Other Commands

- **Lint code**: `npm run lint`
- **Type checking**: `npm run type-check`
- **Run tests**: `npm run test`
- **Test with UI**: `npm run test:ui`

## API Integration

The frontend is configured to communicate with a backend API:

- **Development**: Proxy to `http://localhost:5000`
- **Production**: Uses relative `/api` path
- **Environment Variables**: Configured in `.env.development` and `.env.production`

## Game Rules

1. Players take turns placing stones on the board
2. Black goes first
3. The first player to get 5 stones in a row (horizontally, vertically, or diagonally) wins
4. The game ends in a draw if the board is completely filled

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

MIT
