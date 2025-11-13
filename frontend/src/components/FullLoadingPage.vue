<template>
  <div v-if="isLoading" class="loader-overlay">
    <div class="panda-container">
      <div class="ear ear-left"></div>
      <div class="ear ear-right"></div>
      <div class="panda-head">
        <div class="eye-patch eye-patch-left"></div>
        <div class="eye-patch eye-patch-right"></div>
        <div class="eye eye-left">
          <div class="eyelid"></div>
          <div class="pupil"></div>
        </div>
        <div class="eye eye-right">
          <div class="eyelid"></div>
          <div class="pupil"></div>
        </div>
        <div class="nose"></div>
        <div class="mouth"></div>
      </div>
    </div>

    <!-- From Uiverse.io by ClawHack1 -->
    <div class="loader">
      <div class="loader-inner">
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
        <div class="loader-block"></div>
      </div>
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
  z-index: 9999;
  gap: 5px
}
.panda-container {
  position: relative;
  width: 300px;
  height: 280px;
}

.panda-head {
  position: absolute;
  width: 200px;
  height: 180px;
  background: white;
  border: 4px solid #222;
  border-radius: 50%;
  top: 50px;
  left: 50px;
  z-index: 4;
  box-shadow:
    0 5px 15px rgba(0, 0, 0, 0.1),
    inset 0 -8px 25px rgba(0, 0, 0, 0.08);
}

.ear {
  position: absolute;
  width: 70px;
  height: 70px;
  background: #222;
  border: 4px solid #222;
  border-radius: 50%;
  z-index: 3;
  box-shadow: inset 0 -8px 15px rgba(0, 0, 0, 0.3);
}

.ear-left {
  top: 30px;
  left: 40px;
  transform: rotate(-15deg);
}

.ear-right {
  top: 30px;
  left: 190px;
  transform: rotate(15deg);
}

.eye-patch {
  position: absolute;
  width: 60px;
  height: 70px;
  background: #222;
  border-radius: 50%;
  z-index: 5;
  box-shadow: inset 0 -5px 10px rgba(0, 0, 0, 0.4);
}

.eye-patch-left {
  top: 60px;
  left: 30px;
}

.eye-patch-right {
  top: 60px;
  left: 110px;
}

.eye {
  position: absolute;
  width: 25px;
  height: 30px;
  background: white;
  border-radius: 60%;
  z-index: 6;
  overflow: hidden;
}

.eye-left {
  top: 75px;
  left: 45px;
}

.eye-right {
  top: 75px;
  left: 125px;
}

.eyelid {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #222;
  border-radius: 80%;
  z-index: 7;
  transform-origin: top;
  animation: blink 4s ease-in-out infinite;
}

.pupil {
  position: absolute;
  width: 12px;
  height: 12px;
  background: #000;
  border-radius: 50%;
  z-index: 6;
  top: 9px;
  left: 6px;
}

.nose {
  position: absolute;
  width: 30px;
  height: 25px;
  background: #222;
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  top: 110px;
  left: 85px;
  z-index: 8;
  box-shadow: inset 0 -3px 8px rgba(0, 0, 0, 0.4);
}

.mouth {
  position: absolute;
  width: 40px;
  height: 20px;
  border-bottom: 3px solid #222;
  border-radius: 0 0 50% 50%;
  top: 135px;
  left: 80px;
  z-index: 7;
  transform-origin: center;
  animation: smile 4s ease-in-out infinite;
}

@keyframes blink {
  0%,
  30% {
    transform: scaleY(1);
  }
  35%,
  65% {
    transform: scaleY(0);
  }
  70%,
  100% {
    transform: scaleY(1);
  }
}

@keyframes smile {
  0%,
  30% {
    width: 40px;
    left: 80px;
  }
  35%,
  65% {
    width: 60px;
    left: 70px;
  }
  70%,
  100% {
    width: 40px;
    left: 80px;
  }
}

/* Loading bar */
.loader {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  position: relative;
  margin-top: -30px;
}

.loader:before {
  content: "";
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  border-radius: 50%;
}

.loader-inner {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.loader-block {
  display: inline-block;
  width: 10px;
  height: 10px;
  margin: 2px;
  background-color: #fff;
  box-shadow: 0 0 20px #fff;
  animation: loader_562 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

.loader-block:nth-child(1) {
  animation-delay: 0.1s;
}

.loader-block:nth-child(2) {
  animation-delay: 0.2s;
}

.loader-block:nth-child(3) {
  animation-delay: 0.3s;
}

.loader-block:nth-child(4) {
  animation-delay: 0.4s;
}

.loader-block:nth-child(5) {
  animation-delay: 0.5s;
}

.loader-block:nth-child(6) {
  animation-delay: 0.6s;
}

.loader-block:nth-child(7) {
  animation-delay: 0.7s;
}

.loader-block:nth-child(8) {
  animation-delay: 0.8s;
}

.loader-block:nth-child(9) {
  animation-delay: 0.9s;
}

.loader-block:nth-child(10) {
  animation-delay: 1s;
}

.loader-block:nth-child(11) {
  animation-delay: 1.1s;
}

.loader-block:nth-child(12) {
  animation-delay: 1.2s;
}

@keyframes loader_562 {
  0% {
    transform: scale(1);
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
  }

  20% {
    transform: scale(1, 2.5);
    box-shadow: 0 0 50px rgba(255, 255, 255, 0.7);
  }

  40% {
    transform: scale(1);
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
  }
}
</style>
