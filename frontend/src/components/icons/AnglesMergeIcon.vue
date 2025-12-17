<template>
  <div
    class="merge-arrow"
    :class="sizeClass"
  >
    <i
      class="fa-solid fa-angles-right arrow top"
      style="font-size: 10px"
    />
    <i
      class="fa-solid fa-angles-left arrow bottom"
      style="font-size: 10px"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md', // sm | md | lg
  },
})

const sizeClass = computed(() => `merge-arrow--${props.size}`)
</script>

<style scoped>
.merge-arrow {
  position: relative;
  display: inline-block;
}

/* ===== sizes ===== */
.merge-arrow--sm { width: 12px; height: 12px; }
.merge-arrow--md { width: 20px; height: 20px; }
.merge-arrow--lg { width: 24px; height: 24px; }

.arrow {
  position: absolute;
  font-size: 0.75em;
  transition: transform 0.2s ease, color 0.2s ease;
}

/* top: right arrow */
.arrow.top {
  top: 1.5px;
  left: 5.5px;
}

/* bottom: left arrow */
.arrow.bottom {
  bottom: 1.5px;
  right: 5.5px;
}

/* trạng thái mặc định: luôn giãn ra */
.arrow.top {
  transform: translateX(-4px);
}

.arrow.bottom {
  transform: translateX(4px);
}

</style>
