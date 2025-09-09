<template>
  <div class="status-bar">
    <div class="d-flex align-items-center justify-content-between px-3">
      <div class="status-left">
        <span class="status-item" id="current-repo-status">
          <i class="fas fa-folder me-1"></i>No repository
        </span>
        <span class="status-item" id="current-branch-status">
          <i class="fas fa-code-branch me-1"></i>-
        </span>
        <span class="status-item" id="git-status">
          <i class="fas fa-circle text-success me-1"></i>Clean
        </span>
      </div>
      <div class="status-right">
        <span class="status-item">
          <inline-loading :visible="loading.isLoading" :message="loading.message"/>
        </span>
        <span class="status-item">
          <i class="fas fa-palette me-1"></i>Material Darker
        </span>
        <span class="status-item">
          <i class="fas fa-memory me-1"></i>{{ memoryUsed }}
        </span>
        <span class="status-item">
          <i class="fas fa-clock me-1"></i>{{ currentTime }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import InlineLoading from '@/components/Loading/InlineLoading.vue'
import { useLoadingStore } from '@/stores/loadingStore.js'

const loading = useLoadingStore()
const memoryUsed = ref('Loading...')
const currentTime = ref('--:--:--')

function formatMemory(kb) {
  if (!kb || isNaN(kb)) return 'N/A'
  return Math.round(kb / 1024) + ' MB'
}

async function fetchMemory() {
  try {
    if (window.electronAPI?.getMemoryInfo) {
      const info = await window.electronAPI.getMemoryInfo()
      console.log('Memory info:', info)
      memoryUsed.value = info?.ramKB
        ? formatMemory(info.ramKB)
        : 'N/A'
    } else {
      memoryUsed.value = 'N/A'
    }
  } catch (error) {
    console.error('Error getting memory info:', error)
    memoryUsed.value = 'Error'
  }
}

function updateClock() {
  const now = new Date()
  const hh = String(now.getHours()).padStart(2, '0')
  const mm = String(now.getMinutes()).padStart(2, '0')
  const ss = String(now.getSeconds()).padStart(2, '0')
  currentTime.value = `${hh}:${mm}:${ss}`
}

onMounted(() => {
  fetchMemory()
  setInterval(fetchMemory, 5000)
  setInterval(updateClock, 1000)
})
</script>

<style scoped>
.status-bar {
  background-color: var(--bg-tertiary);
  border-top: 1px solid var(--border-color);
  min-height: 24px;
  font-size: 11px;
  color: var(--text-secondary);
}

.status-item {
  margin-right: 16px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
</style>
