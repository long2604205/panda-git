<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', toast.type]"
        >
          <i :class="getIcon(toast.type)"></i>
          <span class="toast-message">{{ toast.message }}</span>
          <button
            v-if="toast.closable"
            @click="removeToast(toast.id)"
            class="toast-close"
          >
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

// ==================== STATE ====================
const toasts = ref([]);
let toastIdCounter = 0;
const timers = new Map();

// ==================== PROPS ====================
const props = defineProps({
  position: {
    type: String,
    default: 'bottom-right', // top-left, top-right, bottom-left, bottom-right, top-center, bottom-center
    validator: (value) => [
      'top-left',
      'top-right',
      'bottom-left',
      'bottom-right',
      'top-center',
      'bottom-center'
    ].includes(value)
  },
  duration: {
    type: Number,
    default: 3000 // milliseconds
  },
  maxToasts: {
    type: Number,
    default: 5
  }
});

// ==================== EMITS ====================
const emit = defineEmits(['toast-shown', 'toast-hidden']);

// ==================== METHODS ====================
const getIcon = (type) => {
  const icons = {
    success: 'fa-solid fa-check-circle',
    error: 'fa-solid fa-exclamation-circle',
    warning: 'fa-solid fa-exclamation-triangle',
    info: 'fa-solid fa-info-circle',
    loading: 'fa-solid fa-spinner fa-spin'
  };
  return icons[type] || icons.info;
};

const show = (message, type = 'info', options = {}) => {
  const id = toastIdCounter++;

  // Limit max toasts
  if (toasts.value.length >= props.maxToasts) {
    const oldestToast = toasts.value[0];
    removeToast(oldestToast.id);
  }

  const toast = {
    id,
    message,
    type,
    closable: options.closable !== false,
    duration: options.duration || props.duration
  };

  toasts.value.push(toast);
  emit('toast-shown', toast);

  // Auto remove (except loading type)
  if (type !== 'loading' && toast.duration > 0) {
    const timer = setTimeout(() => {
      removeToast(id);
    }, toast.duration);
    timers.set(id, timer);
  }

  return id;
};

const removeToast = (id) => {
  const index = toasts.value.findIndex(t => t.id === id);
  if (index !== -1) {
    const toast = toasts.value[index];
    toasts.value.splice(index, 1);
    emit('toast-hidden', toast);

    // Clear timer if exists
    if (timers.has(id)) {
      clearTimeout(timers.get(id));
      timers.delete(id);
    }
  }
};

const clear = () => {
  toasts.value.forEach(toast => {
    if (timers.has(toast.id)) {
      clearTimeout(timers.get(toast.id));
    }
  });
  timers.clear();
  toasts.value = [];
};

// Helper methods
const success = (message, options) => show(message, 'success', options);
const error = (message, options) => show(message, 'error', options);
const warning = (message, options) => show(message, 'warning', options);
const info = (message, options) => show(message, 'info', options);
const loading = (message, options) => show(message, 'loading', { ...options, closable: false });

// ==================== EXPOSE ====================
defineExpose({
  show,
  success,
  error,
  warning,
  info,
  loading,
  removeToast,
  clear
});

// ==================== LIFECYCLE ====================
onBeforeUnmount(() => {
  clear();
});
</script>

<style scoped>
/* ==================== THEME VARIABLES ==================== */
.toast-container {
  --p-bg-sidebar: #131519;
  --p-border: #2a2d35;
  --p-text-main: #e2e8f0;
  --p-text-muted: #94a3b8;
  --p-highlight: #22d3ee;
  --p-green: #4ade80;
  --p-red: #f87171;
  --p-yellow: #fbbf24;
  --p-orange: #f59e0b;
}

/* ==================== CONTAINER POSITIONING ==================== */
.toast-container {
  position: fixed;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;

  /* Default: bottom-right */
  bottom: 24px;
  right: 24px;
}

/* Position variants */
.toast-container.top-left {
  top: 24px;
  left: 24px;
  bottom: auto;
  right: auto;
}

.toast-container.top-right {
  top: 24px;
  right: 24px;
  bottom: auto;
  left: auto;
}

.toast-container.bottom-left {
  bottom: 24px;
  left: 24px;
  top: auto;
  right: auto;
}

.toast-container.bottom-right {
  bottom: 24px;
  right: 24px;
  top: auto;
  left: auto;
}

.toast-container.top-center {
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  bottom: auto;
  right: auto;
}

.toast-container.bottom-center {
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  top: auto;
  right: auto;
}

/* ==================== TOAST ITEM ==================== */
.toast {
  background-color: var(--p-bg-sidebar);
  border: 1px solid var(--p-border);
  border-radius: 6px;
  padding: 12px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 250px;
  max-width: 400px;
  pointer-events: auto;
  font-size: 13px;
  color: var(--p-text-main);
  backdrop-filter: blur(10px);
}

.toast i {
  font-size: 16px;
  flex-shrink: 0;
}

.toast-message {
  flex: 1;
  word-break: break-word;
}

.toast-close {
  background: none;
  border: none;
  color: var(--p-text-muted);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: var(--p-text-main);
}

.toast-close i {
  font-size: 12px;
}

/* ==================== TOAST TYPES ==================== */
.toast.success {
  border-color: var(--p-green);
}

.toast.success i {
  color: var(--p-green);
}

.toast.error {
  border-color: var(--p-red);
}

.toast.error i {
  color: var(--p-red);
}

.toast.warning {
  border-color: var(--p-orange);
}

.toast.warning i {
  color: var(--p-orange);
}

.toast.info {
  border-color: var(--p-highlight);
}

.toast.info i {
  color: var(--p-highlight);
}

.toast.loading {
  border-color: var(--p-text-muted);
}

.toast.loading i {
  color: var(--p-text-muted);
}

/* ==================== TRANSITIONS ==================== */
.toast-enter-active {
  animation: toast-slide-in 0.3s ease-out;
}

.toast-leave-active {
  animation: toast-fade-out 0.2s ease-in;
}

@keyframes toast-slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes toast-fade-out {
  to {
    opacity: 0;
    transform: translateY(-10px);
  }
}

/* For left-side positions */
.toast-container.top-left .toast-enter-active,
.toast-container.bottom-left .toast-enter-active {
  animation: toast-slide-in-left 0.3s ease-out;
}

@keyframes toast-slide-in-left {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* For center positions */
.toast-container.top-center .toast-enter-active,
.toast-container.bottom-center .toast-enter-active {
  animation: toast-scale-in 0.3s ease-out;
}

@keyframes toast-scale-in {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 640px) {
  .toast-container {
    left: 12px !important;
    right: 12px !important;
    bottom: 12px;
    transform: none !important;
  }

  .toast {
    min-width: auto;
    width: 100%;
  }
}
</style>
