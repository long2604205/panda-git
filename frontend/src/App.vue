<template>
  <div class="flex flex-col h-screen overflow-hidden" :data-theme="theme">
    <panda-navigation/>
    <panda-toolbar
      @fetch="handleFetch"
      @pull="handlePull"
      @push="handlePush"
      @open-settings="handleOpenSettings"
    />
    <panda-workspace />
    <panda-footer :selected-branch="selectedBranch" @change-theme="setTheme" />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import PandaFooter from '@/components/widgets/PandaFooter.vue'
import PandaWorkspace from '@/components/PandaWorkspace.vue'
import PandaNavigation from "@/components/widgets/PandaNavigation.vue";
import PandaToolbar from "@/components/widgets/PandaToolbar.vue";

const theme = ref('dark')
function setTheme(t) {
  theme.value = t
}
const selectedBranch = ref('main')
onMounted(() => {
  document.documentElement.setAttribute('data-theme', theme.value)
})
watch(theme, (newTheme) => {
  document.documentElement.setAttribute('data-theme', newTheme)
})

// ==================== EVENT HANDLERS (LOG ONLY) ====================
const handleFetch = () => {
  console.log('🔄 FETCH: Fetching from remote...');
};

const handlePull = () => {
  console.log('⬇️ PULL: Pulling changes from remote...');
};

const handlePush = () => {
  console.log('⬆️ PUSH: Pushing changes to remote...');
};

const handleOpenSettings = () => {
  console.log('⚙️ OPEN SETTINGS: Opening settings panel...');
};

</script>
<!--https://heroicons.com/solid-->
<style></style>
