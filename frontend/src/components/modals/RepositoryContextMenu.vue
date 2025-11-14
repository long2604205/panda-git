<template>
  <div
    v-if="visible"
    class="context-menu"
    :style="{ top: y + 'px', left: x + 'px' }"
    @click.stop
  >
    <div class="menu-item" @click="() => choose('open')">
      <span class="icon">
        📨
      </span>
      <span class="text">
        Open repository
      </span>
    </div>
    <div class="menu-item" @click="() => choose('open')">
      <span class="icon">📨</span>
      <span class="text">
        Open in Explorer
      </span>
    </div>
    <div class="menu-item" @click="() => choose('open')">
      <span class="icon">📨</span>
      <span class="text">
        Open in Terminal
      </span>
    </div>
    <div class="menu-item" @click="() => choose('open')">
      <span class="icon">👥</span>
      <span class="text">
        Reveal in Explorer
      </span>
    </div>

    <div class="divider"></div>

    <div class="menu-item" @click="() => choose('copy')">
      <span class="icon">📋</span>
      <span class="text">
        Pull
      </span>
    </div>
    <div class="menu-item" @click="() => choose('copy')">
      <span class="icon">📋</span>
      <span class="text">
        Push
      </span>
    </div>

    <div class="divider"></div>

    <div class="menu-item" @click="() => choose('archive')">
      <span class="icon">🗃️</span>
      <span class="text">
        Refresh
      </span>
      <span class="shortcut">F5</span>
    </div>

    <div class="divider"></div>

    <div class="menu-item" @click="() => choose('archive')">
      <span class="icon">🗃️</span>
      <span class="text">
        Rename
      </span>
    </div>
    <div class="menu-item" @click="() => choose('archive')">
      <span class="icon">🗃️</span>
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
  width: 20px;
  height: 20px;
  display: inline-flex;
  opacity: .9;
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
