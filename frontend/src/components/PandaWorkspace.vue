<template>
  <!-- 2. MAIN WORKSPACE -->
  <div class="flex-1 flex overflow-hidden">
    <!-- SIDEBAR -->
    <panda-repository-work-space/>
    <!-- MAIN EDITOR -->
    <panda-main-editor-workspace/>
    <!-- RIGHT SIDEBAR -->
    <panda-commit-workspace/>
  </div>
</template>

<script setup>
import PandaRepositoryWorkSpace from '@/components/repository-workspace/PandaRepositoryWorkSpace.vue'
import PandaMainEditorWorkspace from '@/components/PandaMainEditorWorkspace.vue'
import PandaCommitWorkspace from '@/components/PandaCommitWorkspace.vue'
</script>
