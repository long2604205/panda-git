<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark-custom top-navbar">
    <div class="container-fluid px-2">
      <!-- left menu -->
      <div class="navbar-nav flex-row">
        <div class="nav-item d-flex align-items-center">
          <img src="@/assets/cool.png" alt="Logo" class="app-logo" />
        </div>
        <panda-menu-dropdown label="File" :items="fileMenu" @action="handleMenuAction" />
        <panda-menu-dropdown label="View" :items="viewMenu" />
        <panda-menu-dropdown label="Git" :items="gitMenu" />
        <panda-menu-dropdown label="Window" :items="windowMenu" @action="handleMenuAction" />
        <panda-menu-dropdown label="Help" :items="helpMenu" />
      </div>

      <!-- window controls-->
      <div class="ms-auto d-flex align-items-center">
        <div class="window-controls">
          <button class="btn btn-sm window-btn" id="minimize-btn" @click="minimize">
            <i class="fas fa-minus"></i>
          </button>
          <button class="btn btn-sm window-btn" id="maximize-btn" @click="toggleMaximize">
            <i :class="isMaximized ? 'fas fa-clone' : 'fas fa-square'"></i>
          </button>
          <button class="btn btn-sm window-btn close-btn" id="close-btn" @click="closeApp">
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import PandaMenuDropdown from '../PandaMenuDropdown.vue'
import { computed, defineAsyncComponent, onMounted, ref } from 'vue'
import { showPageInModal } from '@/services/modals.js'

const openRepositoryForm = defineAsyncComponent(
  () => import('@/components/modals/PandaOpenRepositoryForm.vue'),
)
const isMaximized = ref(false)
const minimize = () => window.electronAPI?.minimize()
const maximize = () => window.electronAPI?.maximize()
const toggleMaximize = () => window.electronAPI?.toggleMaximize()
const closeApp = () => window.electronAPI?.closeApp()

onMounted(() => {
  window.electronAPI?.onMaximize(() => (isMaximized.value = true))
  window.electronAPI?.onUnmaximize(() => (isMaximized.value = false))
})

const fileMenu = [
  { icon: 'fas fa-plus', label: 'New Project', action: 'new-project' },
  { icon: 'fas fa-folder-open', label: 'Open Project', action: 'open-project' },
  { icon: 'fas fa-code-branch', label: 'Open Repository', action: 'open-repository' },
  'divider',
  { icon: 'fas fa-times', label: 'Close Project', action: 'close-project' },
  { icon: 'fas fa-sign-out-alt', label: 'Exit', action: 'exit' },
]

const viewMenu = [
  { icon: 'fas fa-sidebar', label: 'Toggle Sidebar', action: 'toggle-sidebar' },
  { icon: 'fas fa-th-large', label: 'Toggle Workspace', action: 'toggle-workspace' },
  'divider',
  { icon: 'fas fa-expand', label: 'Full Screen' },
]

const gitMenu = [
  { icon: 'fas fa-clone', label: 'Clone', action: 'git-clone' },
  { icon: 'fas fa-plus-circle', label: 'Initialize Repository', action: 'git-init' },
  'divider',
  { icon: 'fas fa-check', label: 'Commit', action: 'git-commit' },
  { icon: 'fas fa-upload', label: 'Push', action: 'git-push' },
  { icon: 'fas fa-download', label: 'Pull', action: 'git-pull' },
  'divider',
  { icon: 'fas fa-code-branch', label: 'Branches', action: 'git-branches' },
  { icon: 'fas fa-code-merge', label: 'Merge', action: 'git-merge' },
]

const windowMenu = [
  { icon: 'fas fa-window-minimize', label: 'Minimize', action: 'minimize' },
  { icon: 'fas fa-window-maximize', label: 'Maximize', action: 'toggle-maximize' },
  { icon: 'fas fa-window-close', label: 'Close', action: 'close' },
]

const helpMenu = [
  { icon: 'fas fa-question-circle', label: 'Help Topics' },
  { icon: 'fas fa-info-circle', label: 'About' },
]

const handleMenuAction = (action) => {
  switch (action) {
    case 'open-repository':
      openRepository()
      break
    case 'minimize':
      minimize()
      break
    case 'toggle-maximize':
      maximize()
      break
    case 'close':
      closeApp()
      break
    default:
      console.log('Action:', action)
  }
}

function openRepository() {
  showPageInModal(openRepositoryForm, {}, { width: '30%' })
}
</script>
<style scoped>
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--scrollbar-track);
}

::-webkit-scrollbar-thumb {
  background: var(--scrollbar-thumb);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #666666;
}

::-webkit-scrollbar-corner {
  background: var(--scrollbar-track);
}

/* Top Navbar */
.top-navbar {
  background-color: var(--bg-secondary) !important;
  border-bottom: 1px solid var(--border-color);
  padding: 0;
  min-height: 32px;
  z-index: 1000;
  -webkit-app-region: drag;
  user-select: none;
}

.top-navbar .nav-link {
  color: var(--text-secondary) !important;
  font-size: 12px;
  padding: 6px 12px !important;
  transition: all 0.2s ease;
  border: none;
}

.top-navbar .nav-link:hover {
  color: var(--text-primary) !important;
  background-color: var(--bg-hover);
}

.dropdown-menu-dark {
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow);
}

.dropdown-menu-dark .dropdown-item {
  color: var(--text-secondary);
  font-size: 12px;
  padding: 6px 12px;
}

.dropdown-menu-dark .dropdown-item:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.dropdown-divider {
  border-color: var(--border-color);
}

.project-info {
  font-size: 12px;
  color: var(--text-secondary);
}

.window-controls {
  display: flex;
  gap: 2px;
  -webkit-app-region: no-drag;
}

.window-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  width: 32px;
  height: 24px;
  font-size: 10px;
  transition: all 0.2s ease;
}

.window-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.close-btn:hover {
  background-color: var(--accent-danger) !important;
  color: white !important;
}

.navbar-nav {
  -webkit-app-region: no-drag;
}

.app-logo {
  height: 22px;
  width: auto;
  margin-right: 0.5rem;
  object-fit: contain;
  display: block;
}
</style>
