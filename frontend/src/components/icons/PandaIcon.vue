<template>
  <i
    :class="[iconClass, attrs.class]"
    :style="iconStyle"
  />
</template>

<script setup>
import { computed, useAttrs } from 'vue'

const attrs = useAttrs()

const props = defineProps({
  type: {
    type: String,
    default: 'solid',
  },
  name: {
    type: String,
    required: true,
  },
  size: {
    type: String,
    default: null,
  },
  width: {
    type: String,
    default: null,
  },
  height: {
    type: String,
    default: null,
  },
  color: {
    type: String,
    default: null,
  },
})

const faTypeClass = {
  solid: 'fa-solid',
  regular: 'fa-regular',
  brands: 'fa-brands',
}

const iconClass = computed(() => {
  const prefix = faTypeClass[props.type] || faTypeClass.solid
  return `${prefix} fa-${props.name}`
})

const iconStyle = computed(() => ({
  fontSize: props.size || null,
  width: props.width || null,
  height: props.height || null,
  lineHeight: props.height || null,
  color: props.color || null,
  ...(attrs.style || {}),
}))
</script>
