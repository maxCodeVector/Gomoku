<script setup lang="ts">
import { ElButton, ElSelect, ElOption } from 'element-plus'

const props = defineProps<{
  currentPlayer: 'black' | 'white'
  gameOver: boolean
  winner?: 'black' | 'white' | 'draw'
  boardSize: number
}>()

const emit = defineEmits<{
  newGame: []
  resetGame: []
  undoMove: []
  changeBoardSize: [size: number]
}>()

const handleNewGame = () => {
  emit('newGame')
}

const handleResetGame = () => {
  emit('resetGame')
}

const handleUndoMove = () => {
  emit('undoMove')
}

const handleBoardSizeChange = (size: number) => {
  emit('changeBoardSize', size)
}

const boardSizeOptions = [
  { value: 9, label: '9x9' },
  { value: 13, label: '13x13' },
  { value: 15, label: '15x15' },
  { value: 19, label: '19x19' }
]
</script>

<template>
  <div class="game-controls">
    <div class="controls-section">
      <h3>Game Controls</h3>
      <div class="buttons-row">
        <ElButton type="primary" @click="handleNewGame" class="control-button">
          New Game
        </ElButton>
        <ElButton @click="handleResetGame" class="control-button">
          Reset Game
        </ElButton>
        <ElButton @click="handleUndoMove" class="control-button">
          Undo Move
        </ElButton>
      </div>
    </div>

    <div class="controls-section">
      <h3>Game Settings</h3>
      <div class="settings-row">
        <div class="setting-item">
          <span class="setting-label">Board Size:</span>
          <ElSelect
            :model-value="boardSize"
            @update:model-value="handleBoardSizeChange"
            class="board-size-select"
          >
            <ElOption
              v-for="option in boardSizeOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </ElSelect>
        </div>
      </div>
    </div>

    <div class="game-status">
      <h3>Game Status</h3>
      <div class="status-info">
        <div class="status-item">
          <span class="status-label">Current Player:</span>
          <span :class="['player-indicator', currentPlayer]">
            {{ currentPlayer === 'black' ? 'Black' : 'White' }}
          </span>
        </div>
        <div v-if="gameOver" class="status-item">
          <span class="status-label">Game Result:</span>
          <span class="game-result">
            <span v-if="winner === 'draw'">Draw!</span>
            <span v-else>{{ winner === 'black' ? 'Black' : 'White' }} Wins!</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.game-controls {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.controls-section {
  margin-bottom: 24px;
}

.controls-section h3 {
  margin-top: 0;
  margin-bottom: 12px;
  color: #333;
  font-size: 16px;
}

.buttons-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.control-button {
  min-width: 100px;
}

.settings-row {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.setting-label {
  min-width: 100px;
  color: #666;
}

.board-size-select {
  width: 120px;
}

.game-status {
  background-color: #fff;
  border-radius: 6px;
  padding: 16px;
  border: 1px solid #e0e0e0;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-label {
  min-width: 120px;
  color: #666;
}

.player-indicator {
  padding: 4px 12px;
  border-radius: 4px;
  font-weight: bold;
  color: white;
}

.player-indicator.black {
  background-color: #000;
}

.player-indicator.white {
  background-color: #fff;
  color: #333;
  border: 1px solid #ccc;
}

.game-result {
  font-weight: bold;
  color: #1890ff;
}
</style>