<template>
  <div
    class="checkbox-row"
    :class="{ disabled: disabled }"
    @click="toggle"
  >
    <div :class="['custom-checkbox', { checked: modelValue }]">
      <i class="fa-solid fa-check" />
    </div>

    <span
      v-if="label"
      class="checkbox-label"
    >{{ label }}</span>

    <slot />
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const toggle = () => {
  if (!props.disabled) {
    emit('update:modelValue', !props.modelValue)
  }
}
</script>

<style scoped>
/* Wrapper style: Giống co-item và commit-options-row */
.checkbox-row {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s;
}

.checkbox-row.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Label Style */
.checkbox-label {
  font-size: 11px;
  color: var(--p-text-muted); /* Màu mặc định */
  flex: 1;
  transition: color 0.2s;
}

/* Hover Effect: Đổi màu text và border checkbox */
.checkbox-row:hover .checkbox-label {
  color: var(--text-color);
}
.checkbox-row:hover .custom-checkbox {
  border-color: var(--text-color);
}

/* --- CUSTOM CHECKBOX STYLES (Giữ nguyên từ code cũ) --- */
.custom-checkbox {
  width: 14px;
  height: 14px;
  border: 1px solid var(--p-text-dim);
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0; /* Tránh bị méo khi text dài */
  transition: all 0.2s;
  background-color: transparent;
}

.custom-checkbox.checked {
  background-color: var(--accent-color);
  border-color: var(--accent-color);
  color: var(--bg-main);
}

.custom-checkbox i {
  font-size: 10px;
  display: none;
}

.custom-checkbox.checked i {
  display: block;
}
</style>
