<template>
  <base-form
    v-model="visible"
    :title="title"
    width="400px"
  >
    <template #content>
      <p class="mb-0">{{ message }}</p>
    </template>

    <template #footer>
      <button class="btn btn-cancel" @click="cancel">Cancel</button>
      <button class="btn btn-confirm" @click="confirm">Confirm</button>
    </template>
  </base-form>
</template>

<script setup>
import { computed } from "vue"
import BaseForm from "@/components/common/BaseForm.vue"

const props = defineProps({
  modelValue: Boolean,
  title: String,
  message: String
})

const emit = defineEmits(["update:modelValue", "confirm", "cancel"])

const visible = computed({
  get: () => props.modelValue,
  set: v => emit("update:modelValue", v)
})

function confirm() {
  emit("confirm")
  visible.value = false
}

function cancel() {
  visible.value = false
}
</script>

<style  scoped>
.btn-cancel, .btn-confirm, .btn-confirm:disabled {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: var(--bg-tertiary);
  font-size: 14px;
  font-weight: 500;
}
.btn-confirm:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}
.btn-cancel:hover {
  background: var(--bs-red);
  color: var(--text-primary);
}
</style>
