<template>
  <div class="flex flex-col h-screen overflow-hidden" :data-theme="theme">
    <panda-navigation />
    <panda-workspace />
    <panda-footer :selected-branch="selectedBranch" @change-theme="setTheme" />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import PandaFooter from '@/components/widgets/PandaFooter.vue'
import PandaWorkspace from '@/components/PandaWorkspace.vue'
import PandaNavigation from "@/components/widgets/PandaNavigation.vue";

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
</script>

<style></style>
