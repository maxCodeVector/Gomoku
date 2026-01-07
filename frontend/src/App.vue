<script setup lang="ts">
import { ElContainer, ElHeader, ElMain, ElFooter } from 'element-plus'
import GameBoard from './components/GameBoard.vue'
import GameControls from './components/GameControls.vue'
import { useGameStore } from './stores/gameStore'
import type { CellPosition } from './types/game'

const gameStore = useGameStore()

const handleCellClick = (position: CellPosition) => {
  gameStore.makeMove(position)
}

const handleNewGame = () => {
  gameStore.newGame()
}

const handleResetGame = () => {
  gameStore.resetGame()
}

const handleUndoMove = () => {
  gameStore.undoMove()
}

const handleBoardSizeChange = (size: number) => {
  gameStore.changeBoardSize(size)
}
</script>

<template>
  <ElContainer class="app-container">
    <ElHeader class="app-header">
      <h1>Gomoku Game</h1>
      <p class="subtitle">Five in a Row - A classic strategy game</p>
    </ElHeader>

    <ElMain class="app-main">
      <div class="game-container">
        <div class="game-board-section">
          <GameBoard
            :board="gameStore.getBoard"
            :current-player="gameStore.getCurrentPlayer"
            :game-over="gameStore.isGameOver"
            :winner="gameStore.getWinner"
            @cell-click="handleCellClick"
          />
        </div>

        <div class="game-controls-section">
          <GameControls
            :current-player="gameStore.getCurrentPlayer"
            :game-over="gameStore.isGameOver"
            :winner="gameStore.getWinner"
            :board-size="gameStore.getBoardSize"
            @new-game="handleNewGame"
            @reset-game="handleResetGame"
            @undo-move="handleUndoMove"
            @change-board-size="handleBoardSizeChange"
          />
        </div>
      </div>
    </ElMain>

    <ElFooter class="app-footer">
      <div class="footer-content">
        <p>Gomoku Game &copy; 2024 | Built with Vue 3 + TypeScript + Element Plus</p>
        <p class="game-instructions">
          <strong>How to play:</strong> Players take turns placing stones. Black goes first.
          The first player to get 5 stones in a row (horizontally, vertically, or diagonally) wins!
        </p>
      </div>
    </ElFooter>
  </ElContainer>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: bold;
}

.subtitle {
  margin: 8px 0 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.app-main {
  flex: 1;
  padding: 20px;
  background-color: #f8f9fa;
}

.game-container {
  display: flex;
  gap: 40px;
  max-width: 1400px;
  margin: 0 auto;
  flex-wrap: wrap;
}

.game-board-section {
  flex: 2;
  min-width: 300px;
}

.game-controls-section {
  flex: 1;
  min-width: 300px;
}

.app-footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 20px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.game-instructions {
  margin-top: 10px;
  font-size: 0.9rem;
  opacity: 0.8;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 768px) {
  .game-container {
    flex-direction: column;
  }

  .app-header h1 {
    font-size: 2rem;
  }
}
</style>
