<template>
  <div class="container-fluid main-container">
    <div class="row main-layout-container h-100">
      <!--Repository Workspace-->
      <panda-repository-workspace/>

      <div class="col main-content">
        <!--Toolbar-->
<!--        <button class="btn-primary" @click="showAlert">Hiện thông báo</button>-->
<!--        <panda-toolbar/>-->

<!--        &lt;!&ndash;Commit Panel&ndash;&gt;-->
<!--        <panda-commit-panel/>-->

<!--        &lt;!&ndash;Git Graph&ndash;&gt;-->
<!--        <panda-git-log-panel/>-->
      </div>

      <!--Panda-right-panel-->
<!--      <panda-right-panel-->
<!--        :commit="commitSample"-->
<!--        :is-collapsed="isCollapsedSample"-->
<!--        @toggle="togglePanel"-->
<!--      />-->
    </div>
  </div>
  <div class="alert-container">
    <transition-group name="alert-list" tag="div">
      <alert-notification
        v-for="alert in alerts"
        :key="alert.id"
        :title="alert.title"
        :message="alert.message"
        :type="alert.type"
        :duration="alert.duration"
        @close="removeAlert(alert.id)"
      />
    </transition-group>
  </div>
</template>
<script setup>
import PandaRepositoryWorkspace from '@/components/PandaRepositoryWorkspace.vue'
import PandaToolbar from '@/components/widgets/PandaToolbar.vue'
import PandaCommitPanel from '@/components/PandaCommitPanel.vue'
import { ref } from 'vue'
import AlertNotification from '@/components/modals/AlertNotification.vue'
import PandaRightPanel from '@/components/PandaRightPanel.vue'
import PandaGitLogPanel from '@/components/PandaGitLogPanel.vue'
import mitter from '@/plugins/mitter.js'
const alerts = ref([])

function addAlert({ title, message, type = 'info', duration = 5000 }) {
  const id = Date.now() + Math.random()
  alerts.value.unshift({ id, title, message, type, duration })
}

function removeAlert(id) {
  alerts.value = alerts.value.filter(a => a.id !== id)
}

mitter.on('alert', ({ title, message, type = 'info', duration = 5000 }) => {
  addAlert({ title, message, type, duration })
})

const commitSample = {
  message: "Fix login issue on mobile view",
  hash: "a1b2c3d4",
  author: "Long Nguyen",
  email: "long.nguyen@example.com",
  time: "2025-07-10T10:15:00Z",
  branch: "feature/login-fix",
  files: [
    "src/components/LoginForm.vue",
    "src/views/LoginPage.vue",
    "src/utils/validators.js"
  ]
}

const isCollapsedSample = ref(false)
function togglePanel() {
  isCollapsedSample.value = !isCollapsedSample.value
}
// const showAlert = () => {
//   alertMessage.value = 'Thành công rồi nhé!'
//   alertType.value = 'success'
//   show.value = true
//   setTimeout(() => (show.value = false), 3000)
// }
</script>
<style scoped>
.main-container {
  background: var(--bg-primary);
  height: calc(100vh - 66px);
  padding: 0;
}

.main-layout-container {
  margin-right: 0;
}

.main-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  padding: 0;
}

.alert-container {
  position: fixed;
  bottom: 45px;
  right: 10px;
  display: flex;
  flex-direction: column-reverse;
  gap: 10px;
  z-index: 9999;
}

.alert-list-enter-from,
.alert-list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.alert-list-enter-active,
.alert-list-leave-active,
.alert-list-move {
  transition: all 0.3s ease;
}
</style>
