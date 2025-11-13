<template>
  <div
    class="modal fade"
    :id="id"
    tabindex="-1"
    ref="modalRef"
    aria-hidden="true"
  >
    <div
      class="modal-dialog modal-dialog-centered custom-modal"
      :style="{ maxWidth: width }"
    >
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close btn-close-white" @click="close" />
        </div>
        <div class="modal-body">
          <slot name="content">
            <slot />
          </slot>
        </div>
        <div class="modal-footer">
          <slot name="footer">
            <button type="button" class="btn btn-cancel" @click="close">Close</button>
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, defineExpose } from 'vue'
import { Modal } from 'bootstrap'

const props = defineProps({
  id: { type: String, default: 'base-form-modal' },
  title: { type: String, default: 'Modal' },
  modelValue: Boolean,
  width: { type: String, default: '600px' }, // ✅ thêm prop width
})

const emit = defineEmits(['update:modelValue', 'close'])

const modalRef = ref(null)
let modalInstance = null

const close = () => {
  if (modalInstance) modalInstance.hide()
}

// Mount và lắng nghe sự kiện đóng modal
onMounted(() => {
  if (!modalRef.value) return
  modalInstance = new Modal(modalRef.value, { backdrop: 'static' })

  if (props.modelValue) {
    modalInstance.show()
  }

  modalRef.value.addEventListener('hidden.bs.modal', () => {
    emit('update:modelValue', false)
    emit('close')
  })
})

// Cleanup khi bị huỷ
onBeforeUnmount(() => {
  modalInstance?.dispose()
})

// Watch để mở/tắt theo modelValue
watch(() => props.modelValue, (val) => {
  if (!modalInstance) return
  val ? modalInstance.show() : modalInstance.hide()
})

defineExpose({ close })
</script>

<style scoped>
* {
  font-size: 14px;
}

.modal-content {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.modal-header {
  border-bottom: 1px solid var(--border-color);
}

.modal-footer {
  border-top: 1px solid var(--border-color);
}

.custom-modal {
  width: 100%; /* ✅ để hỗ trợ responsive */
}

.btn-cancel,
.btn-clone,
.btn-clone:disabled {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: var(--bg-tertiary);
  font-size: 14px;
  font-weight: 500;
}

.btn-clone:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.btn-cancel:hover {
  background: var(--bs-red);
  color: var(--text-primary);
}

input {
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  font-size: 14px;
  resize: none;
  min-height: 80%;
}

input::placeholder {
  color: var(--text-muted);
}

input:focus {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  box-shadow: none;
}

input:focus-visible {
  outline: none;
  border: 1px solid var(--border-color);
}
</style>
