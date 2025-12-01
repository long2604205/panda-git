<template>
    <Teleport to="body">
        <div class="toast-container">
            <TransitionGroup name="toast" class="toast-list">
                <div v-for="toast in toasts" :key="toast.id" :class="['toast', toast.type]">
                    <i :class="getIcon(toast.type)"></i>

                    <span class="toast-message">{{ toast.message }}</span>

                    <button v-if="toast.closable" @click="removeToast(toast.id)" class="toast-close-btn">
                        <i class="fa-solid fa-xmark fa-xs"></i>
                    </button>
                </div>
            </TransitionGroup>
        </div>
    </Teleport>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue';
import mitter from '@/plugins/mitter.js'

// ==================== STATE & LOGIC (Giữ nguyên logic đã fix ID) ====================
const toasts = ref([]);
const timers = new Map();
const generateId = () => 'toast_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);

const props = defineProps({
    position: { type: String, default: 'bottom-right' },
    duration: { type: Number, default: 3000 },
    maxToasts: { type: Number, default: 5 }
});

const emit = defineEmits(['toast-shown', 'toast-hidden']);

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
    const id = options.id !== undefined ? String(options.id) : generateId();
    const existingIndex = toasts.value.findIndex(t => t.id === id);
    if (existingIndex !== -1) removeToast(id);

    const toast = {
        id,
        message,
        type,
        closable: options.closable !== false,
        duration: options.duration || props.duration
    };

    if (toasts.value.length >= props.maxToasts) {
        removeToast(toasts.value[0].id);
    }

    toasts.value.push(toast);
    emit('toast-shown', toast);

    if (type !== 'loading' && toast.duration > 0) {
        const timer = setTimeout(() => removeToast(id), toast.duration);
        timers.set(id, timer);
    }
    return id;
};

const removeToast = (id) => {
    const targetId = String(id);
    const index = toasts.value.findIndex(t => t.id === targetId);
    if (index !== -1) {
        const toast = toasts.value[index];
        toasts.value.splice(index, 1);
        emit('toast-hidden', toast);
        if (timers.has(targetId)) {
            clearTimeout(timers.get(targetId));
            timers.delete(targetId);
        }
    }
};

const clear = () => {
    toasts.value.forEach(t => { if (timers.has(t.id)) clearTimeout(timers.get(t.id)) });
    timers.clear();
    toasts.value = [];
};

const success = (msg, opt) => show(msg, 'success', opt);
const error = (msg, opt) => show(msg, 'error', opt);
const warning = (msg, opt) => show(msg, 'warning', opt);
const info = (msg, opt) => show(msg, 'info', opt);
const loading = (msg, opt) => show(msg, 'loading', { ...opt, closable: false });

defineExpose({ show, success, error, warning, info, loading, removeToast, clear });

mitter.on("toast", (p) => show(p.message, p.type, p));
mitter.on("toast-remove", (id) => removeToast(id));

onBeforeUnmount(() => {
    clear();
    mitter.off("toast");
    mitter.off("toast-remove");
});
</script>

<style scoped>
/* Container chính */
.toast-container {
    position: fixed;
    bottom: 32px;
    right: 20px;
    z-index: 1000;
    pointer-events: none;
}

/* Wrapper của TransitionGroup */
.toast-list {
    display: flex;
    flex-direction: column;
    /* gap: 10px;  <-- XÓA DÒNG NÀY ĐI */

    width: 300px;
    position: relative;
}

/* Style Toast */
.toast {
    background: var(--bg-side);
    color: var(--text-color);
    padding: 10px 16px;
    border-radius: 6px;
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
    pointer-events: auto;
    width: 100%;
    box-sizing: border-box;

    /* --- THÊM DÒNG NÀY (Thay thế cho gap) --- */
    margin-bottom: 3px;

    /* Giữ nguyên hiệu ứng chuyển động mượt mà cho các thuộc tính khác */
    transition: all 0.3s ease;
}

.toast i {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

/* Xóa margin của thằng cuối cùng (tùy chọn) */
.toast:last-child {
    margin-bottom: 0;
}

/* Icons & Button */
.toast i {
    font-size: 14px;
}

.toast.success i {
    color: #4ade80;
}

.toast.error i {
    color: #ef4444;
}

.toast.warning i {
    color: #f59e0b;
}

.toast.info i {
    color: var(--accent-color);
}

.toast.loading i {
    animation: spin 1s linear infinite;
    color: var(--p-text-muted);
}

.toast-close-btn {
    background: none;
    border: none;
    color: inherit;
    opacity: 0;
    cursor: pointer;
    margin-left: auto;

    transition: opacity 0.2s ease;
    pointer-events: none;
}

.toast:hover .toast-close-btn {
    opacity: 0.6;
    pointer-events: auto;
}

.toast-close-btn:hover {
    opacity: 1 !important;
}

/* =======================================================
   ANIMATION SECTION
   ======================================================= */

/* 1. KHI XUẤT HIỆN */
.toast-enter-active {
    animation: slide-in 0.3s ease-out forwards;
}

/* 2. KHI BIẾN MẤT */
.toast-leave-active {
    position: absolute;

    /* Animation rớt xuống */
    animation: fade-out 0.3s ease-out forwards;

    /* Khóa vị trí */
    left: 0;
    right: 0;
    width: 100%;
    z-index: 0;
}

/* 3. DI CHUYỂN MƯỢT MÀ */
.toast-move {
    transition: all 0.3s ease;
}

/* KEYFRAMES */
@keyframes slide-in {
    from {
        transform: translateX(100%);
        opacity: 0;
    }

    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes fade-out {
    to {
        opacity: 0;
        transform: translateY(20px);
    }
}

@keyframes spin {
    100% {
        transform: rotate(360deg);
    }
}
</style>
