<template>
  <Teleport to="body">
    <div
      v-if="isVisible"
      ref="menuRef"
      id="context-menu"
      :style="{ top: `${y}px`, left: `${x}px`, display: 'block' }"
      @contextmenu.prevent
    >
      <div class="ctx-item" @click="handleAction('add-group')">
        <div class="ctx-left">
          <i class="fa-solid fa-folder-plus ctx-icon"></i>
          <span>Add new group</span>
        </div>
      </div>
      <!-- Rename -->
      <div class="ctx-item" @click="handleAction('rename-group')">
        <div class="ctx-left">
          <i class="fa-solid fa-pencil ctx-icon"/>
          <span>Rename</span>
        </div>
      </div>

      <div class="menu-separator"></div>

      <!-- Remove -->
      <div class="ctx-item" @click="handleAction('delete-group')">
        <div class="ctx-left">
           <i class="fa-solid fa-trash-can ctx-icon"/>
          <span>Remove</span>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';

// --- STATE ---
const isVisible = ref(false);
const x = ref(0);
const y = ref(0);
const menuRef = ref(null);
const targetData = ref(null);

// --- EMITS ---
const emit = defineEmits(['action-click']);

// --- METHODS ---
/**
 * Open Context Menu
 * @param {MouseEvent} event
 * @param {any} data
 */
const open = async (event, data = null) => {
  event.preventDefault();
  event.stopPropagation();

  targetData.value = data;
  isVisible.value = true;

  x.value = event.pageX;
  y.value = event.pageY;

  await nextTick();
  if (menuRef.value) {
    const { offsetWidth, offsetHeight } = menuRef.value;
    const winWidth = window.innerWidth;
    const winHeight = window.innerHeight;

    if (x.value + offsetWidth > winWidth) {
      x.value = winWidth - offsetWidth - 10;
    }
    if (y.value + offsetHeight > winHeight) {
      y.value = winHeight - offsetHeight - 10;
    }
  }
};


const close = () => {
  isVisible.value = false;
};

const handleAction = (actionName) => {
  emit('action-click', { action: actionName, data: targetData.value });
  close();
};

const handleGlobalClick = (e) => {
  if (isVisible.value) {
    close();
  }
};

onMounted(() => {
  window.addEventListener('click', handleGlobalClick);
  window.addEventListener('resize', close);
  window.addEventListener('scroll', close, true);
});

onUnmounted(() => {
  window.removeEventListener('click', handleGlobalClick);
  window.removeEventListener('resize', close);
  window.removeEventListener('scroll', close, true);
});

defineExpose({
  open,
  close
});
</script>

<style scoped>
/* --- CONTEXT MENU STYLES --- */
#context-menu {
  position: fixed;
  z-index: 1000;
  width: 200px;
  background-color: var(--menu-bg, #1e2128);
  border: 1px solid var(--border-color, #2a2d35);
  border-radius: 6px;
  box-shadow: 0 4px 16px var(--ctx-shadow, rgba(0, 0, 0, 0.5));
  padding: 4px 0;
  animation: fadeIn 0.05s ease-out;
  color: var(--text-color, #e2e8f0);
  font-family: "Be Vietnam Pro", sans-serif;
}

.ctx-item {
  padding: 6px 12px;
  font-size: 10px;
  color: var(--text-color, #e2e8f0);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  position: relative;
  transition: background-color 0.1s;
}

.ctx-item:hover {
  background-color: var(--p-selection, rgba(34, 211, 238, 0.1));
  color: var(--accent-color, #22d3ee);
}

.ctx-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ctx-icon {
  width: 14px;
  text-align: center;
  font-size: 10px;
}

.ctx-shortcut {
  font-size: 10px;
  color: var(--p-text-dim, #64748b);
  font-family: 'JetBrains Mono', monospace;
}

.menu-separator {
  height: 1px;
  background-color: var(--border-color, #2a2d35);
  margin: 4px 0;
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
</style>
