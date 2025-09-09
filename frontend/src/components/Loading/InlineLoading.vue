<template>
  <div v-if="visible" class="inline-loading">
    <span class="message">{{ message }}</span>
    <div class="bar-container">
      <div class="bar"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  visible: Boolean,
  message: String
})
</script>

<style scoped>
.inline-loading {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #c0c0c0;
  gap: 8px;
}

.bar-container {
  width: 100px;
  height: 4px;
  background-color: #444;
  overflow: hidden;
  border-radius: 2px;
  position: relative;
}

.bar {
  width: 60%;
  height: 100%;
  background-color: orange;
  animation: loading 1.4s infinite ease-in-out;
  border-radius: 2px;
}

@keyframes loading {
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(200%);
  }
}
</style>
