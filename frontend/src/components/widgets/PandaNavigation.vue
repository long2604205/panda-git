<template>
  <header
    class="h-10 flex-shrink-0 flex items-center justify-between bg-[var(--bg-header)] border-b border-[var(--border-color)] select-none window-drag pl-3"
  >
    <!-- LEFT: App Icon + Menubar -->
    <div class="flex items-center h-full no-drag">
      <!-- App Icon -->
      <div class="mr-2 flex items-center text-[var(--accent-color)]">
        <img src="@/assets/cool.png" class="h-[24px] w-auto object-contain block" alt="Logo"/>
<!--        <i class="fa-brands fa-git-alt text-lg" />-->
      </div>

      <!-- Menus with Dropdowns -->
      <nav class="flex items-center text-xs text-[var(--p-text-muted)] h-full" ref="menubar">
        <div
          class="menu-trigger"
          v-for="menu in menus"
          :key="menu.name"
          @click.stop="toggleMenu(menu.name)"
          @mouseenter="hoverMenu(menu.name)"
          :class="{ active: activeMenu === menu.name }"
        >
          <div class="menu-btn">{{ menu.name }}</div>
          <div class="menu-dropdown">
            <div
              v-for="item in menu.items"
              :key="item.label"
              class="menu-item"
              @click="onMenuItemClick(item)"
            >
              {{ item.label }}
              <span v-if="item.shortcut" class="shortcut">{{ item.shortcut }}</span>
            </div>
          </div>
        </div>
      </nav>
    </div>

    <!-- RIGHT: Windows Controls -->
    <div class="win-controls no-drag">
      <div class="win-btn" title="Minimize" @click="minimize">
        <i class="fa-solid fa-minus text-xs" />
      </div>
      <div class="win-btn" title="Maximize" @click="toggleMaximize">
        <i class="text-xs" :class="isMaximized ? 'fa-regular fa-clone' : 'fa-regular fa-square'" />
      </div>
      <div class="win-btn close" title="Close" @click="closeApp">
        <i class="fa-solid fa-xmark text-sm" />
      </div>
    </div>
  </header>
</template>

<script setup>
import { defineAsyncComponent, onBeforeUnmount, onMounted, ref } from 'vue'
import { showPageInModal } from '@/services/modals.js'

const isMaximized = ref(false)
const activeMenu = ref(null)
const menubar = ref(null)
const minimize = () => window.electronAPI?.minimize()
const maximize = () => window.electronAPI?.maximize()
const toggleMaximize = () => window.electronAPI?.toggleMaximize()
const closeApp = () => window.electronAPI?.closeApp()
const toggleDevTools = () => window.electronAPI?.openDevtools()
const menus = [
  {
    name: 'File',
    items: [
      { label: 'New Repository...', shortcut: 'Ctrl+N', action: 'newRepository' },
      { label: 'Open Repository', shortcut: 'Ctrl+O', action: 'open-repository' },
      { label: 'Clone Repository...', shortcut: 'Ctrl+Shift+O' },
      { label: 'Preferences', shortcut: 'Ctrl+,' },
      { label: 'Exit', shortcut: 'Alt+F4', action: 'exit' },
    ],
  },
  {
    name: 'View',
    items: [
      { label: 'Show/Hide Sidebar', shortcut: 'Ctrl+B' },
      { label: 'Show History Graph' },
      { label: 'Toggle Terminal', shortcut: 'Ctrl+`' },
      { label: 'Zoom In', shortcut: 'Ctrl+=' },
      { label: 'Zoom Out', shortcut: 'Ctrl+-' },
    ],
  },
  {
    name: 'Git',
    items: [
      { label: 'Fetch', shortcut: 'Ctrl+Shift+F' },
      { label: 'Pull', shortcut: 'Ctrl+Shift+P' },
      { label: 'Push', shortcut: 'Ctrl+Shift+U' },
      { label: 'Stash Changes...' },
      { label: 'Pop Stash...' },
    ],
  },
  {
    name: 'Terminal',
    items: [
      { label: 'New Terminal', shortcut: 'Ctrl+Shift+`' },
      { label: 'Split Terminal', shortcut: 'Ctrl+Shift+P' },
      { label: 'New Terminal Window', shortcut: 'Ctrl+Shift+P' },
    ],
  },
  {
    name: 'Window',
    items: [
      { label: 'Minimize', action: 'window-minimize' },
      { label: 'Maximize', action: 'window-maximize' },
      { label: 'Close', action: 'window-close' },
    ],
  },
  {
    name: 'Help',
    items: [
      {
        label: 'Developer Tools',
        shortcut: 'Ctrl+Shift+I',
        action: 'open-dev-tools',
      },
      { label: 'Documentation' },
      { label: 'Show Release Notes' },
      { label: 'About Panda Git' },
    ],
  },
]
const openRepositoryForm = defineAsyncComponent(() => import('@/components/common/OpenRepositoryForm.vue'))

onMounted(() => {
  window.electronAPI?.onMaximize(() => (isMaximized.value = true))
  window.electronAPI?.onUnmaximize(() => (isMaximized.value = false))
})

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

function toggleMenu(name) {
  activeMenu.value = activeMenu.value === name ? null : name
}

function hoverMenu(name) {
  if (activeMenu.value) activeMenu.value = name
}

function handleClickOutside(e) {
  if (menubar.value && !menubar.value.contains(e.target)) {
    activeMenu.value = null
  }
}

function onMenuItemClick(item) {
  switch (item.action) {
    case 'newRepository':
      console.log('Action: New Repository')
      break
    case 'open-dev-tools':
      toggleDevTools()
      break
    case 'window-minimize':
      minimize()
      break
    case 'window-maximize':
      maximize()
      break
    case 'exit':
    case 'window-close':
      closeApp()
      break
    case 'open-repository':
      openRepository()
      break
    default:
      console.warn('No action defined for', item.action)
  }
}

function openRepository () {
  showPageInModal(openRepositoryForm, {}, {width: '30%'})
}
</script>

<style scoped>
/* --- WINDOWS CONTROLS STYLES --- */
.win-controls {
  display: flex;
  height: 100%;
}

.win-btn {
  width: 46px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
  color: var(--p-text-muted);
}

.win-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: var(--text-color);
}

.win-btn.close:hover {
  background-color: #e81123;
  color: white;
}

/* --- MENU DROPDOWN STYLES --- */
.menu-trigger {
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
}

.menu-btn {
  padding: 0 10px;
  height: 24px;
  display: flex;
  align-items: center;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.1s;
}

.menu-btn:hover,
.menu-trigger.active .menu-btn {
  background-color: var(--p-hover);
  color: var(--text-color);
}

.menu-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: var(--menu-bg);
  border: 1px solid var(--border-color);
  width: max-content;
  min-width: 220px;
  max-width: 320px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border-radius: 0 0 4px 4px;
  padding: 4px 0;
  z-index: 100;
  display: none;
  /* Hidden by default */
  animation: fadeIn 0.1s ease-out;
}

.menu-trigger.active .menu-dropdown {
  display: block;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.menu-item {
  padding: 6px 16px;
  font-size: 12px;
  color: var(--text-color);
  display: flex;
  justify-content: space-between;
  cursor: pointer;
}

.menu-item:hover {
  background-color: var(--p-selection);
  color: var(--accent-color);
}

.menu-item .shortcut {
  color: var(--p-text-dim);
  font-size: 10px;
  margin-left: 16px;
}

.menu-separator {
  height: 1px;
  background-color: var(--border-color);
  margin: 4px 0;
}
</style>
