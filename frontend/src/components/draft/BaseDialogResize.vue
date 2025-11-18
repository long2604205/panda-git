<template>
  <div
    v-if="visible"
    class="modal fade show d-block"
    tabindex="-1"
    style="background: rgba(0, 0, 0, 0.5);"
  >
    <div class="modal-dialog modal-dialog-centered custom-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" @click="close()"></button>
        </div>

        <div class="modal-body">
          <slot />
        </div>

        <div class="modal-footer">
          <slot name="footer">
            <button class="btn btn-secondary" @click="close()">Đóng</button>
          </slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, defineExpose } from 'vue'

const props = defineProps({
  title: String,
  modelValue: Boolean,
  width: {
    type: String,
    default: '600px',
  },
})

const emit = defineEmits(['update:modelValue', 'close'])

const visible = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  visible.value = val
})

const widthComputed = computed(() => {
  const val = props.width.trim()
  if (val.endsWith('%') || val.endsWith('px')) return val
  return '600px'
})

function close() {
  visible.value = false
  emit('update:modelValue', false)
  emit('close')
}

defineExpose({ close, visible })
</script>

<style scoped>
.modal {
  z-index: 1050;
}

/* Ghi đè Bootstrap modal để cho phép custom width 100% màn hình */
.custom-modal {
  margin: 0 auto;
  width: 100%;
  max-width: none;
}

.custom-modal .modal-content {
  margin: auto;
  width: v-bind('widthComputed');
  max-width: 100%;
}
</style>
