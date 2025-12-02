<template>
  <Teleport to="body">
    <div
      v-if="isVisible"
      ref="menuRef"
      id="context-menu"
      :style="{ top: `${y}px`, left: `${x}px`, display: 'block' }"
      @contextmenu.prevent
    >
      <!-- Item 1 -->
      <div
        :class="{ disabled: isActiveRepo }"
        class="ctx-item"
        @click="handleAction('open-repository')"
      >
        <div class="ctx-left">
          <i class="fa-regular fa-circle-check ctx-icon"></i>
          <span>Active</span>
        </div>
        <span class="ctx-shortcut">Alt+T</span>
      </div>

      <!-- Open Multi-level -->
      <div class="ctx-item">
        <div class="ctx-left">
          <i class="fa-solid fa-folder-open ctx-icon"></i>
          <span>Open In</span>
        </div>
        <i class="fa-solid fa-chevron-right text-[10px]"></i>

        <!-- Sub Menu -->
        <div class="ctx-submenu">
          <div class="ctx-item" @click="handleAction('open-in-explorer')">
            <div class="ctx-left">
              <i class="fa-solid fa-folder-tree ctx-icon"/>
              <span>Explorer</span>
            </div>
          </div>
          <div class="ctx-item">
            <div class="ctx-left">
              <i class="fa-solid fa-code-branch ctx-icon"></i>
              <span>Open with</span>
            </div>
            <i class="fa-solid fa-chevron-right text-[10px]"></i>

            <!-- Sub Menu -->
            <div class="ctx-submenu">
              <div class="ctx-item" @click="handleAction('git-fetch')">
                <div class="ctx-left">
                  <php-storm-icon size="5" class="ctx-icon"/>
                  <span>PhpStorm</span>
                </div>
              </div>
              <div class="ctx-item" @click="handleAction('git-pull')">
                <div class="ctx-left">
                  <sublime-text-icon size="5" class="ctx-icon"/>
                  <span>Sublime Text</span>
                </div>
              </div>
              <div class="ctx-item" @click="handleAction('git-pull')">
                <div class="ctx-left">
                  <visual-studio-code-icon class="ctx-icon"/>
                  <span>Visual Studio Code</span>
                </div>
              </div>
            </div>
          </div>
          <div class="ctx-item" @click="handleAction('open-in-terminal')">
            <div class="ctx-left">
              <terminal-icon size="5" class="ctx-icon"/>
              <span>Terminal</span>
            </div>
          </div>
        </div>
      </div>

      <div class="menu-separator"></div>

      <!-- Copy Path -->
      <div class="ctx-item" @click="handleAction('copy-path')">
        <div class="ctx-left">
          <i class="fa-solid fa-rotate ctx-icon"/>
          <span>Refresh</span>
        </div>
        <span class="ctx-shortcut">F5</span>
      </div>

      <div class="menu-separator"></div>
      <!-- Multi-level Item -->
      <div class="ctx-item">
        <div class="ctx-left">
          <i class="fa-solid fa-code-branch ctx-icon"></i>
          <span>Git</span>
        </div>
        <i class="fa-solid fa-chevron-right text-[10px]"></i>

        <!-- Sub Menu -->
        <div class="ctx-submenu">
          <div class="ctx-item" @click="handleAction('git-fetch')">
            <div class="ctx-left">
              <i class="fa-solid fa-download ctx-icon"></i>
              <span>Fetch</span>
            </div>
          </div>
          <div class="ctx-item" @click="handleAction('git-pull')">
            <div class="ctx-left">
              <i class="fa-solid fa-arrow-down ctx-icon"></i>
              <span>Pull</span>
            </div>
          </div>
          <div class="ctx-item" @click="handleAction('git-push')">
            <div class="ctx-left">
              <i class="fa-solid fa-arrow-up ctx-icon"></i>
              <span>Push</span>
            </div>
          </div>
          <div class="menu-separator"></div>
          <div class="ctx-item">
            <div class="ctx-left">
              <i class="fa-solid fa-flask ctx-icon"></i>
              <span>Experimental</span>
            </div>
            <i class="fa-solid fa-chevron-right text-[10px]"></i>
            <!-- Level 3 -->
            <div class="ctx-submenu">
              <div class="ctx-item" @click="handleAction('gc-prune')">GC Prune</div>
            </div>
          </div>
        </div>
      </div>

      <div class="menu-separator"></div>

      <!-- Copy Path -->
      <div class="ctx-item" @click="handleAction('copy-path')">
        <div class="ctx-left">
          <i class="fa-solid fa-copy ctx-icon"></i>
          <span>Copy Path</span>
        </div>
        <span class="ctx-shortcut">Ctrl+C</span>
      </div>

      <!-- Rename -->
      <div class="ctx-item" @click="handleAction('rename')">
        <div class="ctx-left">
          <i class="fa-solid fa-pencil ctx-icon"/>
          <span>Rename...</span>
        </div>
        <span class="ctx-shortcut">F2</span>
      </div>

      <div class="menu-separator"></div>

      <!-- Remove -->
      <div
        :class="{ disabled: isActiveRepo }"
        class="ctx-item"
        @click="handleAction('remove-repo')"
      >
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
import TerminalIcon from '@/components/icons/TerminalIcon.vue'
import PhpStormIcon from '@/components/icons/PhpStormIcon.vue'
import VisualStudioCodeIcon from '@/components/icons/VisualStudioCodeIcon.vue'
import SublimeTextIcon from '@/components/icons/SublimeTextIcon.vue'
// --- STATE ---
const isVisible = ref(false);
const x = ref(0);
const y = ref(0);
const menuRef = ref(null);
const targetData = ref(null); // Lưu dữ liệu của item được click chuột phải (nếu cần)
const isActiveRepo = ref(false)

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

  isActiveRepo.value = data?.active ?? false

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
const handleGlobalClick = () => {
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

.ctx-item.disabled {
  opacity: 0.4;
  pointer-events: none;
}

</style>
