<template>
  <!-- 2. MAIN WORKSPACE -->
  <div class="flex-1 flex overflow-hidden">
    <!-- SIDEBAR -->
    <panda-git-left-side-bar/>
    <!-- MAIN EDITOR -->
    <panda-main-editor-workspace/>
    <!-- RIGHT SIDEBAR -->
    <panda-commit-workspace/>
  </div>
</template>

<script setup>
import PandaGitLeftSideBar from '@/components/repository-workspace/PandaGitLeftSideBar.vue'
import PandaMainEditorWorkspace from '@/components/PandaMainEditorWorkspace.vue'
import PandaCommitWorkspace from '@/components/PandaCommitWorkspace.vue'
</script>
