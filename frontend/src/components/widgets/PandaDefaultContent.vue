<template>
  <div class="container-fluid main-container">
    <div class="row main-layout-container h-100">
      <!--Repository Workspace-->
      <panda-repository-workspace/>

      <div class="col main-content">
        <!--Toolbar-->
<!--        <button class="btn-primary" @click="showAlert">Hiện thông báo</button>-->
        <panda-toolbar/>

        <!--Commit Panel-->
        <panda-commit-panel/>

        <!--Git Graph-->
        <panda-git-log-panel/>
      </div>

      <!--Panda-right-panel-->
      <panda-right-panel
        :commit="commitSample"
        :is-collapsed="isCollapsedSample"
        @toggle="togglePanel"
      />
    </div>
  </div>
  <alert-notification
    v-if="showAlert"
    :message="alertMessage"
    :type="alertType"
    @close="showAlert = false"
  />
</template>
<script setup>
import PandaRepositoryWorkspace from '@/components/PandaRepositoryWorkspace.vue'
import PandaToolbar from '@/components/PandaToolbar.vue'
import PandaCommitPanel from '@/components/PandaCommitPanel.vue'
import { ref } from 'vue'
import AlertNotification from '@/components/modals/AlertNotification.vue'
import PandaRightPanel from '@/components/PandaRightPanel.vue'
import PandaGitLogPanel from '@/components/PandaGitLogPanel.vue'
import mitter from '@/plugins/mitter.js'
const showAlert = ref(false)
const alertMessage = ref('')
const alertType = ref('info')

mitter.on('alert', ({ message, type = 'info' }) => {
  alertMessage.value = message
  alertType.value = type
  showAlert.value = true
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
  height: calc(100vh - 56px);
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
</style>
