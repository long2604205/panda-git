<template>
  <Transition name="fade">
    <div v-if="visible" class="alert-notification" :style="{ height: title ? '80px' : '60px' }">
      <div class="icon-container">
        <i :class="getIconForType(type)" class="icon" />
      </div>
      <div class="message-text-container">
        <p class="message-text">{{ title }}</p>
        <p class="sub-text">{{ message }}</p>
      </div>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 15 15"
        stroke-width="0"
        fill="none"
        stroke="currentColor"
        class="cross-icon"
        @click="close"
      >
        <path
          fill="currentColor"
          d="M11.7816 4.03157C12.0062 3.80702 12.0062 3.44295 11.7816 3.2184C11.5571 2.99385 11.193 2.99385 10.9685 3.2184L7.50005 6.68682L4.03164 3.2184C3.80708 2.99385 3.44301 2.99385 3.21846 3.2184C2.99391 3.44295 2.99391 3.80702 3.21846 4.03157L6.68688 7.49999L3.21846 10.9684C2.99391 11.193 2.99391 11.557 3.21846 11.7816C3.44301 12.0061 3.80708 12.0061 4.03164 11.7816L7.50005 8.31316L10.9685 11.7816C11.193 12.0061 11.5571 12.0061 11.7816 11.7816C12.0062 11.557 12.0062 11.193 11.7816 10.9684L8.31322 7.49999L11.7816 4.03157Z"
          clip-rule="evenodd"
          fill-rule="evenodd"
        ></path>
      </svg>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
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
  setTimeout(() => emit('close'), 6000)
}
const getIconForType = (type) => {
  switch (type) {
    case 'danger':
      return 'bi bi-patch-exclamation-fill alert-danger-type'
    case 'warning':
      return 'bi bi-exclamation-triangle-fill alert-warning-type'
    case 'info':
      return 'fa-solid fa-circle-info alert-info-type'
    case 'success':
      return 'bi bi-check-circle-fill alert-success-type'
  }
}
onMounted(() => {
  setTimeout(() => {
    close()
  }, props.duration)
})
</script>

<style scoped>
.alert-notification {
  width: 330px;
  border-radius: 8px;
  box-sizing: border-box;
  padding: 5px 10px;
  background-color: rgb(26, 26, 26, 26);
  box-shadow: var(--shadow) 0 8px 24px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 5px;
  bottom: 45px;
  right: 10px;
  margin-top: 6px;
}

.alert-notification:hover .cross-icon {
  opacity: 1;
  pointer-events: auto;
}

.alert-notification:hover .cross-icon:hover {
  color: white;
}

.icon-container {
  width: 35px;
  height: 35px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  margin-left: 5px;
}
.icon {
  font-size: 20px;
  width: 20px;
}
.message-text-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  flex-grow: 1;
}
.message-text,
.sub-text {
  margin: 0;
  cursor: default;
}
.message-text {
  color: #ffffff;
  font-size: 15px;
  font-weight: 700;
}
.sub-text {
  font-size: 12px;
  color: #ffffff;
}
.cross-icon {
  width: 18px;
  height: 18px;
  color: #555;
  cursor: pointer;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
}

.alert-danger-type {
  color: red;
}

.alert-info-type {
  color: #82aaff;
}

.alert-warning-type {
  color: #ffcc00;
}

.alert-success-type {
  color: #198754;
}

/* transition fade */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
