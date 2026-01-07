import axios from 'axios'
import type { GameState, CellPosition, GameSettings } from '../types/game'

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000 // 10 second timeout
})

// Request interceptor for adding auth tokens or other headers
apiClient.interceptors.request.use(
  (config) => {
    // You can add authentication tokens here if needed
    // const token = localStorage.getItem('auth_token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for handling errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)

    if (error.response) {
      // Server responded with error status
      switch (error.response.status) {
        case 401:
          console.error('Unauthorized - please login')
          break
        case 403:
          console.error('Forbidden - insufficient permissions')
          break
        case 404:
          console.error('Resource not found')
          break
        case 500:
          console.error('Server error')
          break
        default:
          console.error(`HTTP error: ${error.response.status}`)
      }
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network error - please check your connection')
    } else {
      // Something else happened
      console.error('Request error:', error.message)
    }

    return Promise.reject(error)
  }
)

// Game API endpoints
export const gameApi = {
  // Create a new game
  createGame: (settings?: Partial<GameSettings>) =>
    apiClient.post<{ gameId: string; state: GameState }>('/games', settings),

  // Get game state
  getGame: (gameId: string) =>
    apiClient.get<GameState>(`/games/${gameId}`),

  // Make a move
  makeMove: (gameId: string, position: CellPosition) =>
    apiClient.post<GameState>(`/games/${gameId}/move`, position),

  // Undo last move
  undoMove: (gameId: string) =>
    apiClient.post<GameState>(`/games/${gameId}/undo`),

  // Reset game
  resetGame: (gameId: string) =>
    apiClient.post<GameState>(`/games/${gameId}/reset`),

  // Get game history
  getGameHistory: (gameId: string) =>
    apiClient.get<CellPosition[]>(`/games/${gameId}/history`),

  // Get leaderboard
  getLeaderboard: (limit = 10) =>
    apiClient.get<Array<{ player: string; wins: number; losses: number }>>('/leaderboard', {
      params: { limit }
    })
}

// Utility function to check API health
export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const response = await apiClient.get('/health')
    return response.status === 200
  } catch (error) {
    console.error('API health check failed:', error)
    return false
  }
}

export default apiClient