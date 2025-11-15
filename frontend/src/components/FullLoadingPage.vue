<template>
  <div v-if="isLoading" class="loader-overlay">
    <div class="panda-container">
      <img src="@/assets/cool.png">
    </div>
    <div class="panda-loader">
      <div class="panda-progress" data-percentage="100%"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isLoading: {
    type: Boolean,
    required: true
  }
})
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: var(--bg-primary);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  gap: 5px
}
.panda-container {
  position: relative;
}
.panda-container img {
  height: 400px;
}

.panda-loader {
  width: 400px;
  height: 32px;
  background-color: #000000;
  position: relative;
  overflow: hidden;
  border: 3px solid white;
}

.panda-progress {
  width: 0%;
  height: 100%;
  background-color: #ffffff;
  position: absolute;
  top: 0;
  left: 0;
  animation: progress-animation 2s ease-in-out forwards infinite;
}

.panda-progress::after {
  content: attr(data-percentage);
  position: absolute;
  top: 50%;
  left: 50%;
  font-weight: bold;
  transform: translate(-50%, -50%);
  font-size: 1rem;
  color: black;
}

@keyframes progress-animation {
  0% {
    width: 0;
  }
  25% {
    width: 25%;
  }
  50% {
    width: 50%;
  }
  75% {
    width: 75%;
  }
  100% {
    width: 100%;
  }
}

@keyframes percentage-animation {
  0% {
    content: "0%";
  }
  25% {
    content: "25%";
  }
  50% {
    content: "50%";
  }
  75% {
    content: "75%";
  }
  100% {
    content: "100%";
  }
}

.panda-progress::after {
  animation: percentage-animation 2s ease-in-out forwards infinite;
}
</style>
