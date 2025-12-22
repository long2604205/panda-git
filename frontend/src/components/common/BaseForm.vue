<template>
  <div
    :id="id"
    ref="overlay"
    class="modal-overlay"
  >
    <div
      class="modal-window"
      :style="{ maxWidth: width }"
    >
      <div class="modal-header">
        <h3
          class="font-bold text-sm text-[var(--text-color)]"
          :class="{ 'is-uppercase': props.uppercase }"
        >
          {{ title }}
        </h3>
        <i
          class="fa-solid fa-xmark cursor-pointer text-[var(--p-text-dim)] hover:text-[var(--text-color)]"
          @click="close"
        />
      </div>

      <div class="modal-body">
        <slot name="content">
          <slot />
        </slot>
      </div>

      <div class="modal-footer">
        <slot name="footer">
          <button
            class="btn btn-secondary"
            @click="close"
          >
            Close
          </button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  id: { type: String, default: 'base-form-modal' },
  modelValue: { type: Boolean, default: false },
  title: { type: String, default: 'Modal' },
  width: { type: String, default: '600px' },
  uppercase: { type: Boolean, default: true },
})

const emit = defineEmits(['update:modelValue', 'close'])

const overlay = ref(null)

const open = () => {
  const el = overlay.value
  if (!el) return

  el.classList.remove('open')

  requestAnimationFrame(() => {
    el.classList.add('open')
  })

  setTimeout(() => {
    emit('opened')
  }, 200)
}

const close = () => {
  overlay.value?.classList.remove('open')
  emit('update:modelValue', false)
  emit('close')
}

onMounted(() => {
  if (props.modelValue) open()
})

watch(
  () => props.modelValue,
  (val) => {
    val ? open() : close()
  }
)

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

.is-uppercase {
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
</style>
