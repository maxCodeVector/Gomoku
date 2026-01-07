<script setup lang="ts">
import { ref, computed } from 'vue'
import type { BoardState, CellPosition } from '../types/game'

const props = defineProps<{
  board: BoardState
  currentPlayer: 'black' | 'white'
  gameOver: boolean
  winner?: 'black' | 'white' | 'draw'
}>()

const emit = defineEmits<{
  cellClick: [position: CellPosition]
}>()

const boardSize = computed(() => props.board.length)

const handleCellClick = (row: number, col: number) => {
  if (!props.gameOver && props.board[row][col] === null) {
    emit('cellClick', { row, col })
  }
}

const getCellClass = (cell: string | null) => {
  if (cell === 'black') return 'cell-black'
  if (cell === 'white') return 'cell-white'
  return ''
}
</script>

<template>
  <div class="game-board">
    <div class="board-grid">
      <div
        v-for="(row, rowIndex) in board"
        :key="rowIndex"
        class="board-row"
      >
        <div
          v-for="(cell, colIndex) in row"
          :key="colIndex"
          :class="['board-cell', getCellClass(cell)]"
          @click="handleCellClick(rowIndex, colIndex)"
        >
          <div class="cell-content">
            <div v-if="cell === 'black'" class="stone black-stone"></div>
            <div v-if="cell === 'white'" class="stone white-stone"></div>
            <div v-if="cell === null" class="empty-cell"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.game-board {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.board-grid {
  display: inline-block;
  background-color: #deb887;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.board-row {
  display: flex;
}

.board-cell {
  width: 40px;
  height: 40px;
  border: 1px solid #8b4513;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  background-color: #deb887;
}

.board-cell:hover {
  background-color: #d2b48c;
}

.cell-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stone {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.black-stone {
  background: radial-gradient(circle at 30% 30%, #666, #000);
}

.white-stone {
  background: radial-gradient(circle at 30% 30%, #fff, #ccc);
  border: 1px solid #999;
}

.empty-cell {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.1);
}
</style>