<template>
  <Transition name="fade">
    <div class="alert-notification" v-if="visible">
      <div class="alert-box" :class="type">
        <span>{{ message }}</span>
        <button @click="close">×</button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: 'info', // success | error | warning
  },
  duration: {
    type: Number,
    default: 5000, // milliseconds
  },
})

const visible = ref(true)
const emit = defineEmits(['close'])
const close = () => {
  visible.value = false
  setTimeout(() => emit('close'), 500) // đợi animation fade-out xong mới emit
}

onMounted(() => {
  setTimeout(() => {
    close()
  }, props.duration)
})
</script>

<style scoped>
.alert-notification {
  position: fixed;
  bottom: 30px;
  right: 10px;
  z-index: 9999;
}

.alert-box {
  background-color: var(--bg-secondary);
  color: #fff;
  padding: 10px 16px;
  border-radius: 6px;
  min-width: 300px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 0 8px rgba(0,0,0,0.2);
  transition: all 0.3s ease-in-out;
}

.alert-box.success {
  background-color: #4caf50;
}
.alert-box.error {
  background-color: #f44336;
}
.alert-box.warning {
  background-color: #ff9800;
}

.alert-box button {
  background: none;
  border: none;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
