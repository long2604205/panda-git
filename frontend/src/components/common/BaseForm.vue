<template>
  <div
    :id="id"
    ref="overlay"
    class="modal-overlay"
  >
    <div class="modal-window" :style="{ maxWidth: width }">
      <div class="modal-header">
        <h3 class="font-bold text-sm text-[var(--text-color)]">{{ title }}</h3>
        <i class="fa-solid fa-xmark cursor-pointer text-[var(--p-text-dim)] hover:text-[var(--text-color)]" @click="close"/>
      </div>

      <div class="modal-body">
        <slot name="content">
          <slot />
        </slot>
      </div>

      <div class="modal-footer">
        <slot name="footer">
          <button class="btn btn-secondary" @click="close">Close</button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, defineExpose } from 'vue'

const props = defineProps({
  id: { type: String, default: 'base-form-modal' },
  modelValue: { type: Boolean, default: false },
  title: { type: String, default: 'Modal' },
  width: { type: String, default: '600px' },
})

const emit = defineEmits(['update:modelValue', 'close'])

const overlay = ref(null)

// mở modal
const open = () => {
  const el = overlay.value
  if (!el) return

  // reset trạng thái trước
  el.classList.remove('open')

  // đợi browser render xong frame đầu
  requestAnimationFrame(() => {
    el.classList.add('open')
  })

  setTimeout(() => {
    emit('opened')
  }, 200)
}

// đóng modal
const close = () => {
  overlay.value?.classList.remove('open')
  emit('update:modelValue', false)
  emit('close')
}

onMounted(() => {
  if (props.modelValue) open()
})

// watch v-model để mở / tắt
watch(
  () => props.modelValue,
  (val) => {
    val ? open() : close()
  }
)

// để form cha gọi openForm.value.close()
defineExpose({ open, close })
</script>


<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: var(--modal-overlay);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
  backdrop-filter: blur(2px);
}

.modal-overlay.open {
  opacity: 1;
  pointer-events: auto;
}

.modal-window {
  background-color: var(--modal-bg);
  border: 1px solid var(--border-color);
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  transform: scale(0.95);
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
}

.modal-overlay.open .modal-window {
  transform: scale(1);
}

.modal-header {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  text-transform: uppercase;
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  background-color: var(--p-hover);
  border-radius: 0 0 8px 8px;
}

.btn {
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.btn-secondary {
  background-color: transparent;
  border-color: var(--border-color);
  color: var(--text-color);
}

.btn-secondary:hover {
  background-color: var(--bg-side);
}
</style>
