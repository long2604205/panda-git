<template>
  <Teleport to="body">
    <div
      v-if="isVisible"
      ref="menuRef"
      id="context-menu"
      :style="{ top: `${y}px`, left: `${x}px`, display: 'block' }"
      @contextmenu.prevent
    >
      <div class="ctx-item" @click="handleAction('rename')">
        <div class="ctx-left">
          <i class="fa-solid fa-plus ctx-icon"/>
          <span>Add new group</span>
        </div>
        <span class="ctx-shortcut">F2</span>
      </div>
      <!-- Rename -->
      <div class="ctx-item" @click="handleAction('rename')">
        <div class="ctx-left">
          <i class="fa-solid fa-pencil ctx-icon"/>
          <span>Rename</span>
        </div>
        <span class="ctx-shortcut">F2</span>
      </div>

      <div class="menu-separator"></div>

      <!-- Remove -->
      <div class="ctx-item" style="color: #ef4444;" @click="handleAction('rename')">
        <div class="ctx-left">
           <i class="fa-solid fa-trash-can ctx-icon"/>
          <span>Remove</span>
        </div>
        <span class="ctx-shortcut">Del</span>
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
const targetData = ref(null); // Lưu dữ liệu của item được click chuột phải (nếu cần)

// --- EMITS ---
// Bắn sự kiện ra ngoài component cha khi chọn một hành động
const emit = defineEmits(['action-click']);

// --- METHODS ---

/**
 * Mở Context Menu
 * @param {MouseEvent} event - Sự kiện click chuột
 * @param {any} data - Dữ liệu của item (ví dụ: repo object)
 */
const open = async (event, data = null) => {
  event.preventDefault();
  event.stopPropagation();

  targetData.value = data;
  isVisible.value = true;

  // Tính toán vị trí chuột
  x.value = event.pageX;
  y.value = event.pageY;

  // (Optional) Logic ngăn menu tràn ra khỏi màn hình
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

/**
 * Đóng Context Menu
 */
const close = () => {
  isVisible.value = false;
};

/**
 * Xử lý khi click vào item trong menu
 */
const handleAction = (actionName) => {
  emit('action-click', { action: actionName, data: targetData.value });
  close();
};

// --- LIFECYCLE ---
// Lắng nghe sự kiện click toàn cục để đóng menu khi click ra ngoài
const handleGlobalClick = (e) => {
  if (isVisible.value) {
    // Nếu click vào trong menu thì không đóng (trừ khi click vào item action đã xử lý ở trên)
    // Tuy nhiên logic menu chuẩn thường đóng luôn khi click bất kỳ đâu
    close();
  }
};

onMounted(() => {
  window.addEventListener('click', handleGlobalClick);
  window.addEventListener('resize', close);
  window.addEventListener('scroll', close, true); // Đóng khi scroll
});

onUnmounted(() => {
  window.removeEventListener('click', handleGlobalClick);
  window.removeEventListener('resize', close);
  window.removeEventListener('scroll', close, true);
});

// Expose hàm open để component cha có thể gọi
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
  /* Lưu ý: Các biến var(--menu-bg) cần được define ở global css hoặc parent component */
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

/* Submenu Styling */
.ctx-submenu {
  display: none;
  position: absolute;
  left: 100%;
  top: -4px;
  width: 200px;
  background-color: var(--menu-bg, #1e2128);
  border: 1px solid var(--border-color, #2a2d35);
  border-radius: 6px;
  box-shadow: 0 4px 16px var(--ctx-shadow, rgba(0, 0, 0, 0.5));
  padding: 4px 0;
}

.ctx-item:hover > .ctx-submenu {
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
</style>
