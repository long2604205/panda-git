<template>
  <div
    v-if="visible"
    class="context-menu"
    :style="{ top: y + 'px', left: x + 'px' }"
    @click.stop
  >
    <div class="menu-item" @click="() => choose('open')">
      <span style="color: #6aa39d" class="icon">
        <i class="fa-regular fa-folder-open"/>
      </span>
      <span class="text">
        Open repository
      </span>
    </div>
    <div class="menu-item" @click="() => choose('open')">
      <span style="color: #6aa39d" class="icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" fill="currentColor" class="bi bi-folder-symlink" viewBox="0 0 10 10">
          <path d="m11.798 8.271-3.182 1.97c-.27.166-.616-.036-.616-.372V9.1s-2.571-.3-4 2.4c.571-4.8 3.143-4.8 4-4.8v-.769c0-.336.346-.538.616-.371l3.182 1.969c.27.166.27.576 0 .742"/>
          <path d="m.5 3 .04.87a2 2 0 0 0-.342 1.311l.637 7A2 2 0 0 0 2.826 14h10.348a2 2 0 0 0 1.991-1.819l.637-7A2 2 0 0 0 13.81 3H9.828a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 6.172 1H2.5a2 2 0 0 0-2 2m.694 2.09A1 1 0 0 1 2.19 4h11.62a1 1 0 0 1 .996 1.09l-.636 7a1 1 0 0 1-.996.91H2.826a1 1 0 0 1-.995-.91zM6.172 2a1 1 0 0 1 .707.293L7.586 3H2.19q-.362.002-.683.12L1.5 2.98a1 1 0 0 1 1-.98z"/>
        </svg>
      </span>
      <span class="text">
        Open in Explorer
      </span>
    </div>
    <div class="menu-item" @click="() => choose('open')">
      <span style="color: #6aa39d" class="icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" fill="currentColor" class="bi bi-terminal-fill" viewBox="0 0 10 10">
          <path d="M0 3a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm9.5 5.5h-3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1m-6.354-.354a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2a.5.5 0 1 0-.708.708L4.793 6.5z"/>
        </svg>
      </span>
      <span class="text">
        Open in Terminal
      </span>
    </div>

    <div class="divider"></div>

    <div class="menu-item" @click="() => choose('copy')">
      <span style="color: #c792ea" class="icon">
        <i class="fa-solid fa-download"/>
      </span>
      <span class="text">
        Pull
      </span>
    </div>
    <div class="menu-item" @click="() => choose('copy')">
      <span style="color: #c792ea" class="icon">
        <i class="fa-solid fa-upload"/>
      </span>
      <span class="text">
        Push
      </span>
    </div>

    <div class="divider"></div>

    <div class="menu-item" @click="() => choose('archive')">
      <span style="color: #81c784" class="icon">
        <i class="fa-solid fa-arrows-rotate"/>
      </span>
      <span class="text">
        Refresh
      </span>
      <span class="shortcut">F5</span>
    </div>

    <div class="divider"></div>

    <div class="menu-item" @click="() => choose('archive')">
      <span style="color: #7597e1" class="icon">
        <i class="fa-solid fa-pen-to-square"/>
      </span>
      <span class="text">
        Rename
      </span>
    </div>
    <div class="menu-item" @click="() => choose('archive')">
      <span style="color: #e3504d" class="icon">
        <i class="fa-solid fa-trash-can"/>
      </span>
      <span class="text">Remove</span>
      <span class="shortcut">Delete</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'

const visible = ref(false)
const x = ref(0)
const y = ref(0)
const repo = ref(null)

const emit = defineEmits(['action'])

function open(event, repoItem) {
  event.preventDefault()
  repo.value = repoItem
  x.value = event.clientX
  y.value = event.clientY
  visible.value = true

  setTimeout(() => {
    const menuEl = document.querySelector('.context-menu')
    if (!menuEl) return
    const menuWidth = menuEl.offsetWidth
    const menuHeight = menuEl.offsetHeight
    const pageWidth = window.innerWidth
    const pageHeight = window.innerHeight

    if (x.value + menuWidth > pageWidth) {
      x.value = pageWidth - menuWidth - 10
    }
    if (y.value + menuHeight > pageHeight) {
      y.value = pageHeight - menuHeight - 10
    }
  }, 0)

  document.addEventListener('click', close)
}

function close() {
  visible.value = false
  document.removeEventListener('click', close)
}

function choose(action) {
  emit('action', { action, repo: repo.value })
  close()
}

defineExpose({ open })

onBeforeUnmount(() => {
  document.removeEventListener('click', close)
})
</script>

<style scoped>
.context-menu {
  position: fixed;
  top: 0;
  left: 0;
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  border-radius: 8px;
  box-shadow: 0 6px 18px var(--shadow);
  border: 1px solid var(--border-color);
  width: 200px;
  max-width: 300px;
  padding: 4px 0;
  z-index: 9999;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 30px;
  margin: 0 4px;
  padding: 0 4px;
  font-size: 12px;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.menu-item:hover {
  background: var(--bg-hover);
  border-radius: 4px;
  margin: 0 4px;
  padding: 0 4px;
}

.menu-item .icon {
  width: 15px;
  height: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: .9;
}

.menu-item .icon i {
  font-size: 10px;
  line-height: 1;
  vertical-align: middle;
}

.menu-item .text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  margin: 0 2px;
}

.menu-item .shortcut {
  flex-shrink: 0;
  opacity: 0.6;
  font-size: 11px;
}

.divider {
  height: 1px;
  background: var(--border-color);
  margin: 4px 0;
}
</style>
