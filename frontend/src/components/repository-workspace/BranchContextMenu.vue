<template>
  <div
    v-if="visible"
    class="context-menu no-select"
    :style="{ top: y + 'px', left: x + 'px' }"
    @click.stop
  >
    <div class="menu-item" @click="() => choose('checkout')">
      <span style="color: #6aa39d" class="icon">
        <i class="fa-regular fa-folder-open"/>
      </span>
      <span class="text">
        Checkout
      </span>
    </div>
    <div class="menu-item" @click="() => choose('open')">
      <span style="color: #6aa39d" class="icon">
        <i class="fa-regular fa-folder-open"/>
      </span>
      <span class="text">
        New branch from '{{branch}}'...
      </span>
    </div>

    <div class="divider"></div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'

const visible = ref(false)
const x = ref(0)
const y = ref(0)
const branch = ref(null)

const emit = defineEmits(['action'])

function open(event, branchName) {
  event.preventDefault()
  branch.value = branchName
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
  emit('action', { action, branch: branch.value })
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
  width: 300px;
  max-width: 500px;
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

.menu-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

</style>
