<template>
  <div class="status-bar">
    <div class="status-left">
        <span class="status-item" id="current-repo-status">
          <i class="fas fa-folder me-1"></i>{{ currentRepo }}
        </span>
      <span class="status-item" id="current-branch-status">
          <i class="fas fa-code-branch me-1" style="color: #4fc3f7"></i>
          {{ currentBranch }}
        </span>
      <span class="status-item" id="git-status">
        <i
          class="fas"
          :class="[getStatusIcon(gitStatus), getStatusColor(gitStatus)]"
          :title="gitStatus"
        />
          {{ capitalize(gitStatus) }}
        </span>
    </div>
    <div class="status-right">
        <span class="status-item">
          <inline-loading :visible="loading.isLoading" :message="loading.message" />
        </span>
      <span class="status-item"> <i class="fas fa-palette me-1"></i>Material Darker </span>
      <span class="status-item"> <i class="fas fa-memory me-1"></i>{{ memoryUsed }} </span>
      <span class="status-item"> <i class="fas fa-clock me-1"></i>{{ currentTime }} </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import InlineLoading from '@/components/Loading/InlineLoading.vue'
import { useLoadingStore } from '@/stores/loadingStore.js'
import { useRepositoryStore } from '@/stores/repositoryStore.js'

const loading = useLoadingStore()
const repositoryStore = useRepositoryStore()

const memoryUsed = ref('Loading...')
const currentTime = ref('--:--:--')

const currentRepo = computed(() => repositoryStore.activeRepo?.name || 'No repository')
const currentBranch = computed(() => repositoryStore.activeRepo?.branch || '-')
const gitStatus = computed(() => repositoryStore.activeRepo?.status || '-')

function formatMemory(kb) {
  if (!kb || isNaN(kb)) return 'N/A'
  return Math.round(kb / 1024) + ' MB'
}

async function fetchMemory() {
  try {
    if (window.electronAPI?.getMemoryInfo) {
      const info = await window.electronAPI.getMemoryInfo()
      console.log('Memory info:', info)
      memoryUsed.value = info?.ramKB ? formatMemory(info.ramKB) : 'N/A'
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

const getStatusIcon = (status) => {
  switch (status) {
    case 'clean':
      return 'fa-check-circle'
    case 'dirty':
      return 'fa-exclamation-circle'
    case 'untracked':
      return 'fa-question-circle'
    default:
      return 'fa-circle'
  }
}

const getStatusColor = (status) => {
  switch (status) {
    case 'clean':
      return 'text-success'
    case 'dirty':
      return 'text-warning'
    case 'untracked':
      return 'text-secondary'
    default:
      return 'text-muted'
  }
}

function capitalize(str) {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<style scoped>
.status-bar {
  background-color: var(--bg-tertiary);
  border-top: 1px solid var(--border-color);
  min-height: 34px;
  font-size: 12px;
  color: var(--text-secondary);

  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
}

.status-left,
.status-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding-bottom: 5px;
}
</style>
