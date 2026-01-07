export type Player = 'black' | 'white'
export type CellValue = Player | null
export type BoardState = CellValue[][]

export interface CellPosition {
  row: number
  col: number
}

export interface GameState {
  board: BoardState
  currentPlayer: Player
  gameOver: boolean
  winner?: Player | 'draw'
  moveHistory: CellPosition[]
  boardSize: number
}

export interface GameMove {
  position: CellPosition
  player: Player
  timestamp: Date
}

export interface GameSettings {
  boardSize: number
  enableUndo: boolean
  timeLimit?: number // in seconds
}