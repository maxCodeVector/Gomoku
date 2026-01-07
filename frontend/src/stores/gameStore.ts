import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { GameState, CellPosition, Player, BoardState } from '../types/game'

const createEmptyBoard = (size: number): BoardState => {
  return Array(size).fill(null).map(() => Array(size).fill(null))
}

export const useGameStore = defineStore('game', () => {
  // State
  const boardSize = ref(15)
  const board = ref<BoardState>(createEmptyBoard(boardSize.value))
  const currentPlayer = ref<Player>('black')
  const gameOver = ref(false)
  const winner = ref<Player | 'draw'>()
  const moveHistory = ref<CellPosition[]>([])

  // Getters
  const getBoard = computed(() => board.value)
  const getCurrentPlayer = computed(() => currentPlayer.value)
  const isGameOver = computed(() => gameOver.value)
  const getWinner = computed(() => winner.value)
  const getMoveHistory = computed(() => moveHistory.value)
  const getBoardSize = computed(() => boardSize.value)

  // Actions
  const makeMove = (position: CellPosition) => {
    if (gameOver.value || board.value[position.row][position.col] !== null) {
      return false
    }

    // Make the move
    board.value[position.row][position.col] = currentPlayer.value
    moveHistory.value.push(position)

    // Check for win
    if (checkWin(position)) {
      gameOver.value = true
      winner.value = currentPlayer.value
      return true
    }

    // Check for draw
    if (checkDraw()) {
      gameOver.value = true
      winner.value = 'draw'
      return true
    }

    // Switch player
    currentPlayer.value = currentPlayer.value === 'black' ? 'white' : 'black'
    return true
  }

  const checkWin = (lastMove: CellPosition): boolean => {
    const player = board.value[lastMove.row][lastMove.col]
    if (!player) return false

    const directions = [
      [0, 1],   // horizontal
      [1, 0],   // vertical
      [1, 1],   // diagonal down-right
      [1, -1]   // diagonal down-left
    ]

    for (const [dx, dy] of directions) {
      let count = 1

      // Check positive direction
      for (let i = 1; i < 5; i++) {
        const newRow = lastMove.row + dx * i
        const newCol = lastMove.col + dy * i
        if (
          newRow >= 0 && newRow < boardSize.value &&
          newCol >= 0 && newCol < boardSize.value &&
          board.value[newRow][newCol] === player
        ) {
          count++
        } else {
          break
        }
      }

      // Check negative direction
      for (let i = 1; i < 5; i++) {
        const newRow = lastMove.row - dx * i
        const newCol = lastMove.col - dy * i
        if (
          newRow >= 0 && newRow < boardSize.value &&
          newCol >= 0 && newCol < boardSize.value &&
          board.value[newRow][newCol] === player
        ) {
          count++
        } else {
          break
        }
      }

      if (count >= 5) {
        return true
      }
    }

    return false
  }

  const checkDraw = (): boolean => {
    return board.value.every(row => row.every(cell => cell !== null))
  }

  const resetGame = () => {
    board.value = createEmptyBoard(boardSize.value)
    currentPlayer.value = 'black'
    gameOver.value = false
    winner.value = undefined
    moveHistory.value = []
  }

  const newGame = (size?: number) => {
    if (size && size !== boardSize.value) {
      boardSize.value = size
    }
    resetGame()
  }

  const undoMove = () => {
    if (moveHistory.value.length === 0) return false

    const lastMove = moveHistory.value.pop()
    if (!lastMove) return false

    board.value[lastMove.row][lastMove.col] = null
    currentPlayer.value = currentPlayer.value === 'black' ? 'white' : 'black'
    gameOver.value = false
    winner.value = undefined

    return true
  }

  const changeBoardSize = (size: number) => {
    if (size !== boardSize.value) {
      boardSize.value = size
      resetGame()
    }
  }

  return {
    // State
    board,
    currentPlayer,
    gameOver,
    winner,
    moveHistory,
    boardSize,

    // Getters
    getBoard,
    getCurrentPlayer,
    isGameOver,
    getWinner,
    getMoveHistory,
    getBoardSize,

    // Actions
    makeMove,
    resetGame,
    newGame,
    undoMove,
    changeBoardSize
  }
})