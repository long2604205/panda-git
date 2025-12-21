<template>
  <Teleport to="body">
    <div
      v-if="isVisible"
      id="context-menu"
      ref="menuRef"
      :style="{ top: `${y}px`, left: `${x}px`, display: 'block' }"
      @contextmenu.prevent
    >
      <!-- Copy Path -->
      <div
        v-if="targetData !== repositoryStore.branchName"
        class="ctx-item"
        @click="handleAction('copy-path')"
      >
        <div class="ctx-left">
          <i class="fa-solid fa-rotate ctx-icon" />
          <span>Checkout</span>
        </div>
        <span class="ctx-shortcut">F5</span>
      </div>

      <!-- Item 1 -->
      <div
        :class="{ disabled: isActiveRepo }"
        class="ctx-item"
        @click="handleAction('open-repository')"
      >
        <div class="ctx-left">
          <i class="fa-regular fa-circle-check ctx-icon" />
          <span :title="targetData">New branch form '{{ truncatedTargetData }}'...</span>
        </div>
      </div>

      <div
        v-if="targetData !== repositoryStore.branchName"
        class="menu-separator"
      />

      <!-- Item 1 -->
      <div
        v-if="targetData !== repositoryStore.branchName"
        class="ctx-item"
        @click="handleAction('open-repository')"
      >
        <div class="ctx-left">
          <i class="fa-regular fa-circle-check ctx-icon" />
          <span :title="targetData">Merge '{{ truncatedTargetData }}' into '{{ repositoryStore.branchName }}'</span>
        </div>
      </div>

      <div class="menu-separator" />
      <!-- Copy Path -->
      <div
        class="ctx-item"
        @click="handleAction('copy-path')"
      >
        <div class="ctx-left">
          <i class="fa-solid fa-copy ctx-icon" />
          <span>Update</span>
        </div>
        <span class="ctx-shortcut">Ctrl+C</span>
      </div>

      <div
        class="ctx-item"
        @click="handleAction('copy-path')"
      >
        <div class="ctx-left">
          <i class="fa-solid fa-copy ctx-icon" />
          <span>Push</span>
        </div>
        <span class="ctx-shortcut">Ctrl+C</span>
      </div>

      <div class="menu-separator" />
      <!-- Rename -->
      <div
        class="ctx-item"
        @click="handleAction('rename')"
      >
        <div class="ctx-left">
          <i class="fa-solid fa-pencil ctx-icon" />
          <span>Rename...</span>
        </div>
        <span class="ctx-shortcut">F2</span>
      </div>

      <!-- Remove -->
      <div
        :class="{ disabled: isActiveRepo }"
        class="ctx-item"
        @click="handleAction('remove-repo')"
      >
        <div class="ctx-left">
          <i class="fa-solid fa-trash-can ctx-icon" />
          <span>Delete</span>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRepositoryStore } from '@/stores/repositoryStore.js'
// --- STATE ---
const isVisible = ref(false)
const x = ref(0)
const y = ref(0)
const menuRef = ref(null)
const targetData = ref(null) // Lưu dữ liệu của item được click chuột phải (nếu cần)
const isActiveRepo = ref(false)
const repositoryStore = useRepositoryStore()
// --- EMITS ---
// Bắn sự kiện ra ngoài component cha khi chọn một hành động
const emit = defineEmits(['action-click'])

// --- METHODS ---

/**
 * Mở Context Menu
 * @param {MouseEvent} event - Sự kiện click chuột
 * @param {any} data - Dữ liệu của item (ví dụ: repo object)
 */
const open = async (event, data = null) => {
  event.preventDefault()
  event.stopPropagation()

  targetData.value = data
  isVisible.value = true

  isActiveRepo.value = data?.active ?? false

  // Tính toán vị trí chuột
  x.value = event.pageX
  y.value = event.pageY

  // (Optional) Logic ngăn menu tràn ra khỏi màn hình
  await nextTick()
  if (menuRef.value) {
    const { offsetWidth, offsetHeight } = menuRef.value
    const winWidth = window.innerWidth
    const winHeight = window.innerHeight

    if (x.value + offsetWidth > winWidth) {
      x.value = winWidth - offsetWidth - 10
    }
    if (y.value + offsetHeight > winHeight) {
      y.value = winHeight - offsetHeight - 10
    }
  }
}

/**
 * Đóng Context Menu
 */
const close = () => {
  isVisible.value = false
}

/**
 * Xử lý khi click vào item trong menu
 */
const handleAction = (actionName) => {
  emit('action-click', { action: actionName, data: targetData.value })
  close()
}

// --- LIFECYCLE ---
// Lắng nghe sự kiện click toàn cục để đóng menu khi click ra ngoài
const handleGlobalClick = () => {
  if (isVisible.value) {
    // Nếu click vào trong menu thì không đóng (trừ khi click vào item action đã xử lý ở trên)
    // Tuy nhiên logic menu chuẩn thường đóng luôn khi click bất kỳ đâu
    close()
  }
}

// --- COMPUTED ---
const truncatedTargetData = computed(() => {
  // 1. Lấy dữ liệu và convert sang string
  const text = targetData.value ? String(targetData.value) : ''

  // 2. Cấu hình độ dài tối đa
  const maxLength = 32 // Tùy chỉnh độ dài bạn muốn

  // Nếu ngắn hơn giới hạn thì trả về nguyên vẹn
  if (text.length <= maxLength) {
    return text
  }

  // 3. Tính toán độ dài cắt
  // Trừ 3 ký tự cho dấu '...'
  const availableChars = maxLength - 3

  // Chia tỷ lệ: Thường tên nhánh phần đầu quan trọng hơn, nên mình để 70% đầu, 30% đuôi
  const frontLen = Math.ceil(availableChars * 0.7)
  const backLen = Math.floor(availableChars * 0.3)

  // 4. Cắt chuỗi thô
  let front = text.slice(0, frontLen)
  let back = text.slice(-backLen)

  // 5. LOGIC QUAN TRỌNG: Loại bỏ _ và - thừa ở vết cắt
  // Regex: /[_-]+$/ nghĩa là tìm _ hoặc - ở CUỐI chuỗi front và xoá đi
  front = front.replace(/[_-]+$/, '')

  // Regex: /^[_-]+/ nghĩa là tìm _ hoặc - ở ĐẦU chuỗi back và xoá đi
  back = back.replace(/^[_-]+/, '')

  return `${front}...${back}`
})

onMounted(() => {
  window.addEventListener('click', handleGlobalClick)
  window.addEventListener('resize', close)
  window.addEventListener('scroll', close, true) // Đóng khi scroll
})

onUnmounted(() => {
  window.removeEventListener('click', handleGlobalClick)
  window.removeEventListener('resize', close)
  window.removeEventListener('scroll', close, true)
})

// Expose hàm open để component cha có thể gọi
defineExpose({
  open,
  close,
})
</script>

<style scoped>
/* --- CONTEXT MENU STYLES --- */
#context-menu {
  position: fixed;
  z-index: 1000;
  min-width: 200px;
  max-width: 500px;
  /* Lưu ý: Các biến var(--menu-bg) cần được define ở global css hoặc parent component */
  background-color: var(--menu-bg, #1e2128);
  border: 1px solid var(--border-color, #2a2d35);
  border-radius: 6px;
  box-shadow: 0 4px 16px var(--ctx-shadow, rgba(0, 0, 0, 0.5));
  padding: 4px 0;
  animation: fadeIn 0.05s ease-out;
  color: var(--text-color, #e2e8f0);
  font-family: 'Be Vietnam Pro', sans-serif;
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

.ctx-item.disabled {
  opacity: 0.4;
  pointer-events: none;
}
</style>
