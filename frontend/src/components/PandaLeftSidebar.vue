<template>
  <div class="col-auto git-container" :class="{ collapsed: collapsed }">
    <div class="git-panel">
      <!-- Header -->
      <div class="git-header">
        <h6 class="mb-0">Git</h6>
        <button class="btn btn-sm git-toggle" @click="$emit('toggle-git')">
          <i :class="['fas', collapsed ? 'fa-solid fa-code-branch' : 'fa-chevron-left']"></i>
        </button>
      </div>
      <div class="git-content">
      </div>
    </div>
  </div>
</template>

<script setup>
// Props
defineProps({
  collapsed: Boolean
})
// Emits
const emit = defineEmits(['toggle-git'])

// Methods
const onRepoClick = (repo) => {
  emit('set-active-repo', repo)
}

const onCloseRepo = (repo) => {
  emit('remove-repo', repo)
}

const getStatusColor = (status) => {
  switch (status) {
    case 'clean': return 'text-success'
    case 'dirty': return 'text-warning'
    case 'untracked': return 'text-secondary'
    default: return 'text-muted'
  }
}
</script>
<style scoped>
.git-container {
  width: 280px;
  height: 100%;
  background-color: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  transition: width 0.3s ease;
  overflow: hidden;
  padding: 0;
}

.git-container.collapsed {
  width: 0;
  overflow: hidden;
}

.git-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.git-header {
  position: relative;
  display: flex;
  align-items: center;
  padding: 8px 12px;
  background-color: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-color);
  min-height: 36px;
}

.git-header h6 {
  font-size: 12px;
  font-weight: 500;
  margin: 0;
}

.git-toggle {
  position: absolute;
  right: 4px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 12px;
  z-index: 10;
}

.git-toggle:hover {
  color: var(--text-primary);
}

.git-content {
  flex: 1;
  overflow-y: auto;
}

.git-container.collapsed {
  width: 50px;
}

.git-container.collapsed .git-toggle {
  right: 50%;
  transform: translate(50%, -50%);
}

.git-container .git-header h6,
.git-container .git-content {
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.git-container.collapsed .git-header h6,
.git-container.collapsed .git-content {
  opacity: 0;
  visibility: hidden;
  height: 0;
  pointer-events: none;
}
</style>
