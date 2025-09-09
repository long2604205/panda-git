<!-- components/BranchContextMenu.vue -->
<template>
  <ul
    v-if="visible"
    class="context-menu"
    :style="{ top: y + 'px', left: x + 'px' }"
    @click.stop
  >
    <li @click="() => choose('checkout')">Checkout</li>
    <li @click="() => choose('new-branch')">New Branch from '{{ branch }}'</li>
    <li @click="() => choose('merge-branch')">Merge '{{ branch }}' into '{{currentBranch}}'</li>
    <li @click="() => choose('delete')">Delete</li>
  </ul>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import mitter from '@/plugins/mitter.js'

const visible = ref(false)
const x = ref(0)
const y = ref(0)
const branch = ref('')
const emit = defineEmits(['action'])
const currentBranch = ref('')

onMounted(() => {
  mitter.on('')
  mitter.on('merge-information', (branch) => {
    currentBranch.value = branch
  })
})

onBeforeUnmount(() => {
  mitter.off('merge-information')
})

function open(event, branchName) {
  event.preventDefault()
  branch.value = branchName
  x.value = event.clientX
  y.value = event.clientY
  visible.value = true
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
</script>

<style scoped>
.context-menu {
  position: fixed;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 0;
  margin: 0;
  list-style: none;
  z-index: 9999;
  width: 300px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}
.context-menu li {
  padding: 5px;
  font-size: 12px;
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.context-menu li:hover {
  background-color: var(--bg-hover);
  border-radius: 4px;
}
</style>
