<template>
  <div class="right-panel-wrapper" :style="{ width: containerWidth + 'px' }">
    <!-- Thanh kéo nằm bên trái panel -->
    <div class="resizer-horizontal" @mousedown="startResizeContainer" v-if="!isCollapsed"></div>

    <!-- Panel nội dung -->
    <div class="right-panel" :class="{ collapsed: isCollapsed }">
      <div class="commit-details">
        <div class="commit-message-workspace" :style="{ height: topHeight + 'px' }">
          <div class="details-header">
            <h6 class="mb-0">Commit Details</h6>
            <div class="workspace-toggle">
              <button class="btn btn-sm panel-action-btn" @click="$emit('toggle')">
                <i :class="['fas', isCollapsed ? 'fa-brands fa-github' : 'fa-solid fa-minus']"></i>
              </button>
            </div>
          </div>
          <!-- Content -->
          <div class="details-content">
            <div v-if="!commit" class="no-selection text-center py-4">
              <i class="fas fa-mouse-pointer fa-2x mb-2"></i>
              <p>No selection</p>
              <small>Select a commit or file to view details</small>
            </div>

            <div v-else>
              <div class="commit-details-header">
                <h6>{{ commit.message }}</h6>
                <div class="commit-meta">
                  <div><strong>Hash:</strong> {{ commit.hash }}</div>
                  <div><strong>Author:</strong> {{ commit.author }}</div>
                  <div><strong>Email:</strong> {{ commit.email }}</div>
                  <div><strong>Date:</strong> {{ formatDate(commit.time) }}</div>
                  <div><strong>Branch:</strong> {{ commit.branch }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="resizer-vertical" @mousedown="startVerticalResize"></div>
        <div class="commit-change-file-workspace" :style="{ flex: 1 }">
          <div class="changed-files-workspace-header">
            <h6 class="mb-0">Changed Files ({{ commit.files.length }})</h6>
          </div>
          <!-- Content -->
          <div class="details-content">
            <div v-if="!commit" class="no-selection text-center py-4">
              <i class="fas fa-mouse-pointer fa-2x mb-2"></i>
              <p>No selection</p>
              <small>Select a commit or file to view details</small>
            </div>
            <div class="changed-files">
              <ul class="list-group list-group-flush">
                <li
                  v-for="(file, index) in commit.files"
                  :key="index"
                  class="list-group-item px-0 py-1"
                >
                  <i class="fas fa-file-alt me-2 text-secondary"></i>{{ file }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  commit: Object,
  isCollapsed: Boolean
})

const emit = defineEmits(['toggle'])

const containerWidth = ref(300)
const previousWidth = ref(300)
const topHeight = ref(200)
let isResizingVertical = false
let isResizing = false

watch(() => props.isCollapsed, (val) => {
  if (val) {
    previousWidth.value = containerWidth.value
    containerWidth.value = 50
  } else {
    containerWidth.value = previousWidth.value || 300
  }
})

function formatDate(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleString()
}

const startResizeContainer = (e) => {
  if (props.isCollapsed) return
  isResizing = true
  window.addEventListener('mousemove', resizeContainer)
  window.addEventListener('mouseup', stopResizeContainer)
}

const resizeContainer = (e) => {
  if (!isResizing) return
  const windowWidth = window.innerWidth
  const newWidth = windowWidth - e.clientX
  containerWidth.value = Math.min(Math.max(newWidth, 250), 500)
}

const stopResizeContainer = () => {
  isResizing = false
  window.removeEventListener('mousemove', resizeContainer)
  window.removeEventListener('mouseup', stopResizeContainer)
}

const startVerticalResize = (e) => {
  isResizingVertical = true
  window.addEventListener('mousemove', handleVerticalResize)
  window.addEventListener('mouseup', stopVerticalResize)
}

const handleVerticalResize = (e) => {
  if (!isResizingVertical) return

  const containerTop = e.target.closest('.right-panel').getBoundingClientRect().top
  const newHeight = e.clientY - containerTop

  topHeight.value = Math.min(Math.max(newHeight, 100), 500)
}

const stopVerticalResize = () => {
  isResizingVertical = false
  window.removeEventListener('mousemove', handleVerticalResize)
  window.removeEventListener('mouseup', stopVerticalResize)
}
</script>

<style scoped>
.right-panel-wrapper {
  display: flex;
  flex-direction: row;
  width: 300px;
  min-width: 50px;
  max-width: 500px;
  height: 100%;
  position: relative;
  overflow: hidden;
  padding: 0;
}

/* Thanh kéo nằm bên trái */
.resizer-horizontal {
  width: 5px;
  cursor: col-resize;
  background-color: var(--border-color);
  user-select: none;
}

/* Nội dung panel */
.right-panel {
  width: 100%;
  background-color: var(--bg-secondary);
  border-left: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.right-panel.collapsed .details-content {
  display: none;
}

.right-panel.collapsed .details-header {
  justify-content: center;
}

.right-panel.collapsed .details-header h6 {
  display: none;
}

.right-panel.collapsed .changed-files-workspace-header {
  opacity: 0;
  visibility: hidden;
  height: 0;
  pointer-events: none;
}

.commit-message-workspace {
  height: 50%;
  min-height: 20%;
  max-height: 80%;
  display: flex;
  flex-direction: column;
}

.commit-change-file-workspace {
  height: 50%;
  min-height: 20%;
  max-height: 80%;
  display: flex;
  flex-direction: column;
}

.commit-details {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.details-header,
.changed-files-workspace-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background-color: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-color);
  height: 36px;
}

.details-header,
.changed-files-workspace-header h6 {
  font-size: 14px;
  font-weight: 500;
  margin: 0;
}

.details-header h6{
  font-size: 14px;
}

.details-content {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
}

.commit-details-header {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 12px;
  margin-bottom: 16px;
}
.commit-details-header h6 {
  font-size: 14px;
  margin-bottom: 8px;
  word-wrap: break-word;
}
.commit-meta {
  font-size: 11px;
  color: var(--text-muted);
  line-height: 1.4;
}

.changed-files h6 {
  font-size: 14px;
  margin-bottom: 12px;
  color: var(--text-secondary);
}
.changed-files ul {
  padding-left: 0;
  list-style: none;
  margin: 0;
}
.list-group-item {
  background-color: transparent;
  border: none;
  font-size: 14px;
  color: var(--text-primary);
}

.panel-action-btn {
  font-size: 14px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
}
.workspace-toggle {
  right: 4px;
  top: 50%;
  border: none;
  font-size: 14px;
  z-index: 10;
}

.resizer-vertical {
  height: 6px;
  cursor: row-resize;
  background-color: var(--bg-secondary);
  user-select: none;
}

/* No commit */
.no-selection {
  text-align: center;
  color: var(--text-muted);
  padding: 32px 16px;
}
.no-selection i {
  display: block;
  margin-bottom: 12px;
  opacity: 0.5;
}
</style>
