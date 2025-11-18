<template>
  <div v-if="visible" class="modal fade show d-block" tabindex="-1" style="background: rgba(0, 0, 0, 0.5);">
    <div class="modal-dialog modal-dialog-centered">
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
import { ref, watch, defineExpose } from 'vue'

const props = defineProps({
  title: String,
  modelValue: Boolean,
})

const emit = defineEmits(['update:modelValue', 'close'])

const visible = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  visible.value = val
})

function close() {
  visible.value = false
  emit('update:modelValue', false)
  emit('close')
}

defineExpose({ close })
</script>

<style scoped>
.modal {
  z-index: 1050;
}
</style>
